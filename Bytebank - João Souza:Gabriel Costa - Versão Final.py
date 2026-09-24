from datetime import datetime

#TAXA DE RENDIMENTO DOS COFRINHOS (0,5% AO MÊS, JUROS SIMPLES)
TAXA_RENDIMENTO = 0.005

#LIMITE MÁXIMO POR OPERAÇÃO DE SAQUE
LIMITE_SAQUE = 1000.0

#LIMITE DE CRÉDITO APROVADO NO CADASTRO
LIMITE_CREDITO = 2000.0

#PROGRAMA DE FIDELIDADE BYTEPOINTS (TABELA DE EQUIVALÊNCIA)
REAIS_POR_PONTO = 10.0
PONTOS_POR_RESGATE = 100
CASHBACK_POR_RESGATE = 5.0

#CATEGORIAS DE GASTO DISPONÍVEIS
CATEGORIAS = ["Alimentação", "Transporte", "Lazer", "Contas", "Outros"]

#MENU INICIAL
def exibir_menu():
    print("\n=== ByteBank MVP ===")
    print("[1] Cadastrar Cliente")
    print("[2] Listar Clientes")
    print("--- CONTA ---")
    print("[3] Consultar Saldo")
    print("[4] Depositar")
    print("[5] Sacar")
    print("--- COFRINHOS ---")
    print("[6] Criar Cofrinho")
    print("[7] Guardar no Cofrinho")
    print("[8] Resgatar do Cofrinho")
    print("[9] Simular Rendimento")
    print("--- PIX E RELATÓRIOS ---")
    print("[10] Transferir via PIX")
    print("[11] Relatório de Gastos por Categoria")
    print("[12] Extrato de Transações")
    print("[13] Estornar Última Transação (LIFO)")
    print("--- FIDELIDADE ---")
    print("[20] Consultar BytePoints")
    print("[21] Resgatar Cashback")
    print("--- CARTÃO DE CRÉDITO ---")
    print("[17] Comprar no Crédito")
    print("[18] Ver Fatura")
    print("[19] Pagar Fatura")
    print("--- BOLETOS (FILA) ---")
    print("[14] Agendar Boleto")
    print("[15] Ver Fila de Boletos")
    print("[16] Processar Fila / Virada de Lote (FIFO)")
    print("[0] Sair")
    return input("> Digite a operação desejada: ")

#FORMATAÇÃO FINANCEIRA NO PADRÃO BRASILEIRO (1.250,50)
def formatar_real(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

#LEITURA DE VALOR EM DINHEIRO
def ler_valor(mensagem):
    try:
        return float(input(mensagem))
    except ValueError:
        print("[ERRO] Por favor, insira um valor numérico válido.")
        return None

#ESCOLHA DA CATEGORIA DO GASTO
def selecionar_categoria():
    print("\nCategorias de gasto:")

    for numero, categoria in enumerate(CATEGORIAS, start=1):
        print(f"[{numero}] {categoria}")

    escolha = input("> Categoria deste gasto: ").strip()

    if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(CATEGORIAS):
        print("[ERRO] Categoria inválida. Operação cancelada.")
        return None

    return CATEGORIAS[int(escolha) - 1]

#REGISTRO NO HISTÓRICO DO CLIENTE
def registrar_movimentacao(cliente, tipo, valor, fluxo, categoria=None, referencia=None):
    #APPEND = PUSH: A TRANSAÇÃO VAI PARA O TOPO DA PILHA DE HISTÓRICO
    cliente["historico"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo": tipo,
        "valor": valor,
        "fluxo": fluxo,
        "categoria": categoria,
        "referencia": referencia
    })

#GERA O PRÓXIMO NÚMERO DE CONTA ÚNICO
def gerar_numero_conta(clientes):
    maior = 1000

    for dados in clientes.values():

        if int(dados["numero_conta"]) > maior:
            maior = int(dados["numero_conta"])

    return str(maior + 1)

#BUSCA A CONTA PELO NÚMERO
def buscar_por_numero_conta(clientes, numero):
    for cpf, dados in clientes.items():

        if dados["numero_conta"] == numero:
            return cpf

    return None

#BUSCA O DONO DE UMA CHAVE PIX
def buscar_por_chave_pix(clientes, chave):
    for cpf, dados in clientes.items():

        if dados["chave_pix"] == chave:
            return cpf

    return None

#ESCONDE PARTE DO CPF NA CONFERÊNCIA
def mascarar_cpf(cpf):
    return f"***.{cpf[3:6]}.{cpf[6:9]}-**"

