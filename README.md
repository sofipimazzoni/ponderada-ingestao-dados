# Ponderada Ingestão de Dados

**API utilizada:** https://api.adviceslip.com/advice
- A cada chamada, retorna um conselho diferente.

## Replicação

Para rodar em seu computador local, faça um clone do repositório, em seguida, rode os seguintes comandos na pasta raiz do projeto:

1. Inicializar o docker
```bash
docker-compose up --build
```

2. Abra outro terminal e rode o servidor app.py
```bash
poetry run python app.py
```
**Em alguns casos, é necessário colocar um 3 depois de python (python3), mas isso depende da forma como a linguagem foi instalada em seu sistema.**

3. Por fim, abra outro terminal e execute o arquivo get_api.py
```bash
poetry run python app.py
```
**Da mesma forma que o segundo passo, caso seja necessário, utilize python3 em vez de python.**

Com isso já será possível perceber que os dados foram adicionados ao clickhouse na tabela working_data. Você deve visualizar algo assim:

![](https://res.cloudinary.com/dpu52x6xq/image/upload/v1724637450/Screenshot_2024-08-25_at_15.27.20_d6amp6.png)

Outra forma de saber se deu certo é pelo terminal de execução do arquivo app.py. Ele deve estar parecido com isto:

![](https://res.cloudinary.com/dpu52x6xq/image/upload/v1724637573/Screenshot_2024-08-25_at_15.29.04_dzuqcx.png)

## Criação da view

Para deixar o processo ainda mais completo, crie uma view no próprio DBeaver da seguinte maneira:

```SQL
CREATE VIEW IF NOT EXISTS working_data_view AS
SELECT
    data_ingestao,
    JSONExtractInt(dado_linha, 'date') AS date_unix,
    JSONExtractString(dado_linha, 'dados') AS dados,
    toDateTime(JSONExtractInt(dado_linha, 'data_ingestao') / 1000) AS data_ingestao_datetime
FROM working_data;
```
Após a criação, acesse ela pela interface do próprio DBeaver. Você verá algo parecido com isto:

![](https://res.cloudinary.com/dpu52x6xq/image/upload/v1724637756/Screenshot_2024-08-25_at_15.27.41_l4ehmk.png)

## Testes 

Foram realizados alguns testes na aplicação para ter certeza de que as funções estavam funcionando corretamente. Para executá-los, basta ir na raiz do projeto e rodar o comando `pytest` no terminal. O resultado esperado está abaixo:

![](https://res.cloudinary.com/dpu52x6xq/image/upload/v1724637886/Screenshot_2024-08-25_at_22.39.01_znnex4.png)
