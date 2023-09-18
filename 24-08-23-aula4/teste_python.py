#%% METACARACTERES

# \w - Qualquer caractere (exceto linha nova)
# \W - Qualquer caractere alfanumérico
# \d - Qualquer caractere não-alfanumérico
# \D - Qualquer caractere não dígito
# \s - Espaço em braco
# ^ - Começa com
# $ - Termina com
# "\" - Usado antes de metacarteres para especificar seu significado literal

#%% QUANTIFICADORES

# [] - Opcional entre os que estão dentro dos colchetes
# () - Captura grupos de caracteres
# * - De zero a mais vezes
# ? - Zero ou uma vez
# + - Uma ou mais vezes
# {m,n} - De 'm' a 'n' vezes
# | - Ou

#%% FUNCAO SEARCH
import re

# Função search
frase1 = 'Olá, meu número de telefone é (42)0000-0000'
frase2 = 'A placa de carro que eu anotei durante o acidente foi FRT-1998'
frase3 = 'Entre em contato, meu email é teste@gmail.com'

# telefone da frase 1
telefone = re.search('\(\d{2}\)\d{4,5}-\d{4}', frase1)

# placa da frase 2
placa = re.search('[A-Za-z]{3}-\w{4}',frase2)

# email da frase 3
email = re.search('\w+@\w+\.\w+' , frase3)

#%% FUNCAO MATCH

# basicamente verifica se a frase começa com o padrao

#%% FUNCAO FINDALL

# verifica todo o corpo do textoem busca do padrao

emails = '''Nome: Teste 1
email: teste1@hotmail.com
Nome: Teste 2
email: teste2@gmail.com
Nome: Teste 3
email: fulano@yahoo.com.br
'''

lista_email = re.findall('\w+@\w+\.\w+\.*\w+' , emails)
print(lista_email)