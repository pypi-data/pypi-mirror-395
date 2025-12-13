# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from lino.utils.html import E, join_elems, tostring
from lino.api import dd, rt, _
from lino.core.utils import model_class_path
from lino.modlib.users.mixins import My

from lino.modlib.office.roles import OfficeStaff
from lino.mixins.periods import ObservedDateRange

from .mixins import UploadController
from .roles import UploadsReader

# from .mixins import FileUsable
from lino.core import constants


def filename_leaf(name):
    i = name.rfind("/")
    if i != -1:
        return name[i + 1:]
    return name


class Volumes(dd.Table):
    model = "uploads.Volume"
    required_roles = dd.login_required(OfficeStaff)

    insert_layout = """
    ref root_dir
    description
    """

    detail_layout = """
    ref root_dir
    description
    overview
    UploadsByVolume
    """


class UploadTypes(dd.Table):
    required_roles = dd.login_required(OfficeStaff)
    model = "uploads.UploadType"
    column_names = "upload_area name max_number wanted shortcut *"
    order_by = ["upload_area", "name"]

    insert_layout = """
    name
    upload_area
    """

    detail_layout = """
    id upload_area wanted max_number shortcut
    name
    uploads.UploadsByType
    """


class UploadDetail(dd.DetailLayout):
    main = """
    left preview
    """ + ("albums.ItemsByUpload" if dd.is_installed('albums') else "")

    left = """
    file
    volume:10 library_file:40
    user owner
    upload_area type
    description
    source
    memo.MentionsByTarget
    """

    window_size = (80, "auto")


class Uploads(dd.Table):
    model = "uploads.Upload"
    # required_roles = dd.login_required((OfficeUser, OfficeOperator))
    required_roles = dd.login_required(UploadsReader)
    column_names = "id description file type user owner *"
    order_by = ["-id"]
    default_display_modes = {
        70: constants.DISPLAY_MODE_LIST,
        None: constants.DISPLAY_MODE_TILES
    }
    # extra_display_modes = {constants.DISPLAY_MODE_LIST, constants.DISPLAY_MODE_GALLERY}

    detail_layout = "uploads.UploadDetail"

    insert_layout = """
    type
    description
    file
    volume library_file
    user
    """

    parameters = ObservedDateRange(
        upload_type=dd.ForeignKey("uploads.UploadType", blank=True, null=True)
    )
    params_layout = "start_date end_date user upload_type"

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super().get_request_queryset(ar, **filter)
        if (pv := ar.param_values) is None:
            return qs
        if pv.user:
            qs = qs.filter(user=pv.user)
        if pv.upload_type:
            qs = qs.filter(type=pv.upload_type)
        return qs


class AllUploads(Uploads):
    use_as_default_table = False
    required_roles = dd.login_required(OfficeStaff)


class UploadsByType(Uploads):
    master_key = "type"
    column_names = "file library_file description user * "


class UploadsByVolume(Uploads):
    master_key = "volume"
    column_names = "file library_file description user * "


if dd.is_installed('sources'):

    class UploadsBySource(Uploads):
        master_key = "source"
        column_names = "file library_file description user * "

else:

    class UploadsBySource(dd.Dummy):
        pass


class MyUploads(My, Uploads):
    required_roles = dd.login_required(UploadsReader)
    # required_roles = dd.login_required((OfficeUser, OfficeOperator))
    column_names = "file library_file description user owner *"
    # order_by = ["modified"]

    # @classmethod
    # def get_actor_label(self):
    #     return _("My %s") % _("Uploads")

    # @classmethod
    # def param_defaults(self, ar, **kw):
    #     kw = super(MyUploads, self).param_defaults(ar, **kw)
    #     kw.update(user=ar.get_user())
    #     return kw


def format_row_in_slave_summary(obj):
    """almost as str(), but without the type"""
    return obj.description or filename_leaf(obj.file.name) or str(obj.id)


