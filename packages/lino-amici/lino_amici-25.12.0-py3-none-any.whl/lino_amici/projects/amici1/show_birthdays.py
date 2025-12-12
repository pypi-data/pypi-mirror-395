from datetime import timedelta
from lino.api.shell import *
from django.db.models.functions import Right

qs = contacts.Person.objects.exclude(birth_date='')
qs = qs.annotate(bday=Right("birth_date", 5)).exclude(
    bday="00-00").order_by('bday')

recent = qs.filter(bday__gt=str(dd.today() - timedelta(days=3))[-5:]).filter(
    bday__lt=str(dd.today())[-5:])
coming = qs.filter(bday__lt=str(dd.today() + timedelta(days=3))[-5:]).filter(
    bday__gt=str(dd.today())[-5:])
today = qs.filter(bday=str(dd.today())[-5:])

print("Birthdays today:",
      ", ".join(["{} {}".format(obj.birth_date, obj) for obj in today]))
print("Recent birthdays:",
      ", ".join(["{} {}".format(obj.birth_date, obj) for obj in recent]))
print("Upcoming birthdays:",
      ", ".join(["{} {}".format(obj.birth_date, obj) for obj in coming]))
