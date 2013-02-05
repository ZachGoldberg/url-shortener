from django.db import models
from django.conf import settings
from django import forms


class Link(models.Model):
    """
    Model that represents a shortened URL

    # Initialize by deleting all Link objects
    >>> Link.objects.all().delete()

    # Create some Link objects
    >>> link1 = Link.objects.create(url="http://www.google.com/")
    >>> link2 = Link.objects.create(url="http://www.nileshk.com/")

    # Get base 62 representation of id
    >>> link1.to_base62()
    'B'
    >>> link2.to_base62()
    'C'

    # Set SITE_BASE_URL to something specific
    >>> settings.SITE_BASE_URL = 'http://uu4.us/'

    # Get short URL's
    >>> link1.short_url()
    'http://uu4.us/B'
    >>> link2.short_url()
    'http://uu4.us/C'

    # Test usage_count
    >>> link1.usage_count
    0
    >>> link1.usage_count += 1
    >>> link1.usage_count
    1

    """
    url = models.URLField(verify_exists=True)
    shortcut = models.CharField(max_length=128, unique=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    usage_count = models.IntegerField(default=0)

    def short_url(self):
        return settings.SITE_BASE_URL + self.shortcut

    def __unicode__(self):
        return "%s (http://go/%s)" % (self.url, self.shortcut)


class LinkSubmitForm(forms.Form):
    url = forms.URLField(verify_exists=True,
                         label='URL to be shortened',
                         )
    shortcut = forms.CharField(max_length=128,
                               label='Shortcut text')
