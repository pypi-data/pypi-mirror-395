import autoslug
from django.db import models
from django.utils.translation import gettext_lazy as _

from geobank.enums import ContinentChoices


class Language(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    code2 = models.CharField(max_length=2, blank=True, verbose_name=_("ISO 639-1 Code"))
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    symbol = models.CharField(max_length=10, verbose_name=_("Symbol"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return f"{self.name} ({self.code})"


class BaseModel(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    name_ascii = models.CharField(max_length=200, blank=True, db_index=True)
    slug = autoslug.AutoSlugField(populate_from="name_ascii")
    geoname_id = models.IntegerField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["name"]


class Country(BaseModel):
    code2 = models.CharField(
        max_length=2,
        unique=True,
        verbose_name=_("ISO Alpha-2 Code"),
    )
    code3 = models.CharField(
        max_length=3,
        unique=True,
        verbose_name=_("ISO Alpha-3 Code"),
    )
    fips = models.CharField(
        max_length=2,
        blank=True,
        verbose_name=_("FIPS Code"),
    )
    continent = models.CharField(
        max_length=2,
        db_index=True,
        verbose_name=_("Continent"),
        choices=ContinentChoices.choices,
    )
    tld = models.CharField(
        max_length=5,
        blank=True,
        verbose_name=_("Top Level Domain"),
    )
    population = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Population"),
    )
    postal_code_format = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Postal Code Format"),
    )
    postal_code_regex = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Postal Code Regex"),
    )
    flag_png = models.URLField(
        max_length=500, blank=True, null=True, verbose_name=_("Flag PNG URL")
    )
    flag_svg = models.URLField(
        max_length=500, blank=True, null=True, verbose_name=_("Flag PNG URL")
    )
    languages = models.ManyToManyField(
        Language,
        related_name="countries",
        verbose_name=_("Languages"),
        blank=True,
        help_text=_("Languages spoken in the country"),
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="countries",
        verbose_name=_("Currency"),
        null=True,
        blank=True,
    )
    neighbors = models.ManyToManyField(
        "self",
        verbose_name=_("Neighbors"),
        blank=True,
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name


class CallingCode(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="calling_codes",
        verbose_name=_("Country"),
    )
    code = models.CharField(
        max_length=20,
        verbose_name=_("Code"),
    )

    class Meta:
        verbose_name = _("Calling Code")
        verbose_name_plural = _("Calling Codes")

    def __str__(self):
        return f"{self.country.name}: {self.code}"


class Region(BaseModel):
    code = models.CharField(
        max_length=10,
        verbose_name=_("Code"),
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="regions",
        verbose_name=_("Country"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
        unique_together = (
            "country",
            "code",
        )

    def __str__(self):
        return f"{self.name} ({self.country.code2})"


class City(BaseModel):
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name=_("Latitude"),
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name=_("Longitude"),
        null=True,
        blank=True,
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name=_("Country"),
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name=_("Region"),
        null=True,
        blank=True,
    )
    population = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Population"),
    )
    timezone = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name=_("Timezone"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return f"{self.name}, {self.country.code2}"
