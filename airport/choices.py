from django.db import models
from django.utils.translation import gettext_lazy as _


class AirplaneName(models.TextChoices):
    BOEING_737 = "B737", _("Boeing-737")
    BOEING_747 = "B747", _("Boeing-747")
    BOEING_777 = "B777", _("Boeing-777")
    BOEING_787 = "B787", _("Boeing-787")
    AIRBUS_310 = "A310", _("Airbus-A310")
    AIRBUS_320 = "A320", _("Airbus-A320")
    AIRBUS_340 = "A340", _("Airbus-A340")
    AIRBUS_360 = "A360", _("Airbus-A360")
    E_Jet_170 = "E170", _("E-Jet-170")
    E_Jet_175 = "E175", _("E-Jet-175")
    E_Jet_190 = "E190", _("E-Jet-190")
    E_Jet_195 = "E195", _("E-Jet-195")


class AirplaneTypeName(models.TextChoices):
    SMALL = "SM", _("Small plane")
    MEDIUM = "MD", _("Medium plane")
    LARGE = "LR", _("Large plane")


class CrewRole(models.TextChoices):
    PILOT = "P", _("Pilot")
    CO_PILOT = "CP", _("Co-Pilot")
    FLIGHT_ATTENDANT = "FA", _("Flight Attendant")
