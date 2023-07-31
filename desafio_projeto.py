menu = f'''{'Bem vindo ao SeuBanco.'.center(60, "=")}
Digite os valores referentes à opção que você deseja fazer:
[1] - Criar Usuário
[2] - Criar Conta Corrente
[3] - Depósito
[4] - Saque
[5] - Extrato
[6] - Sair
--> '''
balance = 0
statement = ""
WITHDRAWAL_QUANTITY_LIMIT = 3
WITHDRAWAL_VALUE_LIMIT = 500
daily_draft = 0
users = {}
accounts = {}
count_account = 1
AGENCY = "0001" 

def exit_option():
    print("\nAté a próxima")

def user_option(users):
    print(" Cadastro de usuário ".center(50, "="))

    cpf = str(input("Digite seu CPF: "))
    if cpf not in users and cpf != "":
        name = str(input("Digite seu nome: ")).title()
        date_birth = str(input("Digite a data do seu nascimento: "))
        address = str(input('Digite seu endereço, seguindo o exemplo: "Logradouro, Numero, Bairro, Cidade/sigla do estado": '))
    
        users[cpf] = {"name":name, "date_birth":date_birth, "address":address, "accounts": {}} 

        print("\033[32m") # Green
        print(f"Usuário {users[cpf]['name']} adicionado com sucesso")
        print("\033[0m") # Reset
    else:
        print("\033[31m") # Red
        print(f"CPF já cadastrado no usuário {users[cpf]['name']}. Tente novamente com outro CPF")
        print("\033[0m") # Reset

    return users

def account_option(count_account, users):
    print(" Cadastro de conta corrente ".center(50, "="))
    
    cpf = str(input("Digite o CPF do usuário que você deseja criar a conta: "))

    if cpf not in users:
        print("\033[31m") # Red
        print(f"O CPF digitado, não foi encontrado. Tente novamente com outro CPF")
        print("\033[0m") # Reset        
    else:
        number_account = str(f"{count_account:0>4}")
        count_account += 1
        accounts[number_account] = {"agency": AGENCY, "cpf": cpf, "name": users[cpf]["name"]}
        users[cpf]["accounts"][number_account] = {"agency": AGENCY} 

        print("\033[32m") # Green
        print(f"Conta corrente {number_account} adicionada e vinculada ao usuário: {users[cpf]['name']} de CPF: {cpf}")
        print("\033[0m") # Reset

    return count_account, accounts,  users

def deposit_option(balance, statement, /): 
    deposit = float(input("\nDigite o valor do seu depósito: "))

    if deposit <= 0:
        print("\033[31m")  # Red
        print("\nQuantidade inválida. Depósito não pode ser menor ou igual a zero!\n")
        print("\033[0m")  # Reset
    else:
        balance += deposit
        statement += f"Depósito de R${deposit:.2f}\n"
        print("\033[32m")  # Green
        print("Depósito Efetuado com sucesso!")
        print("\033[0m")  # Reset
    return balance, statement

def draft_option(*, balance, statement, daily_draft, ):
    draft = float(input("Digite o valor que deseja sacar: "))

    if draft <= 0:
        print("\033[31m")  # Red
        print("\nQuantidade inválida. Saque não pode ser menor ou igual a zero!\n")
        print("\033[0m")  # Reset

    else:
        if draft > balance:
            print("\033[31m")  # Red
            print(
                f"\nO valor informado para saque é maior que o saldo atual da sua conta.\nSaldo atual = R${balance:.2f}\n")
            print("\033[0m")  # Reset

        elif draft <= balance:
            if draft <= WITHDRAWAL_VALUE_LIMIT:
                if daily_draft != WITHDRAWAL_QUANTITY_LIMIT:
                    balance -= draft
                    statement += f"Saque de R${draft:.2f}\n"
                    print("\033[32m")  # Green
                    print("Saque efetuado com sucesso!")
                    print("\033[0m")  # Reset
                    daily_draft += 1
                else:
                    print("\033[31m")  # Red
                    print(
                        f"\nVocê excedeu o limite de saques por hoje, volte amanhã\n")
                    print("\033[0m")  # Reset
            else:
                print("\033[31m")  # Red
                print(f"\nVocê excedeu o limite de R$ 500,00 por saque.\n")
                print("\033[0m")  # Reset
    return balance, statement, daily_draft

def statement_option(balance, /,*, statement):
        print(
        f"\nNão foram realizadas movimentações de saldo\nSaldo atual: R${balance}\n" if not statement else f"\n"," O extrato da sua conta é: ".center(50, "="),f"\n{statement}\nSaldo atual: R${balance}\n","=" * 50, sep="")

while True:

    option = str(input(menu))

    # The user chose to leave
    if option == "6":
        exit_option()
        break

    elif option == "1":
        users = user_option(users)

    elif option == "2":
        count_account, accounts, users = account_option(count_account, users)

    # The user chose to deposit
    elif option == "3":
        balance, statement = deposit_option(balance, statement)

    # The user chose to draft
    elif option == "4":
       balance, statement, daily_draft = draft_option(balance=balance, statement=statement, daily_draft=daily_draft)

    elif option == "5":
        statement_option(balance, statement=statement)

    else:
        print("\nOpção inválida. Tente novamente.\n")
