====================
Django Html Metatags
====================

A django app which provides the ability to attach metatags to an object through a generic foreign key.
The app adds a template tag for retreiving the metatags of the object. 

Installation
============
#. Add the `metatags` folder to your python path.
#. Add `metatags` to your `INSTALLED_APPS` setting.

Now log in to your admin site and create some metatags. Check out the included project for an 
example of integrating metatags with flatpages. 

If you don't want to use metatags but don't want to include them in your admin site just unregister
the admin somewhere in your project:
    ``from metatags.models import Metatags, MetatagTypes
      from django.contrib import admin
      
      admin.site.unregister(Metatags)
      admin.site.unregister(MetatagTypes)``