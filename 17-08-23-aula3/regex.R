library(tidyverse)
library(pdftools)

setwd("D:\\Mestrado\\2Sem_23\\FCMII\\17-08-23-aula3")

pdf <- pdf_text("cadastro.pdf")
pdf <- str_split_1(pdf,"\\n")
pdf

# extraindo o nome
nome <-pdf[grepl("[nN]ome:", pdf)]

#gsub(padrao achar, padrao substituir, variavel)
nome <- gsub("[nN]ome:", "",nome)
nome <- gsub("\\(.*\\)", "",nome) # deletar parenteses com 0 ou mais caracteres
nome <- trimws(nome,"both") # tira espacos sobrnado dos lados

# extraindo o alias
apelido <-pdf[grepl("[nN]ome:", pdf)]
apelido <- str_extract(apelido, "\\(.*\\)")
apelido <- gsub("\\(\\w+ |\\)","",apelido)

### TEREFA DO DIA 17/08/2023
# Extraindo o CEP
cep <- pdf[grepl("CEP:", pdf)]
cep <- gsub("CEP:", "", cep)
cep <- gsub("[^0-9-]", "", cep)  # Removendo tudo exceto números e o caractere de traço

# Limpando espaços em branco
cep <- trimws(cep, "both")
cep