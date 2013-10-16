from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.models import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from content_edit.models import CmsContent

@staff_member_required
def ajax_save_content(request):
    """ Save front end edited content """
    site = get_current_site(request)
    content_name = request.POST['content_name']
    cms_content = CmsContent.objects.get(site=site, name=content_name)
    cms_content.content = request.POST['content']
    cms_content.save()
    return HttpResponse('SUCCESS')

@staff_member_required
def sample_content_edit(request):
    """ Just a test and demo view """
    return render(request, 'content_edit/sample_content_edit.html')
