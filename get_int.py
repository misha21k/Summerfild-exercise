def get_int(msg):
     while True:
          try:
               i = int(input(msg))
               return i
          except ValueError as err:
               print(err)

k = get_int('Введите целое число: ')
print(k)
