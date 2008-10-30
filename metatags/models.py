from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from metatags.managers import MetaTagManager
from django.contrib import admin

ATTRIBUTE_CHOICES = (
    ('name','name'),
    ('http-equiv','http-equiv'),
)

class MetatagType(models.Model):
    #metatag attribute list
    attribute   = models.CharField(_('attribute'),max_length=64,choices=ATTRIBUTE_CHOICES)
    value       = models.CharField(_('value'),max_length=128)

    def __unicode__(self):
        return self.value

class Metatag(models.Model):
    #meta tag attributes
    type        = models.ForeignKey(MetatagType)
    content     = models.TextField(_('content'), help_text = _('Content of the metatag.'))
    scheme      = models.CharField(_('scheme'), max_length=64, blank=True, help_text = _('Scheme attribute'))
    
    # Content-object field
    content_type   = models.ForeignKey(ContentType,
            related_name="content_type_set_for_%(class)s")
    object_id      = models.PositiveIntegerField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")

    class meta():
        unique_together = ("type","content_object")
        verbose_name = _('Html metatag')
        verbose_name_plural = _('Html metatags')

    objects = MetaTagManager()
    
    def _content_object(self):
        return "%s" % self.content_object
    _content_object.short_description = "Content object"

    def __unicode__(self):
        return "%s: %s" % (self.type, self.content_object)
    