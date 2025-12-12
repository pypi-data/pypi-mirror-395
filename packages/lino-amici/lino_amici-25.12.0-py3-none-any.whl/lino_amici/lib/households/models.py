from lino.api import dd, _
from lino_xl.lib.households.models import *


class HouseholdDetail(dd.DetailLayout):
    main = "general more"

    general = dd.Panel("""
    address_box
    bottom_box
    """,
                       label=_("General"))

    address_box = "overview:40 data_box:30 lists.MembersByPartner:30"

    data_box = """
    type
    prefix
    name
    language id
    """

    more = dd.Panel("""
    uploads.UploadsByController:30 comments.CommentsByRFC:50
    """,
                    label=_("More"))

    bottom_box = "households.MembersByHousehold"
