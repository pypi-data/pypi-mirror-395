# -*- coding: UTF-8 -*-
# Copyright 2011-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""This middleware was automatically being installed on every Lino site until
20240921. No longer used since then. See :ticket:`5755` (Should we remove
AjaxExceptionResponse?)

The idea was that when an exception occurs during an AJAX call, Lino should not
respond with Django's default HTML formatted error report but with a plain-text
traceback because that's more readable when seen in a browser console.

Originally inspired by https://djangosnippets.org/snippets/650

Additions by LS:

- also logs a warning on the development server because that is easier
  to read than opening firebug and look at the response.

- must work also when :setting:`DEBUG` is False. Yes, on a production
  server it is not wise to publish the traceback, but our nice HTML
  formatted "Congratulations, you found a problem" page is never the
  right answer to an AJAX call.

- :func:`format_request` adds information about the incoming call,
  including POST or PUT data.

"""

import sys
import traceback
from django.conf import settings

# from django.http import HttpResponseServerError
from django.http import HttpResponse

# from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.utils.encoding import smart_str
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from lino.core.utils import format_request

from django.utils.deprecation import MiddlewareMixin


class AjaxExceptionResponse(MiddlewareMixin):
    """The middleware class definition."""

    no_traceback = (PermissionDenied, ObjectDoesNotExist)
    # no_traceback = (PermissionDenied, )

    # see also /docs/specs/invalid_requests.rst
    # it can be helpful to temporarily disable filtering of ObjectDoesNotExist
    # exceptions on a production site in order to debug problems like #2699

    # 20240920 I had a sporadic ObjectDoesNotExist exception on a production
    # server that took me a while to understand because there was no log message
    # at all.

    def process_exception(self, request, exception):
        # if request.is_ajax():  # See https://docs.djangoproject.com/en/5.2/releases/3.1/
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            (exc_type, exc_info, tb) = sys.exc_info()
            # response to client:
            response = "AjaxExceptionResponse {}: {}".format(
                exc_type.__name__, exc_info)
            # message to be logged:
            msg = response + "\nin request {0}\n".format(format_request(request))
            if isinstance(exception, self.no_traceback):
                settings.SITE.logger.warning(msg)
            elif settings.DEBUG:
                msg += "TRACEBACK:\n"
                for tb in traceback.format_tb(tb):
                    msg += smart_str(tb)
                settings.SITE.logger.warning(msg)
            else:
                settings.SITE.logger.exception(msg)
            return HttpResponse(response, status=400)
            # if isinstance(exception, ObjectDoesNotExist):
            #     return HttpResponseBadRequest(response)
            # return HttpResponseServerError(response)
