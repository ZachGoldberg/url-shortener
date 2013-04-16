from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


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
    url = models.URLField()
    shortcut = models.CharField(max_length=128, unique=True)
    submitter = models.ForeignKey(User, null=True)

    date_submitted = models.DateTimeField(auto_now_add=True)
    usage_count = models.IntegerField(default=0)

    def short_url(self):
        return settings.SITE_BASE_URL + self.shortcut

    def __unicode__(self):
        return "%s (http://go/%s)" % (self.url, self.shortcut)


class Click(models.Model):
    link = models.ForeignKey(Link)
    date = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, null=True)
    useragent = models.CharField(max_length=256)

    def __unicode__(self):
        return "%s at %s by %s" % (self.link.shortcut, self.date, self.user)


class LinkSubmitForm(forms.Form):
    url = forms.URLField(
                         label='URL to be shortened',
                         )
    shortcut = forms.CharField(max_length=128,
                               label='Shortcut text')

    def __init__(self, *args, **kwargs):
        super(LinkSubmitForm, self).__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['autofocus'] = 'autofocus'
