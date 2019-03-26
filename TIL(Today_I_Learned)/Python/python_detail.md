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