#CADASTRO
def cadastrar_cliente(clientes):
    nome = input("\n> Nome do cliente: ").strip()

    if nome == "":
        print("[ERRO] O nome do cliente não pode ficar em branco.")
        return

    cpf = input("> CPF do cliente (somente números): ").strip()

    if not cpf.isdigit() or len(cpf) != 11:
        print("[ERRO] O CPF deve conter exatamente 11 números.")
        return

    if cpf in clientes:
        print(f"[ERRO] Este CPF já pertence ao cliente {clientes[cpf]['nome']}.")
        return

    chave_pix = input("> Chave PIX (e-mail ou telefone): ").strip()

    if chave_pix == "":
        print("[ERRO] A chave PIX não pode ficar em branco.")
        return

    dono_da_chave = buscar_por_chave_pix(clientes, chave_pix)

    if dono_da_chave is not None:
        print(f"[ERRO] Esta chave PIX já pertence ao cliente {clientes[dono_da_chave]['nome']}.")
        return

    numero_conta = gerar_numero_conta(clientes)
    clientes[cpf] = {"nome": nome, "numero_conta": numero_conta, "saldo": 0.0, "cofrinhos": {}, "chave_pix": chave_pix, "historico": [], "boletos": [], "limite_credito": LIMITE_CREDITO, "saldo_fatura": 0.0, "compras_credito": [], "pontos": 0}
    print(f"[SUCESSO] Cliente {nome} cadastrado com saldo inicial de R$ {formatar_real(0.0)}.")
    print(f"[INFO] Conta nº {numero_conta} | Chave PIX: {chave_pix}")
    print(f"[INFO] Limite de crédito aprovado: R$ {formatar_real(LIMITE_CREDITO)}")

#TOTAL GUARDADO NOS COFRINHOS
def total_em_cofrinhos(cliente):
    return sum(cliente["cofrinhos"].values())

#LISTAGEM
def listar_clientes(clientes):
    if not clientes:
        print("\n[AVISO] Nenhum cliente cadastrado até o momento.")
        return

    print("\n=== CLIENTES CADASTRADOS ===")
    for cpf, dados in clientes.items():
        guardado = total_em_cofrinhos(dados)
        print(f"{dados['nome']:<15} | Conta: {dados['numero_conta']} | CPF: {cpf} | PIX: {dados['chave_pix']:<20} | Saldo: R$ {formatar_real(dados['saldo'])} | Cofrinhos: R$ {formatar_real(guardado)}")

#EXTRATO DO CLIENTE
def exibir_saldo(cliente):
    guardado = total_em_cofrinhos(cliente)

    print(f"\n=== SALDO DE {cliente['nome'].upper()} ===")
    print(f"Conta nº {cliente['numero_conta']} | Chave PIX: {cliente['chave_pix']}")
    print(f"Disponível na conta: R$ {formatar_real(cliente['saldo'])}")
    print(f"Guardado em cofrinhos: R$ {formatar_real(guardado)}")
    print(f"Patrimônio total: R$ {formatar_real(cliente['saldo'] + guardado)}")
    print(f"BytePoints acumulados: {cliente['pontos']}")
    print(f"Fatura do cartão: R$ {formatar_real(cliente['saldo_fatura'])}")
    print(f"Limite disponível: R$ {formatar_real(cliente['limite_credito'] - cliente['saldo_fatura'])} de R$ {formatar_real(cliente['limite_credito'])}")

    if cliente["cofrinhos"]:
        print("\n--- COFRINHOS ---")
        for nome_caixinha, valor in cliente["cofrinhos"].items():
            print(f"{nome_caixinha:<15} | R$ {formatar_real(valor)}")

#SELEÇÃO DO CLIENTE DA OPERAÇÃO
def selecionar_cliente(clientes):
    if not clientes:
        print("\n[AVISO] Nenhum cliente cadastrado. Cadastre um cliente antes de operar.")
        return None

    identificador = input("\n> CPF ou número da conta do cliente: ").strip()

    #BUSCA DIRETA PELO CPF (CHAVE DO DICIONÁRIO)
    if identificador in clientes:
        return identificador

    #VARREDURA DA COLEÇÃO PELO NÚMERO DA CONTA
    cpf = buscar_por_numero_conta(clientes, identificador)

    if cpf is not None:
        return cpf

    print("[ERRO] Cliente não encontrado.")
    return None

#SELEÇÃO DO COFRINHO DA OPERAÇÃO
def selecionar_cofrinho(cliente):
    if not cliente["cofrinhos"]:
        print(f"[AVISO] {cliente['nome']} ainda não tem cofrinhos. Crie um na opção [6].")
        return None

    print("Cofrinhos disponíveis:", ", ".join(cliente["cofrinhos"].keys()))
    nome_caixinha = input("> Nome da caixinha: ").strip()

    if nome_caixinha not in cliente["cofrinhos"]:
        print("[ERRO] Caixinha não encontrada.")
        return None

    return nome_caixinha

#DEPÓSITO
def depositar(cliente):
    valor = ler_valor("> Digite o valor para depósito: R$ ")

    if valor is None:
        return

    if valor <= 0:
        print("[ERRO] O valor de depósito deve ser positivo.")
        return

    cliente["saldo"] += valor
    registrar_movimentacao(cliente, "Depósito", valor, "entrada")
    print(f"[SUCESSO] Depósito de R$ {formatar_real(valor)} na conta de {cliente['nome']}.")

