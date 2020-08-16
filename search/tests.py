from django.test import TestCase, Client
from django.urls import reverse

from poems.models import Poet, Poem


class TestSearch(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ezekiel_text = (
            "The path of the righteous man is beset on all sides by the "
            "iniquities of the selfish and the tyranny of evil men."
        )

        cls.poet = Poet.objects.create(
            first_name='Jules',
            last_name='Winnfield',
            bio='Mayonnaise',
            photo_url='https://wiki.tarantino.info/images/Jules.jpg'
        )

        cls.poem = Poem.objects.create(
            author=cls.poet,
            title="Ezekiel 25:17",
            text=cls.ezekiel_text,
            year='1994'
        )

    def setUp(self):
        self.client = Client()

    def _check_response(self, url, results, search, query):
        response = self.client.get(
            url
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('results', response.context)
        self.assertIn('search', response.context)
        self.assertIn('query', response.context)
        self.assertEquals(response.context['results'], results)
        self.assertEquals(response.context['search'], search)
        self.assertEquals(response.context['query'], query)

    def test_search_fbv(self):
        subtests = {
            'Empty search query': ([], False, None),
            'Valid poet search query': ([self.poet], True, 'Jul'),
            'Valid poem search query': ([self.poem], True, 'Ezek'),
            'Invalid search query': ([], True, 'Test'),
        }
        for sub_description in subtests:
            with self.subTest(sub_description):
                url = reverse('search')
                search_url = url
                result, search, query = subtests[sub_description]
                if query is not None:
                    search_url = f"{url}?q={query}"
                self._check_response(
                    search_url,
                    result,
                    search,
                    query
                )

    def test_search_view_cbv(self):
        subtests = {
            'Empty search query': ([], False, None),
            'Valid poet search query': ([self.poet], True, 'Jul'),
            'Valid poem search query': ([self.poem], True, 'Ezek'),
            'Invalid search query': ([], True, 'Test'),
        }
        for sub_description in subtests:
            with self.subTest(sub_description):
                url = reverse('search_view')
                search_url = url
                result, search, query = subtests[sub_description]
                if query is not None:
                    search_url = f"{url}?q={query}"
                self._check_response(
                    search_url,
                    result,
                    search,
                    query
                )

    def test_search_template_view_cbv(self):
        subtests = {
            'Empty search query': ([], False, None),
            'Valid poet search query': ([self.poet], True, 'Jul'),
            'Valid poem search query': ([self.poem], True, 'Ezek'),
            'Invalid search query': ([], True, 'Test'),
        }
        for sub_description in subtests:
            with self.subTest(sub_description):
                url = reverse('search_template')
                search_url = url
                result, search, query = subtests[sub_description]
                if query is not None:
                    search_url = f"{url}?q={query}"
                self._check_response(
                    search_url,
                    result,
                    search,
                    query
                )
