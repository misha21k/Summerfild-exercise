import random

i = 1
summ_chel = 0
summ_com = 0
line = '{0:<10}{1:<10}{2:<10}'

while True:
     try:
          col = int(input('Введите количество бросков: '))
          break
     except ValueError:
          print('Кол-во бросков должно быть целым числом')
          continue

print('Нажимайте Enter, чтобы сделать бросок')
input(line.format('№ броска','вы','компьютер'))
while i <= col:
     chel = random.randint(1,6)
     com = random.randint(1,6)
     summ_chel += chel
     summ_com += com
     input(line.format(i,chel,com))
     i += 1
input(line.format('Сумма:',summ_chel,summ_com))
if summ_chel > summ_com:
     print('Вы выиграли')
elif summ_chel == summ_com:
     print('Ничья')
else:
     print('Вы проиграли')
          
