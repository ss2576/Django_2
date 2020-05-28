#from django.test import TestCase

# Create your tests here.


a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
k = 4

for i in range(0, len(a), k):
    print(a[i:i+k])

