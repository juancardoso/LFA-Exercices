####150949 JUAN CARDOSO
####150329 Emanuel Huber


import matplotlib.pyplot as plt
import networkx as nx    
import re
import numpy as np

TESTE_1 = "A"
TESTE_2 = "A.B"
TESTE_3 = "A|B"
TESTE_4 = "A*"
TESTE_5 = "A.A*"
TESTE_6 = "A.B*.(A+B)"
TESTE_7 = "A.B.C"
TESTE_8 = "A|B|C"
TESTE_9 = "A*.B*"
TESTE_10 = "A+"
E = "&"
STATE = 0

#"A.B"
#E-A-E-B-E
class Stack(object):
    def __init__(self):
        self.__stack = []
 
    def push(self, elemento):
        self.__stack.append(elemento)
 
    def pop(self):
        if not self.empty():
            return self.__stack.pop(-1)
 
    def empty(self):
        return len(self.__stack) == 0

    def top(self):
        if not self.empty():
            return self.__stack[-1]
        
class Graph:

    def __init__(self):
        self.edges = []

    def __str__(self):
        return ', '.join(self.nodes)


prioridade = {
    '(': 1,
    ')': 1,
    '[': 1,
    ']': 1,
    '{': 1,
    '}': 1,
    '+': 3,
    '.': 2,
    '*': 3,
    '|': 2,
}



def main():
    print("***O numero do nó inicial e final será mostrado no console***\n")
    print("Digite o regex Ex: A.B*.(A+B)")
    V = input().upper()

    posfix = posFix(V)
    res = thompson(posfix)
    g = nx.DiGraph()
    edges = [(e[0], e[1]) for e in res.edges]
    
    g.add_edges_from(edges)
    pos = nx.layout.spring_layout(g)
    labels = {}
    
    for e in res.edges:
        labels[(e[0], e[1])] = e[2]
    plt.figure(figsize=(20, 20))
    nx.draw(g, pos, with_labels=True, edge_color='black', width=2,
            linewidths=1, node_size=250, node_color='green', alpha=0.9,)

    # print(res.edges)
    inicio = res.edges[0][0]
    fim = res.edges[-1][1]

    print("Nó Inicial: "+ str(inicio)+"\n","Nó Final: "+str(fim)+"\n")
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

    # plt.savefig("./teste.png")  # save as png
    # plt.show()  # display

    ##MOCK
    V = "AB"
    inicio = 1
    fim = 6
    res.edges = [(1,2,"A"),(1,2,E),(2,3,E),(3,4,"B"),(3,4,E),(4,5,E),(5,6,"B"),(4,1,E)]
    ##MOCK
    print("Edges: ",res.edges,"\n")
    afn_afd(res.edges, inicio, fim,V)
    

def S():
    global STATE
    STATE += 1
    return STATE

