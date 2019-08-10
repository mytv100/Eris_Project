from functools import reduce

from django.db.models import Q

from ..models import NewCustomer, NewMovie, Ratings
from math import sqrt
import operator

"""     
    # content_based_filtering
    
    사용자나 아이템을 분석하여 비슷한 아이템 추천

    고객1 여성, 23세
    고객2 여성, 28세
    고객3 남성, 35세

    고객1과 고객2가 유사하다고 판단한다.
 
    # collaborative_filtering

    사용자들로부터 얻은 [기호정보(평점)]에 따라 사용자들의 관심사 예측
    사람 간의 유사도(Similarity)

    고객1과 고객2가 영화 A,B,C를 둘 다 좋아했다면,
    고객1이 영화 D를 좋아한다고 했을 때, 고객2도 영화 D를 좋아할 가능성이 높다. 
"""


def content_based_filtering(customer_pk, movie_pk, business_partner_pk):
    """
    1. 고객이 선택한 영화의 장르가 같은 영화 선택
    2. 그 중 평점이 높은 영화

    :param customer_pk: 추천을 받을 고객 PK
    :param movie_pk: 고객이 선택한 영화 PK
    :param business_partner_pk: 고객이 속한 업체 PK
    :return: 동일 장르 영화 추천 딕셔너리 리스트 [{"movie":movie_pk},]
    """
    # 현재 선택된 영화
    genre_list = NewMovie.objects.get(id=movie_pk).genre_set.all().values_list('name',flat=True)

    # 업체가 소유한 영화 목록 중에 고객이 선택한 영화와 장르가 같은 영화리스트 (평점 높은 순으로 20개)
    """
    movie_list = NewMovie.objects.filter(
        businessPartner__id=business_partner_pk, genre__contains=genre_list
    ).values("movie_pk", "genre", "rate").order_by("-rate")[:20]
    """

    movie_list = NewMovie.objects.filter(
        reduce(operator.or_, (Q(genre_set__name__contains=x) for x in genre_list)),
        businessPartner__id=2).values('id', 'genre_set__name', 'rate', 'votes').order_by('-rate')[:20]

    # 고객이 평가한(이미 관람한) 영화 목록
    movies = Ratings.objects.filter(customer_id=customer_pk, movie_id=movie_pk).values("movie_id")

    # 결과 리스트
    genre_movie_list = []

    # 조회된 영화들을 list에 넣는다
    for j in movie_list:

        # 고객이 현재 선택한 영화라면 건너뛰기
        if j["id"] == movie_pk:
            continue

        # 이미 관람한 영화라면 건너뛰기
        for m in movies:
            if j["id"] == m["movie_id"]:
                continue

        # 관람하지 않은 영화를 list 에 삽입
        genre_movie_list.append({"movie_id": j["id"]})

        # 5개 까지만
        if len(genre_movie_list) == 5:
            break

    # 영화 리스트 반환
    return genre_movie_list


