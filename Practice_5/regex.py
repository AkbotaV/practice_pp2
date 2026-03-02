import re
#1.
a=input()
x=re.search("ab*",a)
print(x)

#2.
a=input()
x=re.search("ab{2}|ab{3}",a)
print(x)

#3.
a=input()
x=re.findall("[a-z]+_[a-z]+",a)
print(x)

#4.
a=input()
x=re.findall("[A-Z][a-z]+",a)
print(x)

#5.
a=input()
x=re.search("^a.*b$",a)
print(x)

#6.
a=input()
x=re.sub(r"[,\.]",":",a)
print(x)

#7.
a=input()
x=re.split("_",a)
v=x[0]
for c in x[1:]:
  c=c.capitalize()
  v+=c
print(v)
#or
s = input()
def toup(m):
  return m.group(1).upper()
x=re.sub(r"_([a-z])",toup,s)
print(x)

#8.
s=input()
x=re.split(r"(?=[A-Z])",s)
print(x)

#9.
s=input()
x=re.sub(r"(?=[A-Z])"," ",s)
print(x)

#10.
s=input()
def tosn(m):
  return "_"+m.group().lower()
x=re.sub("[A-Z]",tosn,s)
print(x)
