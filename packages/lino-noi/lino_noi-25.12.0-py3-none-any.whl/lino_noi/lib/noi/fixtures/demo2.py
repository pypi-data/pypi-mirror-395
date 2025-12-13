# -*- coding: UTF-8 -*-
# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger
from lino.utils import Cycler
from lino.api import rt, dd, _


def objects():
    if not dd.is_installed('uploads'):
        return

    if not dd.is_installed('tickets'):
        return

    Ticket = rt.models.tickets.Ticket
    Upload = rt.models.uploads.Upload

    SCREENSHOTS = Cycler(Upload.objects.filter(volume__ref="screenshots"))
    if len(SCREENSHOTS) == 0:
        # e.g. when lino_book is not installed.
        return
    #     raise Exception("The noi plugin must be installed after uploads")

    qs = Ticket.objects.filter(description='')
    logger.info("Add {} screenshots to {} tickets.".format(
        len(SCREENSHOTS), qs.count()))
    for t in qs:
        shot = SCREENSHOTS.pop()
        t.description = f"<p>Screenshot:</p><p>[file {shot.id}]</p>"
        yield t
