
import sys

qas = {
  'what is an animal that barks?': 'dog',
  'What animal says meow?': 'cat',
  'What animal says quack?': 'duck',
  'What kind of animal swims?': 'fish'}

for q, a in qas.items():
  print(q)
  guess = input(q)
  print(guess)


