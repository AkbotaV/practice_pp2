import math

#Write a Python program to convert degree to radian.
a=int(input())
print(round(a*(math.pi/180),6))

#Write a Python program to calculate the area of a trapezoid.

h = float(input("\nHeight: "))
b1 = float(input("Base, first value: "))
b2 = float(input("Base, second value: "))
area_trap = (b1 + b2) * h / 2
print("Expected Output:", area_trap)

#Write a Python program to calculate the area of regular polygon.

n = int(input("\nInput number of sides: "))
s = float(input("Input the length of a side: "))
area_polygon = (n * s * s) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", int(area_polygon))



#Write a Python program to calculate the area of a parallelogram.
base = float(input("\nLength of base: "))
height = float(input("Height of parallelogram: "))
area_para = base * height
print("Expected Output:", float(area_para))