#SAQUE
def sacar(cliente):
    valor = ler_valor("> Digite o valor para saque: R$ ")

    if valor is None:
        return

    if valor <= 0:
        print("[ERRO] O valor de saque deve ser positivo.")
        return

    if valor > LIMITE_SAQUE:
        print(f"[ERRO] Limite de R$ {formatar_real(LIMITE_SAQUE)} por saque. Faça a operação em partes.")
        return

    if valor > cliente["saldo"]:
        print("[ERRO] Saldo insuficiente para esta operação.")
        return

    categoria = selecionar_categoria()

    if categoria is None:
        return

    cliente["saldo"] -= valor
    registrar_movimentacao(cliente, "Saque", valor, "saida", categoria)
    print(f"[SUCESSO] Saque de R$ {formatar_real(valor)} da conta de {cliente['nome']}. Categoria: {categoria}.")
    creditar_pontos(cliente, valor)

#CRIAÇÃO DE COFRINHO
def criar_cofrinho(cliente):
    nome_caixinha = input("> Nome da nova caixinha (ex: Viagem): ").strip()

    if nome_caixinha == "":
        print("[ERRO] O nome da caixinha não pode ficar em branco.")
        return

    if nome_caixinha in cliente["cofrinhos"]:
        print("[ERRO] Este cliente já tem uma caixinha com esse nome.")
        return

    cliente["cofrinhos"][nome_caixinha] = 0.0
    print(f"[SUCESSO] Caixinha '{nome_caixinha}' criada para {cliente['nome']}.")

#GUARDAR DINHEIRO NA CAIXINHA
def guardar_no_cofrinho(cliente, nome_caixinha, valor):
    if valor <= 0:
        print("[ERRO] O valor a guardar deve ser positivo.")
        return

    if valor > cliente["saldo"]:
        print(f"[ERRO] Saldo insuficiente. Disponível na conta: R$ {formatar_real(cliente['saldo'])}")
        return

    cliente["saldo"] -= valor
    cliente["cofrinhos"][nome_caixinha] += valor
    registrar_movimentacao(cliente, f"Guardou em '{nome_caixinha}'", valor, "interna", None, nome_caixinha)
    print(f"[SUCESSO] R$ {formatar_real(valor)} guardados em '{nome_caixinha}'.")
    print(f"[INFO] Caixinha: R$ {formatar_real(cliente['cofrinhos'][nome_caixinha])} | Conta: R$ {formatar_real(cliente['saldo'])}")

#RESGATAR DINHEIRO DA CAIXINHA
def resgatar_do_cofrinho(cliente, nome_caixinha, valor):
    if valor <= 0:
        print("[ERRO] O valor a resgatar deve ser positivo.")
        return

    if valor > cliente["cofrinhos"][nome_caixinha]:
        print(f"[ERRO] A caixinha '{nome_caixinha}' tem apenas R$ {formatar_real(cliente['cofrinhos'][nome_caixinha])}")
        return

    cliente["cofrinhos"][nome_caixinha] -= valor
    cliente["saldo"] += valor
    registrar_movimentacao(cliente, f"Resgatou de '{nome_caixinha}'", valor, "interna", None, nome_caixinha)
    print(f"[SUCESSO] R$ {formatar_real(valor)} resgatados de '{nome_caixinha}'.")
    print(f"[INFO] Caixinha: R$ {formatar_real(cliente['cofrinhos'][nome_caixinha])} | Conta: R$ {formatar_real(cliente['saldo'])}")

#SIMULAÇÃO DE RENDIMENTO (JUROS SIMPLES)
def simular_rendimento(cliente):
    if not cliente["cofrinhos"]:
        print(f"[AVISO] {cliente['nome']} ainda não tem cofrinhos para render.")
        return

    try:
        meses = int(input("> Simular rendimento para quantos meses? "))
    except ValueError:
        print("[ERRO] Informe um número inteiro de meses.")
        return

    if meses <= 0:
        print("[ERRO] O período deve ser de pelo menos 1 mês.")
        return

    print(f"\n=== SIMULAÇÃO: {TAXA_RENDIMENTO * 100}% AO MÊS EM {meses} MESES ===")
    total_hoje = 0.0
    total_futuro = 0.0

    for nome_caixinha, valor in cliente["cofrinhos"].items():
        rendimento = valor * TAXA_RENDIMENTO * meses
        total_hoje += valor
        total_futuro += valor + rendimento
        print(f"{nome_caixinha:<15} | Hoje: R$ {formatar_real(valor)} | Rende: R$ {formatar_real(rendimento)} | Total: R$ {formatar_real(valor + rendimento)}")

    print(f"\n[TOTAL] Hoje: R$ {formatar_real(total_hoje)} | Em {meses} meses: R$ {formatar_real(total_futuro)}")
    print("[AVISO] Simulação apenas. Nenhum valor foi movimentado.")

