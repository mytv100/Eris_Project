---
## django-extensions

Graph models : Render a graphical overview of project or specified apps
---
* i wanted to exclude the default apps such as session, admin, etc in graph.
* so i tried to use 'exclude option', but it didn't work as i thought.
* so i used the 'include-model option' and it worked as i thought.

---
### proxy model: 상속받은 모델의 테이블을 그대로 사용함 

```python
class BusinessPartner(User):
    class Meta:
        proxy = True
```
=> User 테이블을 그대로 사용함.
---
### ManyToMany field
다대다 관계에 있는 모델 사이에 
새로운 field 를 추가해주고 싶을 때 사용한다.
```python
class Movie(models.Model):
    ...
    
class Actor(models.Model):
    # M2M fields 한 쪽에만 만들어주면 됨
    movie: Movie = models.ManyToManyField( 
        Movie,
        through='ActorMovie',
        through_fields=('actor', 'movie'),
    )


class ActorMovie(models.Model): 
    actor: Actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE
    )

    movie: Movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE
    ) 
```

M2M 관계에 있던 Movie 와 Actor 를
 
1대N (Actor 대 ActorMovie)

1대N (Movie 대 ActorMovie)

으로 나눠준다.

on_delete 속성을 models.CASCADE 로 지정해줘서
Actor 나 Movie 가 삭제되면 관련된 ActorMovie 도 삭제 된다

---
model의 field 나 함수의 parameter 뒤에 : class

ex)`request : Request`

변수의 타입을 지정해줌
-> 지정해주면 `request.` 했을때 자동완성에서
적절한 것 찾아서 보여줌

---

`Model.objects` return the manager instance
-> iterator로 사용 불가능
`Model.objects.all()` return get_query_set()

`Model.objects.filter()` == `Model.objects.all().filter()`
-> 같은 결과 반환 

---

