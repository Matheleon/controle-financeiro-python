# ==========================================
# CONTROLE FINANCEIRO - MAIN.PY
# ==========================================

import json
from datetime import datetime
import os


# ==========================================
# CATEGORIAS PADRONIZADAS
# ==========================================

CATEGORIAS = {
    "1": "Alimentação",
    "2": "Transporte",
    "3": "Aluguel",
    "4": "Contas",
    "5": "Lazer",
    "6": "Outros"
}


# ==========================================
# CARREGAR DADOS
# ==========================================

def carregar_dados():

    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []


# ==========================================
# SALVAR DADOS
# ==========================================

def salvar_dados(dados):

    with open("dados.json", "w", encoding="utf-8") as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# VALIDAR DATA
# ==========================================

def validar_data():

    while True:

        data = input(
            "Digite a data (dd/mm/aaaa): "
        )

        try:
            datetime.strptime(
                data,
                "%d/%m/%Y"
            )

            return data

        except ValueError:
            print(
                "Data inválida."
            )


# ==========================================
# VALIDAR VALOR
# ==========================================

def validar_valor():

    while True:

        try:
            valor = float(
                input(
                    "Digite o valor: R$ "
                )
            )

            if valor <= 0:
                print(
                    "Digite valor maior que zero."
                )
                continue

            return valor

        except ValueError:
            print(
                "Digite um número válido."
            )


# ==========================================
# ESCOLHER CATEGORIA
# ==========================================

def escolher_categoria():

    while True:

        print("\nCategorias:")

        for chave, valor in CATEGORIAS.items():
            print(f"{chave} - {valor}")

        opcao = input(
            "Escolha categoria: "
        )

        if opcao in CATEGORIAS:
            return CATEGORIAS[opcao]

        print("Categoria inválida.")


# ==========================================
# ADICIONAR MOVIMENTAÇÃO
# ==========================================

def adicionar_movimentacao(dados):

    print(
        "\n===== ADICIONAR ====="
    )

    while True:

        tipo = input(
            "Tipo (receita/despesa): "
        ).lower()

        if tipo in [
            "receita",
            "despesa"
        ]:
            break

        print("Tipo inválido.")

    categoria = escolher_categoria()

    valor = validar_valor()

    data = validar_data()

    descricao = input(
        "Descrição: "
    )

    movimentacao = {
        "tipo": tipo,
        "categoria": categoria,
        "valor": valor,
        "data": data,
        "descricao": descricao
    }

    dados.append(
        movimentacao
    )

    salvar_dados(dados)

    print(
        "Movimentação salva!"
    )


# ==========================================
# VER MOVIMENTAÇÕES
# ==========================================

def ver_movimentacoes(dados):

    if not dados:
        print(
            "\nNenhuma movimentação."
        )
        return

    print(
        "\n===== MOVIMENTAÇÕES ====="
    )

    for i, item in enumerate(
        dados,
        start=1
    ):

        print(f"""
{i}

Tipo:
{item["tipo"]}

Categoria:
{item["categoria"]}

Valor:
R$ {item["valor"]:.2f}

Data:
{item["data"]}

Descrição:
{item["descricao"]}
        """)


# ==========================================
# FILTRAR
# ==========================================

def filtrar_movimentacoes(dados):

    if not dados:
        print(
            "Sem dados."
        )
        return

    print("""
1 - Filtrar por categoria
2 - Filtrar por mês
    """)

    opcao = input(
        "Escolha: "
    )

    if opcao == "1":

        categoria = (
            escolher_categoria()
        )

        resultados = [

            item for item in dados

            if item[
                "categoria"
            ] == categoria
        ]

    elif opcao == "2":

        mes = input(
            "Digite mês (MM): "
        )

        resultados = [

            item for item in dados

            if item["data"][3:5]
            == mes
        ]

    else:
        print("Inválido.")
        return

    if not resultados:
        print(
            "Nada encontrado."
        )
        return

    print(
        "\n===== RESULTADOS ====="
    )

    for item in resultados:

        print(item)


# ==========================================
# RESUMO FINANCEIRO
# ==========================================

def resumo_financeiro(dados):

    receitas = sum(

        item["valor"]

        for item in dados

        if item["tipo"]
        == "receita"
    )

    despesas = sum(

        item["valor"]

        for item in dados

        if item["tipo"]
        == "despesa"
    )

    saldo = (
        receitas - despesas
    )

    print(f"""
===== RESUMO =====

Receitas:
R$ {receitas:.2f}

Despesas:
R$ {despesas:.2f}

Saldo:
R$ {saldo:.2f}
    """)


# ==========================================
# ABRIR DASHBOARD
# ==========================================

def abrir_dashboard():

    print(
        "Abrindo dashboard..."
    )

    os.system(
        "python dashboard.py"
    )


# ==========================================
# MENU PRINCIPAL
# ==========================================

def menu():

    dados = carregar_dados()

    while True:

        print("""
======== MENU ========

1 - Adicionar movimentação
2 - Ver movimentações
3 - Filtrar movimentações
4 - Resumo financeiro
5 - Dashboard
6 - Sair
        """)

        opcao = input(
            "Escolha: "
        )

        if opcao == "1":
            adicionar_movimentacao(
                dados
            )

        elif opcao == "2":
            ver_movimentacoes(
                dados
            )

        elif opcao == "3":
            filtrar_movimentacoes(
                dados
            )

        elif opcao == "4":
            resumo_financeiro(
                dados
            )

        elif opcao == "5":
            abrir_dashboard()

        elif opcao == "6":
            print("Saindo...")
            break

        else:
            print(
                "Opção inválida."
            )


# ==========================================
# INICIAR
# ==========================================

if __name__ == "__main__":
    menu()