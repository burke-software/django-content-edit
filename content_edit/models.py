from django.db import models
from ckeditor.fields import RichTextField

from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

class CmsContent(models.Model):
    """ CMS like Content area """
    name = models.CharField(max_length=255, unique=True)
    content = RichTextField(blank=True)
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __unicode__(self):
        return self.name
