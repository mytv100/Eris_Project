# Create your tests here.
from http import HTTPStatus

from django.test import TestCase

from movie_recommendation.models import Movie


class TestMovie(TestCase):

    def test_movie(self):
        movie = Movie.objects.create(aaa='필드 데이터1', bbb='필드 데이터2')

        response = self.client.get(
            path='/movie-recommend/movie/'
        )

        print(response.data)
        self.assertEqual(response.data[0]['aaa'], movie.aaa)
        self.assertEqual(response.data[0]['bbb'], movie.bbb)

    def test_POST_request(self):
        response = self.client.post(
            path='/movie-recommend/movie/',
            data={
                "aaa": "string",
                "bbb": "string"
            }
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(Movie.objects.exists())
