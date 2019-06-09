import csv
import urllib.request
import cx_Oracle
import sys
from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
if __name__ == '__main__':
  stock_list=[]
  outputfiles_list=[]
  with open('stock_list.txt','r') as x:
    stock_names=x.readlines()
    for each_line in stock_names:
        if len(each_line)!=1:
            stock_list.append(each_line[0:len(each_line)-1])
  print(stock_list)
  print(len(stock_list))
  urllib.request.urlopen("http://api.kibot.com/?action=login&user=guest&password=guest")
  con=cx_Oracle.connect('lokesh','lokeshit','localhost:1521/orcl')
  cur=con.cursor()
  for stock_number in stock_list:
      fileName = str(stock_number)+"_His.csv" 
      print(fileName)
      response=urllib.request.urlopen("http://api.kibot.com/?action=history&symbol="+stock_number+"&interval=daily&period="+sys.argv[1])
      html = response.read()
      print(html)
      dat=html.decode("utf-8")
      print(dat)
      lst=dat.split()
      x=open(fileName,'w')
      example=csv.writer(x)
      example.writerow(["Symbol","Date","Open","High","Low",
                        "Close","Volume"])
      for p in lst:
          line=stock_number+","+p
          lst=line.split(",")
          sy=lst[0]
          dt=lst[1]
          op=float(lst[2])
          hi=float(lst[3])
          lo=float(lst[4])
          cl=float(lst[5])
          vl=int(lst[6])
          query="insert into stock_hist values('"+sy+"','"+dt+"',"+str(op)+","+str(hi)+","+str(lo)+","+str(cl)+","+str(vl)+")"
          cur.execute(query)
          example.writerow(lst)
      x.close()
  cur.close()
  con.commit()
  master = Tk()
  variable = StringVar(master)
  variable.set(stock_list[0]) # default value
  w = OptionMenu(master, variable, *stock_list)
  w.pack()
  variable1 = StringVar(master)
  variable1.set(stock_list[0]) # default value
  w1 = OptionMenu(master, variable1, *stock_list)
  w1.pack()
  def compare():
    val1=variable.get()
    val2=variable1.get()
    fil1=val1+"_His.csv"
    fil2=val2+"_His.csv"
    print(fil1)
    print(fil2)
    df1 = pd.read_csv(fil1)
    df2=pd.read_csv(fil2)
    print(df1)
    print(df2)
    print(df1['Close'].max())
    print(df1['Close'].mean())
    print(df1['Close'].std())
    print(df2['Close'].max())
    print(df2['Close'].mean())
    print(df2['Close'].std())
    lst1=list(df1['Close'])
    lst2=list(df2['Close'])
    x=range(1,len(lst1)+1)
    plt.plot(x,lst1,label=val1)
    plt.plot(x,lst2,label=val2)
    plt.xlabel('days')
    plt.ylabel('close price')
    plt.legend()
    plt.show()
  button = Button(master, text="compare", command=compare)
  button.pack()
  mainloop()
  con.close()





