from django.test import TestCase
from django.template import Template, Context
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from content_edit.models import CmsContent


class SimpleTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        user.is_staff = True
        user.save()
        self.client.login(username='temporary', password='temporary')

    def test_edit_content(self):
        """ Test viewing a new content area and chaning it.
        """
        self.assertEqual(CmsContent.objects.count(), 0)

        response = self.client.get(reverse('sample_content_edit'))
        self.assertEqual(CmsContent.objects.count(), 1)
        
    def test_save_content(self):
        """ Test saving content """
        test_content = '<p>Hello</p>'
        response = self.client.get(reverse('sample_content_edit'))
        response = self.client.post(
            reverse('ajax_save_content'), {
            'content_name': 'fun_content',
            'content': test_content,
        },)
        cms_content = CmsContent.objects.get(site=1, name="fun_content")
        self.assertEqual(cms_content.content, test_content)
        response = self.client.get(reverse('sample_content_edit'))
        self.assertContains(response, test_content)


class TemplateTagDefaultSettingsTests(TestCase):
    def setUp(self):  
        self.content1 = CmsContent(name='name1', content='content1',site_id=1)
        self.content1.save()

        self.admin_user = User.objects.create_user('admin', 'admin@gmail.com', 'temporary')
        self.admin_user.is_staff = True
        self.admin_user.save()

        self.user_wo_perm = User.objects.create_user('user_wo_perm', 'admin@gmail.com', 'temporary')
        self.user_wo_perm.save()

        content_type = ContentType.objects.get_for_model(CmsContent)

        self.user_w_add_perm = User.objects.create_user('user_w_add_perm', 'admin@gmail.com', 'temporary')
        self.user_w_add_perm.save()
        add_perm = Permission.objects.create(codename='content_edit_add_cmscontent',
                                       name='add',
                                       content_type=content_type)
        self.user_w_add_perm.user_permissions.add(add_perm)

        self.user_w_change_perm = User.objects.create_user('user_w_change_perm', 'admin@gmail.com', 'temporary')
        self.user_w_change_perm.save()
        change_perm = Permission.objects.create(codename='content_edit_change_cmscontent',
                                       name='change',
                                       content_type=content_type)
        self.user_w_change_perm.user_permissions.add(change_perm)

    def test_existing_content_without_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context())
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')

    def test_existing_content_for_user_without_perms(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.user_wo_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')    

    def test_existing_content_for_user_with_add_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.user_w_add_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')

    def test_existing_content_for_user_with_change_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.user_w_change_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')

    def test_existing_content_for_admin_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.admin_user}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'<div id="content_name1" onblur="save_cms_content(this, \'name1\')" contenteditable="true">content1</div>')

    def test_non_existing_content_without_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context())
        self.assertEqual(2, CmsContent.objects.count())
        self.assertEqual(out,'')
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_user_without_perms(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.user_wo_perm}))
        self.assertEqual(2, CmsContent.objects.count())
        self.assertEqual(out,'')   
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_user_with_add_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.user_w_add_perm}))
        self.assertEqual(2, CmsContent.objects.count())
        self.assertEqual(out,'')
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_user_with_change_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.user_w_change_perm}))
        self.assertEqual(2, CmsContent.objects.count())
        self.assertEqual(out,'')
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_admin_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.admin_user}))
        self.assertEqual(2, CmsContent.objects.count())
        self.assertEqual(out,'<div id="content_name2" onblur="save_cms_content(this, \'name2\')" contenteditable="true"></div>')
        CmsContent.objects.exclude(name='name1').delete()


