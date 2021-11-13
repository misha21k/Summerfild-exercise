import sys,xml.sax.saxutils

def main():
     rezul = process_options()
     if rezul != (None,None):
          print_start()
          count = 0
          while True:
               try:
                    line = input()
                    if count == 0:
                         color = 'lightgreen'
                    elif count % 2:
                         color = 'white'
                    else:
                         color = 'lightyellow'
                    print_line(line, color, rezul[0],rezul[1])
                    count += 1
               except EOFError:
                    break
          print_end()
     else:
          print('usage:\ncsv2html_ans.py [maxwidth=int] [format=str]',
                ' < infile.csv > outfile.html')

def process_options():
     rezul = [100,'.0f']
     i = 1
     try:
          if sys.argv[i].startswith('maxwidth='):
               rezul[0] = int(sys.argv[i].replace('maxwidth=',''))
               i += 1
          if sys.argv[i].startswith('format='):
               rezul[1] = sys.argv[i].replace('format=','')
               i += 1
          if sys.argv[i]:
               return (None,None)
     except IndexError:
          return (rezul[0],rezul[1])
     except ValueError:
          return (None,None)

def print_start():
     print("<table border='1'>")

def print_end():
     print("</table>")

def print_line(line, color, maxwidth,form):
     print("<tr bgcolor='{0}'>".format(color))
     fields = extract_fields(line)
     for field in fields:
          if not field:
               print('<td></td>')
          else:
               number = field.replace(',','')
               try:
                    x = float(number)
                    print("<td align='right'>{0:{1}}</td>".format(x,form))
               except ValueError:
                    field = field.title()
                    field = field.replace(' And ',' and ')
                    field = xml.sax.saxutils.escape(field)
                    if len(field) <= maxwidth:
                         print('<td>{0}</td>'.format(field))
                    else:
                         print('<td>{0:.{1}} ...</td>'.format(field,maxwidth))
     print('</tr>')

def extract_fields(line):
     fields = []
     field = ''
     quote = None
     for c in line:
          if c in "\"'":
               if quote is None: # начало строки в ковычках
                    quote = c
               elif quote == c: # конец строки в ковычках
                    quote = None
               else:
                    field += c # другая ковычка внутри строки в ковычках
               continue
          if quote is None and c == ',': # конец поля
               fields.append(field)
               field = ''
          else:
               field += c                  #добавить символ в поле
     if field:
          fields.append(field)  # добавить последнее поле в список
     return fields

main()
               
