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

        with open(
            "dados.json",
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(
                arquivo
            )

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        return []


# ==========================================
# SALVAR DADOS
# ==========================================

def salvar_dados(dados):

    with open(
        "dados.json",
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(

            dados,

            arquivo,

            indent=4,

            ensure_ascii=False
        )


# ==========================================
# ADICIONAR MOVIMENTAÇÃO
# ==========================================

def adicionar_movimentacao(dados):

    print(
        "\n===== ADICIONAR MOVIMENTAÇÃO ====="
    )

    etapa = 1

    tipo = None
    categoria = None
    valor = None
    data = None
    descricao = None

    while True:

        # ==================================
        # ETAPA 1 - TIPO
        # ==================================

        if etapa == 1:

            print("""
===== TIPO =====

1 - Receita
2 - Despesa

v - voltar menu
s - sair
            """)

            entrada = input(
                "Escolha: "
            ).lower()

            if entrada == "v":
                return

            if entrada == "s":

                print(
                    "Operação cancelada."
                )

                return

            if entrada == "1":

                tipo = "receita"

                # receita vai direto
                # para valor
                etapa = 3

            elif entrada == "2":

                tipo = "despesa"

                # despesa precisa
                # escolher categoria
                etapa = 2

            else:

                print(
                    "Opção inválida."
                )

        # ==================================
        # ETAPA 2 - CATEGORIA
        # (SÓ DESPESA)
        # ==================================

        elif etapa == 2:

            print(
                "\n===== CATEGORIAS ====="
            )

            for chave, valor_cat in (
                CATEGORIAS.items()
            ):

                print(
                    f"{chave} - {valor_cat}"
                )

            print("\nv - voltar")
            print("s - sair")

            entrada = input(
                "\nEscolha categoria: "
            ).lower()

            if entrada == "v":

                etapa = 1
                continue

            if entrada == "s":

                print(
                    "Operação cancelada."
                )

                return

            if entrada in CATEGORIAS:

                categoria = (
                    CATEGORIAS[
                        entrada
                    ]
                )

                etapa = 3

            else:

                print(
                    "Categoria inválida."
                )

        # ==================================
        # ETAPA 3 - VALOR
        # ==================================

        elif etapa == 3:

            entrada = input(
                "\nDigite valor "
                "(ou v/s): R$ "
            ).lower()

            if entrada == "v":

                # receita volta
                # para tipo
                if tipo == "receita":
                    etapa = 1

                # despesa volta
                # para categoria
                else:
                    etapa = 2

                continue

            if entrada == "s":

                print(
                    "Operação cancelada."
                )

                return

            try:

                valor = float(
                    entrada
                )

                if valor <= 0:

                    print(
                        "Valor deve ser "
                        "maior que zero."
                    )

                    continue

                etapa = 4

            except ValueError:

                print(
                    "Digite um "
                    "número válido."
                )

        # ==================================
        # ETAPA 4 - DATA
        # ==================================

        elif etapa == 4:

            entrada = input(
                "\nData "
                "(dd/mm/aaaa)"
                " ou v/s: "
            ).lower()

            if entrada == "v":

                etapa = 3
                continue

            if entrada == "s":

                print(
                    "Operação cancelada."
                )

                return

            try:

                datetime.strptime(

                    entrada,

                    "%d/%m/%Y"
                )

                data = entrada

                etapa = 5

            except ValueError:

                print(
                    "Data inválida."
                )

        # ==================================
        # ETAPA 5 - DESCRIÇÃO
        # ==================================

        elif etapa == 5:

            entrada = input(
                "\nDescrição "
                "(ou v/s): "
            )

            if entrada.lower() == "v":

                etapa = 4
                continue

            if entrada.lower() == "s":

                print(
                    "Operação cancelada."
                )

                return

            descricao = entrada

            break

    # ==================================
    # RECEITA NÃO TEM CATEGORIA
    # ==================================

    if tipo == "receita":

        categoria = "Receita"

    # ==================================
    # SALVAR
    # ==================================

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

    salvar_dados(
        dados
    )

    print(
        "\nMovimentação salva "
        "com sucesso!"
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
====================

Movimentação #{i}

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

====================
""")


# ==========================================
# FILTRAR MOVIMENTAÇÕES
# ==========================================

def filtrar_movimentacoes(dados):

    if not dados:

        print(
            "\nSem dados."
        )

        return

    print("""
===== FILTROS =====

1 - Categoria
2 - Mês
3 - Voltar
    """)

    opcao = input(
        "Escolha: "
    )

    # =====================
    # FILTRAR CATEGORIA
    # =====================

    if opcao == "1":

        print(
            "\nCategorias:"
        )

        for chave, categoria in (
            CATEGORIAS.items()
        ):

            print(
                f"{chave} - "
                f"{categoria}"
            )

        categoria_opcao = input(
            "\nEscolha categoria: "
        )

        if categoria_opcao not in (
            CATEGORIAS
        ):

            print(
                "Categoria inválida."
            )

            return

        categoria = (
            CATEGORIAS[
                categoria_opcao
            ]
        )

        resultados = [

            item

            for item in dados

            if item[
                "categoria"
            ] == categoria
        ]

    # =====================
    # FILTRAR MÊS
    # =====================

    elif opcao == "2":

        mes = input(
            "Digite mês (MM): "
        )

        resultados = [

            item

            for item in dados

            if item[
                "data"
            ][3:5] == mes
        ]

    elif opcao == "3":

        return

    else:

        print(
            "Opção inválida."
        )

        return

    # =====================
    # RESULTADOS
    # =====================

    if not resultados:

        print(
            "\nNenhum resultado."
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
===== RESUMO FINANCEIRO =====

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
        "\nAbrindo dashboard..."
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

            print(
                "\nSaindo..."
            )

            break

        else:

            print(
                "\nOpção inválida."
            )


# ==========================================
# INICIAR
# ==========================================

if __name__ == "__main__":

    menu()