class AreaUploads(Uploads):
    # required_roles = dd.login_required((OfficeUser, OfficeOperator))
    required_roles = dd.login_required(UploadsReader)
    stay_in_grid = True
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    detailed_summary = False

    # 20180119
    # @classmethod
    # def get_known_values(self):
    #     return dict(upload_area=self._upload_area)
    # @classmethod
    # def get_actor_label(self):
    #     if self._upload_area is not None:
    #         return self._upload_area.text
    #     return self._label or self.__name__

    @classmethod
    def get_table_summary(self, ar):
        obj = ar.master_instance
        if obj is None:
            return
        UploadType = rt.models.uploads.UploadType
        # Upload = rt.models.uploads.Upload
        elems = []
        types = []
        perm = ar.get_user().user_type.has_required_roles(self.required_roles)
        qs = UploadType.objects.all()
        if isinstance(obj, UploadController):
            area = obj.get_upload_area()
            if area is not None:
                qs = qs.filter(upload_area=area)
        else:
            return E.div(
                "{} is not an UploadController!".format(
                    model_class_path(obj.__class__))
            )
        volume = obj.get_uploads_volume()
        # print(20190208, volume)
        for ut in qs:
            sar = ar.spawn(self, master_instance=obj,
                           known_values=dict(type_id=ut.id))
            # logger.info("20140430 %s", sar.data_iterator.query)
            files = []
            for m in sar:
                text = format_row_in_slave_summary(m)
                edit = ar.obj2html(
                    m,
                    text,  # _("Edit"),
                    # icon_name='application_form',
                    title=_("Edit metadata of the uploaded file."),
                )
                mf = m.get_media_file()
                if mf:
                    show = ar.renderer.href_button(
                        mf.get_download_url(),
                        # u"\u21A7",  # DOWNWARDS ARROW FROM BAR (↧)
                        # u"\u21E8",
                        # "\u21f2",  # SOUTH EAST ARROW TO CORNER (⇲)
                        "⎙",  # Unicode symbol Print Screen
                        style="text-decoration:none;",
                        # _(" [show]"),  # fmt(m),
                        target="_blank",
                        # icon_name=settings.SITE.build_static_url(
                        #     'images/xsite/link'),
                        # icon_name='page_go',
                        # style="vertical-align:-30%;",
                        title=_("Open the file in a new browser window"),
                    )
                    # title=_("Open the uploaded file in a new browser window"))
                    # logger.info("20140430 %s", tostring(e))
                    files.append(E.span(edit, " ", show))
                else:
                    files.append(edit)
            if perm and ut.wanted and (ut.max_number < 0 or len(files) < ut.max_number):
                btn = self.insert_action.request_from(
                    sar,
                    master_instance=obj,
                    known_values=dict(type_id=ut.id, volume=volume),
                ).ar2button()
                if btn is not None:
                    files.append(btn)
            if len(files) > 0:
                chunks = (str(ut), ": ") + tuple(join_elems(files, ", "))
                types.append(chunks)
        # logger.info("20140430 %s", [tostring(e) for e in types])
        # elems += [str(ar.bound_action.action.__class__), " "]
        # if ar.bound_action.action.window_type == "d":
        if self.detailed_summary:
            if len(types) == 0:
                elems.append(E.ul(E.li(str(ar.no_data_text))))
            else:
                elems.append(E.ul(*[E.li(*chunks) for chunks in types]))
        else:
            if len(types) == 0:
                elems.append(str(ar.no_data_text))
                # elems.append(" / ")
            else:
                for chunks in types:
                    elems.extend(chunks)
                    # elems.append(" / ")
            # elems.append(obj.show_uploads.as_button_elem(ar))
        # ba = self.find_action_by_name("show_uploads")
        return E.div(*elems)


class UploadsByController(AreaUploads):
    master_key = "owner"
    column_names = "file volume library_file type description user *"

    insert_layout = dd.InsertLayout(
        """
    file
    volume library_file
    type
    description
    """,
        hidden_elements="volume",
        window_size=(60, "auto"),
    )

    @classmethod
    def format_upload(self, obj):
        return str(obj.type)
