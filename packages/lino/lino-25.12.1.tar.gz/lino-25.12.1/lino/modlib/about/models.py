# Copyright 2012-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime

# from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext
from django.utils.html import mark_safe, format_html
from django.conf import settings

from lino.utils.report import EmptyTable
# from lino.utils.jsgen import js_code
from lino.utils.code import codetime
from lino.utils.diag import analyzer
from lino.utils.html import E, join_elems, forcetext, tostring

from lino.api import rt, dd

from .choicelists import TimeZones, DateFormats


def dtfmt(dt):
    if isinstance(dt, float):
        # assert dt
        dt = datetime.datetime.fromtimestamp(dt)
        # raise ValueError("Expected float, go %r" % dt)
    return gettext("%(date)s at %(time)s") % dict(
        date=dd.fds(dt.date()), time=settings.SITE.strftime(dt.time())
    )


class About(EmptyTable):
    """
    The window that opens via the menu command :menuselection:`Site --> About`.
    This window shows information about this :term:`Lino site`.

    """

    label = _("About")
    help_text = _("Show information about this site.")
    required_roles = set()
    hide_top_toolbar = True
    detail_layout = dd.DetailLayout(
        """
    about_html
    # server_status
    """,
        window_size=(60, 20),
    )

    # @dd.constant()
    # def about_html(cls):
    @dd.htmlbox()
    def about_html(cls, obj, ar=None):
        site = settings.SITE
        body = ""

        body += "".join([tostring(e) for e in site.welcome_html()])

        for p in site.sorted_plugins:
            for i in p.get_site_info(ar):
                body += i

        if site.languages:
            body += tostring(
                E.p(
                    str(_("Languages"))
                    + ": "
                    + ", ".join([lng.django_code for lng in site.languages])
                )
            )

        # print "20121112 startup_time", site.startup_time.date()
        # showing startup time here makes no sense as this is a constant text
        # body.append(E.p(
        #     gettext("Server uptime"), ' : ',
        #     E.b(dtfmt(site.startup_time)),
        #     ' ({})'.format(settings.TIME_ZONE)))
        if site.is_demo_site:
            body += tostring(E.p(gettext(_("This is a Lino demo site."))))
        if site.the_demo_date:
            s = _("We are running with simulated date set to {0}.").format(
                dd.fdf(site.the_demo_date)
            )
            body += tostring(E.p(s))

        # features = []
        # for k, v in site.features.items():
        #     if v:
        #         features.append(k)
        # body += tostring(E.p("{} : {}".format(
        #     _("Enabled features:"), ", ".join(features))))

        # style = "border: 1px solid black; border-radius: 2px; padding: 5px;"
        #
        # f_table_head = []
        # f_table_head.append(E.th(str(_("Feature")), style=style))
        # f_table_head.append(E.th(str(_("Description")), style=style))
        # f_table_head.append(E.th(str(_("Status")), style=style))
        # thead = E.thead(E.tr(*f_table_head))
        # trs = []
        #
        # for key in feats:
        #     row = E.tr(E.td(key, style=style), E.td(str(feats[key]['description']), style=style),
        #     E.td(str(_("Active")) if key in site.features.active_features else str(_("Inactive")), style=style))
        #     trs.append(row)
        # tbody = E.tbody(*trs)
        # body.append(E.table(thead, tbody))

        body += tostring(E.p(str(_("Source timestamps:"))))
        items = []
        times = []
        packages = set(["django"])

        items.append(
            E.li(gettext("Server timestamp"), " : ",
                 E.b(dtfmt(site.kernel.lino_version))))

        for p in site.installed_plugins:
            packages.add(p.app_name.split(".")[0])
        for src in packages:
            label = src
            value = codetime(src)
            if value is not None:
                times.append((label, value))

        times.sort(key=lambda x: x[1])
        for label, value in times:
            items.append(E.li(str(label), " : ", E.b(dtfmt(value))))
        body += tostring(E.ul(*items))
        body += tostring(
            E.p(
                "{} : {}".format(
                    _("Complexity factors"),
                    ", ".join(analyzer.get_complexity_factors(dd.today())),
                )
            )
        )
        body = mark_safe(body)
        body = format_html("<div>{}</div>", body)
        # return js_code(rt.html_text(body))
        # return rt.html_text(body)
        # return mark_safe(body)
        # print("20230313", repr(body))
        return body

    # @dd.displayfield(_("Server status"))
    # def server_status(cls, obj, ar):
    #     st = settings.SITE.startup_time
    #     return rt.html_text(
    #         E.p(_("Running since {} ({}) ").format(
    #             st, naturaltime(st))))
