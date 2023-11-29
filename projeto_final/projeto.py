## Importing necessary libraries
import numpy as np 
import pandas as pd 
import sqlite3 as sql
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go

## Create a connection to the database
con = sql.connect("D:\\Mestrado\\2Sem_23\\FCMII\\projeto_final\\archive\mental_health.sqlite")

## Verificando as colunas da base de dados
table = pd.read_sql('''
SELECT * FROM sqlite_master 
WHERE TYPE = 'table'; ''',con)
table

## Nível de participação em cada pesquisa e analisaremos 
## como o número de entrevistados evoluiu ao longo do tempo.

query = """
    SELECT 
        SurveyID,
        COUNT() AS No_of_Employee
    FROM Answer
    GROUP BY SurveyID;
"""

Employee_per_survey = pd.read_sql(query, con).astype({"No_of_Employee": int})

barplot = Employee_per_survey.plot.bar(x='SurveyID',y='No_of_Employee', color = '#7A111E', alpha = 0.85)
plt.title('Número de funcionários que participaram da pesquisa por ano', fontsize = 15)
plt.ylabel('Número de empregados')
plt.xlabel('SurveyID')

'''
O número de entrevistados aumentou de 2014 para 2016, mas 
diminuiu nos anos seguintes. Vejamos mais de perto a distribuição 
etária dos colaboradores que participaram nos inquéritos de 
saúde mental realizados entre 2014 e 2019.
'''

##########################################################
query = """

SELECT SurveyID, 
       CASE 
            WHEN AnswerText BETWEEN 18 AND 24 THEN '18-24'
            WHEN AnswerText BETWEEN 25 AND 34 THEN '25-34'
            WHEN AnswerText BETWEEN 35 AND 44 THEN '35-44'
            WHEN AnswerText BETWEEN 45 AND 54 THEN '45-54'
            WHEN AnswerText BETWEEN 55 AND 64 THEN '55-64'
            WHEN AnswerText BETWEEN 65 AND 99 THEN 'Maior que 65 '
        END AS age_group,  
    COUNT(*) AS count
FROM Answer
WHERE SurveyID IN (2014, 2016, 2017, 2018, 2019)
      AND QuestionID=1
      AND AnswerText > 18
      
GROUP BY SurveyID, age_group
ORDER BY SurveyID, age_group; 
"""

Age_Survey = pd.read_sql(query, con)
# Obtenha uma lista de faixas etárias exclusivas no dataframe
SurveyID_groups = Age_Survey['SurveyID'].unique()

# Cria uma figura e um objeto de eixo
fig, ax = plt.subplots()

# Trace uma linha para cada faixa etária
for SurveyID_group in SurveyID_groups:
    ax.plot(Age_Survey.loc[Age_Survey['SurveyID'] == SurveyID_group, 'age_group'], Age_Survey.loc[Age_Survey['SurveyID'] == SurveyID_group, 'count'], label=SurveyID_group)

# Defina os rótulos dos eixos x e y
ax.set_xlabel('Grupo de idade')
ax.set_ylabel('Contagem')

# Defina o título
ax.set_title('Contagem de usuários por faixa etária',fontsize = 15)

# Mostre a legenda
ax.legend()

# Mostre gráfico
plt.show()

'''
Os dados são divididos em seis faixas etárias que vão de 18 a 24 anos
até maiores de 65 anos, e cada pesquisa tem uma contagem diferente 
para cada faixa etária. A contagem mais alta é na faixa etária 
de 25 a 34 anos em cada pesquisa.
'''

############################################

# Explorando números e possíveis causas

'''
O conjunto de dados captura respostas de 80 países diferentes, com a 
maioria das respostas vindo dos EUA (2.604)! Meu foco será na saúde 
mental na indústria de tecnologia nos EUA. O gráfico de barras 
borboleta baseia-se em dados de pesquisas de saúde mental realizadas
por empresas de tecnologia 
'''
# No entanto, por serem dados somente leitura, não podemos alterar 
# o texto para dar conta do nome do país, precisamos considerar os 
# Estados Unidos e os Estados Unidos da América juntos

query = """
SELECT SurveyID, 
       SUM(CASE WHEN AnswerText = 'male' OR AnswerText = 'Male' THEN 1 ELSE 0 END) AS male_count,
       SUM(CASE WHEN AnswerText = 'female' OR AnswerText = 'Female'THEN 1 ELSE 0 END) AS female_count
FROM Answer
WHERE     QuestionID == 2 
      OR (QuestionID == 9 AND AnswerText == 1 ) 
      OR (QuestionID == 3 AND AnswerText =='United States of America' OR AnswerText =='United States')
GROUP BY SurveyID
"""

#Pergunta 2: qual é o seu gênero?
#Pergunta 9: Seu empregador é principalmente uma empresa/organização de tecnologia?
#Pergunta 3: Em que país você mora?

df=pd.read_sql(query, con)
pos = np.arange(len(df)) + .5 # bars centered on the y axis
fig, (ax_left, ax_right) = plt.subplots(ncols=2)
ax_left.barh(pos, df['male_count'], align='center', facecolor='#1C5894')
ax_left.set_xlim((0,1100))
ax_left.set_yticks([])
ax_left.set_xlabel('male count')
ax_left.invert_xaxis()
ax_right.barh(pos, df['female_count'], align='center', facecolor='#B2182B')
ax_right.set_xlim((0,1000))
ax_right.set_yticks(pos)
ax_right.set_yticklabels(df['SurveyID'].values, ha='center', x=-0.06)
ax_right.set_xlabel('Female count')
plt.title('Total de pessoas na tecnologia por genêro',fontsize = 15)
plt.tick_params(left = False)
plt.show()

######################################################

'''
Esses dados detalham o número de colaboradores que participaram do
inquérito de saúde mental, organizado por estado e ano, de 2016 a 2019.
'''
query = """
SELECT year, state, COUNT(*) AS Employee_count
FROM (
 SELECT UserID,SurveyID AS year,
        MAX(CASE WHEN QuestionID == 4  THEN AnswerText END) AS state,
        MAX(CASE WHEN (QuestionID == 5  AND AnswerText !=1)  THEN AnswerText END) AS Self_Employed,
        MAX(CASE WHEN QuestionID == 13  THEN AnswerText END) AS Tech_company,
        COUNT (*) as count

 FROM Answer
 WHERE   QuestionID == 4  AND AnswerText !=-1
         OR (QuestionID == 5  )
         OR (QuestionID == 13 AND AnswerText == 1 ) 
GROUP BY UserID
HAVING state IS NOT NULL
       AND Self_Employed IS NOT NULL
       AND Tech_company IS NOT NULL
)

GROUP BY year, state
ORDER BY year
"""

#Pergunta 4 qual estado? remova -1 (fora dos EUA)
#Pergunta 5 você trabalha por conta própria?
#Pergunta 9: Seu empregador é principalmente uma empresa/organização de tecnologia?

df=pd.read_sql(query, con)

state_appreviation = pd.read_csv('/kaggle/input/states/stateAPP1.csv')
state_appreviation = state_appreviation.applymap(lambda x: x.strip() if isinstance(x, str) else x)
merged_df = pd.merge(df, state_appreviation ,on="state")

fig = px.choropleth(merged_df,
                    locations="StateCode",
                    locationmode="USA-states",
                    color="Employee_count", 
                    hover_name = "Employee_count",
                    color_continuous_scale =px.colors.sequential.Reds,
                    animation_frame="year",
                    scope="usa"
                    )

fig.update_layout(
    title={
        'text':"Number of Employees who took the survey by State ",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)
fig.show()