#TRANSFERÊNCIA PIX
def transferir_pix(clientes, cpf_origem):
    chave = input("> Chave PIX de destino: ").strip()
    cpf_destino = buscar_por_chave_pix(clientes, chave)

    #VERIFICAÇÃO DA CHAVE DE DESTINO
    if cpf_destino is None:
        print("[ERRO] Chave PIX não encontrada. Nenhum valor foi transferido.")
        return

    if cpf_destino == cpf_origem:
        print("[ERRO] Esta chave pertence ao próprio cliente da operação.")
        return

    origem = clientes[cpf_origem]
    destino = clientes[cpf_destino]

    valor = ler_valor("> Valor da transferência: R$ ")

    if valor is None:
        return

    if valor <= 0:
        print("[ERRO] O valor da transferência deve ser positivo.")
        return

    if valor > origem["saldo"]:
        print(f"[ERRO] Saldo insuficiente. Disponível na conta: R$ {formatar_real(origem['saldo'])}")
        return

    categoria = selecionar_categoria()

    if categoria is None:
        return

    #CONFIRMAÇÃO ANTES DE MOVIMENTAR O DINHEIRO
    print("\n--- CONFIRA OS DADOS DO PIX ---")
    print(f"Destinatário: {destino['nome']}")
    print(f"CPF: {mascarar_cpf(cpf_destino)} | Conta nº {destino['numero_conta']}")
    print(f"Chave: {chave}")
    print(f"Valor: R$ {formatar_real(valor)}")
    print(f"Categoria: {categoria}")
    confirmacao = input("> Confirmar transferência? (s/n): ").strip().lower()

    if confirmacao != 's':
        print("[CANCELADO] Transferência cancelada. Nenhum valor foi movimentado.")
        return

    origem["saldo"] -= valor
    destino["saldo"] += valor
    registrar_movimentacao(origem, "PIX enviado", valor, "saida", categoria, cpf_destino)
    registrar_movimentacao(destino, "PIX recebido", valor, "entrada", None, cpf_origem)
    print(f"[SUCESSO] PIX de R$ {formatar_real(valor)} enviado para {destino['nome']}.")
    print(f"[INFO] Novo saldo de {origem['nome']}: R$ {formatar_real(origem['saldo'])}")
    creditar_pontos(origem, valor)

#EXTRATO DE TRANSAÇÕES
def exibir_extrato(cliente):
    if not cliente["historico"]:
        print(f"\n[AVISO] {cliente['nome']} ainda não tem movimentações.")
        return

    print(f"\n=== EXTRATO DE {cliente['nome'].upper()} ===")

    for movimentacao in cliente["historico"]:

        if movimentacao["fluxo"] == "entrada":
            sinal = "+"
        elif movimentacao["fluxo"] == "saida":
            sinal = "-"
        elif movimentacao["fluxo"] == "credito":
            sinal = "C"
        else:
            sinal = "~"

        descricao = movimentacao["tipo"]

        if movimentacao["categoria"]:
            descricao += f" ({movimentacao['categoria']})"

        print(f"{movimentacao['data']} | {sinal} R$ {formatar_real(movimentacao['valor']):>12} | {descricao}")

    print(f"\nTotal de movimentações: {len(cliente['historico'])}")
    print(f"Saldo atual na conta: R$ {formatar_real(cliente['saldo'])}")
    print("Legenda: (+) entrou  (-) saiu  (C) crédito  (~) interna (cofrinho ou fatura)")

#RELATÓRIO DE GASTOS POR CATEGORIA
def relatorio_categoria(cliente):
    gastos_por_categoria = {}
    total_gasto = 0.0
    total_entradas = 0.0

    #PERCORRE O HISTÓRICO E AGRUPA (GROUP BY EM MEMÓRIA)
    for movimentacao in cliente["historico"]:

        if movimentacao["fluxo"] == "entrada":
            total_entradas += movimentacao["valor"]

        elif movimentacao["fluxo"] == "saida" or movimentacao["fluxo"] == "credito":
            total_gasto += movimentacao["valor"]
            categoria = movimentacao["categoria"]

            if categoria in gastos_por_categoria:
                gastos_por_categoria[categoria] += movimentacao["valor"]
            else:
                gastos_por_categoria[categoria] = movimentacao["valor"]

    if total_gasto == 0:
        print(f"\n[AVISO] {cliente['nome']} ainda não registrou nenhum gasto.")
        return

    print(f"\n=== GASTOS POR CATEGORIA: {cliente['nome'].upper()} ===")
    print(f"Entradas registradas: R$ {formatar_real(total_entradas)}")
    print(f"Total gasto: R$ {formatar_real(total_gasto)}")

    if total_entradas > 0:
        consumo = total_gasto / total_entradas * 100
        print(f"Orçamento consumido: {consumo:.1f}% do que entrou")

    print()

    #DO MAIOR GASTO PARA O MENOR
    ranking = sorted(gastos_por_categoria.items(), key=lambda item: item[1], reverse=True)

    for categoria, valor in ranking:
        percentual = valor / total_gasto * 100
        barra = "#" * int(percentual / 5)
        print(f"{categoria:<15} | R$ {formatar_real(valor):>12} | {percentual:>5.1f}% | {barra}")

