from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .models import Poet, Poem

User = get_user_model()


class TestPoems(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='admin')
        self.auth_client = Client()
        self.unauth_client = Client()

        self.auth_client.force_login(self.user)

        self.photo_url = 'https://wiki.tarantino.info/images/Jules.jpg'
        self.ezekiel = "Ezekiel 25:17"
        self.ezekiel_text = (
            "The path of the righteous man is beset on all sides by the "
            "iniquities of the selfish and the tyranny of evil men."
        )

    def _create_poet(self, fname='Jules', lname='Winnfield',
                     bio='Mayonnaise', url=None):
        if url is None:
            url = self.photo_url
        poet = Poet.objects.create(
            first_name=fname,
            last_name=lname,
            bio=bio,
            photo_url=url
        )
        return poet

    def _create_poem(self, poet):
        poem = Poem.objects.create(
            author=poet,
            title=self.ezekiel,
            text=self.ezekiel_text,
            year='1994'
        )
        return poem

    def test_index_view(self):
        poet = self._create_poet()

        response = self.unauth_client.get(
            reverse('index')
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('poets', response.context)
        self.assertEqual(len(response.context['poets']), 1)
        self.assertEqual(poet, response.context['poets'][0])

    def test_poet_view(self):
        poet = self._create_poet()
        self._create_poem(poet)
        poems = poet.poem_set.all()
        divide_at = poems.count() // 2

        response = self.unauth_client.get(
            reverse('poet', args=(poet.pk,)),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('poet', response.context)
        self.assertIn('poems', response.context)
        self.assertIn('divide_at', response.context)
        self.assertEqual(poet, response.context['poet'])
        self.assertEqual(poems.first(), response.context['poems'][0])
        self.assertEqual(divide_at, response.context['divide_at'])

    def test_poet_create_unauth_user_fails(self):
        response = self.unauth_client.post(
            reverse('add_poet'),
            data={
                'first_name': 'test',
                'last_name': 'test',
                'bio': 'test',
                'photo_url': 'https://test.com'
            }
        )
        login_url = reverse('login')
        add_poet_url = reverse('add_poet')
        self.assertRedirects(response, f"{login_url}?next={add_poet_url}")
        self.assertEqual(Poet.objects.count(), 0)

    def test_poet_create_auth_user_succeeds(self):
        response = self.auth_client.post(
            reverse('add_poet'),
            data={
                'first_name': 'test',
                'last_name': 'test',
                'bio': 'test',
                'photo_url': 'https://test.test/'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Poet.objects.count(), 1)
        poet = Poet.objects.first()
        self.assertEqual(poet.first_name, 'test')
        self.assertEqual(poet.last_name, 'test')
        self.assertEqual(poet.bio, 'test')
        self.assertEqual(poet.photo_url, 'https://test.test/')

    def test_poet_update_unauth_user_fails(self):
        poet = self._create_poet()
        update_poet_url = reverse('update_poet', args=(poet.pk,))
        response = self.unauth_client.post(
            update_poet_url,
            data={
                'first_name': 'test',
                'last_name': 'test',
                'bio': 'test',
                'photo_url': 'https://test.com'
            }
        )
        login_url = reverse('login')
        self.assertRedirects(response, f"{login_url}?next={update_poet_url}")
        self.assertNotEqual(poet.first_name, 'test')
        self.assertNotEqual(poet.last_name, 'test')
        self.assertNotEqual(poet.bio, 'test')
        self.assertNotEqual(poet.photo_url, 'test')

    def test_poet_update_auth_user_succeeds(self):
        poet = self._create_poet()
        self.auth_client.post(
            reverse('update_poet', args=(poet.pk,)),
            data={
                'first_name': 'test',
                'last_name': 'test',
                'bio': 'test',
                'photo_url': 'https://test.com'
            },
            follow=True
        )
        self.assertEqual(Poet.objects.count(), 1)
        upd_poet = Poet.objects.first()
        self.assertEqual(upd_poet.first_name, 'test')
        self.assertEqual(upd_poet.last_name, 'test')
        self.assertEqual(upd_poet.bio, 'test')
        self.assertEqual(upd_poet.photo_url, 'https://test.com')

    def test_poet_delete_unauth_user_fails(self):
        poet = self._create_poet()
        delete_poet_url = reverse('delete_poet', args=(poet.pk,))
        response = self.unauth_client.post(
            delete_poet_url
        )
        login_url = reverse('login')
        self.assertRedirects(response, f"{login_url}?next={delete_poet_url}")
        self.assertEqual(Poet.objects.count(), 1)
        self.assertEqual(Poet.objects.first(), poet)

    def test_poet_delete_auth_user_succeeds(self):
        poet = self._create_poet()
        delete_poet_url = reverse('delete_poet', args=(poet.pk,))
        response = self.auth_client.post(
            delete_poet_url,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Poet.objects.count(), 0)

    def test_poem_view(self):
        poet = self._create_poet()
        poem = self._create_poem(poet)
        response = self.unauth_client.get(
            reverse('poem', args=(poem.pk,)),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('poem', response.context)
        self.assertEqual(poem, response.context['poem'])

    def test_poem_create_unauth_user_fails(self):
        poet = self._create_poet()
        response = self.unauth_client.post(
            reverse('add_poem'),
            data={
                'author': poet,
                'title': 'test',
                'text': 'test',
                'year': '1990'
            }
        )
        login_url = reverse('login')
        add_poem_url = reverse('add_poem')
        self.assertRedirects(response, f"{login_url}?next={add_poem_url}")
        self.assertEqual(Poem.objects.count(), 0)

    def test_poem_create_auth_user_succeeds(self):
        poet = self._create_poet()
        response = self.auth_client.post(
            reverse('add_poem'),
            data={
                'author': poet.id,
                'title': 'test',
                'text': 'test',
                'year': '1990'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Poem.objects.count(), 1)
        poem = Poem.objects.first()
        self.assertEqual(poem.author, poet)
        self.assertEqual(poem.title, 'test')
        self.assertEqual(poem.text, 'test')
        self.assertEqual(poem.year, '1990')

    def test_poem_update_unauth_user_fails(self):
        poet = self._create_poet()
        poem = self._create_poem(poet)
        new_poet = self._create_poet(
            'new',
            'name',
            'test',
            'https://test.com/'
        )
        update_poem_url = reverse('update_poem', args=(poem.pk,))
        response = self.unauth_client.post(
            update_poem_url,
            data={
                'author': new_poet,
                'title': 'test',
                'text': 'test',
                'year': '1990'
            }
        )
        login_url = reverse('login')
        self.assertRedirects(response, f"{login_url}?next={update_poem_url}")
        self.assertNotEqual(poem.author, new_poet)
        self.assertNotEqual(poem.title, 'test')
        self.assertNotEqual(poem.text, 'test')
        self.assertNotEqual(poem.year, '1990')

    def test_poem_update_auth_user_succeeds(self):
        poet = self._create_poet()
        poem = self._create_poem(poet)
        new_poet = self._create_poet(
            'new',
            'name',
            'test',
            'https://test.com/'
        )
        self.auth_client.post(
            reverse('update_poem', args=(poem.pk,)),
            data={
                'author': new_poet.id,
                'title': 'test',
                'text': 'test',
                'year': '1990'
            },
            follow=True
        )
        self.assertEqual(Poem.objects.count(), 1)
        upd_poem = Poem.objects.first()
        self.assertEqual(upd_poem.author, new_poet)
        self.assertEqual(upd_poem.title, 'test')
        self.assertEqual(upd_poem.text, 'test')
        self.assertEqual(upd_poem.year, '1990')

    def test_poem_delete_unauth_user_fails(self):
        poet = self._create_poet()
        poem = self._create_poem(poet)
        delete_poem_url = reverse('delete_poem', args=(poem.pk,))
        response = self.unauth_client.post(
            delete_poem_url
        )
        login_url = reverse('login')
        self.assertRedirects(response, f"{login_url}?next={delete_poem_url}")
        self.assertEqual(Poem.objects.count(), 1)
        self.assertEqual(Poem.objects.first(), poem)

    def test_poem_delete_auth_user_succeeds(self):
        poet = self._create_poet()
        poem = self._create_poem(poet)
        delete_poem_url = reverse('delete_poem', args=(poem.pk,))
        response = self.auth_client.post(
            delete_poem_url,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, poet.get_absolute_url())
        self.assertEqual(Poem.objects.count(), 0)
