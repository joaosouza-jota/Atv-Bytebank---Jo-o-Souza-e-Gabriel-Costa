#TAXA DE RENDIMENTO DOS COFRINHOS (0,5% AO MÊS, JUROS SIMPLES)
TAXA_RENDIMENTO = 0.005

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
    print("[0] Sair")
    return input("> Digite a operação desejada: ")

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
def registrar_movimentacao(cliente, tipo, valor, fluxo, categoria=None):
    cliente["historico"].append({
        "tipo": tipo,
        "valor": valor,
        "fluxo": fluxo,
        "categoria": categoria
    })

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

    clientes[cpf] = {"nome": nome, "saldo": 0.0, "cofrinhos": {}, "chave_pix": chave_pix, "historico": []}
    print(f"[SUCESSO] Cliente {nome} cadastrado com saldo inicial de R$ 0.00.")
    print(f"[INFO] Chave PIX registrada: {chave_pix}")

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
        print(f"{dados['nome']:<15} | CPF: {cpf} | PIX: {dados['chave_pix']:<20} | Saldo: R$ {dados['saldo']:.2f} | Cofrinhos: R$ {guardado:.2f}")

#EXTRATO DO CLIENTE
def exibir_saldo(cliente):
    guardado = total_em_cofrinhos(cliente)

    print(f"\n=== SALDO DE {cliente['nome'].upper()} ===")
    print(f"Chave PIX: {cliente['chave_pix']}")
    print(f"Disponível na conta: R$ {cliente['saldo']:.2f}")
    print(f"Guardado em cofrinhos: R$ {guardado:.2f}")
    print(f"Patrimônio total: R$ {cliente['saldo'] + guardado:.2f}")

    if cliente["cofrinhos"]:
        print("\n--- COFRINHOS ---")
        for nome_caixinha, valor in cliente["cofrinhos"].items():
            print(f"{nome_caixinha:<15} | R$ {valor:.2f}")

#SELEÇÃO DO CLIENTE DA OPERAÇÃO
def selecionar_cliente(clientes):
    if not clientes:
        print("\n[AVISO] Nenhum cliente cadastrado. Cadastre um cliente antes de operar.")
        return None

    cpf = input("\n> CPF do cliente: ").strip()

    if cpf not in clientes:
        print("[ERRO] Cliente não encontrado.")
        return None

    return cpf

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
    print(f"[SUCESSO] Depósito de R$ {valor:.2f} na conta de {cliente['nome']}.")

#SAQUE
def sacar(cliente):
    valor = ler_valor("> Digite o valor para saque: R$ ")

    if valor is None:
        return

    if valor <= 0:
        print("[ERRO] O valor de saque deve ser positivo.")
        return

    if valor > cliente["saldo"]:
        print("[ERRO] Saldo insuficiente para esta operação.")
        return

    categoria = selecionar_categoria()

    if categoria is None:
        return

    cliente["saldo"] -= valor
    registrar_movimentacao(cliente, "Saque", valor, "saida", categoria)
    print(f"[SUCESSO] Saque de R$ {valor:.2f} da conta de {cliente['nome']}. Categoria: {categoria}.")

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
        print(f"[ERRO] Saldo insuficiente. Disponível na conta: R$ {cliente['saldo']:.2f}")
        return

    cliente["saldo"] -= valor
    cliente["cofrinhos"][nome_caixinha] += valor
    registrar_movimentacao(cliente, f"Guardou em '{nome_caixinha}'", valor, "interna")
    print(f"[SUCESSO] R$ {valor:.2f} guardados em '{nome_caixinha}'.")
    print(f"[INFO] Caixinha: R$ {cliente['cofrinhos'][nome_caixinha]:.2f} | Conta: R$ {cliente['saldo']:.2f}")

