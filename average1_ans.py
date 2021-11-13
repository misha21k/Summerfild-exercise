numbers = []
summ = 0
Min = None
Max = None

while True:
     try:
          line = input('enter a number or Enter to finish: ')
          if not line:
               break
          numbers.append(int(line))
          summ += numbers[len(numbers)-1]
          if Min == None or Min > numbers[len(numbers)-1]:
               Min = numbers[len(numbers)-1]
          if Max == None or Max < numbers[len(numbers)-1]:
               Max = numbers[len(numbers)-1]
     except ValueError as err:
          print(err)
          continue

if numbers:
     print('count = ',len(numbers),' sum = ',summ,' minimum = ',Min,' maximum = ',Max,
           ' mean = ',summ/len(numbers))
