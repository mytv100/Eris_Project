import random
import pickle

from ..models import Customer

f = open("customer.txt", 'w')
for i in range(100):
    customer = Customer()
    customer.gender = "man" if random.randint(0, 1) else "woman"
    customer.age = random.randrange(10, 80, 1)
    customer.nickname = "customer" + str(i)
    pickle.dump(customer, f)
f.close()

f = open("customer.txt", 'r')

while ():
    customer: Customer = pickle.load(f)
    if customer == None:
        break
    else:
        pass
        # api 로 customer data 전송
        # http://127.0.0.1:8000/api/doc/customer/customer_create

f.close()
