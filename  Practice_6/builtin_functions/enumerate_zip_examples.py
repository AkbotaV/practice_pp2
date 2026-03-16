#1
#enumerate-index
fruits=["apple","banana","cherry"]
for i,fruit in enumerate(fruits):
    print(i,fruit)

#2
#zip-pares
name=["Ali","Dana","Aruzhan"]
score=[85,90,78]
for n,s in zip(names, scores):
    print(n,s)

list1=[1,2,3]
list2=["a","b","c"]
for n,l in zip(list1, list2):
    print(n,l)

#type conv
a = "10"
b = 5
c = 3.5

print(int(a))
print(float(b))
print(str(c))