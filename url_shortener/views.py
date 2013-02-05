from django.shortcuts import (
    get_object_or_404,
    render_to_response)
from django.http import (
    Http404,
    HttpResponseRedirect)
from django.template import RequestContext
from django.conf import settings

from url_shortener.models import Click, Link, LinkSubmitForm


def follow(request, shortcut):
    """
    View which gets the link for the given shortcut value
    and redirects to it.
    """
    try:
        link = Link.objects.get(shortcut=shortcut)
        link.usage_count += 1
        link.save()

        Click.objects.create(
            link=link,
            user=request.user,
            useragent=request.META['HTTP_USER_AGENT'])

        return HttpResponseRedirect(link.url)
    except:
        values = default_values(request)
        values["error"] = "This shortcut doesn't yet exit.  Create it now!"
        values["link_form"].initial["shortcut"] = shortcut
        return index(request, values)


def default_values(request, link_form=None):
    """
    Return a new object with the default values that are typically
    returned in a request.
    """
    if not link_form:
        link_form = LinkSubmitForm()

    allowed_to_submit = is_allowed_to_submit(request)
    return {'show_bookmarklet': allowed_to_submit,
            'show_url_form': allowed_to_submit,
            'site_name': settings.SITE_NAME,
            'site_base_url': settings.SITE_BASE_URL,
            'link_form': link_form,
            }


def info(request, shortcut):
    """
    View which shows information on a particular link
    """
    link = get_object_or_404(Link, shortcut=shortcut)
    values = default_values(request)
    values['link'] = link
    return render_to_response(
        'shortener/link_info.html',
        values,
        context_instance=RequestContext(request))


def submit(request):
    """
    View for submitting a URL
    """
    if settings.REQUIRE_LOGIN and not request.user.is_authenticated():
        # TODO redirect to an error page
        raise Http404
    url = None
    link_form = None
    if request.GET:
        link_form = LinkSubmitForm(request.GET)
    elif request.POST:
        link_form = LinkSubmitForm(request.POST)
    if link_form and link_form.is_valid():
        url = link_form.cleaned_data['url']
        shortcut = link_form.cleaned_data['shortcut']
        submitter = request.user
        link = None
        try:
            link = Link.objects.get(shortcut=shortcut)
        except Link.DoesNotExist:
            pass

        if link is None:
            new_link = Link(url=url,
                            shortcut=shortcut,
                            submitter=submitter)
            new_link.save()
            link = new_link
        values = default_values(request)
        values['link'] = link
        return render_to_response(
            'shortener/submit_success.html',
            values,
            context_instance=RequestContext(request))
    values = default_values(request, link_form=link_form)
    return render_to_response(
        'shortener/submit_failed.html',
        values,
        context_instance=RequestContext(request))


def index(request, values=None):
    """
    View for main page (lists recent and popular links)
    """
    if not values:
        values = default_values(request)

    values['recent_links'] = Link.objects.all().order_by(
        '-date_submitted')[0:10]
    values['most_popular_links'] = Link.objects.all().order_by(
        '-usage_count')[0:10]
    return render_to_response(
        'shortener/index.html',
        values,
        context_instance=RequestContext(request))


def is_allowed_to_submit(request):
    """
    Return true if user is allowed to submit URLs
    """
    return not settings.REQUIRE_LOGIN or request.user.is_authenticated()