#RESGATAR DINHEIRO DA CAIXINHA
def resgatar_do_cofrinho(cliente, nome_caixinha, valor):
    if valor <= 0:
        print("[ERRO] O valor a resgatar deve ser positivo.")
        return

    if valor > cliente["cofrinhos"][nome_caixinha]:
        print(f"[ERRO] A caixinha '{nome_caixinha}' tem apenas R$ {cliente['cofrinhos'][nome_caixinha]:.2f}")
        return

    cliente["cofrinhos"][nome_caixinha] -= valor
    cliente["saldo"] += valor
    registrar_movimentacao(cliente, f"Resgatou de '{nome_caixinha}'", valor, "interna")
    print(f"[SUCESSO] R$ {valor:.2f} resgatados de '{nome_caixinha}'.")
    print(f"[INFO] Caixinha: R$ {cliente['cofrinhos'][nome_caixinha]:.2f} | Conta: R$ {cliente['saldo']:.2f}")

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
        print(f"{nome_caixinha:<15} | Hoje: R$ {valor:.2f} | Rende: R$ {rendimento:.2f} | Total: R$ {valor + rendimento:.2f}")

    print(f"\n[TOTAL] Hoje: R$ {total_hoje:.2f} | Em {meses} meses: R$ {total_futuro:.2f}")
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
        print(f"[ERRO] Saldo insuficiente. Disponível na conta: R$ {origem['saldo']:.2f}")
        return

    categoria = selecionar_categoria()

    if categoria is None:
        return

    #CONFIRMAÇÃO ANTES DE MOVIMENTAR O DINHEIRO
    print("\n--- CONFIRA OS DADOS DO PIX ---")
    print(f"Destinatário: {destino['nome']}")
    print(f"CPF: {mascarar_cpf(cpf_destino)}")
    print(f"Chave: {chave}")
    print(f"Valor: R$ {valor:.2f}")
    print(f"Categoria: {categoria}")
    confirmacao = input("> Confirmar transferência? (s/n): ").strip().lower()

    if confirmacao != 's':
        print("[CANCELADO] Transferência cancelada. Nenhum valor foi movimentado.")
        return

    origem["saldo"] -= valor
    destino["saldo"] += valor
    registrar_movimentacao(origem, "PIX enviado", valor, "saida", categoria)
    registrar_movimentacao(destino, "PIX recebido", valor, "entrada")
    print(f"[SUCESSO] PIX de R$ {valor:.2f} enviado para {destino['nome']}.")
    print(f"[INFO] Novo saldo de {origem['nome']}: R$ {origem['saldo']:.2f}")

#RELATÓRIO DE GASTOS POR CATEGORIA
def relatorio_categoria(cliente):
    gastos_por_categoria = {}
    total_gasto = 0.0
    total_entradas = 0.0

    #PERCORRE O HISTÓRICO E AGRUPA (GROUP BY EM MEMÓRIA)
    for movimentacao in cliente["historico"]:

        if movimentacao["fluxo"] == "entrada":
            total_entradas += movimentacao["valor"]

        elif movimentacao["fluxo"] == "saida":
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
    print(f"Entradas registradas: R$ {total_entradas:.2f}")
    print(f"Total gasto: R$ {total_gasto:.2f}")

    if total_entradas > 0:
        consumo = total_gasto / total_entradas * 100
        print(f"Orçamento consumido: {consumo:.1f}% do que entrou")

    print()

    #DO MAIOR GASTO PARA O MENOR
    ranking = sorted(gastos_por_categoria.items(), key=lambda item: item[1], reverse=True)

    for categoria, valor in ranking:
        percentual = valor / total_gasto * 100
        barra = "#" * int(percentual / 5)
        print(f"{categoria:<15} | R$ {valor:>8.2f} | {percentual:>5.1f}% | {barra}")

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
        #EXIT
        elif opcao == '0':
            print("\nEncerrando o sistema ByteBank. Até logo!")
            break

        else:
            print("\n[ERRO] Opção inválida. Escolha uma das opções do menu.")

if __name__ == "__main__":
    print("Inicializando o Sistema...")
    main()