#CRÉDITO DE PONTOS POR GASTO (1 PONTO A CADA R$ 10)
def creditar_pontos(cliente, valor):
    pontos = int(valor / REAIS_POR_PONTO)

    if pontos > 0:
        cliente["pontos"] += pontos
        print(f"[BYTEPOINTS] +{pontos} ponto(s). Saldo do programa: {cliente['pontos']} pontos.")

#CONSULTA DO SALDO DE PONTOS
def consultar_pontos(cliente):
    print(f"\n=== BYTEPOINTS DE {cliente['nome'].upper()} ===")
    print(f"Pontos acumulados: {cliente['pontos']}")
    print(f"Regra: 1 ponto a cada R$ {formatar_real(REAIS_POR_PONTO)} em saques e transferências.")
    print(f"Troca: {PONTOS_POR_RESGATE} pontos = R$ {formatar_real(CASHBACK_POR_RESGATE)} de cashback.")

    resgates = cliente["pontos"] // PONTOS_POR_RESGATE

    if resgates > 0:
        print(f"Disponível para resgate: R$ {formatar_real(resgates * CASHBACK_POR_RESGATE)}")
    else:
        faltam = PONTOS_POR_RESGATE - cliente["pontos"]
        print(f"Faltam {faltam} ponto(s) para o primeiro resgate.")

#RESGATE DE CASHBACK
def resgatar_cashback(cliente, pontos):
    if pontos <= 0:
        print("[ERRO] A quantidade de pontos deve ser positiva.")
        return

    if pontos > cliente["pontos"]:
        print(f"[ERRO] Saldo insuficiente. {cliente['nome']} tem {cliente['pontos']} ponto(s).")
        return

    if pontos % PONTOS_POR_RESGATE != 0:
        print(f"[ERRO] O resgate é feito em blocos de {PONTOS_POR_RESGATE} pontos.")
        return

    #CONVERSÃO PELA TABELA DE EQUIVALÊNCIA
    cashback = pontos / PONTOS_POR_RESGATE * CASHBACK_POR_RESGATE
    cliente["pontos"] -= pontos
    cliente["saldo"] += cashback
    registrar_movimentacao(cliente, "Cashback resgatado", cashback, "entrada")
    print(f"[SUCESSO] {pontos} ponto(s) viraram R$ {formatar_real(cashback)} na conta.")
    print(f"[INFO] Pontos restantes: {cliente['pontos']} | Saldo: R$ {formatar_real(cliente['saldo'])}")

#COMPRA NO CARTÃO DE CRÉDITO
def comprar_no_credito(cliente, valor, estabelecimento):
    limite_disponivel = cliente["limite_credito"] - cliente["saldo_fatura"]

    if valor <= 0:
        print("[ERRO] O valor da compra deve ser positivo.")
        return

    if valor > limite_disponivel:
        print(f"[ERRO] Compra negada. Limite disponível: R$ {formatar_real(limite_disponivel)}")
        return

    categoria = selecionar_categoria()

    if categoria is None:
        return

    #A COMPRA NÃO TOCA NO SALDO: AUMENTA A FATURA E CONSOME O LIMITE
    cliente["saldo_fatura"] += valor
    cliente["compras_credito"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "estabelecimento": estabelecimento,
        "valor": valor,
        "categoria": categoria
    })
    registrar_movimentacao(cliente, f"Crédito em {estabelecimento}", valor, "credito", categoria)
    print(f"[SUCESSO] Compra de R$ {formatar_real(valor)} aprovada em {estabelecimento}.")
    print(f"[INFO] Fatura: R$ {formatar_real(cliente['saldo_fatura'])} | Limite restante: R$ {formatar_real(cliente['limite_credito'] - cliente['saldo_fatura'])}")

#CONSULTA DA FATURA ABERTA
def exibir_fatura(cliente):
    print(f"\n=== FATURA DO CARTÃO: {cliente['nome'].upper()} ===")

    if not cliente["compras_credito"]:
        print("Nenhuma compra lançada nesta fatura.")
    else:

        for compra in cliente["compras_credito"]:
            print(f"{compra['data']} | {compra['estabelecimento']:<20} | R$ {formatar_real(compra['valor']):>10} | {compra['categoria']}")

    if cliente["saldo_fatura"] == 0 and cliente["compras_credito"]:
        print("\nTotal da fatura: R$ 0,00 (quitada)")
    else:
        print(f"\nTotal da fatura: R$ {formatar_real(cliente['saldo_fatura'])}")
    print(f"Limite disponível: R$ {formatar_real(cliente['limite_credito'] - cliente['saldo_fatura'])} de R$ {formatar_real(cliente['limite_credito'])}")
    print(f"Saldo em conta: R$ {formatar_real(cliente['saldo'])}")

