![image](https://github.com/NatanGPS/Desafio_Dados/assets/94939074/4cb644dd-0ceb-436e-a7c6-53f36cb11cb8)# Documentação Case Técnico 
## Primeira etapa:

### Definindo ferramentas que serão utilizadas
<br> Para esse desafio optei por utilizar a ferramenta "Apache Hop" para fazer o tratamento, limpeza e a organização dos dados que chegaram até mim. Uma etapa importante, visto que, um simples erro pode atrapalhar na veracidade de alguma consulta.

<br> Utilizando a pipeline do Apache Hop, montei um flow para filtrar a tabela e após a filtragem, subir a tabela pro banco de dados. Então, primeiramente fiz a filtragem da primeira tabela "Informações judiciarias" ficando da seguinte forma:

<img src="https://media.discordapp.net/attachments/971178165479301134/1238826266807767101/image.png?ex=6640b25e&is=663f60de&hm=85194ced1472c7835c85bfc32ff94349cef374bd51c7a04b6b7beb331effcdd1&=&format=webp&quality=lossless&width=500&height=350" alt="" width="650" height="400"><br>

<br> Tendo em vista os espaços que estão vazios e as possiveis irregularidades em alguma linha ou coluna, podemos configurar a filtragem para corrigir automaticamente esses erros.
<br> Com todos as irregularidades resolvidas podemos subir nossa tabela para o banco de dados, nesse dasafio, optei por usar o banco de dados PostgreSQl.

<br> No final do processo a pipeline ficou da seguinte forma:

<img src="https://media.discordapp.net/attachments/971178165479301134/1238826044060864616/image.png?ex=6640b229&is=663f60a9&hm=0eb07b3c05e260181a35aee9a2575264936af4eb35dad4ed1ee12b59ff1dd907&=&format=webp&quality=lossless" alt="" width="1000" height="500"><br>

<br> Agora, ao entrar no meu banco de dados posso confirmar que a tabela realmente foi criada e os dados foram importados de acordo com o planejado

<img src="https://media.discordapp.net/attachments/971178165479301134/1238830743862644827/image.png?ex=6640b689&is=663f6509&hm=dbba4ea4352414a96d3483093b98e058452e872f29e63570cdce7dbddefd06e7&=&format=webp&quality=lossless&width=1253&height=671" alt="" width="1000" height="400"><br>

<br> Vou repetir exatamente o mesmo proceso para as demais tabelas.

### Definindo o que são fatores de riscos e como serão classificados
