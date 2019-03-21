TESTE_1 = "A"
TESTE_2 = "A.B"
TESTE_3 = "A|B"
TESTE_4 = "A*"
TESTE_5 = "A.A*"
TESTE_6 = "A.B*.(A+B)"

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
    posfix = posFix(TESTE_6)
    #thompson(entrada,)


def thompson(entrada):
    print("Implement here")


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
