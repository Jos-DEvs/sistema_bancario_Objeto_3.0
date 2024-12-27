import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print(f'{"Saque realizado com sucesso!":=^50}') # Centralizar o texto
            pe_pagina = f"{relogio()} SACAR"
            print(f"{pe_pagina:^50}") # Centralizar o texto
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def validar_cpf(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
        
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    return cliente.contas[0]

# FUNÇÕES #

# Função que gera a data e horas
def relogio():
    data_de_hoje = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    return data_de_hoje

# Função de confirmação da operação
def confirmacao_de_sucesso_da_operacao(status = False, **meu_dict):   
                
    if meu_dict.get("deposito"): # Verifica se "deposito" existe e é True
        print(f'{"Deposito realizado com sucesso!":=^50}') # Centralizar o texto
        pe_pagina = f"{relogio()} DEPOSITAR"
        print(f"{pe_pagina:^50}") # Centralizar o texto
        meu_dict.clear()
    
    elif meu_dict.get("saque"):  # Verifica se "saque" existe e é True
        print(f'{"Saque realizado com sucesso!":=^50}') # Centralizar o texto
        pe_pagina = f"{relogio()} SACAR"
        print(f"{pe_pagina:^50}") # Centralizar o texto
        meu_dict.clear()
    
    elif meu_dict.get("cliente"):  # Verifica se "cliente" existe e é True
        print(f'{"Cadastro realizado com sucesso!":=^50}') # Centralizar o texto
        pe_pagina = f"{relogio()} CADASTRO DO CLIENTE"
        print(f"{pe_pagina:^50}") # Centralizar o texto
        meu_dict.clear()
        
    elif meu_dict.get("conta"):  # Verifica se "conta" existe e é True
        print(f'{"Cadastro realizado com sucesso!":=^50}') # Centralizar o texto
        pe_pagina = f"{relogio()}: CADASTRO DA CONTA"
        print(f"{pe_pagina:^50}") # Centralizar o texto
        meu_dict.clear()
        
    else:
        print("Nenhuma operação identificada.")

# Função para efetuar um depósito
def depositar(clientes):
    cpf_cliente = input("Informe seu CPF (somente número): ")
    cliente = validar_cpf(cpf_cliente, clientes) 

    if not cliente:
        print("Operação falhou! Esse CPF não pertence a nenhum cliente")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
    
    confirmacao_de_sucesso_da_operacao(deposito = True)

# Função para efetuar um saque
def sacar(clientes):
    cpf_cliente = input("Informe o CPF do cliente: ")
    cliente = validar_cpf(cpf_cliente, clientes)

    if not cliente:
        print("Operação falhou! Esse CPF não pertence a nenhum cliente")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função para exibir extrato
def exibir_extrato(clientes):
    cpf_cliente = input("Informe o CPF do cliente: ")
    cliente = validar_cpf(cpf_cliente, clientes)

    if not cliente:
        print("Operação falhou! Esse CPF não pertence a nenhum cliente")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

# Função para criar um cliente
def criar_cliente(clientes):
    cpf_cliente = input("Informe seu CPF (somente número): ")
    cliente = validar_cpf(cpf_cliente, clientes)

    if cliente:
        print("Operação falhou! Esse CPF já pertence a um outro cliente")
        return

    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe seu endereço (logradouro, nro - bairro - cidade/sigla do estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf_cliente, endereco=endereco)

    clientes.append(cliente)

    confirmacao_de_sucesso_da_operacao(cliente = True)

# Função para criar uma conta
def criar_conta(numero_conta, clientes, contas):
    cpf_cliente = input("Informe seu CPF do cliente: ")
    cliente = validar_cpf(cpf_cliente, clientes)

    if not cliente:
        print("Operação falhou! Esse CPF não pertence a nenhum cliente")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    confirmacao_de_sucesso_da_operacao(conta = True)

# Função para listar as contas
def listar_contas(lista_contas):
    if not lista_contas:
        print("-" * 46)
        print("Ainda não foi cadastrada uma conta no sistema.")
        print("-" * 46)
    else:
        print("-" * 35)
    
        for i in lista_contas:
            print(textwrap.dedent(str(i)))     
            #print(f"Agência:\t{i._agencia} \n C/C:\t\t{i._numero} \n Titular:\t{i._cliente}")
            print("-" * 35)


# Função para inicciar o sistema
def main():
    
    lista_clientes = []
    lista_contas = []
    
    while 1 == 1:
        
        # Construir o menu
        print("\n\n")
        print(35 * "-")
        print("Bem-vindo! O que deseja fazer hoje? \n")
        print(" [ncl] Novo Cliente \n [ncc] Nova Conta Corrente \n [ls] Listar Contas \n [d] Depositar\n [s] Sacar \n [e] Extrato \n [q] Sair")

        # Entrada de dados do usuário
        opcao = input("=> ")
        
        # OPeração de criar cliente
        if opcao == "ncl":        
            criar_cliente(lista_clientes)
            
        # Operação de criar uma conta
        elif opcao == "ncc":            
            numero_conta = len(lista_contas) + 1
            criar_conta(numero_conta, lista_clientes, lista_contas)
        
        # Operação de listar contas
        elif opcao =="ls":
            listar_contas(lista_contas)
        
        # Operação de depósito
        elif opcao == "d":
            depositar(lista_clientes) 
            
        # Operação de sacar
        elif opcao =="s":
            sacar(lista_clientes)
            
        # Operação de exibir extratos
        elif opcao =="e":
            exibir_extrato(lista_clientes)
        
        # Sair do aplicativo
        elif opcao == "q":
            print("Até logo!")
            break
                
        else:
            print("Opção inválida, por favor selecione novamente a operação desejada.\n")  

# iniciar o sistema
main()
