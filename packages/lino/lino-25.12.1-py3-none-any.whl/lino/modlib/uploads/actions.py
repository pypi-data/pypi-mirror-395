# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import rt, dd, _
from .mixins import base64_to_image


class CameraStream(dd.Action):  # TODO: rename this to CaptureImage
    """Uses ImageCapture API to take images and videos through device camera"""

    label = _("Camera")
    select_rows = False
    http_method = "POST"
    button_text = "📷"  # U+1F4F7
    show_in_side_toolbar = True

    preprocessor = "Lino.captureImage"

    parameters = {
        "description": dd.CharField(_("Description"), max_length=200, blank=True),
        "type": dd.ForeignKey("uploads.UploadType", blank=True, null=True),
    }

    params_layout = """
    type
    description
    """

    def handle_uploaded_file(self, ar, **kwargs):
        file = base64_to_image(ar.request.POST["image"])
        upload = rt.models.uploads.Upload(file=file, user=ar.get_user(), **kwargs)
        upload.save_new_instance(ar)
        return upload

    def run_from_ui(self, ar, **kwargs):
        upload = self.handle_uploaded_file(ar, **ar.action_param_values)
        ar.goto_instance(upload)
