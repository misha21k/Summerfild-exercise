def sort(numbers):
     i = 0
     while i < len(numbers)-1:
          if numbers[i] > numbers[i+1]:
               lev = numbers[i]
               numbers[i] = numbers[i+1]
               numbers[i+1] = lev
               if i:
                    i += -1
          else:
               i += 1
     return numbers

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
     print('numbers: ',numbers)
     numbers = sort(numbers)
     i = 0
     while i <= (len(numbers)-1)/2-1:
          i += 1
     if i >= (len(numbers)-1)/2:
          med = numbers[i]
     else:
          med = (numbers[i]+numbers[i+1])/2
     print('count = ',len(numbers),' sum = ',summ,' minimum = ',Min,' maximum = ',Max,
           ' mean = ',summ/len(numbers),'mediana = ',med)
