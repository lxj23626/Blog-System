from django.test import TestCase

# Create your tests here.
dic = {'abc':123, 'abcd':234,'bcd':345}

dic2={}
for k,v in dic.items():
    if 'a' in k:
        dic.pop(k)

print(dic)
print(dic2)