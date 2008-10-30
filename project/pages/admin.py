from django import forms
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django import template
from metatags.models import Metatag, MetatagType
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.contenttypes import generic
from django.http import HttpResponseRedirect
admin.site.unregister(FlatPage)

class MetatagInline(generic.GenericTabularInline):
    model = Metatag
    extra = 1

class FlatPageForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/]+$',
        help_text = _("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."),
        error_message = _("This value must contain only letters, numbers,"
                          " underscores, dashes or slashes."))

    class Meta:
        model = FlatPage

class FlatPageCreateForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/]+$',
        help_text = _("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."),
        error_message = _("This value must contain only letters, numbers,"
                          " underscores, dashes or slashes."))

    class Meta:
        model = FlatPage
        fields = ('url', 'title',)
        
    def save(self, commit=True):
        page = super(FlatPageCreateForm, self).save(commit=False)
        if commit:
            page.save()
        return page

class FlatPageAdmin(admin.ModelAdmin):
    
    form = FlatPageForm
    add_form = FlatPageCreateForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content','sites')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name')}),
    )
    list_display = ('url', 'title')
    list_filter = ('sites', 'enable_comments', 'registration_required')
    search_fields = ('url', 'title')
    inlines = [
        MetatagInline,
    ]

    def add_view(self, request):
        if not self.has_change_permission(request):
            raise PermissionDenied
        if request.method == 'POST':
            form = self.add_form(request.POST)
            if form.is_valid():
                new_page = form.save()
                current_site = Site.objects.get_current()
                new_page.sites.add(current_site)
                description = MetatagType.objects.get(value='description')
                keywords = MetatagType.objects.get(value='keywords')
                page_description = Metatag.objects.create(type=description,content_object=new_page)
                page_keywords = Metatag.objects.create(type=keywords,content_object=new_page)
                if "_addanother" in request.POST:
                    return HttpResponseRedirect(request.path)
                elif '_popup' in request.REQUEST:
                    return self.response_add(request, new_page)
                else:    
                    return HttpResponseRedirect('../%s/' % new_page.id)
        else:
            form = self.add_form()
            print self.add_form
        return render_to_response('admin/pages/add_form.html', {
            'title': _('Add flatpage'),
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_add_permission': True,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_file_field': False,
            'has_absolute_url': False,
            'auto_populated_fields': (),
            'opts': self.model._meta,
            'save_as': False,
            'url_help_text': self.model._meta.get_field('url').help_text,
            'root_path': self.admin_site.root_path,
            'app_label': self.model._meta.app_label,            
        }, context_instance=template.RequestContext(request))
admin.site.register(FlatPage, FlatPageAdmin)