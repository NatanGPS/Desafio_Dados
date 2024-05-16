# Primeira coisa que precisamos fazer é importar todos frameworks que vamos utilizar ao longo do projeto 
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split # Utilizado para separar dados de treino e teste
from sklearn.preprocessing import StandardScaler # Utilizado para fazer a normalização dos dados
from sklearn.preprocessing import MinMaxScaler # Utilizado para fazer a normalização dos dados
from sklearn.preprocessing import LabelEncoder # Utilizado para fazer o OneHotEncoding
from sklearn.linear_model import LinearRegression # Algoritmo de Regressão Linear
from sklearn.metrics import r2_score # Utilizado para medir a acuracia do modelo preditivo



#Esses comandos permitem que nossa tabela apareça de forma completa sem limites (pode ser usado tambem para limilitar a tabela )
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Defino uma variavel para carregar todos os dados da minha tabela nela
df_dados = pd.read_csv("tabela_info.csv")

#print(df_dados.shape) # print para verificar escala da tabela
#print(df_dados.head()) #print para ver as primeiras linhas da tabela 
#print(df_dados.info()) # print pra saber volume de linhas por coluna
df_dados.drop('nome', axis=1, inplace=True)


# Essa pré análise é super importante pq podemos observar quais colunas podemos excluir, e quais devemos fazer um OneHotCoding por exemplo.
# aqui por exemplo posso perceber que muitas colunas da minha tabela estão salvas como objetos
# nesse caso preciso descobrir o problema na coluna para posteriormente transformalas em int ou float caso seja necessario


# Por exemplo, valores NaN ou Null precisam ser tratados de alguma forma 

#print(df_dados.isnull().sum())


df_dados['capital_social'] = df_dados['capital_social'].fillna(0)
df_dados['renda_estimada'] = df_dados['renda_estimada'].fillna(0)
df_dados['faturamento_estimado'] = df_dados['faturamento_estimado'].fillna(0)

df_dados['participacao'] = df_dados['participacao'].fillna(0)
df_dados['chance_empregaticia'] = df_dados['chance_empregaticia'].fillna("DESCONHECIDA")
df_dados['cnae'] = df_dados['cnae'].fillna("NAO EXiSTE")
df_dados['qualificacao'] = df_dados['qualificacao'].fillna("NÃO POSSUI")


# Função para substituir "1BILHAOEAIS" por 1000000000
def substituir_bilhao(texto):
    if isinstance(texto, str) and "1BILHAOEAIS" in texto:
        texto = texto.replace("1BILHAOEAIS", "1000000000")
    return texto

# Aplicar a função substituir_bilhao antes de calcular_media
df_dados['renda_estimada'] = df_dados['renda_estimada'].apply(substituir_bilhao)
df_dados['faturamento_estimado'] = df_dados['faturamento_estimado'].apply(substituir_bilhao)



# Função para calcular a média entre os valores antes e depois do "A"
def calcular_media(texto):
    if isinstance(texto, str) and "A" in texto:
        valores = texto.split("A")
        numeros = [int(num) for num in valores if num.isdigit()]
        if len(numeros) == 2:
            media = sum(numeros) / 2
            return str(media)
    return texto

# Aplicar a função calcular_media nas colunas desejadas
df_dados['renda_estimada'] = df_dados['renda_estimada'].apply(calcular_media)
df_dados['faturamento_estimado'] = df_dados['faturamento_estimado'].apply(calcular_media)

# Salvar o DataFrame modificado em um novo arquivo CSV
#df_dados.to_csv("tabela_filtrada3_modificada.csv", index=False)
#print(df_dados.isnull().sum())
df_dados['renda_estimada'] = df_dados['renda_estimada'].astype(np.float64)
#print(df_dados.loc[df_dados['faturamento_estimado'] == '1BILHAOEAIS'])

df_dados['faturamento_estimado'] = df_dados['faturamento_estimado'].astype(np.float64)



# Vamos carregar em uma lista as variaveis que são do tipo INT64 E FLOAT64
variaveis_numericas = []
for i in df_dados.columns[0:16].tolist():
        if df_dados.dtypes[i] == 'int64' or df_dados.dtypes[i] == 'float64':            
            #print(i, ':' , df_dados.dtypes[i]) 
            variaveis_numericas.append(i)

def BloxPlotNumericos():
     # Aqui definimos o tamanho da tela para exibição dos gráficos
    plt.rcParams["figure.figsize"] = [15.00, 12.00]
    plt.rcParams["figure.autolayout"] = True

    # Aqui definimos em quantas linhas e colunas queremos exibir os gráficos
    f, axes = plt.subplots(2, 5) #2 linhas e 5 colunas

    linha = 0
    coluna = 0

    for i in variaveis_numericas:
        sns.boxplot(data = df_dados, y=i, ax=axes[linha][coluna])
        coluna += 1
        if coluna == 5:
            linha += 1
            coluna = 0            

    plt.show()  



# Certo, podemos começar as preparações do nosso modelo preditivo

#print("Menor idade: {}".format(df_dados["idade"].min()))
#print("Maior idade: {}".format(df_dados["idade"].max()))

# Vamos fazer um engenharia de atributos

