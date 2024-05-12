![image](https://github.com/NatanGPS/Desafio_Dados/assets/94939074/4cb644dd-0ceb-436e-a7c6-53f36cb11cb8)# Documentação Case Técnico 
## Primeira etapa:

### Definindo ferramentas que serão utilizadas
<br> Para esse desafio optei por utilizar a ferramenta "Apache Hop" para fazer o tratamento, limpeza e a organização dos dados que chegaram até mim. Uma etapa importante, visto que, um simples erro pode atrapalhar na veracidade de alguma consulta.

<br> Utilizando a pipeline do Apache Hop, montei um flow para filtrar a tabela e após a filtragem, subir a tabela pro banco de dados. Então, primeiramente fiz a filtragem da primeira tabela "Informações judiciarias" ficando da seguinte forma:

<img src="https://media.discordapp.net/attachments/971178165479301134/1238826266807767101/image.png?ex=6640b25e&is=663f60de&hm=85194ced1472c7835c85bfc32ff94349cef374bd51c7a04b6b7beb331effcdd1&=&format=webp&quality=lossless&width=500&height=350" alt="" width="650" height="400"><br>

<br> Tendo em vista os espaços que estão vazios e as possiveis irregularidades em alguma linha ou coluna, podemos configurar a filtragem para corrigir automaticamente esses erros.
<br> Com todos as irregularidades resolvidas podemos subir nossa tabela para o banco de dados, nesse desafio, optei por usar o banco de dados PostgreSQl.

<br> No final do processo a pipeline ficou da seguinte forma:

<img src="https://media.discordapp.net/attachments/971178165479301134/1238826044060864616/image.png?ex=6640b229&is=663f60a9&hm=0eb07b3c05e260181a35aee9a2575264936af4eb35dad4ed1ee12b59ff1dd907&=&format=webp&quality=lossless" alt="" width="1000" height="500"><br>

<br> Agora, ao entrar no meu banco de dados posso confirmar que a tabela realmente foi criada e os dados foram importados de acordo com o planejado

<img src="https://media.discordapp.net/attachments/971178165479301134/1238830743862644827/image.png?ex=6640b689&is=663f6509&hm=dbba4ea4352414a96d3483093b98e058452e872f29e63570cdce7dbddefd06e7&=&format=webp&quality=lossless&width=1253&height=671" alt="" width="1000" height="400"><br>

<br> Vou repetir exatamente o mesmo proceso para as demais tabelas.

### Definindo o que são fatores de riscos e como serão classificados
<br> Com 3 tabelas extensas dessas não conseguimos saber ao certo quais informações serão vitais para avaliar nossos clientes, como não recebi instruções especificas sobre quais deveria usar, tomei a liberdade de pesquisar mais a fundo sobre como empresas de credito e seguro avaliam seus possiveis clientes. Sabendo disso, resolvi separar apenas as colunas que iria usar a fim de fazer uma tabela menor somente com os dados que irei utilizar, ficou da seguinte forma: CPF, IDADE, SERVIDOR PUBLICO, CHANCE EMPREGATICIA, RENDA ESTIMADA, TOTAL DE PROCESSOS, POSSUI EMPRESA, FATURAMENTO ESTIMADO. Com uma pequena consulta SQL pude separar isso em uma tabela só, além disso foi possivel por meio da consulta filtrar e preparar algumas colunas para que posteriormente fossem totalmente limpas de valores incorretos e nulos. Segue a consulta que utilizei

    SELECT DISTINCT
    ip.nome AS nome,
    ip.cpf AS cpf,
    ip.idade AS idade,
    ip.servidor_publico AS servidor_publico,
    ip.endereco_residencial AS chance_empregaticia,
    REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
        ip.precisao, 'ATE', ''), 'DE', ''), 'ACIMA DE', ''), '.', ''), ',', ''), 'R$', ''), 'R', ''), ' A ', 'A'), ' ', ''), 'ACIMA', '')AS renda_estimada,
    j.total AS total_processos,
    s.cnae AS cnae,
    s.qualificacao AS qualificacao,
    s.participacao AS participacao,
    s.capital_social AS capital_social,
    REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
        s.faturamento_estimado, 'ATE', ''), 'DE', ''), 'ACIMA DE', ''), '.', ''), ',', ''), 'R$', ''), 'R', ''), ' A ', 'A'), ' ', ''), 'ACIMA', '')AS faturamento_estimado
    FROM 
      informacoes_pessoais ip
    JOIN 
      judiciario j
    ON 
      ip.cpf = j.id
    JOIN 
      societario s
    ON 
      j.id = s.id
    WHERE 
      j.tipo = 'NUMERO DE PROCESSOS'

