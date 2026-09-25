import re
print(re.match(r"=|==", "==").group())   # mostra =   (pegou a primeira que serviu)
print(re.match(r"==|=", "==").group())   # mostra ==  (maior primeiro: certo)

# O mesmo efeito com letras: a regex fica com a 1a opcao que serve
print(re.match(r"a|ab", "ab").group())   # mostra a

# Fora da regex, no Python, = e == sao coisas diferentes:
x = 5              # =  guarda 5 dentro de x (atribuicao)
print(x == 5)      # == pergunta "x e igual a 5?" -> mostra True
print(x == 7)      # -> mostra False