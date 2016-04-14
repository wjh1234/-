第 0014 题： 纯文本文件 student.txt为学生信息, 里面的内容（包括花括号）如下所示：

{
    "1":["张三",150,120,100],
    "2":["李四",90,99,95],
    "3":["王五",60,66,68]
}
请将上述内容写到 student.xls 文件中，如下图所示：

student.xls


#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
dic={
    "1":["张三",150,120,100],
    "2":["李四",90,99,95],
    "3":["王五",60,66,68]
}

tt= [[k]+v for k,v in dic.items()]
tt= sorted(tt)
import xlsxwriter 
            
workbook=xlsxwriter.Workbook('demo2.xlsx')
worksheet=workbook.add_worksheet() 
format=workbook.add_format()
format.set_border(10)
worksheet.write_row('A1',tt[0],format)
worksheet.write_row('A2',tt[1],format)
worksheet.write_row('A3',tt[2],format) 
workbook.close()