<br> Perceba que, nos comandos REPLACE que utilizei, deixei  a letra A nos campos que possuiam mais de um valor, como por exemplo alguns valores da coluna "renda_estimada" que vinham dessa forma: "12000 A 20000", o fato de deixar a letra A me permite que posteriormente eu consiga fazer uma media dessa renda e substituir a linha por apenas um valor para que, dessa forma, eu possa usar a linha ao meu favor, além disso, varios campos estavam com valor nulo, o que pode atrapalhar nas consultas analiticas que pretendo fazer, então pra resolver isso, upei a tabela no python e com algumas linhas de codigo fui resolvendo alguns problemas que observei na tabela, as linhas que utilizei pra essa correção foram as seguinte: (o arquivo tambem está anexado nesse protifolio)

        # Primeira coisa que precisamos fazer é importar todos frameworks que vamos utilizar ao longo do projeto 
        import pandas as pd
        import matplotlib as plt
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        import warnings
        warnings.filterwarnings("ignore")


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
        df_dados['participacao'] = df_dados['participacao'].fillna(0)
        df_dados['chance_empregaticia'] = df_dados['chance_empregaticia'].fillna("DESCONHECIDA")
        df_dados['cnae'] = df_dados['cnae'].fillna("NAO EXiSTE")
        df_dados['qualificacao'] = df_dados['qualificacao'].fillna("NÃO POSSUI")



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
        df_dados.to_csv("tabela_filtrada3_modificada.csv", index=False)



<br> Pronto! Dessa forma nossa tabela está finalmente limpa, sem valores nullos ou incorretos, além de estarem com seu tipo correto. Agora precisamos fazer um modo de analisar os clientes.

### Fazendo um modelo preditivo para análise de risco
<br> Existem diversas formas de se fazer uma análise de risco, muitas empresas utilizam formulas proprias para fazer o calculo do score, no meu caso vou utilizar os dados presentes da nossa tabela e uma outra tabela de scores para que a IA possa aprender a fazer os calculos que se aproximem da tabela de score, dessa forma ela vai conseguir calcular um score de risco para cada pessoa e quanto maior for nossa tabela melhor será a exatidão do score calculado. Por enquanto estou upando a tabela manualmente, mas a ideia de utilizar um banco de dados é conectar o script diretamente ao banco para que, dessa forma, ele se atualize a cada atualização das tabelas. Sabendo disso podemos continuar nosso codigo, vamos continuar utilizando o mesmo codigo que usei logo acima, dessa forma, a cada atualização da tabela nossa filtragem dos valores indesejados permanece funcionando. A partir desse momento comecarei a fazer os comentarios pelo proprio codigo que irei anexar aqui, mas quando tiver uma função um pouco mais longa eu irei explicar por aqui


### Considerações finais
Após finalizar o codigo, pude perceber que, existe uma grande necessidade de encontrar dados que são mais relacionados entre si, e que, para um bom funcionamento da maquina, muitos dados teriam que ser colocados para que a maquina seja mais eficaz, provavelmente a melhor forma seria usa-la com uma visão mais a longo prazo, ou até mesmo utilizar uma outra forma de treinamento, mas o que pude perceber é que, pessoas com mais de 50 ano e menos que 80 e que ganham em média mais de 2000 são as que mais fizeram pontuação.


Sei que o modelo é muito básico e poderia fazer apenas uma coisa mais básica no PowerBi ou ate mesmo no Metabase, mas a minha ideia foi mostrar um pouco de tudo que sei e, de certa forma, mostrar a forma como eu penso quando estou resolvendo um problema como este. Agradeço a atenção e o tempo para ler até aqui, foi um teste muito legal de ser feito. Espero que gostem!
