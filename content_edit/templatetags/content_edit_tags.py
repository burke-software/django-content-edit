from django import template
from django.contrib.sites.models import get_current_site
from content_edit.models import CmsContent

register = template.Library()

class CmsContentNode(template.Node):
    def __init__(self, content_name):
        self.content_name = content_name
    def render(self, context):
        site = get_current_site(context['request'])
        content = CmsContent.objects.get_or_create(
            site=site, name=self.content_name)[0]
        if context['request'].user.is_staff:
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

