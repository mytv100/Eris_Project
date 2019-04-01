list comprehension (리스트 내포) & lambda & filter & map
```python
num_list = [ x for x in range(10)] 
# result = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

mapped_list = list(map(lambda x : x%2 == 0, num_list)) 
# result = [True, False, True, False, True, False, True, False, True, False]

filtered_list = list(filter(lambda x : x%2 == 0, num_list)) 
# result = [0, 2, 4, 6, 8]

mapped_list = list(map(lambda x : x*2, num_list))
# result = [0, 2, 4, 6, 8 ,10, 12, 14, 16, 18]

filtered_list = list(filter(lambda x : x*2, num_list))
# result = [1, 2, 3, 4, 5, 6, 7, 8, 9] => { 0*2 == 0 => False}

```

`lambda` 는 `def function()` 과 동일함

`map` 과 `filter` 둘 다 parameter로 function 과 iterable 객체를 입력받음.
`map`은 iterable 객체의 값들은 function 에 매핑시켜줌
`filter` 는 iterable 객체의 값들은 function 으로 필터링함 

-> function 이 lambda x: x * 2 이고, iterable 객체가 0을 가지고 있을 때,
 0 * 2 == 0 이므로 False 라서 필터링되서 출력안됨 

---
####가상 환경 virtualenv
가상 환경 생성 명령어 : virtualenv "envName"

-> 해당 디렉토리로 이동한 상태에서

가상 환경 활성화 명령어 : source bin/activate

가상 환경 종료 명령어 : deactive

가상 환경이 활성화된 상태에서 설치한 라이브러리와 실행한 스크립트는 해당 가상환경에만 영향을 미침

---
삼항연산자

```
for i in range(10):
    step = i if [True or False] else -1
```
if문 뒤에 True 가 나오면
if문 앞의 문장이 실행되고,
False가 나오면 else문으로 넘어가서
step = -1 이 된다.

---

plain python file(.py)에서 django 의 클래스를 import 하려고 하니까 
error가 발생함

-> Run/Debug Configurations 편집 창에서 환경 변수에
`DJANGO_SETTINGS_MODULE=configuration.settings` 를 추가 해줌

->.py 에 import django; django.setup() 넣어줌

=> django의 클래스를 사용하려면 장고가 setup을 해줘야 사용가능하다.

---
#### pickle
```
# pickle 로 데이터 파일에 저장
# data 는 클래스나 dictionary 같은 객체도 가능
# binary 형태로 저장하기 떄문에 "wb" 로 열어야함
f=open("text.txt","wb")
pickle.dump(data,f)
f.close()

# pickle 로 데이터 파일에서 읽어오기
f=open("text.txt","rb")
data = pickle.load(f)
f.close()
```

---
import 부분에 대하여
relative 알아보기

---