#Calcula AFN
def thompson(exp):
    s = Stack()

    if len(exp) == 1:
        g = Graph()
        g.edges.append((S(), S(), 'A'))
        return g

    for e in exp:
        if e.isalpha():
            s.push(e)
        elif e == '.':
            op1 = s.pop()
            op2 = s.pop()
            g = Graph()
            if isinstance(op2, Graph):
                g.edges.append((S(), op2.edges[0][0], '&'))
                g.edges += op2.edges
                if isinstance(op1, Graph):
                    g.edges.append((g.edges[-1][1], op1.edges[0][0], '&'))
                    g.edges += op1.edges
                    g.edges.append((g.edges[-1][1], S(), '&'))
                else:
                    g.edges.append((g.edges[-1][1], S(), '&'))
                    g.edges.append((g.edges[-1][1], S(), op1))
                    g.edges.append((g.edges[-1][1], S(), '&'))
            else:
                g.edges.append((S(), S(), '&'))
                g.edges.append((g.edges[-1][1], S(), op2))
                if isinstance(op1, Graph):
                    g.edges.append((g.edges[-1][1], op1.edges[0][0], '&'))
                    g.edges += op1.edges
                    g.edges.append((g.edges[-1][1], S(), '&'))
                else:
                    g.edges.append((g.edges[-1][1], S(), '&'))
                    g.edges.append((g.edges[-1][1], S(), op1))
                    g.edges.append((g.edges[-1][1], S(), '&'))
            s.push(g)
        elif e == '|':
            op1 = s.pop()
            op2 = s.pop()
            g = Graph()
            finalState = S()
            finalOp1 = 1
            finalOp2 = 1
            if isinstance(op2, Graph):
                g.edges.append((S(), op2.edges[0][0], '&'))
                g.edges += op2.edges
                finalOp2 = op2.edges[-1][1]
            else:
                g.edges.append((S(), S(), '&'))
                g.edges.append((g.edges[-1][1], S(), op2))
                finalOp2 = g.edges[-1][1]
            if isinstance(op1, Graph):
                g.edges.append((g.edges[0][0], op1.edges[0][0], '&'))
                g.edges += op1.edges
                finalOp1 = op1.edges[-1][1]
            else:
                g.edges.append((g.edges[0][0], S(), '&'))
                g.edges.append((g.edges[-1][1], S(), op1))
                finalOp1 = g.edges[-1][1]
            #Add final states
            g.edges.append((finalOp2, finalState, '&'))
            g.edges.append((finalOp1, finalState, '&'))
            s.push(g)
        elif e == '*':
            op = s.pop()
            g = Graph()
            if isinstance(op, Graph):
                g.edges.append((S(), op.edges[0][0], '&'))
                g.edges += op.edges
                g.edges.append((g.edges[-1][1], op.edges[1][0], '&'))
                g.edges.append((g.edges[0][0], S(), '&'))
                g.edges.append((g.edges[-2][2], g.edges[-1][1], '&'))
            else:
                g.edges.append((S(), S(), '&'))
                g.edges.append((g.edges[-1][1], S(), op))
                g.edges.append((g.edges[-1][1], g.edges[-1][0], '&'))
                g.edges.append((g.edges[-1][0], S(), '&'))
                g.edges.append((g.edges[0][0], g.edges[-1][1], '&'))

            s.push(g)
        elif e == '+':
            op = s.pop()
            g = Graph()
            if isinstance(op, Graph):
                # AND
                g.edges.append((S(), op.edges[0][0], '&'))
                g.edges += op.edges
                g.edges.append((g.edges[-1][1], S(), '&'))
                # *
                g.edges.append((g.edges[-1][1], op.edges[0][0], '&'))
                g.edges += op.edges
                g.edges.append((g.edges[-1][1], op.edges[1][0], '&'))
                g.edges.append((g.edges[0][0], S(), '&'))
                g.edges.append((g.edges[-2][2], g.edges[-1][1], '&'))

            else:
                # AND
                g.edges.append((S(), S(), '&'))
                g.edges.append((g.edges[-1][1], S(), op))
                g.edges.append((g.edges[-1][1], S(), '&'))
                # *
                g.edges.append((g.edges[-1][1], S(), op))
                g.edges.append((g.edges[-1][1], g.edges[-1][0], '&'))
                g.edges.append((g.edges[-2][1], S(), '&'))
                g.edges.append((g.edges[2][0], g.edges[-1][1], '&'))
            s.push(g)

    
    return s.pop()

#Calcula no closure
def calcClosure(edges):
    closure = []
    interation = True;

    while interation == True:
        interation = False
        for i in range(len(edges)):
            nfrom = edges[i][0]
            nto = edges[i][1]
            weight = edges[i][2]
            if len(closure) == 0 and i == 0:
                closure.append(nfrom)
                if weight == E:
                    closure.append(nto)
            else:
                if weight == E and nfrom in closure:
                    if not nto in closure:
                        interation = True
                        closure.append(nto)
    return closure


#Retorna o alfabeto do regex passado inicialmente
def getAlfabeto(alfabeto):
    return list(dict.fromkeys(re.findall("[A-Z]", alfabeto)))

#Retorna todos os estados do qual o no e o peso passado conseguem alcancar
def getAllStatesNode(idNumber,weight,edges):
    dfaedge = getStatsFromNode(idNumber,weight,edges)
    lenDfaedge = 0
    
    while len(dfaedge) != lenDfaedge:
        lenDfaedge = len(dfaedge)
        for e in dfaedge:
            addNodes = getStatsFromNode(e,weight,edges)
            if len(addNodes) > 0:
                for i in addNodes:
                    if not i in dfaedge:
                        dfaedge.append(i)
    
    return dfaedge

#Retorna o estados do qual um no pode chegar pelo peso
def getStatsFromNode(idNumber,weight,edges,vazio = True):
    #Pega todos os edges que o no do idNumber chega
    dfaedge = []
    for e in edges:
        if e[0] == idNumber:
            if e[2] == weight or (vazio and e[2] == E):
                if not e[1] in dfaedge:
                    dfaedge.append(e[1])
    
    return dfaedge

# def addcreateTableAlfabet(ed,alfabeto):
#     for x in alfabeto:
#        ed[x] = {}

#SE NO NAO ESTIVER NO ARR PASSADO ELE IRA ADICIONAR
def addSeNaoRepetir(arr,addNodes):
    for node in addNodes:
        if not node in arr:
            arr.append(node) 

