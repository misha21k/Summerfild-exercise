print('Введите целое число и нажмите Enter или просто нажмите Enter')
summ = 0;      #Сумма введённых чисел
i = 0;         #Количество введений
while True:
     s = input('Введите целое число: ')
     if s:
          try:
               znach = int(s)
          except ValueError:
               print('Вы ввели не целое число')
               continue
          summ += znach
          i += 1
     else:
          break
if i:
     print('Сумма введённых цифр: ',summ,'. Количество введённых цифр: ',i,'. Среднее арифметическое: ',summ/i)
input()
