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
    posfix = posFix(TESTE_10)
    res = thompson(posfix)
    print(res.edges)
    #import json
    #g = {
    #    "initial_state":"s0",
    #    "alphabet":list(set(res.nodes))
    #}
    #g['states'] = ['s%d' % i for i in range(len(res.nodes))]
    #g['accepting_states'] = ['s0', g['states'][-1]]
    #g['transitions'] = [["s"+str(k), res.nodes[k], "s"+str(v[0])] for k, v in enumerate(res.edges) if len(v) > 0]
    #print(g)
    #with open('graph.json', 'w') as json_file:  
    #    json.dump(g, json_file)
    #from PySimpleAutomata import DFA, automata_IO
#
    #dfa_example = automata_IO.dfa_json_importer('graph.json')

    #new_dfa = DFA.dfa_completion(dfa_example)
    #new_dfa=DFA.dfa_minimization(dfa_example)

    #automata_IO.dfa_to_dot(new_dfa, 'output', '.')
    #thompson(entrada,)

def S():
    global STATE
    STATE += 1
    return STATE

def thompson(exp):
    s = Stack()

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
                g.edges.append((g.edges[-2][1], S(), '&'))
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
                g.edges.append((g.edges[0][0], g.edges[-1][1], '&'))
            s.push(g)

    
    return s.pop()

def posFix(exp):
    print("PF - Input: ",exp)
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

    print("PF - Output: ",posfix)
    return posfix


if __name__ == '__main__':
    main()