##ADICIONA A LISTA DE CLOSURES UM NOVO CLOSURE, 
# VERIFICANDO SE O MESMO JA NAO EXISTE PARA NAO ADICIONAR 2X
def addSeNaoRepetirClosure(closures,addNodes,closuresNotAlreadyPass, DEBUG = False):
    nExist = True
    for clos in closures:
        if len(closures[clos]['C']) == len(addNodes):
            npA = np.asarray(closures[clos]['C'])
            npB = np.asarray(addNodes)

            if len(npA) > 1:
                npA.sort()
            
            if len(npB) > 1:
                npB.sort()

            if np.array_equal(npA,npB): 
                nExist = False

    if nExist:
        name = "S"+str(len(closures))
        closures[name] = {"C":addNodes}
        closuresNotAlreadyPass.append(name)

#ADICIONA AS TUPLAS PARA TODAS AS LETRAS DO ALFABETO PARA O DETERMINADO CLOSURE PASSADO
def addTabelaEstados(estados,alfabeto,nomeClosure):
    tupla = {}
    for x in alfabeto:
         tupla[x] = ""
    estados[nomeClosure] = tupla

#ACHA QUAL E A TAG DO CLOSURE DO CONJUNTO EX: S3
def findClosure(closures,conjunto):
    npB = np.asarray(conjunto)

    if len(npB) > 0:
        npB.sort()

    for cl in closures:
        npA = np.asarray(closures[cl]["C"])
        if len(npA) > 0:
            npA.sort()
        if np.array_equal(npA,npB):
            return cl

#Transforma o AFN em AFD
def afn_afd(edges, initialNode, finalNode, input):
    alfabeto = getAlfabeto(input)
    closuresNotAlreadyPass = ["S0"]
    closures = {}
    conjunto = {}
    estados = {}
        
    while len(closuresNotAlreadyPass) > 0:
        closureName = closuresNotAlreadyPass[0]
        del closuresNotAlreadyPass[0]
         
        if(closureName == "S0"):
            closures[closureName] = {"C":[initialNode]}
            #NO CLOSURE INICIAL NAO POSSO TER UM NO LEVANDO PRA ESSE ESTADO (ESTADO INICIAL)
            closures[closureName]["U"] = [f for f in getAllStatesNode(edges[0][0],E,edges) if f != initialNode]
        
        #BUSCA OS CONJUNTOS COM AS LETRAS DO ALFABETO
        for letra in alfabeto:
            for nodeValue in closures[closureName]["C"]:
                if conjunto.get(letra) == None or len(conjunto[letra]) == 0:
                    conjunto[letra] = getStatsFromNode(nodeValue,letra,edges,False) 
                else:
                    conjunto[letra].append(getStatsFromNode(nodeValue,letra,edges,False))

        # estados = {"S0":{"A":"SX","B":"SX"}}
        addTabelaEstados(estados,alfabeto,closureName)
        
        # print("Uniao: ",closures[closureName]['U'])
                
        #ADICIONA A UNIAO AO CONJUNTO
        # if closureName == "S0":
        for letra in alfabeto:
            for node in closures[closureName]['U']:
                aux = getStatsFromNode(node,letra,edges,False) 
                if len(aux) > 0:
                    addSeNaoRepetir(conjunto[letra],aux)

                  
        #ADICIONA O CONJUNTO AO CLOSURE SE O MESMO JA NAO ESTIVER LA
        for e in conjunto:
            addSeNaoRepetirClosure(closures,conjunto[e],closuresNotAlreadyPass)

        #LINKA A TRANSICAO DE ESTADOS COM O CLOSURE
        for conj in conjunto:
            closureFound = findClosure(closures,conjunto[conj]) 
            estados[closureName][conj] = closureFound

        #ADICIONA A UNIAO DOS CLOSURES FALTANTES
        for cl in closures:
            if closures[cl].get("U") == None:
                for union in closures[cl]["C"]:
                    aux = getAllStatesNode(union,E,edges)
                    if len(aux) > 0:
                        if closures[cl].get("U") == None:
                            closures[cl]["U"] = aux
                        else:
                            closures[cl]["U"].append(aux)

        conjunto = {}

    print("Estados: ", estados)
    print("Closure",closures)

#Calcula a expressao para posfixa
def posFix(exp):
    # print("PF - Input: ",exp)
    stack = Stack()
    posfix = ""

    for x in exp:
        if(x >= 'A' and x <= 'Z'):
            posfix += x
        elif(x == '(' or x == '[' or x == '{'):
            stack.push(x)
        elif(x == ')' or x == ']' or x == '}'):
            posfix+=stack.pop()
            while prioridade[x] !=  prioridade[stack.top()]:
                posfix+=stack.pop()
            
            stack.pop()
        elif(x == '.' or x == '+' or x == '|' or x == '*'):
            while stack.top() != None and prioridade[x] <=  prioridade[stack.top()]:
                posfix+=stack.pop()

            stack.push(x)

    while stack.empty() != True:
        posfix+=stack.pop()

    # print("PF - Output: ",posfix)
    return posfix


if __name__ == '__main__':
    main()


#https://www.youtube.com/watch?v=Efbtw2SjqRg
#FIZ COM BASE NESSE VIDEO