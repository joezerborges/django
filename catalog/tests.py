from django.test import TestCase

from django.test import SimpleTestCase
from django.urls import reverse


class BookstorePagesTests(SimpleTestCase):
	def test_three_pages_load(self):
		for page_name in ('home', 'books', 'about'):
			with self.subTest(page=page_name):
				response = self.client.get(reverse(f'catalog:{page_name}'))
				self.assertEqual(response.status_code, 200)

	def test_catalog_shows_three_books(self):
		response = self.client.get(reverse('catalog:books'))

		self.assertContains(response, 'Torto Arado')
		self.assertContains(response, 'A Hora da Estrela')
		self.assertContains(response, 'O Pequeno Príncipe')
		self.assertEqual(len(response.context['books']), 3)
