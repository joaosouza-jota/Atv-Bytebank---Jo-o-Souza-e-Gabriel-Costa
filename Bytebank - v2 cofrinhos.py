#TAXA DE RENDIMENTO DOS COFRINHOS (0,5% AO MÊS, JUROS SIMPLES)
TAXA_RENDIMENTO = 0.005

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
    print("[0] Sair")
    return input("> Digite a operação desejada: ")

#LEITURA DE VALOR EM DINHEIRO
def ler_valor(mensagem):
    try:
        return float(input(mensagem))
    except ValueError:
        print("[ERRO] Por favor, insira um valor numérico válido.")
        return None

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

    clientes[cpf] = {"nome": nome, "saldo": 0.0, "cofrinhos": {}}
    print(f"[SUCESSO] Cliente {nome} cadastrado com saldo inicial de R$ 0.00.")

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
        print(f"{dados['nome']:<15} | CPF: {cpf} | Saldo: R$ {dados['saldo']:.2f} | Cofrinhos: R$ {guardado:.2f}")

#EXTRATO DO CLIENTE
def exibir_saldo(cliente):
    guardado = total_em_cofrinhos(cliente)

    print(f"\n=== SALDO DE {cliente['nome'].upper()} ===")
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
                valor_deposito = ler_valor("> Digite o valor para depósito: R$ ")

                if valor_deposito is not None:

                    if valor_deposito > 0:
                        clientes[cpf]["saldo"] += valor_deposito
                        print(f"[SUCESSO] Depósito de R$ {valor_deposito:.2f} na conta de {clientes[cpf]['nome']}.")
                    else:
                        print("[ERRO] O valor de depósito deve ser positivo.")
        #SAQUE
        elif opcao == '5':
            cpf = selecionar_cliente(clientes)

            if cpf:
                valor_saque = ler_valor("> Digite o valor para saque: R$ ")

                if valor_saque is not None:

                    if valor_saque > 0:

                        if valor_saque <= clientes[cpf]["saldo"]:
                            clientes[cpf]["saldo"] -= valor_saque
                            print(f"[SUCESSO] Saque de R$ {valor_saque:.2f} da conta de {clientes[cpf]['nome']}.")
                        else:
                            print("[ERRO] Saldo insuficiente para esta operação.")
                    else:
                        print("[ERRO] O valor de saque deve ser positivo.")
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
        #EXIT
        elif opcao == '0':
            print("\nEncerrando o sistema ByteBank. Até logo!")
            break

        else:
            print("\n[ERRO] Opção inválida. Escolha uma das opções do menu.")

if __name__ == "__main__":
    print("Inicializando o Sistema...")
    main()