#PAGAMENTO DA FATURA COM O SALDO DA CONTA
def pagar_fatura(cliente):
    if cliente["saldo_fatura"] <= 0:
        print(f"\n[AVISO] {cliente['nome']} não tem fatura em aberto.")
        return

    print(f"\nFatura em aberto: R$ {formatar_real(cliente['saldo_fatura'])}")
    print(f"Saldo em conta: R$ {formatar_real(cliente['saldo'])}")
    valor = ler_valor("> Valor a pagar (pode ser parcial): R$ ")

    if valor is None:
        return

    if valor <= 0:
        print("[ERRO] O valor do pagamento deve ser positivo.")
        return

    if valor > cliente["saldo_fatura"]:
        print(f"[ERRO] O valor excede a fatura de R$ {formatar_real(cliente['saldo_fatura'])}.")
        return

    if valor > cliente["saldo"]:
        print("[ERRO] Saldo insuficiente na conta para este pagamento.")
        return

    #O DINHEIRO SAI DA CONTA, ABATE A FATURA E DEVOLVE O LIMITE
    cliente["saldo"] -= valor
    cliente["saldo_fatura"] -= valor
    registrar_movimentacao(cliente, "Pagamento de fatura", valor, "interna", None, "FATURA")

    if cliente["saldo_fatura"] == 0:
        print(f"[SUCESSO] Fatura quitada com R$ {formatar_real(valor)}. Limite totalmente restabelecido.")
    else:
        print(f"[SUCESSO] Pagamento parcial de R$ {formatar_real(valor)}.")
        print(f"[INFO] Fatura restante: R$ {formatar_real(cliente['saldo_fatura'])}")

    print(f"[INFO] Saldo em conta: R$ {formatar_real(cliente['saldo'])} | Limite disponível: R$ {formatar_real(cliente['limite_credito'] - cliente['saldo_fatura'])}")

#AGENDAMENTO DE BOLETO (TAD FILA / ENQUEUE)
def agendar_boleto(cliente):
    descricao = input("> Descrição do boleto (ex: Conta de Luz): ").strip()

    if descricao == "":
        print("[ERRO] A descrição do boleto não pode ficar em branco.")
        return

    valor = ler_valor("> Valor do boleto: R$ ")

    if valor is None:
        return

    if valor <= 0:
        print("[ERRO] O valor do boleto deve ser positivo.")
        return

    categoria = selecionar_categoria()

    if categoria is None:
        return

    #APPEND = ENQUEUE: O BOLETO ENTRA NO FIM DA FILA
    cliente["boletos"].append({"descricao": descricao, "valor": valor, "categoria": categoria})
    print(f"[SUCESSO] Boleto '{descricao}' de R$ {formatar_real(valor)} agendado.")
    print(f"[INFO] Posição na fila: {len(cliente['boletos'])}º")

#CONSULTA DA FILA DE BOLETOS
def listar_fila_boletos(cliente):
    if not cliente["boletos"]:
        print(f"\n[AVISO] {cliente['nome']} não tem boletos agendados.")
        return

    print(f"\n=== FILA DE BOLETOS: {cliente['nome'].upper()} ===")
    total_agendado = 0.0

    for posicao, boleto in enumerate(cliente["boletos"], start=1):
        total_agendado += boleto["valor"]
        print(f"{posicao}º | {boleto['descricao']:<20} | R$ {formatar_real(boleto['valor']):>10} | {boleto['categoria']}")

    print(f"\nTotal agendado: R$ {formatar_real(total_agendado)}")
    print(f"Saldo disponível: R$ {formatar_real(cliente['saldo'])}")

    if total_agendado > cliente["saldo"]:
        print("[ATENÇÃO] O saldo atual não cobre a fila inteira.")

#VIRADA DE LOTE (TAD FILA / DEQUEUE)
def processar_fila_boletos(cliente):
    if not cliente["boletos"]:
        print(f"\n[AVISO] {cliente['nome']} não tem boletos para processar.")
        return

    print(f"\n=== VIRADA DE LOTE: {cliente['nome'].upper()} ===")
    print(f"Saldo antes do processamento: R$ {formatar_real(cliente['saldo'])}")
    print(f"Boletos na fila: {len(cliente['boletos'])}\n")

    pagos = 0
    total_pago = 0.0

    while cliente["boletos"]:
        #ESPIA O PRIMEIRO DA FILA SEM RETIRAR
        proximo = cliente["boletos"][0]

        if proximo["valor"] > cliente["saldo"]:
            print(f"[PARADO] Saldo insuficiente para '{proximo['descricao']}' (R$ {formatar_real(proximo['valor'])}).")
            print("[INFO] A ordem de chegada é respeitada: o lote para aqui.")
            break

        #POP(0) = DEQUEUE: O PRIMEIRO A ENTRAR É O PRIMEIRO A SAIR
        boleto = cliente["boletos"].pop(0)
        cliente["saldo"] -= boleto["valor"]
        registrar_movimentacao(cliente, f"Boleto '{boleto['descricao']}'", boleto["valor"], "saida", boleto["categoria"])
        pagos += 1
        total_pago += boleto["valor"]
        print(f"[PAGO] {boleto['descricao']:<20} | R$ {formatar_real(boleto['valor']):>10} | Saldo: R$ {formatar_real(cliente['saldo'])}")

    print(f"\n[RESUMO] {pagos} boleto(s) liquidado(s), total de R$ {formatar_real(total_pago)}.")
    print(f"Boletos restantes na fila: {len(cliente['boletos'])}")
    print(f"Saldo final: R$ {formatar_real(cliente['saldo'])}")

