from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
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
