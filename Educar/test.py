import string
import random


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))



user1 = id_generator()
user2 = id_generator()
print(user1, user2)
