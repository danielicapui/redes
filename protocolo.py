from collections import namedtuple
class Protocolo:
    def __init__(self):
        self.mensagem=namedtuple("mensagem",['cod','valor'])
    def mostrarCampos(self):
        cod=[1,2,3,4,4,5]
        valor=[-1,'x',-1,'x',-1,'x']
        significado=['Cliente solicita quantidade de recursos disponíveis','Servidor informa a quantidade X de recursos disponíveis','Cliente solicita Token','Servidor fornece Token X','Recurso não disponível','Cliente devolve Token X']
        print("-"*20+" Protocolo "+"-"*20)
        for i in range(0,5,1):
            print("cod:{}   valor:{}    significado:{}".format(cod[i],valor[i],significado[i]))
    def mensagem_consulta_tokens(self):
        return self.mensagem(1,-1)
    def mensagem_solicita_tokens(self):
        return self.mensagem(3,-1)
    def mensagem_devolve_tokens(self,n=1):
        return self.mensagem(5,n)
    @staticmethod
    def get(cod,valor):
        mensagem=namedtuple("mensagem",['cod','valor'])
        s=mensagem(str(cod),str(valor))
        return s