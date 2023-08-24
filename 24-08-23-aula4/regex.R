
##################################
# Carregamento
library(tidyverse)
library(pdftools)

setwd("D:\\Mestrado\\2Sem_23\\FCMII\\24-08-23-aula4")

pdf <- pdf_text("cadastro.pdf")
pdf <- str_split_1(pdf,"\\n")
pdf

###################################

## 24/08/2023 TAREFA ABAIXO
# extraindo o endereço
endereco <- pdf[grepl("Endereço:",pdf)]
endereco <- gsub("Endereço:","",endereco)
endereco <- gsub("CEP.*[0-9]$","",endereco)
endereco <- gsub("\\.$","",endereco)
endereco <- trimws(endereco,"both")

endereco1 <- gsub(",.*","", endereco) # nome da rua

num_endereco <- gsub("[^0-9]","",endereco)
num_endereco <- gsub("^$","S/N", num_endereco) # numero

bairro <- gsub(".*,(.*)","\\1",endereco) # bairro
bairro <- trimws(bairro,"both")

###################################

### TEREFA DO DIA 17/08/2023
# Extraindo o CEP
cep <- pdf[grepl("CEP:", pdf)]
cep <- gsub("CEP:", "", cep)
cep <- gsub("[^0-9-]", "", cep)
cep <- trimws(cep, "both")

###################################

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

#extraindo telefone
telefone <- pdf[grepl("Tel:|Telefone:",pdf)]
telefone <- gsub("Tel:|Telefone:|[-()]","",telefone)
telefone <- gsub("\\s","",telefone)
telefone <- gsub("^(\\d{2})","(\\1)",telefone)
telefone <- gsub("^(.{9})", "\\1-", telefone)

# extraindo cpf
cpf <- pdf[grepl("CPF:|cpf:",pdf)]
cpf <- gsub("CPF:|cpf:","",cpf)
cpf <- gsub("-|\\.","",cpf)
cpf <- trimws(cpf,"both")

# extraindo data de nascimento
data_nascimento <- pdf[grepl("Data de nascimento:|Dt nasc:", pdf)]
data_nascimento <- gsub("Data de nascimento:|Dt nasc:","", data_nascimento)
obs_data <- gsub("[0-9-]","",data_nascimento)

# Criando a base de dados
cadastro <- cbind(nome,apelido,data_nascimento, endereco1,num_endereco,bairro, cep,telefone,cpf)
cadastro <- as.data.frame(cadastro)















