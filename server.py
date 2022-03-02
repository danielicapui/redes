#!/usr/bin/env python3
import socket
import threading
from protocolo import Protocolo
from utills import *
class Servidor:
    def __init__(self,host='localhost',port=50000,n=None,ip=None,estado=None):
        if not estado:
            self.tokens=[ True for _ in  range(n)]
            self.ip=[]
        else:
            self.tokens=estado
            self.ip=ip
        self.soquete=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.soquete.bind((host,port))
        self.fabrica_tokens=self.tokens
    def start(self):
        inicial_tokens=self.tokens
        inicial_ip=self.ip
        try:
            while True:
                self.soquete.listen()
                print("Esperando conexão com o cliente")
                conn,ender=self.soquete.accept()
                print("Conectando em:",ender)
                novo_thread = threading.Thread(target=self.manipula, args=(conn,ender))
                novo_thread.start()
        except KeyboardInterrupt:
            op=int(input("Digite 1 para retornar os tokens como o padrão da aplicação e 2 para ssalvar os dados"))
            if op==1:
                    self.apagar_historico()
            if(inicial_tokens!=self.tokens and inicial_ip!=self.ip and op==2):    
                insertInto("user","ip,porta,conexao",self.ip)
                insertInto("tokens","token_id,state",self.token)
                print("Salvando os dados")
                return True
            print("Desligando o servidor.")
            return False
    def adicionar_estado(self,token=None,index=None,ip=None):
        self.token=[token[i] for i in range(len(index))]
        self.ip=ip
    def manipula(self, conn, ender):
        while True:
            data=conn.recv(1024).decode('utf-8')
            print(conn,ender)
            if not data:
                print("Conexão fechando.")
                conn.close()
                break
            m=data.split()
            p=Protocolo.get(m[0],m[1])
            d=self.recebe_msg(p,conn,ender)     
            mensagem=d.cod+" "+d.valor
            conn.sendall(mensagem.encode())
            self.add_dado(d,conn,ender)
        return True
    def add_dado(self,d,conn,ender):
        t=None
        if (d.cod=='4' or d.cod=='5') and d.valor!='-1':
            t=[conn,ender,str(d.cod)+" "+str(d.valor)]
        else:
            return t
        self.ip.append(t)
        return  t        
    def consulta_tokens(self):
        t=0
        for i in self.tokens:
            if i==True:
                t=t+1
        return t
    def sem_tokens(self):
        for i in self.tokens:
            if i==True:
                return False
        return True
    def fornece_tokens(self):
        if self.sem_tokens()==False:
            for i in range(len(self.tokens)):
                if self.tokens[i]==True:
                    self.tokens[i]=False
                    print(self.tokens)
                    return i
        else:
            return -1
    #verifica se 
    def devolveu(self,conn,ender):
        if self.ip==[]:
            return False
        for i in range(len(self.ip)):
            t=self.ip[i][2].split()
            if self.ip[i][0]==conn and self.ip[i][1]==ender and t[0]=='5' and t[1]!='-1':
                self.ip.pop(i)
                print(self.ip)
                return True
        return False
    #verifica se pegou um token
    def pegou_token(self,conn,ender):
        for i in range(len(self.ip)):
            t=self.ip[i][2].split()
            if self.ip[i][0]==conn and self.ip[i][1]==ender and t[0]=='4' and t[1]!='-1':
                return True
        return False
    def apagar_historico(self):
        self.ip=[]
        self.tokens=self.fabrica_tokens
        tokens="token_id integer primary key unique, state boolean not null"
        usuario="ip varchar(16) primary key,porta varchar(6) not null"
        criarTabela("tokens",tokens)
        criarTabela("user",usuario)
        print("historico apagado no servidor")
    def recebe_tokens(self,n,conn,ender):
        self.tokens[n]=True
        print("token recebido:",n)
        self.devolveu(conn,ender)
        return n
    def recebe_msg(self,mensagem,conn,ender):
        cod=int(mensagem.cod)
        valor=int(mensagem.valor)
        if cod==1 and  valor==-1:
            numero=self.consulta_tokens()
            return Protocolo.get(2,numero)
        elif cod==3 and valor==-1:
            if not self.pegou_token(conn,ender):
                if self.sem_tokens():
                    return Protocolo.get(6,-1)
                numero=self.fornece_tokens()
                print("cliente de ip:{} e porta:{} pegou um token de index:{}".format(conn,ender,numero))
                return Protocolo.get(4,numero)
            else:
                print("cliente de ip:",ender," já pegou um token e não devolveu.")
                return Protocolo.get(4,-1)
        elif cod==5 and valor>=0:
            if self.pegou_token(conn,ender):
                numero=self.recebe_tokens(valor,conn,ender)
                print("cliente de ip:{} e porta:{} devolveu um token de index:{}".format(conn,ender,numero))
                return Protocolo.get(5,numero)
            else:
                print("Cliente não pegou nenhum token.")
                return Protocolo.get(5,-1)
#define o servidor
def configurar_servidor():
    host=input("Digite o host do servidor:")
    port=int(input("Digite a porta do servidor:"))
    n=int(input("Digite a quantidade de tokens:"))
    servidor=Servidor(host,port,n)
    return servidor
def main():
    servidor=None
    conexao,cur=start("estado")
    while True:
        op=int(input("Digite 1 para ouvir um servidor\nDigite 2 para configurar um servidor\nDigite 3 para criar servidor com estado:\nDigite 4 para carregar os dados do servidor e ouvir\nDigite 5 para limpar o histórico de conexões."))
        #terceiro passo primeira vez
        if op==1:
            if servidor!=None:
                servidor.start()
                break
            print("Servidor não inicializado")
        #primeiro passo na primeira vez e na outras
        elif op==2:
            servidor=configurar_servidor()
        #segundo passo na primeira vez
        elif op==3:
            tokens="token_id integer primary key,state boolean not null"
            usuario="ip varchar(16) primary key,porta varchar(6) not null,conexao varchar(4) not null"
            criarTabela("tokens",tokens)
            criarTabela("user",usuario)
            n=len(servidor.tokens)
            dados=[(i,True) for i in range(n)]
            print(dados)
            insertInto("tokens","token_id,state",dados)
        #segundo passo depois de criar o arquivo estado.sqlite3
        elif op==4:
            if servidor==None:
                print("Servidor não inicializado.")
            elif servidor!=None:
                i=buscaTabela("tokens","token_id")
                token=buscaTabela("tokens","state")
                ip=buscaTabela("user","ip,porta,conexao")
                print(i,token)
                servidor.adicionar_estado(token,i,ip)
                servidor.start()
                break
        #limpa as tabelas
        elif op==5:
            if servidor!=None:
                servidor.apagar_historico()
        else:
            print("Opção invalida")
if __name__=='__main__':
    main()
