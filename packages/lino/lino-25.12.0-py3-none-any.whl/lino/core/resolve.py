# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.db import models
from django.utils.functional import Promise


def resolve_action(spec, action=None):
    from lino.core.boundaction import BoundAction
    from lino.core.actors import Actor
    from lino.core.actions import Action
    givenspec = spec

    if isinstance(spec, str):
        site = settings.SITE
        # if spec.startswith('webshop.'):
        #     print("20210320", spec, repr(site.models.resolve(spec)))
        # spec = site.models.resolve(spec)
        parts = spec.split(".")
        if len(parts) < 2 or len(parts) > 3:
            raise Exception(
                "Invalid action specifier '{}' (must be of form `plugin_name.ClassName[.action_name]`).".format(
                    spec
                )
            )
        app = site.models[parts[0]]
        cls = getattr(app, parts[1])
        if len(parts) == 2:
            spec = cls
        else:
            if action is not None:
                raise Exception(
                    "Invalid action specifier '{}' when action keyword is specified.".format(
                        spec
                    )
                )

            if issubclass(cls, Actor):
                spec = cls.get_action_by_name(parts[2])
            else:
                spec = getattr(cls, parts[2])
        # spec = site.actors.resolve(spec) or site.models.resolve(spec)

    if isinstance(spec, BoundAction):
        return spec

    if isinstance(spec, Action):
        return spec.defining_actor.get_action_by_name(spec.action_name)

    if isinstance(spec, type) and issubclass(spec, models.Model):
        spec = spec.get_default_table()
        assert spec is not None

    if isinstance(spec, type) and issubclass(spec, Actor):
        if action:
            a = spec.get_action_by_name(action)
            # ~ print 20121210, a
            if a is None:
                raise Exception(
                    "{} has no action named '{}'".format(spec, action))
        else:
            a = spec.default_action
            # assert a is not None
            if a is None:
                raise Exception("%r default_action is None?!" % spec)
        return a

    raise Exception("Action spec %r returned invalid object %r" %
                    (givenspec, spec))


def resolve_layout(cls, k, spec, layout_class, **options):
    # k: just for naming the culprit in error messages
    from lino.core.utils import Panel as utils_Panel
    if isinstance(spec, Promise):
        spec = str(spec)
    if isinstance(spec, str):
        if "\n" in spec or "." not in spec:
            return layout_class(spec, cls, **options)
        else:
            layout_class = settings.SITE.models.resolve(spec)
            if layout_class is None:
                raise Exception(
                    "Unresolved {} {!r} for {}".format(k, spec, cls))
            return layout_class(None, cls, **options)
    elif isinstance(spec, utils_Panel):
        options.update(spec.options)
        return layout_class(spec.desc, cls, **options)
    else:
        if not isinstance(spec, layout_class):
            if not isinstance(cls, type):
                # cls is an action instance
                cls = cls.__class__
            msg = (
                "{}.{}.{} must be a string, " "a Panel or an instance of {} (not {!r})"
            )
            raise Exception(
                msg.format(cls.__module__, cls.__name__,
                           k, layout_class.__name__, spec)
            )
        if spec._datasource is None:
            spec.set_datasource(cls)
            return spec
        elif not issubclass(cls, spec._datasource):
            raise Exception(
                "Cannot reuse %s instance (%s of %r) for %r"
                % (spec.__class__, k, spec._datasource, cls)
            )
    return spec


def install_layout(cls, k, layout_class, **options):
    """
    - `cls` is the actor (a class object)

    - `k` is one of 'grid_layout', 'detail_layout', 'insert_layout',
      'params_layout', 'card_layout'

    - `layout_class`

    """
    # if str(cls) == 'courses.Pupils':
    #     print("20160329 install_layout", k, layout_class)
    dl = cls.__dict__.get(k, None)
    if dl is None:  # and not cls._class_init_done:
        dl = getattr(cls, k, None)
    if dl is None:
        return
    setattr(cls, k, resolve_layout(cls, k, dl, layout_class, **options))


def params_layout_class(cls):
    from lino.core.actions import Action
    from lino.core.actors import Actor
    from lino.core.layouts import ParamsLayout, ActionParamsLayout
    # replaces cls._params_layout_class
    # from lino.utils.report import Report
    if isinstance(cls, type) and issubclass(cls, Actor):
        return ParamsLayout
        # if issubclass(cls, AbstractTable):
        #     return layouts.ParamsLayout
        # if issubclass(cls, Report):
        #     return layouts.ParamsLayout
    elif isinstance(cls, Action):
        return ActionParamsLayout


def register_params(cls):
    """`cls` is either an actor (a class object) or an action (an
    instance).

    """
    plc = params_layout_class(cls)
    if cls.parameters is not None:
        for k, v in cls.parameters.items():
            v.set_attributes_from_name(k)
            v.table = cls
            # v.model = cls  # 20181023 experimentally

        if cls.params_layout is None:
            if plc is None:
                raise Exception(f"{cls} has no _params_layout_class")
            cls.params_layout = plc.join_str.join(
                cls.parameters.keys()
            )
    if cls.params_layout is not None:
        install_layout(cls, "params_layout", plc)

    # # e.g. accounting.ByJournal is just a mixin but provides a default value for its children
    # elif cls.params_layout is not None:
    #     raise Exception("{} has a params_layout but no parameters".format(cls))

    # if isinstance(cls, type) and cls.__name__.endswith("Users"):
    # # if isinstance(cls, type) and cls.model is not None and cls.model.__name__ == "User":
    #     # if str(cls.model) != "users.User":
    #     #     raise Exception("{} {}".format(cls, cls.model))
    #     print("20200825 {}.register_params {} {}".format(
    #         cls, cls.parameters, cls.params_layout))


def make_params_layout_handle(self):
    # `self` is either an Action instance or an Actor class object
    return self.params_layout.get_layout_handle()
