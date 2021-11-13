import random

chis = ['Его','Её','Их']
sush = ['мужчина','мальчик','дед','кот','Кощей Бессмертный',
        'волк','утюг']
nar  = ['громко','тихо','спокойно','ровно','плохо','хорошо','культурно',
        'правильно','сильно','слабо']
glag = ['пел','сидел','слышал','спал','храпел','валялся','питался',
        'убился']

while True:
     try:
          line = input('Введите кол-во строк от 1 до 10 или Enter для 5: ')
          if line:
               i = int(line)
               if not 0 < i < 11:
                    print('Вы ввели число не от 1 до 10, попробуйте ещё раз')
                    continue
          else:
               i = 5
          while i > 0:
               if random.randint(0,1):
                    print(random.choice(chis)+' '+random.choice(sush)+' '+
                    random.choice(nar)+' '+random.choice(glag))
               else:
                    print(random.choice(chis)+' '+random.choice(sush)+' '+
                    random.choice(glag))
               i += -1
     except ValueError:
          print('Вы какую-то фигню ввели, попробуйте ещё')
          continue
     break
