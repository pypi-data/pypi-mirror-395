# -*- coding: UTF-8 -*-
# Copyright 2021-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.views.generic import View
from lino.core.views import json_response


class Suggestions(View):
    def get(self, request):
        trigger = request.GET.get("trigger")
        query = request.GET.get("query")
        suggester = settings.SITE.plugins.memo.parser.suggesters[trigger]
        return json_response({"suggestions": list(suggester.get_suggestions(query))})
