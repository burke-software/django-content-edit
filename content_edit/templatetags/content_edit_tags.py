from django import template
from django.contrib.auth.models import AnonymousUser 
try:
    from django.contrib.sites.models import get_current_site
    site = True
except:
    site = False


from content_edit.models import CmsContent
from content_edit.settings import *

register = template.Library()

class CmsContentNode(template.Node):
    def __init__(self, content_name):
        self.content_name = content_name
    def render(self, context):
        user = context.get('user', None)
        request = context.get('request',None)
        if not user:
            if request:
                user = getattr(request, 'user', None)
            if not user:
                user = AnonymousUser()
        current_site=None

        object_filter = {'name': self.content_name}

        # Get current Site object (if used)
        if site:
            if request:
                current_site = get_current_site(request)
            if current_site:
                object_filter['site'] = current_site
            else:
                object_filter['site_id'] = 1

        # Get current content object
        if AUTOCREATE or (not CHECK_PERMS and user.is_staff) or (CHECK_PERMS and user.has_perm('content_edit_add_cmscontent')):
            content = CmsContent.objects.get_or_create(**object_filter)[0]
        else:
            try:
                content = CmsContent.objects.get(**object_filter)
            except CmsContent.DoesNotExist:
                content= CmsContent(content='')

        # Check user Perms
        change_perm = False
        if user.is_authenticated():
            if (CHECK_PERMS and user.has_perm('content_edit_change_cmscontent')) or (not CHECK_PERMS and user.is_staff):
                change_perm = True

        # Generate content
        if change_perm:
            html_content = '<div id="content_{0}" onblur="save_cms_content(this, \'{0}\')" contenteditable="true">{1}</div>'.format(
                content.name, content.content)
        else:
            html_content = content.content
        return html_content

@register.tag(name="cms_content")
def do_cms_content(parser, token):
    """ Get or create the cms content for this site and name
    then render it
    """
    try:
        tag_name, content_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])
    if not (content_name[0] == content_name[-1] \
        and content_name[0] in ('"', "'")):
            raise template.TemplateSyntaxError(
                "%r tag's argument should be in quotes" % tag_name)
    return CmsContentNode(content_name[1:-1])

