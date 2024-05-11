# Documentação Case Técnico 
## Primeira etapa:

### Definindo ferramentas que serão utilizadas
<br> Para esse desafio optei por utilizar a ferramenta "Apache Hop" para fazer o tratamento, limpeza e a organização dos dados que chegaram até mim. Uma etapa importante, visto que, um simples erro pode atrapalhar na veracidade de alguma consulta.

<br> Utilizando a pipeline do Apache Hop, montei um flow para filtrar a tabela e após a filtragem, subir a tabela pro banco de dados. Então, primeiramente fiz a filtragem da primeira tabela "Informações judiciarias" ficando da seguinte forma:

<img src="https://media.discordapp.net/attachments/971178165479301134/1238826266807767101/image.png?ex=6640b25e&is=663f60de&hm=85194ced1472c7835c85bfc32ff94349cef374bd51c7a04b6b7beb331effcdd1&=&format=webp&quality=lossless&width=500&height=350" alt="" width="650" height="400"><br>

<br> Tendo em vista os espaços que estão vazios e as possiveis irregularidades em alguma linha ou coluna, podemos configurar a filtragem para corrigir automaticamente esses erros
