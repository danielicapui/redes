#!/usr/bin/env python3
import socket
import time
import threading
from protocolo import Protocolo
class Cliente:
    def __init__(self,host='127.0.0.1',port=50000,id=None):
        self.soquete=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host=host
        self.port=port
        self.token=False
        self.soquete.connect((self.host,self.port))
        self.id=id
    def ver_recursos(self):
        self.soquete.sendall(str.encode("1 -1"))
        data=self.soquete.recv(1024).decode("utf-8")
        s=data.split()
        print("mensagem recebida: cod:{} valor:{}".format(s[0],s[1]))
    def solicita_recursos(self):
        print(f'Cliente de id:{self.id} solicita_recursos')
        self.soquete.sendall(str.encode("3 -1"))
        data=self.soquete.recv(1024).decode().split()
        m=Protocolo.get(data[0],data[1])
        cod=int(m.cod)
        valor=int(m.valor)
        print("Cliente de id:{} mensagem recebida: cod:{} valor:{}".format(self.id,cod,valor))
        if cod==4 and valor!=-1:
            self.token=m.valor
            print(f' Cliente id:{self.id} recebu token:{self.token}\n')
            return self.token
        elif cod==6 and valor==-1:
            print(f'token não recebido.cod:{cod} valor:{valor}')
            print("Aguardando e tentando de novo.\n")
            time.sleep(2)
            return False
        else:
            print(f'Você já possuí um token. cod:{cod} valor:{valor}\n')
            return True
    def tentar_pegar_token(self):
        p=False
        while p==False:
            p=self.solicita_recursos()
            if p!=False:
                return p
    def devolve_recursos(self):
        if self.token==False:
            return False
        mensagem="5 "+str(self.token)
        self.soquete.sendall(str.encode(mensagem))
        data=self.soquete.recv(1024).decode()
        s=data.split()
        m=Protocolo.get(s[0],s[1])
        if int(m.cod)==5 and int(m.valor)!=-1:
            print(f'Cliente de id:{self.id} devolveu token de id:{m.valor}\n')
            self.token=False
            return True
        else:
            print(f'Cliente de id:{self.id} Nenhum token para devolver.\n')
            return False
def clientesPegam(tam,host,port):
    h=[]
    for id in range(tam):
        h.append(Cliente(host,port,id))
    return h
def start(clientes,tam):
    for i in range(tam):
        novo_thread = threading.Thread(target=manipula,args=(i,clientes))
        novo_thread.start()
    return clientes
def manipula(i,clientes):
    clientes[i].tentar_pegar_token()
    time.sleep(3)
    clientes[i].devolve_recursos()
    clientes[i].ver_recursos()
def main():
    tam=int(input("Número de clientes:"))
    port=int(input("Digite a porta do servidor:"))
    host=input("Digite o ip:")
    clientes=clientesPegam(tam,host,port)
    start(clientes,tam)
    return 0
if __name__=='__main__':
        main()