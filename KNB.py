import random

print('name_1 ','name_2 ','name_3 ')
y = ['камень','ножницы','бумага']
summ = [0,0,0]
for i in range(0,100):
     par = [0,0,0]
     x = [random.choice(y),random.choice(y),random.choice(y)]
     for j in range(0,3):
          for k in range(0,3):
               if (y[j] == x[k])*(y[j-1] not in x):
                    summ[k] += 1
                    par[k] = 1
     print(par)
print(summ)
                    
                    
     
