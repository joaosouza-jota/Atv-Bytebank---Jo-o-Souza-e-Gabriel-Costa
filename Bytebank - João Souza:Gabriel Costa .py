#MENU INICIAL
def exibir_menu():
    print("\n=== ByteBank MVP ===")
    print("[1] Cadastrar Cliente")
    print("[2] Listar Clientes")
    print("[3] Consultar Saldo")
    print("[4] Depositar")
    print("[5] Sacar")
    print("[6] Sair")
    return input("> Digite a operação desejada: ")

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

    clientes[cpf] = {"nome": nome, "saldo": 0.0}
    print(f"[SUCESSO] Cliente {nome} cadastrado com saldo inicial de R$ 0.00.")

#LISTAGEM
def listar_clientes(clientes):
    if not clientes:
        print("\n[AVISO] Nenhum cliente cadastrado até o momento.")
        return

    print("\n=== CLIENTES CADASTRADOS ===")
    for cpf, dados in clientes.items():
        print(f"{dados['nome']} | CPF: {cpf} | Saldo: R$ {dados['saldo']:.2f}")

#LISTAGEM
def selecionar_cliente(clientes):
    if not clientes:
        print("\n[AVISO] Nenhum cliente cadastrado. Cadastre um cliente antes de operar.")
        return None

    cpf = input("\n> CPF do cliente: ").strip()

    if cpf not in clientes:
        print("[ERRO] Cliente não encontrado.")
        return None

    return cpf

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
                print(f"[SALDO] O saldo de {clientes[cpf]['nome']} é: R$ {clientes[cpf]['saldo']:.2f}")
        #DEPÓSITO
        elif opcao == '4':
            cpf = selecionar_cliente(clientes)

            if cpf:
                try:
                    valor_deposito = float(input("> Digite o valor para depósito: R$ "))

                    if valor_deposito > 0:
                        clientes[cpf]["saldo"] += valor_deposito
                        print(f"[SUCESSO] Depósito de R$ {valor_deposito:.2f} na conta de {clientes[cpf]['nome']}.")
                    else:
                        print("[ERRO] O valor de depósito deve ser positivo.")
                except ValueError:
                    print("[ERRO] Por favor, insira um valor numérico válido.")
        #SAQUE
        elif opcao == '5':
            cpf = selecionar_cliente(clientes)

            if cpf:
                try:
                    valor_saque = float(input("> Digite o valor para saque: R$ "))

                    if valor_saque > 0:

                        if valor_saque <= clientes[cpf]["saldo"]:
                            clientes[cpf]["saldo"] -= valor_saque
                            print(f"[SUCESSO] Saque de R$ {valor_saque:.2f} da conta de {clientes[cpf]['nome']}.")
                        else:
                            print("[ERRO] Saldo insuficiente para esta operação.")
                    else:
                        print("[ERRO] O valor de saque deve ser positivo.")
                except ValueError:
                    print("[ERRO] Por favor, insira um valor numérico válido.")
        #EXIT
        elif opcao == '6':
            print("\nEncerrando o sistema ByteBank. Até logo!")
            break

        else:
            print("\n[ERRO] Opção inválida. Escolha uma opção entre 1 e 6.")

if __name__ == "__main__":
    print("Inicializando o Sistema...")
    main()
