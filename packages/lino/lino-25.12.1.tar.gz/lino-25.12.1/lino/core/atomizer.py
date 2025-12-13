# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.conf import settings

from lino import logger
from lino.utils import curry
from lino.utils import choosers
# from lino.core import store
from lino.core import actors
from lino.core import fields
# from lino.core import vfields
from .vfields import (
    VirtualField, DisplayField, RemoteField, RequestField)

from .vfields import DummyField
from .storefields import (
    FIELD_TYPES,
    StoreField, ComboStoreField,
    MethodStoreField, RequestStoreField,
    OneToOneRelStoreField, OneToOneStoreField,
    VirtStoreField, FileFieldStoreField, PasswordStoreField,
    GenericForeignKeyField, GenericRelField, ComboStoreField,
    PreviewTextStoreField, DisplayStoreField, IntegerStoreField, AutoStoreField,
    DecimalStoreField, BooleanStoreField, ForeignKeyStoreField, DateStoreField,
    TimeStoreField, DateTimeStoreField, IncompleteDateStoreField
)
from lino.core.utils import resolve_model
from lino.utils.choosers import check_for_chooser


# def none_getter(obj, ar=None):
#     return None


def make_remote_field(model, name):
    parts = name.split("__")
    if len(parts) == 1:
        return
    # It's going to be a RemoteField
    # logger.warning("20151203 RemoteField %s in %s", name, cls)

    cls = model
    field_chain = []
    editable = False
    # gettable = True
    leaf_chooser = None
    for n in parts:
        if model is None:
            return
            # raise Exception(
            #     "Invalid remote field {0} for {1}".format(name, cls))

        if isinstance(model, str):
            # Django 1.9 no longer resolves the
            # rel.model of ForeignKeys on abstract
            # models, so we do it here.
            model = resolve_model(model)
            # logger.warning("20151203 %s", model)

        fld = model.get_data_elem(n)
        if fld is None:
            return
            # raise Exception(
            #     "Invalid RemoteField %s.%s (no field %s in %s)" %
            #     (full_model_name(model), name, n, full_model_name(model)))

        if isinstance(fld, DummyField):
            # a remote field containing at least one dummy field is itself a
            # dummy field
            return fld

        # Why was this? it caused docs/specs/avanti/courses.rst to fail
        # if isinstance(fld, models.ManyToOneRel):
        #     gettable = False

        # make sure that the atomizer gets created.
        get_atomizer(model, fld, fld.name)

        if isinstance(fld, VirtualField):
            fld.lino_resolve_type()
        leaf_chooser = check_for_chooser(model, fld, name)

        field_chain.append(fld)
        if isinstance(
            fld, (models.OneToOneRel, models.OneToOneField, models.ForeignKey)
        ):
            editable = True
        if getattr(fld, "remote_field", None):
            model = fld.remote_field.model
        else:
            model = None

    # if not gettable:
    #     # raise Exception("20231112")
    #     return RemoteField(none_getter, name, fld)

    if leaf_chooser is not None:
        d = choosers.get_choosers_dict(cls)
        d[name] = leaf_chooser

    def getter(obj, ar=None):
        try:
            for fld in field_chain:
                if obj is None:
                    return None
                obj = fld._lino_atomizer.full_value_from_object(obj, ar)
            return obj
        except Exception as e:
            # raise
            msg = "Error while computing {}: {} ({} in {})"
            raise Exception(msg.format(name, e, fld, field_chain))
            # ~ if False: # only for debugging
            if True:  # see 20130802
                logger.exception(e)
                return str(e)
            return None

    if not editable:
        rf = RemoteField(getter, name, fld)
        # choosers.check_for_chooser(model, rf)
        return rf

    def setter(obj, value):
        # logger.info("20180712 %s setter() %s", name, value)
        # all intermediate fields are OneToOneRel
        target = obj
        try:
            for i, fld in enumerate(field_chain):
                # print("20180712a %s" % fld)
                if isinstance(fld, (models.OneToOneRel, models.ForeignKey)):
                    reltarget = getattr(target, fld.name, None)
                    if reltarget is None:
                        rkw = {fld.field.name: target}
                        # print(
                        #     "20180712 create {}({})".format(
                        #         fld.related_model, rkw))
                        reltarget = fld.related_model(**rkw)
                        reltarget.save_new_instance(
                            fld.related_model.get_default_table().create_request()
                        )

                    setattr(target, fld.name, reltarget)

                    if target == obj and target.id is None:
                        # Model.save_new_instance will be called do not insert this record.
                        target = reltarget
                        continue
                    target.full_clean()
                    target.save()
                    # print("20180712b {}.{} = {}".format(
                    #     target, fld.name, reltarget))
                    target = reltarget
                else:
                    setattr(target, fld.name, value)
                    target.full_clean()
                    target.save()
                    # print(
                    #     "20180712c setattr({},{},{}".format(
                    #         target, fld.name, value))
                    return True
        except Exception as e:
            if False:  # only for debugging
                logger.exception(e)
                return str(e)
            raise e.__class__("Error while setting %s: %s" % (name, e))
            return False

    rf = RemoteField(getter, name, fld, setter)
    # choosers.check_for_chooser(model, rf)
    return rf


