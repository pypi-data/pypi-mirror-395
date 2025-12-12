# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.db import models
from lino.core.actors import Actor
from lino.core import actions
from lino.core import constants
from lino import logger
from lino.core.utils import resolve_fields_list


class Group:
    def __init__(self):
        self.sums = []

    def process_row(self, collector, row):
        collector.append(row)

    # ~ def add_to_table(self,table):
    # ~ self.table = table
    # ~ for col in table.computed_columns.values():


class TableHandle:
    """
    For every table we create one "handle" per renderer.

    See also :meth:`lino.core.actors.Actor.setup_handle`, which is called during
    startup and sets more attributes.

    """

    _layouts = None
    store = None

    def __init__(self, actor):
        self.actor = actor

    def __str__(self):
        return str(self.actor) + "Handle"

    def setup_layouts(self):
        if self._layouts is not None:
            return
        self._layouts = [self.grid_layout]

    def get_actor_url(self, *args, **kw):
        return settings.SITE.kernel.get_actor_url(self.actor, *args, **kw)

    def submit_elems(self):
        return []

    def get_grid_layout(self):
        self.setup_layouts()
        return self._layouts[0]

    def get_columns(self):
        lh = self.get_grid_layout()
        # ~ print 20110315, layout._main.columns
        return lh.main.columns

    def get_slaves(self):
        return [sl.get_handle() for sl in self.actor._slaves]


