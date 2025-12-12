from modeltranslation.translator import TranslationOptions, register

from .models import City, Country, Region


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("name",)
