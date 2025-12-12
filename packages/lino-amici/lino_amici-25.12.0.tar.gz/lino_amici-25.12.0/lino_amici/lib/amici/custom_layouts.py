from lino.api import rt

rt.models.cal.GuestsByEvent.column_names = 'partner role remark workflow_buttons *'

rt.models.countries.Places.detail_layout = """
name country
type parent zip_code id
addresses.AddressesByCity
contacts.PartnersByCity PlacesByPlace
"""

rt.models.system.SiteConfigs.set_detail_layout("""
#site_company #next_partner_id:10
default_build_method simulate_today
site_calendar default_event_type pupil_guestrole
max_auto_events hide_events_before
""",
                                               window_size=(60, 'auto'))
