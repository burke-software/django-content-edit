django-content-edit
===================

A very simple way to let users edit content on the front end of a website when you don't quite need a full CMS.

django-content-edit is not a CMS. Use something like django-cms for that. django-content-edit is for when you 
just need a few editable areas in your templates.

- Allow designers to insert staff editable content without learning a CMS or Django models
- Logged in staff can edit content on the frontend with ckeditor inline. Admin view is optional!
- Content can be reused on the same site with the same name. Content is unique per Site
- Currently requires the Django Sites framework

[![Build Status](https://travis-ci.org/burke-software/django-content-edit.png?branch=master)](https://travis-ci.org/burke-software/django-content-edit)

![ScreenShot](/images/screen.png)

# Setup

1. pip install django-content-edit
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
```

