import sys

Zero  = [' *** ','*   *','*   *','*   *','*   *','*   *',' *** ']
One   = ['  *  ',' **  ','* *  ','  *  ','  *  ','  *  ','*****']
Two   = [' *** ','*   *','*   *','   * ','  *  ',' *   ','*****']
Three = [' *** ','*   *','    *',' *** ','    *','*   *',' *** ']
Four  = ['   * ','  ** ',' * * ','*  * ','*****','   * ','   * ']
Five  = ['*****','*    ','*    ','**** ','    *','*   *',' *** ']
Six   = [' *** ','*   *','*    ','**** ','*   *','*   *',' *** ']
Seven = ['*****','    *','   * ','  *  ',' *   ','*    ','*    ']
Eight = [' *** ','*   *','*   *',' *** ','*   *','*   *',' *** ']
Nine  = [' *** ','*   *','*   *',' ****','    *','*   *',' *** ']

Digits = [Zero,One,Two,Three,Four,Five,Six,Seven,Eight,Nine]

try:
     digits = input('Введите целое число: ')
     #digits = sys.argv[1]
     row = 0
     while row < 7:
          line = ''
          column = 0
          while column < len(digits):
               number = int(digits[column])
               digit = Digits[number]
               for i in digit[row]:
                    if i == '*':
                         line += str(number)
                    else:
                         line += i
               line += '  '
               column += 1
          print(line)
          row += 1
#except IndexError:
     #print('usage: bigdigits.py <number>')
except ValueError as err:
     print(err,'in',digits)
input()
               