#ESTORNO DA ÚLTIMA TRANSAÇÃO (TAD PILHA / LIFO)
def estornar_ultima_transacao(clientes, cpf):
    cliente = clientes[cpf]

    if not cliente["historico"]:
        print(f"[AVISO] {cliente['nome']} não tem transações para estornar.")
        return

    #TOPO DA PILHA: O ÚLTIMO A ENTRAR É O PRIMEIRO A SAIR
    topo = cliente["historico"][-1]

    print("\n--- TRANSAÇÃO NO TOPO DA PILHA ---")
    print(f"Data: {topo['data']}")
    print(f"Operação: {topo['tipo']}")
    print(f"Valor: R$ {formatar_real(topo['valor'])}")

    #VALIDAÇÕES ANTES DE MEXER EM QUALQUER SALDO
    if topo["fluxo"] == "entrada" and topo["valor"] > cliente["saldo"]:
        print("[ERRO] O saldo atual não cobre a devolução desta entrada. Estorno bloqueado.")
        return

    #PONTOS GANHOS NA OPERAÇÃO PRECISAM VOLTAR JUNTO
    pontos_da_operacao = 0

    if topo["tipo"] == "Saque" or topo["tipo"] == "PIX enviado":
        pontos_da_operacao = int(topo["valor"] / REAIS_POR_PONTO)

        if pontos_da_operacao > cliente["pontos"]:
            print("[ERRO] Os pontos desta operação já foram resgatados. Estorno bloqueado.")
            return

    contraparte = None

    if topo["tipo"] == "PIX enviado":
        contraparte = clientes[topo["referencia"]]

        if topo["valor"] > contraparte["saldo"]:
            print(f"[ERRO] {contraparte['nome']} já não tem o valor recebido. Estorno bloqueado.")
            return

    if topo["fluxo"] == "credito" and topo["valor"] > cliente["saldo_fatura"]:
        print("[ERRO] A fatura já não comporta o estorno desta compra.")
        return

    if topo["fluxo"] == "interna" and topo["referencia"] != "FATURA":
        caixinha = topo["referencia"]

        if topo["tipo"].startswith("Guardou") and topo["valor"] > cliente["cofrinhos"][caixinha]:
            print(f"[ERRO] A caixinha '{caixinha}' não tem mais esse valor. Estorno bloqueado.")
            return

        if topo["tipo"].startswith("Resgatou") and topo["valor"] > cliente["saldo"]:
            print("[ERRO] Saldo insuficiente para devolver o valor à caixinha.")
            return

    confirmacao = input("> Confirmar o estorno desta transação? (s/n): ").strip().lower()

    if confirmacao != 's':
        print("[CANCELADO] Nenhuma transação foi estornada.")
        return

    #REVERSÃO DO IMPACTO FINANCEIRO
    if topo["fluxo"] == "entrada":
        cliente["saldo"] -= topo["valor"]

        if topo["tipo"] == "Cashback resgatado":
            cliente["pontos"] += int(topo["valor"] / CASHBACK_POR_RESGATE * PONTOS_POR_RESGATE)

        if topo["tipo"] == "PIX recebido":
            remetente = clientes[topo["referencia"]]
            remetente["saldo"] += topo["valor"]
            registrar_movimentacao(remetente, "Estorno de PIX enviado", topo["valor"], "entrada", None, cpf)

    elif topo["fluxo"] == "credito":
        cliente["saldo_fatura"] -= topo["valor"]

        if cliente["compras_credito"]:
            cliente["compras_credito"].pop()

    elif topo["fluxo"] == "saida":
        cliente["saldo"] += topo["valor"]

        if topo["tipo"] == "PIX enviado":
            contraparte["saldo"] -= topo["valor"]
            registrar_movimentacao(contraparte, "Estorno de PIX recebido", topo["valor"], "saida", "Estorno", cpf)

    elif topo["referencia"] == "FATURA":
        cliente["saldo"] += topo["valor"]
        cliente["saldo_fatura"] += topo["valor"]

    else:
        caixinha = topo["referencia"]

        if topo["tipo"].startswith("Guardou"):
            cliente["cofrinhos"][caixinha] -= topo["valor"]
            cliente["saldo"] += topo["valor"]
        else:
            cliente["cofrinhos"][caixinha] += topo["valor"]
            cliente["saldo"] -= topo["valor"]

    if pontos_da_operacao > 0:
        cliente["pontos"] -= pontos_da_operacao
        print(f"[BYTEPOINTS] -{pontos_da_operacao} ponto(s) retirados junto com o estorno.")

    #POP: REMOVE E DEVOLVE O TOPO DA PILHA
    estornada = cliente["historico"].pop()

    print(f"[SUCESSO] '{estornada['tipo']}' de R$ {formatar_real(estornada['valor'])} foi estornado.")
    print(f"[INFO] Novo saldo de {cliente['nome']}: R$ {formatar_real(cliente['saldo'])}")
    print(f"[INFO] Transações restantes na pilha: {len(cliente['historico'])}")

