
def m1(n):
    s = ""
    for i in range(0,n):
        for j in range(0,n):
            s+="*"
        s+="\n"
    print(s)
    pass

def m2(n):
    s = ""
    for i in range(0,n):
        for j in range(0,i+1):
            s+="*"
        s+="\n"
    print(s)
    pass

def m3(n):
    for i in range(0,n):
        s = ""
        for j in range(0,n-i):
            s+="*"
        print(s)
    pass

def m4(n):
    for i in range(0,n):
        s = ""
        for j in range(0,n-i):
            s+=" "
        for j in range(0, 2*i+1):
            s+="*"
        print(s)
    pass

def m5(n):
    for i in range(0,n):
        s = ""
        for j in range(0,i):
            s+=" "
        for j in range(0, 2*(n-i)-1):
            s+="*"
        print(s)
    pass

d = int(input("Qual desafio quer imprimir (1 - 5)?"))
n = int(input("Número de linhas para impressão. Max(20): "))
if n > 20: 
    n = 20
if d == 1: m1(n)
elif d == 2: m2(n)
elif d == 3: m3(n)
elif d == 4: m4(n)
elif d == 5: m5(n)
else:
    m4(n)
    m5(n)

