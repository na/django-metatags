from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from basic.metatags.managers import MetaTagManager
# Create your models here.

class Metatag(models.Model):
    #meta tag attributes
    name            = models.CharField(_('name attribute'),max_length=25,help_text=_('Name attribute for the meta tag'))
    content         = models.TextField(_('content attribute'),help_text = _('Content attribute for the meta tag'))
    
    # Content-object field
    content_type   = models.ForeignKey(ContentType,
            related_name="content_type_set_for_%(class)s")
    object_id      = models.PositiveIntegerField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")
    
    objects = MetaTagManager()