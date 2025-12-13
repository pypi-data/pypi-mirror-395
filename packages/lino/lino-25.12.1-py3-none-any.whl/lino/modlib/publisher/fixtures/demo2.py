from asgiref.sync import async_to_sync
from django.conf import settings
from lino.modlib.linod.choicelists import Procedures
from lino.api import rt


def objects():
    yield None
    ar = rt.login("robin")
    if True:  # settings.SITE.use_linod:
        Procedures.update_publisher_pages.run(ar)
        # async_to_sync(Procedures.update_publisher_pages.run)(ar)
