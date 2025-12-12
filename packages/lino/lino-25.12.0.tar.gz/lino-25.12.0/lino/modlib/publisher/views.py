# -*- coding: UTF-8 -*-
# Copyright 2020-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
from typing import Optional
from django import http
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import redirect
from django.utils import translation
from django.views.generic import View
from jinja2 import Template
from etgen.html import E
from lino.api import dd, _
from lino.core import auth
from lino.core import constants
from lino.core.atomizer import get_atomizer
from lino.core.elems import Panel
# from lino.core.requests import BaseRequest
from lino.core.views import json_response, ar2html
# from lino.utils.html import table2html, tostring
from lino.utils.html import tostring, ar2pager, format_html, mark_safe
from lino.modlib.bootstrap5 import PAGE_TITLE_TEMPLATE
from .choicelists import SpecialPages
from .forms import ParamsForm

FORM_PANEL_TEMPLATE = Template("""
<div class="container form-group {{ dflex }}">
    {% for item in items %}
        {% if item.__class__.__name__ == "Panel" %}
            {{ render_form_panel(item.elements, item.vertical) }}
        {% else %}
            {% set field = params_form[item.name] %}
            <div class="align-self-end" style="width: 25ch">
                {{ field.as_field_group() }}
            </div>
        {% endif %}
    {% endfor %}
</div>
""")

FORM_TEMPLATE = Template("""
<nav id="sidebar" class="collapse d-lg-block sidebar bg-light">
    <div class="position-sticky">
        <div class="list-group list-group-flush mx-3 mt-4">
        <h5 class="px-3">Filters</h5>
        <form method="get" class="form">
            {{ render_form_panel(layout_main.elements, layout_main.vertical) }}
            <button type="submit" class="btn btn-primary">{{_("Filter")}}</button>
        </form>
        </div>
    </div>
</nav>
""")


def render_form(layout_main, params_form):
    def render_form_panel(items, vertical):
        dflex = "d-flex flex-wrap" if not vertical else ""
        return FORM_PANEL_TEMPLATE.render({
            "dflex": dflex, "items": items, "params_form": params_form, "render_form_panel": render_form_panel})
    
    return FORM_TEMPLATE.render({"render_form_panel": render_form_panel, "layout_main": layout_main, "_": _})


class List(View):
    table_class = None
    form_param_prefix = "pv"
    publisher_template = "publisher/{skin}/list.pub.html"

    def get(self, request, **kwargs):
        request_get = {k: v[0] if len(v := request.GET.getlist(k)) == 1 else v for k in request.GET.keys()}
        param_values = self.table_class.params_layout.params_store.parse_prefixed_params(request, self.form_param_prefix)
        
        rnd = settings.SITE.plugins.publisher.renderer
        ar = self.table_class.create_request(renderer=rnd, request=request, param_values=param_values, **kwargs)
        
        if not ar.get_permission():
            msg = "No permission to run {}".format(ar)
            # raise Exception(msg)
            raise PermissionDenied(msg)
        display_mode = ar.display_mode
        if display_mode is None:
            display_mode = self.table_class.default_display_modes[None]
        if display_mode == constants.DISPLAY_MODE_GRID:
            display_mode = constants.DISPLAY_MODE_HTML

        main = tostring(ar2html(ar, display_mode))
        # print(main)

        params_layout_main = self.table_class.params_layout.get_layout_handle().main
        params_form = ParamsForm(
            actor=self.table_class,
            initial=param_values,
            prefix=self.form_param_prefix,
        )
        params_form = mark_safe(render_form(params_layout_main, params_form))

        context = dict(
            dd=dd,
            obj=None,
            ar=ar,
            home=SpecialPages.home.get_object(),
            # title=ar.get_title(),
        )
        heading = format_html(PAGE_TITLE_TEMPLATE, ar.get_title_base())
        if self.table_class.params_panel_pos == "top":
            heading = params_form + heading
        elif self.table_class.params_panel_pos == "bottom":
            heading += params_form
        else:
            context.update({"params_form": params_form})
        # main = table2html(ar)
        toolbar = ar2pager(ar, display_mode, initial_values=request_get)
        page_content = format_html("<div>{}</div>", heading+tostring(toolbar)+main)
        context.update(page_content=page_content)
        # context.update(main=main)
        tplname = self.publisher_template.format(skin=dd.plugins.publisher.skin)
        tpl = dd.plugins.jinja.renderer.jinja_env.get_template(tplname)
        if settings.SITE.developer_site_cache:
            rnd.build_js_cache(False)
        return http.HttpResponse(
            tpl.render(**context), content_type='text/html;charset="utf-8"')


class SlaveList(List):
    def get(self, request, mk=None):
        # mi = self.table_class.get_master_instance()
        # print(f"20251025 {mk} {pk}")
        return super().get(request, master_key=mk)


