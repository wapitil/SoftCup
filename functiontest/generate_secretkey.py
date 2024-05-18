# 随机生成一个密钥
import random
import string
def generate_secretkey():
    
    key = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    print(key)
    return key

generate_secretkey()