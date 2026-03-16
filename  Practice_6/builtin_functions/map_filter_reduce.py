from functools import reduce

numbers=[1,2,4,5,7,8]

#1
square=list(map(lambda x:x**2,numbers))
print(square)
even_num=list(filter(lambda x:x%2==0,numbers))
print(even_num)

#2
res=reduce(lambda a,b:a+b,numbers)
print(res)
prod = reduce(lambda a, b: a * b, numbers)
print(prod)