def collaborative_filtering(customer_pk, movie_pk, business_partner_pk):
    """
    1. 고객이 평가한 영화들과 다른 고객이 평가한 영화들의 유사도를 평가하여
    2. 유사도가 높은 다른 고객이 평점을 남긴(고객은 남기지 않은) 영화 추천

    :param customer_pk: 추천을 받을 고객의 PK
    :param movie_pk: 고객이 선택한 영화의 PK
    :param business_partner_pk: 고객이 속한 업체 PK
    :return: 고객 유사도 영화 추천 딕셔너리 리스트 [{"movie":movie_pk},]
    """
    customer = NewCustomer.objects.get(id=customer_pk)
    age = customer.age // 10  # 10~19 -> 1 / 20~29 ->2
    gender = customer.gender

    # 고객이 관람한 영화
    movie_list_a = Ratings.objects.filter(customer_id=customer_pk, movie_id=movie_pk).values('movie_id', 'rate')
    # movie_list_a = CustomerMovie.objects.filter(customer=customer_pk).select_related('movie').values("movie", "rate")

    # 업체에 속한 고객들중 동일 나이대, 동일 성별
    customers = NewCustomer.objects.filter(businessPartner__id=business_partner_pk,
                                           gender=gender, age__lt=((age + 1) * 10),
                                           age__gte=(age * 10)).values("id", "age")
    """
        c = Customer.objects.filter(
                                            gender=gender, age__lt=((age + 1) * 10),
                                            age__gte=(age * 10))

        for customer in c:
            plt.scatter(customer.age, customer.gender)
            plt.annotate(customer.nickname[8:],
                         xy=(customer.age,customer.gender),
                         xytext=(5, -5),
                         textcoords='offset points')

        plt.title("VS")
        plt.xlabel("Age")
        plt.ylabel("gender")
        plt.show()
    """

    rate = {}  # 유사도 계산을 위한 평점 차이 저장 딕셔너리
    customer_dict = {}  # 유사도 저장 딕셔너리
    # for j in customers:
    # 유사도가 작을수록 유사하기 때문에
    # 같은 영화를 하나도 보지 않았다면 평점의 평균을 10으로해준다.
    average = 10
    movie_list_b = (Ratings.objects
                    .filter(customer__gender=gender,
                            customer__age__lt=((age + 1) * 10),
                            customer__age__gte=(age * 10))
                    .select_related('movie').values("movie_id", "rate"))

    # 다른 고객들의 영화리스트와 현재 고객의 영화리스트를 비교해서 둘다 평가한 영화가 있다면,
    # rate 딕셔너리에 평점의 차를 넣는다.
    for c in customers:
        for m in movie_list_a:
            for n in movie_list_b:
                if m["movie_id"] == n["movie_id"] and m["rate"] != 0 and n["rate"] != 0:
                    rate[m["movie_id"]] = m["rate"] - n["rate"]

        # 같은 영화가 하나라도 있다면 rate 딕셔너리의 평균을 구한다.
        if len(rate) != 0:
            average = sum(rate.values()) / len(rate)

        # 피타고라스 공식과 round 함수를 사용하여 소수 첫번째 자리까지 반올림해서
        # 유사도를 구한 뒤 딕셔너리에 넣음

        customer_dict[c['id']] = round(sqrt(pow((age * 10) - c['age'], 2) + pow(average, 2)), 1)

    # 결과 리스트
    customer_movie_list = []
    # 유사도 값이 작을수록 유사하다, 가장 유사도 값이 작은 4명의 고객이
    # 시청(평가)한 영화중 평점이 높은 2개 영화를 list 에 넣는다.
    # sorted(customer_dict.items(), key=operator.itemgetter(1), reverse=True)[:4]

    movies = (Ratings.objects
                  .filter(customer__in=sorted(customer_dict.items(), key=operator.itemgetter(1), reverse=True)[:4])
                  .values("movie_id")
                  .order_by("-rate")[:2])

    for m in movies:

        # 이미 봤거나
        for movie in movie_list_a:
            if movie["movie_id"] == m["movie_id"]:
                break

        # 현재 선택된 영화인 경우 건너뛰기
        if m["movie_id"] == movie_pk:
            continue

        customer_movie_list.append(m)

    return customer_movie_list


def movie_filtering(customer_pk, movie_pk, business_partner_pk):
    """
    :param customer_pk: 추천을 받을 고객의 PK
    :param movie_pk: 고객이 선택한 영화의 PK
    :param business_partner_pk: 고객이 속한 업체 PK
    :return: 영화 추천 딕셔너리 리스트 [{"movie":movie_pk},]
    """

    customer_pk = int(customer_pk)
    movie_pk = int(movie_pk)

    genre_movie_list = content_based_filtering(customer_pk, movie_pk, business_partner_pk)
    customer_movie_list = collaborative_filtering(customer_pk, movie_pk, business_partner_pk)

    # 두 리스트를 합쳐서 중복을 제거한다.
    movies = customer_movie_list + genre_movie_list
    movie_list = list({movie['movie_id']: movie for movie in movies}.values())
    return movie_list
