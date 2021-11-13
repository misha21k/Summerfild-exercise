import random

chis = ['Его','Её','Их']
sush = ['мужчина','мальчик','дед','кот','Кощей Бессмертный',
        'волк','утюг']
nar  = ['громко','тихо','спокойно','ровно','плохо','хорошо','культурно',
        'правильно','сильно','слабо']
glag = ['пел','сидел','слышал','спал','храпел','валялся','питался',
        'убился']
i = 0

while i < 5:
     if random.randint(0,1):
          print(random.choice(chis)+' '+random.choice(sush)+' '+
          random.choice(nar)+' '+random.choice(glag))
     else:
          print(random.choice(chis)+' '+random.choice(sush)+' '+
          random.choice(glag))
     i += 1
     
