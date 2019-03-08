## 진행상황 및 계획
영화 추천 서비스 API(Eris)

영화 사이트(업체)에서 고객 data와 보유중인 영화 list data를 Eris에 제공

Eris는 업체명_고객ID(nickname) 형식으로 database에 고객 data 저장

(보유중인 영화 리스트는 어떻게 처리하지?)

imdb에서 movie data를 가져와서 database에 저장,

업체에서 영화의 전체 평점(기존 imdb에서 가져온 평점 + 추가된 평점)을 기준으로 
원할 때는 그대로 반환해줌

그 외에 각 고객에게 맞는 영화 리스트를 원할 때는 filtering 과정을 통하여
리스트를 반환해줌 

#
**To-do list**
1. connect database : mysql or postgresql 
2. create models : customer data & movie data & 두 모델 사이의 관계
3. develop crawler for movie data : imdb
4. make customer dummy(?) data  
5. make url in api form
6. develop filtering algorithm : colaborative or content-based
7. make documents