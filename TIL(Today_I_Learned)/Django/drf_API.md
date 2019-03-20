---
#### 실행 순서
 1. API로 request가 들어옴 (http://ip:port/appName/modelName 형식으로)
 2. Project의 urls.py -> App의 urls.py -> Router -> views.py ->ViewSet
 3. ViewSet에서 Serializer 호출해서 형태를 만들어줌
 4. response 를 반환해줌
---
#### Serializer
 * 보여주는 형식을 정의함, 틀
---
#### ViewSet
 * http method 를 drf ViewSet method 로 변형을 해줌
 ~~~
   get -> list or [ retrieve(read) : detail ]
   post -> create
   put -> update
   patch -> partial_update
   del -> delete
 ~~~
 
 
---