idade_bins = [0, 30, 40, 50 , 60, 80]
idade_categoria =["Até 30", "31 a 40", "41 a 50", "51 a 60", "Maior que 60"]
df_dados["FAIXA_ETARIA"] = pd.cut(df_dados["idade"], idade_bins, labels=idade_categoria)

#print(df_dados["FAIXA_ETARIA"].value_counts())


# Avaliando qual faixa etaria tem tido maiores salarios
#print(df_dados.groupby(["FAIXA_ETARIA"]).mean()['renda_estimada'])
#print(df_dados.info())


variaveis_categoricas = []
for i in df_dados.columns[0:48].tolist():
        if df_dados.dtypes[i] == 'object' or df_dados.dtypes[i] == 'category':            
            #print(i, ':' , df_dados.dtypes[i]) 
            variaveis_categoricas.append(i)  


def BloxPlotStrings():
     
    # Com este comando iremos exibir todos gráficos de todas colunas de uma vez só para facilitar nossa analise.
    plt.rcParams["figure.figsize"] = [15.00, 22.00]
    plt.rcParams["figure.autolayout"] = True

    f, axes = plt.subplots(3, 2) #3 linhas e 2 colunas

    linha = 0
    coluna = 0

    for i in variaveis_categoricas:    
        sns.countplot(data = df_dados, x=i, ax=axes[linha][coluna])
    
        coluna += 1
        if coluna == 2:
            linha += 1
            coluna = 0            

    plt.show()


# Agora que entendemos um pouco mais sobre os dados que estamos trabalhando vamos
# começar a fase de pre-processamento

#O primeiro passo pra isso é configurar o nosso encoder para que a nossa IA consiga interpretar as nossas variaveis que nao são numericos como numeros.


lb = LabelEncoder()

# Aplica o encoder nas variáveis que estão com string
df_dados['FAIXA_ETARIA'] = lb.fit_transform(df_dados['FAIXA_ETARIA'])
df_dados['servidor_publico'] = lb.fit_transform(df_dados['servidor_publico'])
df_dados['chance_empregaticia'] = lb.fit_transform(df_dados['chance_empregaticia'])
df_dados['cnae'] = lb.fit_transform(df_dados['cnae'])
df_dados['qualificacao'] = lb.fit_transform(df_dados['qualificacao'])



df_dados.dropna(inplace = True) #----> apenas por segurança ja que já tratamos a tabela anteriormente

#print(df_dados.head(200)) -----> aqui podemos ver como fica essa conversao de string para numeros
#print(df_dados.info()) #-----> teste para ver se todos as variaveis agora são numericas

# Separando a variavel alvo
target = df_dados.iloc[:,11:12]

preditoras = df_dados.copy()
del preditoras['score'] 
preditoras.head()

# Divisão em Dados de Treino e Teste.
X_treino, X_teste, y_treino, y_teste = train_test_split(preditoras, target, test_size = 0.3, random_state = 40)


# Vamos aplicar a normalização em treino e teste
# Padronização
sc = MinMaxScaler(feature_range=(0, 1))
X_treino_normalizados = sc.fit_transform(X_treino)
X_teste_normalizados = sc.transform(X_teste)

#Pronto com nossa divisão de teste e treinos feitas, podemos começar a treinar e avaliar nosso modelo preditivo


modelo = RandomForestRegressor()
modelo = modelo.fit(X_treino_normalizados, y_treino)

print(r2_score(y_teste, modelo.fit(X_treino_normalizados, y_treino).predict(X_teste_normalizados))) 


#Aqui neste momento temos algumas opções
#podemos obersevar a partir desse comando que a acertividade da nossa IA é de 70% o que significa que a cada 100 clientes ele acerta 70 e 30 sao "perdidos"
#Dessa forma precisamos alimentar o nosso robo com mais informações. A nivel de produção o que teria de ser feito é alimentar o robo por meio de uma API ou
#jogar ele em uma API DOTNET para que ele seja alimentado com mais dados e aumente sua acertividade, por ser um programa teste, onde as informações são puramente ficcticias 
#vou optar por alimenta-lo manualmente com "informações fantasia" para demonstrar o uso.

CPF =10212357678
IDADE = 67
SERVIDOR_PUBLICO = 0
CHANCE_EMPREGATICIA = 2
RENDA_ESTIMADA = 30000
TOTAL_PROCESSOS = 2
CNAE = 3456
QUALIFICACAO = 498394
PARTICIPACAO = 100
CAPITAL_SOCIAL = 1000000
FATURAMENTO_ESTIMADO = 2000000

FAIXA_ETARIA = 2

dados_novos = [CPF, IDADE, SERVIDOR_PUBLICO, CHANCE_EMPREGATICIA, RENDA_ESTIMADA, 
               TOTAL_PROCESSOS, CNAE, QUALIFICACAO, PARTICIPACAO, CAPITAL_SOCIAL, FATURAMENTO_ESTIMADO, FAIXA_ETARIA]

# Reshape
X = np.array(dados_novos).reshape(1, -1)
X = sc.transform(X)

print('Pontuação do cliente: {}'.format(modelo.predict(X)))

# Através do hitmap podemos observar a correlação entre todas variáveis.
plt.rcParams["figure.figsize"] = (18,8)
ax = sns.heatmap(df_dados.corr(), annot=True)
