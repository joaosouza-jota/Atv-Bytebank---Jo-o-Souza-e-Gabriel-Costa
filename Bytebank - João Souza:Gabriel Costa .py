#MENU INICIAL
def exibir_menu():
    print("\n=== ByteBank MVP ===")
    print("[1] Consultar Saldo")
    print("[2] Depositar")
    print("[3] Sacar")
    print("[4] Sair")
    return input("> Digite a operação desejada: ")

#CAIXA
def main():
    saldo = 0.0

    while True:
        opcao = exibir_menu()
        #CONSULTAR SALDO
        if opcao == '1':
            print(f"\n[SALDO] Seu saldo atual é: R$ {saldo:.2f}")
        #DEPÓSITO  
        elif opcao == '2':
            try:
                valor_deposito = float(input("\n> Digite o valor para depósito: R$ "))
                
                if valor_deposito > 0:
                    saldo += valor_deposito
                    print(f"[SUCESSO] Depósito de R$ {valor_deposito:.2f} realizado.")
                else:
                    print("[ERRO] O valor de depósito deve ser positivo.")
            except ValueError:
                print("[ERRO] Por favor, insira um valor numérico válido.")
        #SAQUE        
        elif opcao == '3':
            try:
                valor_saque = float(input("\n> Digite o valor para saque: R$ "))
                
                if valor_saque > 0:
                    
                    if valor_saque <= saldo:
                        saldo -= valor_saque
                        print(f"[SUCESSO] Saque de R$ {valor_saque:.2f} realizado.")
                    else:
                        print("[ERRO] Saldo insuficiente para esta operação.")
                else:
                    print("[ERRO] O valor de saque deve ser positivo.")
            except ValueError:
                print("[ERRO] Por favor, insira um valor numérico válido.")
        #EXIT        
        elif opcao == '4':
            print("\nEncerrando o sistema ByteBank. Até logo!")
            break
            
        else:
            print("\n[ERRO] Opção inválida. Escolha uma opção entre 1 e 4.")

if __name__ == "__main__":
    print("Inicializando o Sistema...")
    main()
