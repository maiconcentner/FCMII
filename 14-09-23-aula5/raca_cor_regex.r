# Ler o conteúdo do arquivo
linhas <- readLines("RACA_COR.CNV", warn = FALSE)

# Inicializar vetores para armazenar as informações
descricao_raca_cor <- character(0)
codigos <- character(0)

# Loop para percorrer as linhas
for (linha in linhas) {
  # Verificar se a linha contém a informação de raça/cor e código
  if (grepl("^\\s+\\d+\\s+([^0-9]+)\\s+(\\d+)$", linha)) {
    descricao_raca_cor <- c(descricao_raca_cor, gsub("^\\s+\\d+\\s+([^0-9]+)\\s+\\d+$", "\\1", linha))
    codigos <- c(codigos, gsub("^\\s+\\d+\\s+[^0-9]+\\s+(\\d+)$", "\\1", linha))
  } else if (grepl("^\\s+\\d+\\s+SEM INFORMAÇÃO\\s+", linha)) {
    descricao_raca_cor <- c(descricao_raca_cor, "SEM INFORMAÇÃO")
    codigos <- c(codigos, gsub("^\\s+\\d+\\s+SEM INFORMAÇÃO\\s+(\\d+)$", "\\1", linha))
  }
}

# Substituir os códigos "M", "G", "C", "DE", "D" por "1M", "1G", "1C", "DE", "D"
codigos <- gsub("M", "1M", codigos)
codigos <- gsub("G", "1G", codigos)
codigos <- gsub("C", "1C", codigos)
codigos <- gsub("DE", "DE", codigos)
codigos <- gsub("D", "D", codigos)

# Criar o data.frame
dados <- data.frame(descricao_raca_cor = descricao_raca_cor, codigos = codigos, stringsAsFactors = FALSE)
dados <- rbind(dados, data.frame(descricao_raca_cor = 'SEM INFORMAÇÃO', 
                                 codigos = '99'))
dados <- rbind(dados, data.frame(descricao_raca_cor = 'RAÇA/COR=06 (INDEVIDO)', 
                                 codigos = '06'))
dados <- rbind(dados, data.frame(descricao_raca_cor = 'RAÇA/COR=09 (INDEVIDO)', 
                                 codigos = '09'))
dados <- rbind(dados, data.frame(descricao_raca_cor = 'RAÇA/COR  (OUTROS INDEVIDOS)', 
                                 codigos = '1M,1G,1C,DE, D,87'))

