from django.contrib import admin
from django.forms.widgets import Textarea

from ckeditor.fields import RichTextField
import reversion.admin

from content_edit.models import CmsContent
from content_edit.settings import *

class CmsContentAdmin(reversion.admin.VersionAdmin):
    list_display = ('name', 'site',)
    list_filter = ('site',)
    search_fields = ('name','content')
    if not ADMIN_WYSIWYG:
        formfield_overrides = {
            RichTextField: {'widget': Textarea }
        }

admin.site.register(CmsContent, CmsContentAdmin)
