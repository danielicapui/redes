import sqlite3,sys,os
def start(name):
    name=name or input()
    global conn
    conn=sqlite3.connect(name+'.sqlite3')
    global cur
    cur=conn.cursor()
    return conn,cur
def buscaTabela(nome,p="*"):
    global cur,conn
    lista=[]
    cur.execute('select {} from {}'.format(p,nome))
    for row in cur:
        print(row)
        lista.append(row)
    conn.commit()
    print("-"*20)
    return lista
def handleP(tabela):
    a=[]
    tam=tabela.split(",")
    for i in range(len(tam)):
        a.append("?")
        if(i!=len(tam)-1):
            a.append(",")
    return "".join(a)
##aqui seria para caso não soubesse os nomes
def addTabela(nome,tabela):
    global conn,cur
    for item in tabela:
        print("Inserindo item:{}".format(item))
        cur.execute("insert into {} values {}".format(nome,item))
    for row in cur.execute("select * from {}".format(nome)):
        print(row)
    conn.commit()
def handle_args(args=None):
    args=args or input().split(",")
    return "".join(args)
def criarTabela(nome,args):
    global cur,conn
    cur.execute("drop table if exists {}".format(nome))
    cur.execute("create table {} ({})".format(nome,args))
    conn.commit()
def insertInto(nome,args,dados):
    global cur,conn
    p=handleP(args)
    s=f"insert into {nome} ({args}) values ({p})"
    cur.executemany(s,dados)
    conn.commit()

if '__name__'=='__main__':
    name=sys.args[1] or input()
    conn=sqlite3.connect(name+'.sqlite3')
    cur=conn.cursor()