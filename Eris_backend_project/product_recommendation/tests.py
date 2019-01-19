# Create your tests here.
from http import HTTPStatus

from django.test import TestCase

from product_recommendation.models import Asdf
from rest_framework.response import Response


class Testasdf(TestCase):

    def test_asdf(self):
        asdf = Asdf.objects.create(aaa='필드 데이터1', bbb='필드 데이터2')

        response = self.client.get(
            path='/product-recommend/asdf/'
        )

        print(response.data)
        self.assertEqual(response.data[0]['aaa'], asdf.aaa)
        self.assertEqual(response.data[0]['bbb'], asdf.bbb)

    def test_POST_request(self):
        response = self.client.post(
            path='/product-recommend/asdf/',
            data={
                "aaa": "string",
                "bbb": "string"
            }
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(Asdf.objects.exists())
