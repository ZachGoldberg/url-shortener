from django.contrib import admin

from url_shortener.models import Click, Link


class LinkAdmin(admin.ModelAdmin):
    model = Link
    extra = 3
    readonly_fields = ('date_submitted', )


class ClickAdmin(admin.ModelAdmin):
    readonly_fields = ('date', )

admin.site.register(Link, LinkAdmin)
admin.site.register(Click, ClickAdmin)
