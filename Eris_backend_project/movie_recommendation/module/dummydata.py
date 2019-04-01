import random
import pickle


# import django
#
# django.setup()
# from movie_recommendation.models import Customer

class Customer:
    def __init__(self):
        self.gender = None
        self.age = None
        self.nickname = None

    def setdata(self, gender, age, nickname):
        self.gender = gender
        self.age = age
        self.nickname = nickname


f = open("customer.txt", 'wb')
for i in range(100):
    customer = Customer()
    gender = "man" if random.randint(0, 1) else "woman"
    age = random.randrange(10, 80, 1)
    nickname = "customer" + str(i)
    customer.setdata(gender, age, nickname)
    pickle.dump(customer, f)
f.close()

f = open("customer.txt", 'rb')
customer_list = []
while True:
    try:
        customer = pickle.load(f)
        customer_list.append(customer)
    except EOFError:
        break



# api 로 customer data 전송
# http://127.0.0.1:8000/api/doc/customer/customer_create

f.close()