class TemplateTagNoAUTOCREATETests(TestCase):
    def setUp(self):  

        from content_edit.templatetags import content_edit_tags
        setattr(content_edit_tags,'AUTOCREATE',False)

        self.content1 = CmsContent(name='name1', content='content1',site_id=1)
        self.content1.save()

        self.admin_user = User.objects.create_user('admin', 'admin@gmail.com', 'temporary')
        self.admin_user.is_staff = True
        self.admin_user.save()

        self.user_wo_perm = User.objects.create_user('user_wo_perm', 'admin@gmail.com', 'temporary')
        self.user_wo_perm.save()

        content_type = ContentType.objects.get_for_model(CmsContent)

        self.user_w_add_perm = User.objects.create_user('user_w_add_perm', 'admin@gmail.com', 'temporary')
        self.user_w_add_perm.save()
        add_perm = Permission.objects.create(codename='content_edit_add_cmscontent',
                                       name='add',
                                       content_type=content_type)
        self.user_w_add_perm.user_permissions.add(add_perm)

        self.user_w_change_perm = User.objects.create_user('user_w_change_perm', 'admin@gmail.com', 'temporary')
        self.user_w_change_perm.save()
        change_perm = Permission.objects.create(codename='content_edit_change_cmscontent',
                                       name='change',
                                       content_type=content_type)
        self.user_w_change_perm.user_permissions.add(change_perm)

    def test_existing_content_without_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context())
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')

    def test_existing_content_for_user_without_perms(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.user_wo_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')    

    def test_existing_content_for_user_with_add_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.user_w_add_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')

    def test_existing_content_for_user_with_change_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.user_w_change_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')

    def test_existing_content_for_admin_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.admin_user}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'<div id="content_name1" onblur="save_cms_content(this, \'name1\')" contenteditable="true">content1</div>')

    def test_non_existing_content_without_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context())
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'')
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_user_without_perms(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.user_wo_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'')   
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_user_with_add_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.user_w_add_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'')
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_user_with_change_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.user_w_change_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'')
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_admin_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.admin_user}))
        self.assertEqual(2, CmsContent.objects.count())
        self.assertEqual(out,'<div id="content_name2" onblur="save_cms_content(this, \'name2\')" contenteditable="true"></div>')
        CmsContent.objects.exclude(name='name1').delete()

def tearDown(self):
    from content_edit.templatetags import content_edit_tags
    setattr(content_edit_tags,'AUTOCREATE',True)



class TemplateTagCHECK_PERMSTests(TestCase):
    def setUp(self):  

        from content_edit.templatetags import content_edit_tags
        setattr(content_edit_tags,'CHECK_PERMS',False)

        self.content1 = CmsContent(name='name1', content='content1',site_id=1)
        self.content1.save()

        self.admin_user = User.objects.create_user('admin', 'admin@gmail.com', 'temporary')
        self.admin_user.is_staff = True
        self.admin_user.save()

        self.user_wo_perm = User.objects.create_user('user_wo_perm', 'admin@gmail.com', 'temporary')
        self.user_wo_perm.save()

        content_type = ContentType.objects.get_for_model(CmsContent)

        self.user_w_add_perm = User.objects.create_user('user_w_add_perm', 'admin@gmail.com', 'temporary')
        self.user_w_add_perm.save()
        add_perm = Permission.objects.create(codename='content_edit_add_cmscontent',
                                       name='add',
                                       content_type=content_type)
        self.user_w_add_perm.user_permissions.add(add_perm)

        self.user_w_change_perm = User.objects.create_user('user_w_change_perm', 'admin@gmail.com', 'temporary')
        self.user_w_change_perm.save()
        change_perm = Permission.objects.create(codename='content_edit_change_cmscontent',
                                       name='change',
                                       content_type=content_type)
        self.user_w_change_perm.user_permissions.add(change_perm)

    def test_existing_content_without_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context())
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')

    def test_existing_content_for_user_without_perms(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.user_wo_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')    

    def test_existing_content_for_user_with_add_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.user_w_add_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')

    def test_existing_content_for_user_with_change_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.user_w_change_perm}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'content1')

    def test_existing_content_for_admin_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name1' %}"
        ).render(Context({'user':self.admin_user}))
        self.assertEqual(1, CmsContent.objects.count())
        self.assertEqual(out,'<div id="content_name1" onblur="save_cms_content(this, \'name1\')" contenteditable="true">content1</div>')

    def test_non_existing_content_without_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context())
        self.assertEqual(2, CmsContent.objects.count())
        self.assertEqual(out,'')
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_user_without_perms(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.user_wo_perm}))
        self.assertEqual(2, CmsContent.objects.count())
        self.assertEqual(out,'')   
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_user_with_add_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.user_w_add_perm}))
        self.assertEqual(2, CmsContent.objects.count())
        self.assertEqual(out,'')
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_user_with_change_perm(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.user_w_change_perm}))
        self.assertEqual(2, CmsContent.objects.count())
        self.assertEqual(out,'')
        CmsContent.objects.exclude(name='name1').delete()

    def test_non_existing_content_for_admin_user(self):
        out = Template(
            "{% load content_edit_tags %}"
            "{% cms_content 'name2' %}"
        ).render(Context({'user':self.admin_user}))
        self.assertEqual(2, CmsContent.objects.count())
        self.assertEqual(out,'<div id="content_name2" onblur="save_cms_content(this, \'name2\')" contenteditable="true"></div>')
        CmsContent.objects.exclude(name='name1').delete()

def tearDown(self):
    from content_edit.templatetags import content_edit_tags
    setattr(content_edit_tags,'CHECK_PERMS',True)