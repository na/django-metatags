from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.flatpages.models import FlatPage
from photologue.models import Photo
# Create your models here.


class PageImage(models.Model):
    page = models.OneToOneField(FlatPage,primary_key=True)
    image = models.ForeignKey(Photo)
    
    class Meta:
        verbose_name = _('page image')
        verbose_name_plural = _('page images')
        db_table = 'flatpage_image'
        ordering = ('page',)
   
    def __unicode__(self):
        return "image for %s" % self.page.title

