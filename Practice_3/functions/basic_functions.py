#1
def MyFunction():
  print("Hello world!")
MyFunction()

#2 valid names
calculate_sum()
_private_function()
myFunction2()

#3 returns a value
def  greetings():
  return "Hello from a func"
message=greetings()
print(message)

#4 OR
def get_greeting():
  return "Hello from a function"

print(get_greeting())

#5 pass, func definition cannot be empty
def my_function():
  pass