class Element(View):
    # actor = None
    # publisher_view = None
    table_class = None

    def get(self, request, pk=None, **kw):
        # print("20220927 a get()")
        # if pk is None:
        #     return http.HttpResponseNotFound()
        # rnd = settings.SITE.kernel.default_renderer
        rnd = settings.SITE.plugins.publisher.renderer

        # kw = dict(actor=self.publisher_model.get_default_table(),
        #     request=request, renderer=rnd, permalink_uris=True)
        kw.update(renderer=rnd, request=request)
        # kw = dict(renderer=rnd, permalink_uris=True)
        # if rnd.front_end.media_name == 'react':
        #     kw.update(hash_router=True)

        kw.update(selected_pks=[pk])
        #
        # print(f"20251025 {self.table_class} {kw}")
        try:
            ar = self.table_class.create_request(**kw)
        except ObjectDoesNotExist as e:
            # print("20240911", e)
            return http.HttpResponseNotFound(
                f"No row #{pk} in {self.table_class} ({e})")
        if len(ar.selected_rows) == 0:
            # print(f"20241003 Oops {ar} has no rows")
            return http.HttpResponseNotFound(
                f"20241003 No row #{pk} in {self.table_class}")
        obj = ar.selected_rows[0]

        # m = self.table_class.model
        # try:
        #     obj = m.objects.get(pk=pk)
        # except m.DoesNotExist as e:
        #     return http.HttpResponseNotFound(f"No row #{pk} in {m} ({e})")
        # ar = BaseRequest(renderer=rnd, request=request, selected_rows=[obj])
        # ar = BaseRequest(renderer=rnd, request=request)
        if settings.SITE.developer_site_cache:
            rnd.build_js_cache(False)
        return obj.get_publisher_response(ar)


class SlaveElement(Element):
    def get(self, request, mk=None, pk=None):
        # mi = self.table_class.get_master_instance()
        # print(f"20251025 {mk} {pk}")
        return super().get(request, pk=pk, master_key=mk)


class Index(View):

    ref = 'home'

    def get(self, request):
        dv = settings.SITE.models.publisher.Pages
        if len(settings.SITE.languages) == 1:
            # language = settings.SITE.languages[0].django_code
            language = translation.get_language()
        else:
            language = request.LANGUAGE_CODE
        # if settings.SITE.plugins.publisher.with_trees:
        #     Tree = settings.SITE.models.publisher.Tree
        #     try:
        #         tree = Tree.objects.get(ref=self.ref)
        #     except Tree.DoesNotExist:
        #         return http.HttpResponseNotFound(f"No tree for {self.ref}")
        #     obj = tree.get_root_page(language)
        # else:
        #     Page = settings.SITE.models.publisher.Page
        #     qs = Page.objects.filter(parent__isnull=True, language=language)
        #     obj = qs.first()
        try:
            obj = SpecialPages.home.get_object(language=language)
        except MultipleObjectsReturned as e:
            return http.HttpResponseNotFound(
                f"Multiple home pages for {language} ({e})")

        # print(20250829, obj)
        if obj is None:
            return http.HttpResponseNotFound(
                f"No root page for {self.ref} in {language}")
        # try:
        #     obj = dv.model.objects.get(
        #         parent=None, publisher_tree=tree)
        # except dv.model.DoesNotExist:
        #     return http.HttpResponseNotFound(f"No row {ref} in {dv.model}")

        # print("20231025", index_node)
        rnd = settings.SITE.plugins.publisher.renderer
        if settings.SITE.developer_site_cache:
            rnd.build_js_cache(False)
        ar = dv.create_request(request=request, renderer=rnd,
                               selected_rows=[obj])
        return obj.get_publisher_response(ar)


class Login(View):
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(request, username=username, password=password)
        
        if user is None:
            return json_response({"success": False})
        
        auth.login(request, user)
        
        return json_response({"success": True})


class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect(request.META.get('HTTP_REFERER', '/'))


class EmptyTable(View):
    """ Renders empty tables in publisher. """

    table_class: Optional[dd.Actor] = None
    publisher_template = "publisher/empty_table.html"

    def get(self, request, field):
        """ request.GET """
        table = self.table_class
        de = table.get_data_elem(field)
        sf = get_atomizer(table, de, field)
        rnd = settings.SITE.plugins.publisher.renderer
        ar = table.create_request(request=request, renderer=rnd)
        table_content = sf.full_value_from_object(table.create_instance(ar), ar)
        context = dict(
            dd=dd,
            obj=None,
            ar=ar,
            home=SpecialPages.home.get_object(),
        )
        context.update(table_content=table_content)
        tpl = dd.plugins.jinja.renderer.jinja_env.get_template(self.publisher_template)
        if settings.SITE.developer_site_cache:
            rnd.build_js_cache(False)
        return http.HttpResponse(
            tpl.render(**context), content_type='text/html;charset="utf-8"')
