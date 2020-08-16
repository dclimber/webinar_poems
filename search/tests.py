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

        self.urls_to_test = (
            (reverse('search'), 'Search Function-based View'),
            (reverse('search_view'), 'SearchView Class-based View'),
            (reverse('search_template'), 'SearchTemplateView Class-based View')
        )

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

    def test_search_empty_query(self):
        for url, sub_description in self.urls_to_test:
            with self.subTest(sub_description):
                self._check_response(
                    url,
                    [],
                    False,
                    None
                )

    def test_search_valid_query_poet(self):
        for url, sub_description in self.urls_to_test:
            with self.subTest(sub_description):
                query = 'Jul'
                search_url = f"{url}?q={query}"
                self._check_response(
                    search_url,
                    [self.poet],
                    True,
                    query
                )

    def test_search_valid_query_poem(self):
        for url, sub_description in self.urls_to_test:
            with self.subTest(sub_description):
                query = 'Ezek'
                search_url = f"{url}?q={query}"
                self._check_response(
                    search_url,
                    [self.poem],
                    True,
                    query
                )

    def test_search_invalid_query(self):
        for url, sub_description in self.urls_to_test:
            with self.subTest(sub_description):
                query = 'Test'
                search_url = f"{url}?q={query}"
                self._check_response(
                    search_url,
                    [],
                    True,
                    query
                )
