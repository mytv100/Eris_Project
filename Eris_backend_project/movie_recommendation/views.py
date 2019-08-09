from rest_framework.response import Response

from movie_recommendation.models import NewCustomer, NewMovie, Genre, Ratings, BusinessPartner
from django.utils import timezone
from django.db.models import Sum, Count


def initData(request):
    businesspartner = BusinessPartner.objects.get(username='user1')

    # 장르 데이터
    f = open('movie_recommendation/module/data/ml-100k/u.genre', 'rb')
    genre_list = []
    for line in f.readlines():
        string = line.decode('ISO-8859-1')
        string_list = string.split('|')
        Genre.objects.create(name=string_list[0])
        genre_list.append(string_list[0])
        if string_list[0] == 'Western':
            break
    f.close()

    # 영화 데이터
    f = open('movie_recommendation/module/data/ml-100k/u.item', 'rb')

    for line in f.readlines():
        string = line.decode('ISO-8859-1')
        string_list = string.split('|')
        released_date = timezone.datetime.strptime(string_list[2], '%d-%b-%Y')  # .strftime('%Y-%m-%d')
        movie = NewMovie.objects.create(id=string_list[0], title=string_list[1], released_date=released_date)
        movie.businessPartner.add(businesspartner)

        for i in range(5, 24):
            if string_list[5]:
                genre = Genre.objects.get(name=genre_list[i - 5])
                movie.genre_set.add(genre)
    f.close()

    # 고객 데이터
    f = open('movie_recommendation/module/data/ml-100k/u.user', 'rb')

    for line in f.readlines():
        string = line.decode('ISO-8859-1')
        string_list = string.split('|')
        customer = NewCustomer.objects.create(id=string_list[0], age=string_list[1], gender=string_list[2],
                                              occupation=string_list[3])
        customer.businessPartner.add(businesspartner)
    f.close()

    # 평점 데이터
    f = open('movie_recommendation/module/data/ml-100k/u.data', 'rb')

    for line in f.readlines():
        string = line.decode('ISO-8859-1')
        string_list = string.split("\t")
        Ratings.objects.create(customer_id=string_list[0], movie_id=string_list[1], rate=string_list[2])

    f.close()

    # 영화 데이터에 평점, 투표 수 추가
    query_set = Ratings.objects.values('rate', 'movie__id')
    qs_annotate = query_set.values('movie__id').annotate(count=Count('movie__id'), sum=Sum('rate'))
    for q in qs_annotate:
        NewMovie.objects.filter(id=q['movie__id']).update(votes=q['count'], rate=round(q['sum'] / q['count'],1))

    return Response(None)
