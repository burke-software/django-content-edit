django-content-edit
===================

A very simple way to let users edit content on the front end of a website when you don't quite need a full CMS.

# Setup

1. pip install django-content-edit
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

