# ByteBank

Sistema bancário de terminal desenvolvido em Python puro, sem bibliotecas externas.

Projeto Prático Avaliativo AV2 da disciplina **BD015 (Algoritmo e Estrutura de Dados)** da CESAR School, ministrada pelo Prof. Fernando Ferreira de Carvalho. O sistema simula o core de uma fintech operado por um atendente do banco: múltiplas contas em memória, transferências PIX, cartão de crédito, cofrinhos, programa de pontos e as estruturas lineares de pilha e fila aplicadas a estorno e pagamentos.

## Squad

- João Vitor Souza
- Gabriel Costa

## Como executar

O projeto não precisa de compilação nem de instalação de dependências. Basta ter o **Python 3** instalado.

```bash
python3 main.py
```

Para conferir se o Python está disponível na máquina:

```bash
python3 --version
```

Ao iniciar, o sistema exibe o menu de operações em loop contínuo. A navegação é feita digitando o número da operação desejada, e a opção `[0]` encerra o programa.

> A base de contas é gravada em `contas_bytebank.txt` após cada operação e restaurada automaticamente na próxima execução. Para começar do zero, basta apagar esse arquivo.

## Funcionalidades

### Nível 1 — Operações básicas

- Menu interativo em loop contínuo com encerramento amigável
- Consulta de saldo com visão consolidada (conta, cofrinhos, fatura e pontos)
- Depósito com bloqueio de valores nulos e negativos
- Saque com validação de saldo, valores negativos e **limite de R$ 1.000,00 por operação**
- Tratamento de exceções (`try/except`) contra entradas de texto inválidas
- Formatação financeira no padrão brasileiro (`R$ 1.250,50`)

### Nível 2 — Múltiplas contas e PIX

- Cadastro de clientes com nome, CPF, número de conta gerado automaticamente e chave PIX
- Validação de unicidade de CPF e de chave PIX
- Busca de conta por **CPF** (acesso direto) ou por **número da conta** (varredura da coleção)
- Transferência PIX com verificação da chave de destino, conferência do destinatário antes do envio e débito/crédito atômico entre as contas

### Nível 3 — Estruturas lineares

- **Pilha (LIFO):** toda operação financeira é empilhada no histórico com `append`. A função de estorno usa `pop()` para retirar o topo e reverter o impacto financeiro daquele evento exato, incluindo os dois lados de um PIX
- **Fila (FIFO):** boletos agendados entram no fim da fila com `append` e a virada de lote os processa com `pop(0)`, debitando na ordem exata de chegada e parando quando o saldo não cobre o próximo
- Extrato detalhado com data, hora e sinal por tipo de movimentação

### Funcionalidades extras

- **Cofrinhos:** caixinhas nomeadas por cliente, com guardar, resgatar e simulação de rendimento por juros simples (0,5% ao mês)
- **Categorização de gastos:** toda saída exige categoria, e o relatório agrega os gastos por categoria (`GROUP BY` em memória) com percentual do orçamento consumido
- **Cartão de crédito:** limite aprovado de R$ 2.000,00, compras que consomem limite sem tocar no saldo, consulta de fatura e pagamento total ou parcial que restabelece o limite
- **BytePoints:** 1 ponto a cada R$ 10,00 em saques e transferências, resgatáveis em blocos de 100 pontos por R$ 5,00 de cashback

### Persistência em TXT

- `salvar_contas_txt(contas)` grava a base inteira em `contas_bytebank.txt`, uma linha por registro, com campos separados por `|`
- `carregar_contas_txt()` lê o arquivo ao iniciar e reconstrói o dicionário de contas
- Cada linha começa com o tipo do registro (`CONTA`, `COFRINHO`, `HISTORICO`, `BOLETO`, `COMPRA`) e o CPF do dono:

```text
CONTA|11111111111|Ana Souza|1001|850.0|ana@x.com|2000.0|80.0|35
COFRINHO|11111111111|Viagem|300.0
HISTORICO|11111111111|14/10/2026 16:51|PIX enviado|250.0|saida|Alimentação|22222222222
BOLETO|11111111111|Conta de Luz|120.0|Contas
```

- As linhas são gravadas e lidas na ordem das listas, então a pilha do histórico e a fila de boletos voltam exatamente como estavam e o estorno continua funcionando depois de reiniciar
- O salvamento é automático após cada operação. Fechar a janela não perde dados
- Linhas corrompidas são ignoradas com aviso, sem derrubar o carregamento

### Analisador de Log HTTP

- A opção `[22]` lê um arquivo de log de servidor no formato padrão (`IP - - [data] "GET /pagina HTTP/1.1" 200 1234`) e conta as requisições **200 (Sucesso)** e **404 (Não Encontrado)**, com o percentual de cada uma
- O código de status é extraído cortando a linha nas aspas: ele é o primeiro item depois da requisição
- Linhas fora do formato são ignoradas e contabilizadas à parte
- O repositório inclui `servidor.log` como exemplo. Basta apertar Enter no caminho para analisá-lo

## Mapa do menu

| Opção | Operação |
|---|---|
| 1, 2 | Cadastrar cliente, listar clientes |
| 3, 4, 5 | Consultar saldo, depositar, sacar |
| 6 a 9 | Criar cofrinho, guardar, resgatar, simular rendimento |
| 10 | Transferir via PIX |
| 11, 12 | Relatório de gastos por categoria, extrato de transações |
| 13 | Estornar última transação (LIFO) |
| 14 a 16 | Agendar boleto, ver fila, processar virada de lote (FIFO) |
| 17 a 19 | Comprar no crédito, ver fatura, pagar fatura |
| 20, 21 | Consultar BytePoints, resgatar cashback |
| 22 | Analisar log HTTP do servidor |
| 0 | Sair |

## Estruturas de dados

Cada cliente é um dicionário indexado pelo CPF, o que torna a busca por CPF imediata e impede cadastro duplicado:

```python
clientes = {
    "12345678901": {
        "nome": "João",
        "numero_conta": "1001",
        "saldo": 1000.0,
        "chave_pix": "joao@email.com",
        "cofrinhos": {"Viagem": 500.0},
        "historico": [],
        "boletos": [],
        "limite_credito": 2000.0,
        "saldo_fatura": 0.0,
        "compras_credito": [],
        "pontos": 150
    }
}
```

O `historico` é usado como **pilha** e a lista `boletos` como **fila**. Cada movimentação registra data, tipo, valor, fluxo (entrada, saída, crédito ou interna), categoria e uma referência usada pelo estorno para localizar a contraparte de um PIX ou a caixinha de um cofrinho.

## Regras de negócio

| Regra | Valor |
|---|---|
| Limite por saque | R$ 1.000,00 |
| Limite de crédito aprovado | R$ 2.000,00 |
| Rendimento dos cofrinhos | 0,5% ao mês (juros simples) |
| Acúmulo de pontos | 1 ponto a cada R$ 10,00 |
| Resgate de cashback | 100 pontos = R$ 5,00 |

Todas estão declaradas como constantes no topo do arquivo e podem ser ajustadas em um único lugar.
