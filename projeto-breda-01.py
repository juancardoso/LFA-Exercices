##150949 - Juan Cardoso
##150329 - Emanuel Huber 


# G = (V, T, P, S)
# V = VARIAVEIS
# T = ALFABETO
# P = REGRAS DE PRODUCAO
# S = VARIAVEL INICIAL
DEBUG = False


#S-XY X-XaA X-XbB X-F Aa-aA Ab-bA AY-Ya Ba-aB Bb-bB BY-Yb Fa-aF Fb-bF FY-404 aA-F

V = ["S","X","Y","A","B","F"]
T = ["a","b"]
P = [("S","XY"),
     ("X","XaA"),
     ("X","XbB"),
     ("X","F"),
     ("Aa","aA"),
     ("Ab","bA"),
     ("AY","Ya"),
     ("Ba","aB"),
     ("Bb","bB"),
     ("BY","Yb"),
     ("Fa","aF"),
     ("Fb","bF"),
     ("FY",""),
     ("aA","F")]

S = "S"

R = [1,2,13,14,13]

if not DEBUG:
    print("Digite Variaveis: Eg: A B")
    V = input().split(" ")
    print("Digite Alfabeto: Eg: A B")
    T = input().split(" ")
    print("Digite Regra de Prod: Eg: A-B aA-A (404 para vazio)")
    P = [(x.split("-")[0], "" if x.split("-")[1] == "404" else x.split("-")[1]) for x in input().split(" ")]
    print("Digite Variavel Inicial: Eg: S")
    S = input()
    print("Regras do Usuario: Eg: 1 2 3 4 5 6 7 8")
    R = [int(x) for x in input().split(" ")]


for r in R:
    if P[r-1][0] in S:
        index = S.find(P[r-1][0])
        part1 = S[:index]
        part2 = S[index + len(P[r-1][0]):]
        S = part1 + P[r-1][1] + part2

print(S)