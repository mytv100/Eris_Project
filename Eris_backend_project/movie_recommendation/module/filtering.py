from ..models import Customer, Movie, CustomerMovie


def movie_filtering(customer, movie):
    """
    :param customer: 추천을 받을 고객
    :param movie: 고객이 선택한 영화 (없어도 됨)
    :return: 영화 추천 리스트
    """

    age_div = customer.age % 10
    gender_div = customer.gender
    genre_div = movie.genre

    customer_movie_list = []
    genre_movie_list = []

    # 10대, 20대, 30대.... 10살 단위 + 성별이 동일한 고객들 조회
    customers = Customer.objects.filter(gender=gender_div, age__gte=age_div * 10, age_lt=(age_div + 1) * 10)
    # 평점이 8.0 이상인 동일한 장르의 영화들 조회
    movies = Movie.objects.filter(genre=genre_div, rate__gte=8.0)

    # 조회된 고객들이 시청(평가)한 영화중 평점 8.0점 이상을 부여한 영화를 list에 넣는다.
    for c in customers:
        customer_movies = CustomerMovie.objects.filter(customer=c, rate__gte=8.0)
        for customer_movie in customer_movies:
            customer_movie_list.append(customer_movie)

    # 조회된 영화들을 list에 넣는다
    for m in movies:
        genre_movie_list.append(m.id)
    # 두 리스트를 합쳐서 중복을 제거한다.
    movie_list = list(set(customer_movie_list + genre_movie_list))
    return movie_list