#CAIXA
def main():
    clientes = {}

    while True:
        opcao = exibir_menu()
        #CADASTRAR CLIENTE
        if opcao == '1':
            cadastrar_cliente(clientes)
        #LISTAR CLIENTES
        elif opcao == '2':
            listar_clientes(clientes)
        #CONSULTAR SALDO
        elif opcao == '3':
            cpf = selecionar_cliente(clientes)

            if cpf:
                exibir_saldo(clientes[cpf])
        #DEPÓSITO
        elif opcao == '4':
            cpf = selecionar_cliente(clientes)

            if cpf:
                depositar(clientes[cpf])
        #SAQUE
        elif opcao == '5':
            cpf = selecionar_cliente(clientes)

            if cpf:
                sacar(clientes[cpf])
        #CRIAR COFRINHO
        elif opcao == '6':
            cpf = selecionar_cliente(clientes)

            if cpf:
                criar_cofrinho(clientes[cpf])
        #GUARDAR NO COFRINHO
        elif opcao == '7':
            cpf = selecionar_cliente(clientes)

            if cpf:
                nome_caixinha = selecionar_cofrinho(clientes[cpf])

                if nome_caixinha:
                    valor = ler_valor("> Valor para guardar: R$ ")

                    if valor is not None:
                        guardar_no_cofrinho(clientes[cpf], nome_caixinha, valor)
        #RESGATAR DO COFRINHO
        elif opcao == '8':
            cpf = selecionar_cliente(clientes)

            if cpf:
                nome_caixinha = selecionar_cofrinho(clientes[cpf])

                if nome_caixinha:
                    valor = ler_valor("> Valor para resgatar: R$ ")

                    if valor is not None:
                        resgatar_do_cofrinho(clientes[cpf], nome_caixinha, valor)
        #SIMULAR RENDIMENTO
        elif opcao == '9':
            cpf = selecionar_cliente(clientes)

            if cpf:
                simular_rendimento(clientes[cpf])
        #TRANSFERIR VIA PIX
        elif opcao == '10':
            cpf = selecionar_cliente(clientes)

            if cpf:
                transferir_pix(clientes, cpf)
        #RELATÓRIO POR CATEGORIA
        elif opcao == '11':
            cpf = selecionar_cliente(clientes)

            if cpf:
                relatorio_categoria(clientes[cpf])
        #EXTRATO DE TRANSAÇÕES
        elif opcao == '12':
            cpf = selecionar_cliente(clientes)

            if cpf:
                exibir_extrato(clientes[cpf])
        #ESTORNO DA ÚLTIMA TRANSAÇÃO
        elif opcao == '13':
            cpf = selecionar_cliente(clientes)

            if cpf:
                estornar_ultima_transacao(clientes, cpf)
        #AGENDAR BOLETO
        elif opcao == '14':
            cpf = selecionar_cliente(clientes)

            if cpf:
                agendar_boleto(clientes[cpf])
        #VER FILA DE BOLETOS
        elif opcao == '15':
            cpf = selecionar_cliente(clientes)

            if cpf:
                listar_fila_boletos(clientes[cpf])
        #PROCESSAR A FILA
        elif opcao == '16':
            cpf = selecionar_cliente(clientes)

            if cpf:
                processar_fila_boletos(clientes[cpf])
        #COMPRAR NO CRÉDITO
        elif opcao == '17':
            cpf = selecionar_cliente(clientes)

            if cpf:
                estabelecimento = input("> Estabelecimento: ").strip()

                if estabelecimento == "":
                    print("[ERRO] Informe o estabelecimento da compra.")
                else:
                    valor = ler_valor("> Valor da compra: R$ ")

                    if valor is not None:
                        comprar_no_credito(clientes[cpf], valor, estabelecimento)
        #VER FATURA
        elif opcao == '18':
            cpf = selecionar_cliente(clientes)

            if cpf:
                exibir_fatura(clientes[cpf])
        #PAGAR FATURA
        elif opcao == '19':
            cpf = selecionar_cliente(clientes)

            if cpf:
                pagar_fatura(clientes[cpf])
        #CONSULTAR PONTOS
        elif opcao == '20':
            cpf = selecionar_cliente(clientes)

            if cpf:
                consultar_pontos(clientes[cpf])
        #RESGATAR CASHBACK
        elif opcao == '21':
            cpf = selecionar_cliente(clientes)

            if cpf:
                consultar_pontos(clientes[cpf])

                try:
                    pontos = int(input("> Quantos pontos deseja resgatar? "))
                    resgatar_cashback(clientes[cpf], pontos)
                except ValueError:
                    print("[ERRO] Informe um número inteiro de pontos.")
        #EXIT
        elif opcao == '0':
            print("\nEncerrando o sistema ByteBank. Até logo!")
            break

        else:
            print("\n[ERRO] Opção inválida. Escolha uma das opções do menu.")

if __name__ == "__main__":
    print("Inicializando o Sistema...")
    main()