def create_atomizer(holder, fld, name):
    """
    The holder is where the (potential) choices come from. It can be
    a model, an actor or an action. `fld` is a data element.
    """
    if name is None:
        # print("20181023 create_atomizer() no name {}".format(fld))
        return
        # raise Exception("20181023 create_atomizer() {}".format(fld))
    if isinstance(fld, RemoteField):
        """
        Hack: we create a StoreField based on the remote field,
        then modify some of its behaviour.
        """
        sf = create_atomizer(holder, fld.field, fld.name)

        # print("20180712 create_atomizer {} from {}".format(sf, fld.field))

        def value_from_object(unused, obj, ar=None):
            return fld.func(obj, ar)

        def full_value_from_object(unused, obj, ar=None):
            return fld.func(obj, ar)

        def set_value_in_object(sf, ar, instance, v):
            # print("20180712 {}.set_value_in_object({}, {})".format(
            #     sf, instance, v))
            old_value = sf.value_from_object(instance, ar.request)
            if old_value != v:
                return fld.setter(instance, v)

        sf.value_from_object = curry(value_from_object, sf)
        sf.full_value_from_object = curry(full_value_from_object, sf)
        sf.set_value_in_object = curry(set_value_in_object, sf)
        return sf

    meth = getattr(fld, "_return_type_for_method", None)
    if meth is not None:
        # uh, this is tricky...
        # raise Exception(f"20250523 {fld} has a _return_type_for_method")
        # print(f"20250523 {fld} has a _return_type_for_method")
        return MethodStoreField(fld, name)

    # sf_class = getattr(fld, 'lino_atomizer_class', None)
    # if sf_class is not None:
    #     return sf_class(fld, name)

    if isinstance(fld, DummyField):
        return None
    if isinstance(fld, RequestField):
        delegate = create_atomizer(holder, fld.return_type, fld.name)
        return RequestStoreField(fld, delegate, name)
    if isinstance(fld, type) and issubclass(fld, actors.Actor):
        # raise Exception(f"20250523 {fld} is an actor!")
        return
    # if isinstance(fld, type) and issubclass(fld, actors.Actor):
    #     raise Exception("20230219")
    #     # 20210618 & 20230218
    #     if settings.SITE.kernel.default_ui.support_async:
    #         return SlaveTableStoreField(fld, name)
    #     return DisplayStoreField(fld, name)

    if isinstance(fld, VirtualField):
        delegate = create_atomizer(holder, fld.return_type, fld.name)
        if delegate is None:
            # e.g. VirtualField with DummyField as return_type
            return None
            # raise Exception("No atomizer for %s %s %s" % (
            #     holder, fld.return_type, fld.name))
        return VirtStoreField(fld, delegate, name)
    if isinstance(fld, models.FileField):
        return FileFieldStoreField(fld, name)
    if isinstance(fld, models.ManyToManyField):
        return StoreField(fld, name)
    if isinstance(fld, fields.PasswordField):
        return PasswordStoreField(fld, name)
    if isinstance(fld, models.OneToOneField):
        return OneToOneStoreField(fld, name)
    if isinstance(fld, models.OneToOneRel):
        return OneToOneRelStoreField(fld, name)

    if settings.SITE.is_installed("contenttypes"):
        from lino.core.gfks import GenericForeignKey, GenericRel
        from lino.modlib.gfks.fields import GenericForeignKeyIdField

        if isinstance(fld, GenericForeignKey):
            return GenericForeignKeyField(fld, name)
        if isinstance(fld, GenericRel):
            return GenericRelField(fld, name)
        if isinstance(fld, GenericForeignKeyIdField):
            return ComboStoreField(fld, name)

    if isinstance(fld, models.ForeignKey):
        return ForeignKeyStoreField(fld, name)
    if isinstance(fld, models.TimeField):
        return TimeStoreField(fld, name)
    if isinstance(fld, models.DateTimeField):
        return DateTimeStoreField(fld, name)
    if isinstance(fld, fields.IncompleteDateField):
        return IncompleteDateStoreField(fld, name)
    if isinstance(fld, models.DateField):
        return DateStoreField(fld, name)
    if isinstance(fld, models.BooleanField):
        return BooleanStoreField(fld, name)
    if isinstance(fld, models.DecimalField):
        return DecimalStoreField(fld, name)
    if isinstance(fld, models.AutoField):
        return AutoStoreField(fld, name)
        # kw.update(type='int')
    if isinstance(fld, models.SmallIntegerField):
        return IntegerStoreField(fld, name)
    if isinstance(fld, DisplayField):
        return DisplayStoreField(fld, name)
    if isinstance(fld, models.IntegerField):
        return IntegerStoreField(fld, name)
    if isinstance(fld, fields.PreviewTextField):
        return PreviewTextStoreField(fld, name)
    if isinstance(fld, models.ManyToOneRel):
        # raise Exception("20190625 {} {} {}".format(holder, fld, name))
        return
    if (sft := FIELD_TYPES.get(fld.__class__, None)) is not None:
        return sft(fld, name)
    kw = {}
    if choosers.uses_simple_values(holder, fld):
        return StoreField(fld, name, **kw)
    else:
        return ComboStoreField(fld, name, **kw)


def get_atomizer(holder, fld, name):
    """
    Return the :term:`atomizer` for this database field.

    An atomizer is an instance of a subclass of :class:`StoreField`.

    """
    # if name is None:
    #     raise Exception("20250523 name is None")
    sf = getattr(fld, "_lino_atomizer", None)
    if sf is None:
        sf = create_atomizer(holder, fld, name)
        if sf is None:
            # print(f"20250523 {repr(fld)} on {holder} has no StoreField")
            # For example dummy fields and slave tables don't have an atomizer
            return
        assert isinstance(sf, StoreField)
        # if not isinstance(sf, StoreField):
        #     raise Exception("{} is not a StoreField".format(sf))
        # if isinstance(fld, type):
        #     raise Exception("20240913 trying to set class attribute")
        setattr(fld, "_lino_atomizer", sf)
    return sf