class AbstractTable(Actor):
    """An AbstractTable is the definition of a tabular data table, usually
    displayed in a Grid (but it's up to the user interface to decide
    how to implement this).

    Base class for :class:`Table <lino.core.dbtables.Table>` and
    :class:`VirtualTable <lino.core.tables.VirtualTable>`.

    """

    abstract = True

    _handle_class = TableHandle
    _detail_action_class = actions.ShowDetail
    # _params_layout_class = layouts.ParamsLayout

    hide_zero_rows = False
    """Set this to `True` if you want to remove rows which contain no
    values when rendering this table as plain HTML.  This is ignored
    when rendered as ExtJS.

    """

    column_names = "*"

    tablet_columns = None
    """
    The columns that must remain visible when this table is rendered
    on a tablet device.
    """

    mobile_columns = None
    """
    The columns that must remain visible when this table is rendered
    on a mobile device.
    """

    popin_columns = None
    """
    The columns that must pop in below the first column if there is no
    space to render them on the device.

    If None: All columns not listed in mobile_columns nor Tablet_columns
    will not pop-in.
    """

    start_at_bottom = False
    """Set this to `True` if you want your table to *start at the
    bottom*.  Unlike reverse ordering, the rows remain in their
    natural order, but when we open a grid on this table, we want it
    to start on the last page.

    Use cases are in :class:`lino_xl.lib.trading.InvoicesByJournal` and
    :class:`lino_xl.lib.accounting.InvoicesByJournal`.
    """

    group_by = None
    """
    A list of field names that define the groups of rows in this table.
    Each group can have her own header and/or total lines.
    """

    custom_groups = []
    """
    Used internally to store :class:`groups <Group>` defined by this Table.
    """

    master_field = None
    """
    For internal use. Automatically set to the field descriptor of the
    :attr:`master_key`.

    """

    get_data_rows = None
    """
    Maybe deprecated.  Use get_request_queryset() instead.

    Virtual tables *must* define this method, model-based tables *may* define
    it. e.g. in case they need local filtering.

    This will be called with a
    :class:`lino.core.requests.ActionRequest` object and is expected to
    return or yield the list of "rows"::

        @classmethod
        def get_data_rows(self, ar):
            ...
            yield somerow

    """

    preview_limit = settings.SITE.preview_limit

    row_height = 1
    """
    Number of text rows per data row.

    """

    variable_row_height = False
    """
    Set this to `True` if you want each row to get the height that it
    needs.

    """

    auto_fit_column_widths = settings.SITE.auto_fit_column_widths
    """Set this to `True` if you want to have the column widths adjusted
    to always fill the available width.  This implies that there will
    be no horizontal scrollbar.

    """

    active_fields = frozenset()
    """
    A list of field names that are "active".
    Value and inheritance as for :attr:`hidden_columns`.

    When a field is "active", this means only that it will cause an
    immediate "background" save and refresh of the :term:`detail
    window` when their value was changed. The true "activity"
    (i.e. other fields being updated according to the value of an
    active field) is defined in the model's :meth:`full_clean
    <dd.Model.full_clean>` and :meth:`FOO_changed
    <dd.Model.FOO_changed>` methods.

    Note that active fields are active only in a :term:`detail
    window`, not in an :term:`insert window`.  That's because there
    they would lead to the unexpected behaviour of closing the window.

    """

    hidden_columns = frozenset()

    form_class = None
    help_url = None

    page_length = 20
    """Number of rows to display per page.  Used to control the height of
    a combobox of a ForeignKey pointing to this model

    """

    cell_edit = True
    """`True` (default) to use ExtJS CellSelectionModel, `False` to use
    RowSelectionModel.  When `True`, the users cannot select multiple
    rows.  When `False`, the users cannot edit individual cells using
    the :kbd:`F2` key..

    """

    show_detail_navigator = True
    """
    Whether a Detail view on a row of this table should have a navigator.
    """

    default_group = Group()

    default_layout = 0

    typo_check = True
    """
    True means that Lino shoud issue a warning if a subclass
    defines any attribute that did not exist in the base class.
    Usually such a warning means that there is something wrong.
    """

    table_as_calendar = False
    """Whether the primereact Datatable is used to display a calendar view.

    Used only in :term:`React front end`.
    """

    default_display_modes = {
        70: constants.DISPLAY_MODE_SUMMARY,
        None: constants.DISPLAY_MODE_GRID
    }
    """
    Which :term:`display mode` to use in a :term:`slave panel`,
    depending on available width.

    See :ref:`dg.table.default_display_modes`.
    """

    parent_layout = None

    @classmethod
    def attach_to_parent_layout(cls, parent):
        cls.parent_layout = parent

    @classmethod
    # def get_display_mode(cls, available_width=None):
    def get_display_mode(cls):
        """Return the fallback :term:`display mode` to use."""
        return cls.default_display_modes[None]
        # rv = cls.default_display_modes[None]
        # if available_width is not None:
        #     found = None
        #     for w, v in cls.default_display_modes.items():
        #         if w is not None and w <= available_width:
        #             if found is None:
        #                 found = w
        #                 rv = v
        #             elif found > w:
        #                 found = w
        #                 rv = v
        # return rv
        # current_choice = (0, None)
        # for dmi in cls.display_mode:
        #     if available_width is not None:
        #         if dmi[0] is None and current_choice[0] == 0:
        #             current_choice = (0, dmi[1])
        #         elif available_width > dmi[0] > current_choice[0]:
        #             current_choice = dmi
        #     elif dmi[0] is None:
        #         return dmi[1]
        # return current_choice[1]

    max_render_depth = 2
    """
    Used to limit the rendering of slave card views.
    """

    hide_if_empty = False
    """
    In a detail view if a slave table is empty, it's element will be hidden
    """

    stay_in_grid = False
    """Set this to True if Lino should prefer grid mode and not open a
    detail window on a newly created record.  :class:`SubmitDetail
    <lino.core.actions.SubmitDetail>` closes the window when this is
    True.

    Usage example :class:`LanguageKnowledgesByPerson
    <lino_xl.lib.cv.models.LanguageKnowledgesByPerson>`.

    """

    no_phantom_row = False
    """Suppress a :term:`phantom row` in situations where Lino would otherwise add
    one.

    The phantom row can disturb for example when users want to see the number of
    existing entries.  End users can double-click on the phantom row to open an
    insert window and create a new item.

    Used for :class:`lino_xl.lib.accounting.ByJournal` where a phantom row
    is disturbing and not needed.

    """

    order_by = None
    """If specified, this must be a tuple or list of field names that
will be passed to Django's `order_by
<https://docs.djangoproject.com/en/5.2/ref/models/querysets/#order-by>`__
method in order to sort the rows of the queryset.

    """

    filter = None
    """
    If specified, this must be a :class:`django.db.models.Q` object that will be
    passed to Django's `filter
    <https://docs.djangoproject.com/en/5.2/ref/models/querysets/#filter>`__
    method.

    If you allow a user to insert rows into a filtered table, you should make
    sure that new records satisfy your filter condition, otherwise you can get
    surprising behaviour if the user creates a new row.

    If your filter consists of simple static values on some known field, then
    you might prefer to use :attr:`known_values
    <lino.core.actors.Actor.known_values>` instead because this will add
    automatic behaviour.

    One advantage of :attr:`filter` over
    :attr:`known_values  <lino.core.actors.Actor.known_values>`
    is that this can use the full range of Django's `field lookup methods
    <https://docs.djangoproject.com/en/5.2/topics/db/queries/#field-lookups>`_

    """

    exclude = None
    """
    If specified, this must be a :class:`django.db.models.Q` object that will be
    passed to Django's `exclude
    <https://docs.djangoproject.com/en/5.2/ref/models/querysets/#exclude>`__
    method.

    This is the logical opposite of :attr:`filter`.
    """

    extra = None
    """
    Examples::

      extra = dict(select=dict(lower_name='lower(name)'))
      # (or if you prefer:)
      # extra = {'select':{'lower_name':'lower(name)'},'order_by'=['lower_name']}

    List of SQL functions and which RDBMS supports them:
    http://en.wikibooks.org/wiki/SQL_Dialects_Reference/Functions_and_expressions/String_functions

    """

    hide_sums = False
    """
    Set this to True if you don't want Lino to display sums in a table
    view.
    """

    use_paging = False
    """
    Set this to True in Extjs6 to not use a Buffered Store, and use a JsonStore with paging instead.
    """

    drag_drop_sequenced_field = None
    """
    Extjs6 only
    Enables drag and drop reordering for a table.
    Set to the field name that is used to track the order.
    Only used in lino.mixins.sequenced.Sequenced. Field name seqno
    """

    focus_on_quick_search = False
    """
    If True , when the grid opens, the initial keyboard focus will be in the quick search field.
    """

    @classmethod
    def class_init(cls):
        super().class_init()
        resolve_fields_list(cls, "tablet_columns", set, {})
        resolve_fields_list(cls, "mobile_columns", set, {})
        resolve_fields_list(cls, "popin_columns", set, {})
        if cls.model is not None:
            if not isinstance(cls.model, type):
                raise Exception(f"{cls}.model is {repr(cls.model)}")
            if not issubclass(cls.model, models.Model):
                if cls.model._lino_default_table is None:
                    cls.model._lino_default_table = cls

    # @classmethod
    # def get_request_queryset(self, ar, **filter):
    #     return []

    @classmethod
    def spawn(cls, suffix, **kw):
        kw["app_label"] = cls.app_label
        return type(cls.__name__ + str(suffix), (cls,), kw)

    @classmethod
    def parse_req(self, request, rqdata, **kw):
        """
        This is called when an incoming web request on this actor is being
        parsed.

        If you override :meth:`parse_req`, then keep in mind that it will
        be called *before* Lino checks the requirements.  For example the
        user may be AnonymousUser even if the requirements won't let it be
        executed.  `ar.subst_user.user_type` may be None, e.g. when called
        from `find_appointment` in :class:`welfare.pcsw.Clients`.

        """
        return kw

    @classmethod
    def get_row_by_pk(self, ar, pk):
        """
        `dbtables.Table` overrides this.
        """
        try:
            return ar.data_iterator[int(pk) - 1]
        except (ValueError, IndexError):
            return None

    @classmethod
    def get_default_action(cls):
        from lino.core import sai
        return sai.SHOW_TABLE

    @classmethod
    def get_actor_editable(self):
        if self._editable is None:
            return self.get_data_rows is None
        return self._editable

    @classmethod
    def setup_columns(self):
        pass

    @classmethod
    def get_column_names(self, ar):
        """Dynamic tables can subclass this method and return a value for
        :attr:`column_names` that depends on the request.

        """
        # if settings.SITE.mobile_view:
        #     return self.column_names_m or self.column_names
        # else:
        #     return self.column_names
        return self.column_names

    @classmethod
    def group_from_row(self, row):
        return self.default_group

    @classmethod
    def wildcard_data_elems(self):
        for cc in self.virtual_fields.values():
            yield cc
        # ~ return []

    @classmethod
    def get_filter_kw(self, ar, **kw):
        """
        Return a dict with the "master keywords" for this table
        and the given action request ``ar``.

        For example, if you have two models :class:`Book` and :class:`Author`,
        and a foreign key :attr:`Book.author`, which points to the author of the
        book, and a table `BooksByAuthor` having `master_key` set to
        ``'author'``, then :meth:`BooksByAuthor.get_filter_kw` would return a
        dict `{'author': <PK>}` where `<PK>` is the primary key of the action
        request's :attr:`master_instance
        <lino.core.requests.BaseRequest.master_instance>`.

        Another example is :class:`lino_xl.lib.tickets.EntriesBySession`, where
        blog entries are not directly linked to a session, but in the detail of
        a session we want to display a table of related blog entries.

        :class:`lino_xl.lib.households.SiblingsByPerson` Household
        members are not directly linked to a Person, but usually a
        Person is member of exactly one household, and in the Detail
        of a Person we want to display the members of that household.
        """
        from lino.core.gfks import gfk2lookup, GenericForeignKey

        master_instance = ar.master_instance
        if self.master is None:
            pass
            # master_instance may be e.g. a lino.core.actions.EmptyTableRow
            # UsersWithClients as "slave" of the "table" Home
        elif self.master is models.Model:
            pass
        elif isinstance(self.master_field, GenericForeignKey):
            kw = gfk2lookup(self.master_field, master_instance, **kw)
        elif self.master_field is not None:
            if master_instance is None:
                if not self.master_field.null:
                    # ~ logger.info('20120519 %s.get_filter_kw()--> None',self)
                    return  # cannot add rows to this table
            else:
                # logger.info("20240414 master_instance is %s", master_instance)
                # master_instance = master_instance.get_typed_instance(self.master)
                if not isinstance(master_instance, self.master):
                    # e.g. a ByUser table descendant called by AnonymousUser
                    msg = "20240731 %r is not a %s (%s.master_key = '%s')" % (
                        master_instance,
                        self.master,
                        self,
                        self.master_key,
                    )
                    # logger.exception(msg)
                    logger.warning(msg)
                    # raise Exception(msg)
                    # raise PermissionDenied(msg)
                    # raise BadRequest(msg)
                    # master_instance = None
                    return  # cannot add rows to this table
            kw[self.master_field.name] = master_instance
        # else:
        #     msg = "20150322 Cannot handle master {0}".format(master_instance)
        #     raise Exception(msg)
        return kw

    # @fields.displayfield(_("Details"))
    # def detail_pointer(cls, obj, ar):
    #     # print("20181230 detail_pointer() {}".format(cls))
    #     return obj.as_summary_item(ar)

    @classmethod
    def run_action_from_console(self, pk=None, an=None):
        """
        Not yet stable. Used by print_tx25.py.
        To be combined with the `show` management command.
        """
        settings.SITE.startup()
        # 20240404 stopped using default_list_action_name
        if an is None:
            ba = self.default_action if pk is None else self.detail_action
        else:
            ba = self.get_action_by_name(an)
        # ~ print ba
        if pk is None:
            ar = self.create_request(action=ba)
        else:
            ar = self.create_request(action=ba, selected_pks=[pk])

        ba.action.run_from_ui(ar)
        kw = ar.response
        msg = kw.get("message")
        if msg:
            print(msg)
        url = kw.get("open_url") or kw.get("open_webdav_url")
        if url:
            os.startfile(url)

    @classmethod
    def add_quick_search_filter(cls, data, search_text):
        """Add a filter to the given data iterator in order to apply a quick
        search for the given `search_text`.

        """
        return data
