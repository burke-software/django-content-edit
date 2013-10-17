from django.conf import settings

CHECK_PERMS = getattr(settings, 'CONTENT_EDIT_CHECK_PERMS', False)
ADMIN_WYSIWYG = getattr(settings, 'CONTENT_EDIT_ADMIN_WYSIWYG', True)
AUTOCREATE = getattr(settings, 'CONTENT_EDIT_AUTOCREATE', True)