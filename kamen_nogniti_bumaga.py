import random

form = ['камень','ножницы','бумага']
i = 1
chel_ar = []
com_ar = []
chel_sum = 0
com_sum = 0

while True:
     Name = input('Введите своё имя: ')
     if not Name:
          print('Вы не ввели своё имя')
          continue
     break

while i <= 3:
     j = 1
     print('Раунд',i)
     chel = input('{0}, введите "{1[0]}", "{1[1]}" или "{1[2]}": '.format(Name,form))
     if chel not in form:
          print('{0}, нужно ввести "{1[0]}", "{1[1]}" или "{1[2]}"'.format(Name,form))
          continue
     com = random.choice(form)
     print('{0}, компьютер показал "{1}"'.format(Name,com))
     
     while j <= 3:
          if form[j-2] == chel and form[j-1] == com:
               print('{0}, вы выиграли раунд'.format(Name))
               chel_ar += [1]
               com_ar += [0]
               chel_sum += 1
          elif form[j-2] == com and form[j-1] == chel:
               print('{0}, вы проиграли раунд'.format(Name))
               chel_ar += [0]
               com_ar += [1]
               com_sum += 1
          elif com == chel:
               print('Ничья в раунде')
               chel_ar += [1]
               com_ar += [1]
               chel_sum += 1
               com_sum += 1
          else:
               j += 1
               continue
          break

     i += 1

line = '{0:<10}{1:<10}  {2:<10}'
print(line.format('Раунд',Name,'Компьютер'))
i = 1
while i <= 3:
     print(line.format(i,chel_ar[i-1],com_ar[i-1]))
     i += 1
print(line.format('Сумма:',chel_sum,com_sum))

if chel_sum > com_sum:
     print('{0}, вы выиграли'.format(Name))
elif chel_sum < com_sum:
     print('{0}, вы проиграли'.format(Name))
else:
     print('Ничья')


          
          
          
