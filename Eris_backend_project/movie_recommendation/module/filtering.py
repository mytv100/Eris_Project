from ..models import Customer, Movie, CustomerMovie
from math import sqrt
import operator

""" 
content_based_filtering
1. 고객과 가장 유사한 고객 (유사도 평가)
2. 그 고객이 평가한 영화 중 점수 높은 것 추천

collaborative_filtering
1. 고객이 평가한 영화들과 다른 고객이 평가한 영화들의 유사도를 평가하여
2. 유사도가 높은 다른 고객이 평점을 남긴(고객은 남기지 않은) 영화 추천
"""


def content_based_filtering(genre):
    """
    사용자나 아이템을 분석하여 비슷한 아이템 추천

    고객1 여성, 23세
    고객2 여성, 28세
    고객3 남성, 35세

    고객1과 고객2가 유사하다고 판단한다.

    영화 장르,
    """
    genre_movie_list = []

    # 동일한 장르의 영화들 중 평점(IMDB 기준)이 높은 10개의 영화를 조회
    movies = Movie.objects.filter(genre__contains=genre).order_by('-rate')[:10]

    # 조회된 영화들을 list에 넣는다
    for m in movies:
        genre_movie_list.append(m)

    return genre_movie_list


def collaborative_filtering(customer, customers):
    """
    사용자들로부터 얻은 [기호정보(평점)]에 따라 사용자들의 관심사 예측
    사람 간의 유사도(Similarity)

    고객1과 고객2가 영화 A,B,C를 둘 다 좋아했다면,
    고객1이 영화 D를 좋아한다고 했을 때, 고객2도 영화 D를 좋아할 가능성이 높다.

    """
    rate = {}
    customer_dict = {}
    customer_movie_list = []

    movie_list_a = CustomerMovie.objects.filter(customer=customer)

    for j in customers:
        movie_list_b = CustomerMovie.objects.filter(customer=j)

        for m in movie_list_a:
            for n in movie_list_b:
                if m.movie_id == n.movie_id:
                    rate[m.movie_id] = m.rate - n.rate

        average = sum(rate.values()) / len(rate)
        customer_dict[j] = round(sqrt(pow(customer.age - j.age, 2) + pow(average, 2)),1)

    # 조회된 고객들이 시청(평가)한 영화중 평점이 높은 2개 영화를 list에 넣는다.
    for c in sorted(customer_dict.items(), key=operator.itemgetter(1))[-4:]:
        customer_movies = CustomerMovie.objects.filter(customer=c[0]).order_by('-rate')[:2]
        for customer_movie in customer_movies:
            customer_movie_list.append(customer_movie.movie)

    return customer_movie_list


def movie_filtering(customer, movie):
    """
    :param customer: 추천을 받을 고객
    :param movie: 고객이 선택한 영화 (없어도 됨)
    :return: 영화 추천 리스트
    """
    age_div = customer.age / 10
    gender_div = customer.gender
    genre_div = movie.genre

    # 10대, 20대, 30대.... 10살 단위 + 성별이 동일한 고객들 조회
    customers = Customer.objects.filter(gender=gender_div, age__lt=((age_div + 1) * 10), age__gte=(age_div * 10))

    customer_movie_list = collaborative_filtering(customer, customers)

    # 동일한 장르의 영화들 중 평점(IMDB 기준)이 높은 10개의 영화를 조회
    genre_movie_list = content_based_filtering(genre_div)

    # 두 리스트를 합쳐서 중복을 제거한다.
    movie_list = list(set(customer_movie_list + genre_movie_list))
    return movie_list
