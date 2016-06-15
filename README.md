django-content-edit
===================

A very simple way to let users edit content on the front end of a website when you don't quite need a full CMS.

django-content-edit is not a CMS. Use something like django-cms for that. django-content-edit is for when you 
just need a few editable areas in your templates.

- Allow designers to insert staff editable content without learning a CMS or Django models
- Logged in staff can edit content on the frontend with ckeditor inline. Admin view is optional!
- Content can be reused on the same site with the same name. Content is unique per Site

[![Build Status](https://travis-ci.org/burke-software/django-content-edit.png?branch=master)](https://travis-ci.org/burke-software/django-content-edit)

![ScreenShot](/images/screen.png)

# Setup

This currently support Django 1.9 and Python 3.5.

1. `pip install django-content-edit`
1. Run `python manage.py syncdb --migrate` You can run without south's --migrate, but I don't suggest it.
1. Add `'content_edit',` to INSTALLED_APPS
1. Add `url(r'^content_edit/', include('content_edit.urls')),` to urls.py
1. Add these to your templates as needed. Checkout the sample template in content_edit/templates for an example.

```
{% load content_edit_tags %}
{% load static %}
<script type="text/javascript" src='{% static 'ckeditor/ckeditor.js' %}'></script>
<script type="text/javascript" src='{% static 'jquery/jquery.js' %}'></script>
<script type="text/javascript" src='{% static 'content_edit/content_edit.js' %}'></script>
...
{% cms_content 'any_name_you_want' %}
```

# Settings

The following app-specific settings are available to customize the bevhavior.

- CONTENT_EDIT_AUTOCREATE
Controls, whether a new content objects is created automatically, when the specific name is requested via the template tag, but no content object exists for that name; default: True

- CONTENT_EDIT_CHECK_PERMS
Controls, whether add and change permissions of the current user are checked in the template tag; default: False

- CONTENT_EDIT_ADMIN_WYSIWYG
Defines, how the content is repesented in the admin for editing. Either via a WYSIWIG editor or via a normal Textarea Widget; default: True
