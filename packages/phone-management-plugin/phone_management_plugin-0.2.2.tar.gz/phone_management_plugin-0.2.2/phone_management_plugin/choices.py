from django.utils.translation import gettext_lazy as _
from utilities.choices import ChoiceSet


class PhoneRangeTypeChoices(ChoiceSet):
    key = "PhoneNumberRange.type"

    TYPE_FREEPHONE = "freephone"
    TYPE_FIXED = "fixed"
    TYPE_MOBILE = "mobile"

    CHOICES = [
        (TYPE_FREEPHONE, "Freephone", "red"),
        (TYPE_FIXED, "Fixed", "green"),
        (TYPE_MOBILE, "Mobile", "blue"),
    ]


class PhoneNumberStatusChoises(ChoiceSet):
    key = "PhoneNumber.type"

    STATUS_ACTIVE = "active"
    STATUS_RESERVED = "reserved"
    STATUS_DEPRECATED = "deprecated"

    CHOICES = [
        (STATUS_ACTIVE, _("Active"), "blue"),
        (STATUS_RESERVED, _("Reserved"), "cyan"),
        (STATUS_DEPRECATED, _("Deprecated"), "red"),
    ]


class PhoneCountryCodeChoises(ChoiceSet):
    COUNTRY_BELGIUM = "+32"
    COUNTRY_NETHERLANDS = "+31"
    COUNTRY_FRANCE = "+33"
    COUNTRY_AUSTRIA = "+43"
    COUNTRY_BULGARIA = "+359"
    COUNTRY_CROATIA = "+385"
    COUNTRY_CYPRUS = "+357"
    COUNTRY_CZECH = "+420"
    COUNTRY_DENMARK = "+45"
    COUNTRY_ESTONIA = "+372"
    COUNTRY_FINLAND = "+358"
    COUNTRY_GERMANY = "+49"
    COUNTRY_GREECE = "+30"
    COUNTRY_HUNGARY = "+36"
    COUNTRY_ICELAND = "+354"
    COUNTRY_IRELAND = "+353"
    COUNTRY_ITALY = "+39"
    COUNTRY_LATVIA = "+371"
    COUNTRY_LIECHTENSTEIN = "+423"
    COUNTRY_LITHUANIA = "+370"
    COUNTRY_LUXEMBOURG = "+352"
    COUNTRY_MALTA = "+356"
    COUNTRY_NORWAY = "+47"
    COUNTRY_POLAND = "+48"
    COUNTRY_PORTUGAL = "+351"
    COUNTRY_ROMANIA = "+40"
    COUNTRY_SLOVAKIA = "+421"
    COUNTRY_SLOVENIA = "+386"
    COUNTRY_SPAIN = "+34"
    COUNTRY_SWEDEN = "+46"

    CHOICES = [
        (COUNTRY_BELGIUM, _("Belgium (+32)")),
        (COUNTRY_NETHERLANDS, _("Netherlands (+31)")),
        (COUNTRY_FRANCE, _("France (+33)")),
        (COUNTRY_AUSTRIA, _("Austria (+43)")),
        (COUNTRY_BULGARIA, _("Bulgaria (+359)")),
        (COUNTRY_CROATIA, _("Croatia (+385)")),
        (COUNTRY_CYPRUS, _("Cyprus (+357)")),
        (COUNTRY_CZECH, _("Czech Republic (+420)")),
        (COUNTRY_DENMARK, _("Denmark (+45)")),
        (COUNTRY_ESTONIA, _("Estonia (+372)")),
        (COUNTRY_FINLAND, _("Finland (+358)")),
        (COUNTRY_GERMANY, _("Germany (+49)")),
        (COUNTRY_GREECE, _("Greece (+30)")),
        (COUNTRY_HUNGARY, _("Hungary (+36)")),
        (COUNTRY_ICELAND, _("Iceland (+354)")),
        (COUNTRY_IRELAND, _("Ireland (+353)")),
        (COUNTRY_ITALY, _("Italy (+39)")),
        (COUNTRY_LATVIA, _("Latvia (+371)")),
        (COUNTRY_LIECHTENSTEIN, _("Liechtenstein (+423)")),
        (COUNTRY_LITHUANIA, _("Lithuania (+370)")),
        (COUNTRY_LUXEMBOURG, _("Luxembourg (+352)")),
        (COUNTRY_MALTA, _("Malta (+356)")),
        (COUNTRY_NORWAY, _("Norway (+47)")),
        (COUNTRY_POLAND, _("Poland (+48)")),
        (COUNTRY_PORTUGAL, _("Portugal (+351)")),
        (COUNTRY_ROMANIA, _("Romania (+40)")),
        (COUNTRY_SLOVAKIA, _("Slovakia (+421)")),
        (COUNTRY_SLOVENIA, _("Slovenia (+386)")),
        (COUNTRY_SPAIN, _("Spain (+34)")),
        (COUNTRY_SWEDEN, _("Sweden (+46)")),
    ]
