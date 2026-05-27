# ==========================================
# DASHBOARD FINANCEIRO - DASHBOARD.PY
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os


# ==========================================
# CARREGAR DADOS
# ==========================================

def carregar_dados():

    try:

        df = pd.read_json(
            "dados.json"
        )

        return df

    except FileNotFoundError:

        print(
            "\nArquivo dados.json não encontrado."
        )

        return None

    except ValueError:

        print(
            "\nArquivo JSON vazio."
        )

        return None


# ==========================================
# MOSTRAR TABELA
# ==========================================

def mostrar_tabela(df):

    print(
        "\n===== MOVIMENTAÇÕES =====\n"
    )

    print(
        df.to_string(
            index=False
        )
    )


# ==========================================
# ESTATÍSTICAS
# ==========================================

def mostrar_estatisticas(df):

    receitas = df[
        df["tipo"] == "receita"
    ]

    despesas = df[
        df["tipo"] == "despesa"
    ]

    total_receitas = receitas[
        "valor"
    ].sum()

    total_despesas = despesas[
        "valor"
    ].sum()

    saldo = (
        total_receitas
        - total_despesas
    )

    maior_receita = (

        receitas["valor"].max()

        if not receitas.empty

        else 0
    )

    maior_despesa = (

        despesas["valor"].max()

        if not despesas.empty

        else 0
    )

    quantidade = len(df)

    print(f"""
===== ESTATÍSTICAS =====

Total de Receitas:
R$ {total_receitas:.2f}

Total de Despesas:
R$ {total_despesas:.2f}

Saldo Atual:
R$ {saldo:.2f}

Maior Receita:
R$ {maior_receita:.2f}

Maior Despesa:
R$ {maior_despesa:.2f}

Quantidade de Movimentações:
{quantidade}
""")


# ==========================================
# APENAS DESPESAS
# ==========================================

def apenas_despesas(df):

    return df[
        df["tipo"]
        == "despesa"
    ]


# ==========================================
# VALIDAR DESPESAS
# ==========================================

def validar_despesas(df):

    despesas = apenas_despesas(df)

    if despesas.empty:

        print(
            "\nNão existem despesas "
            "para gerar gráficos."
        )

        return None

    return despesas


# ==========================================
# GRÁFICO PIZZA
# ==========================================

def grafico_pizza(df):

    despesas = validar_despesas(df)

    if despesas is None:
        return

    gastos_categoria = (

        despesas
        .groupby("categoria")[
            "valor"
        ]
        .sum()

    )

    plt.figure(
        figsize=(8, 6)
    )

    plt.pie(

        gastos_categoria.values,

        labels=
        gastos_categoria.index,

        autopct="%1.1f%%"

    )

    plt.title(
        "Distribuição de Gastos"
    )

    plt.show()


# ==========================================
# GRÁFICO BARRAS
# ==========================================

def grafico_barras(df):

    despesas = validar_despesas(df)

    if despesas is None:
        return

    gastos_categoria = (

        despesas
        .groupby("categoria")[
            "valor"
        ]
        .sum()

    )

    plt.figure(
        figsize=(8, 5)
    )

    plt.bar(

        gastos_categoria.index,

        gastos_categoria.values

    )

    plt.xlabel(
        "Categoria"
    )

    plt.ylabel(
        "Valor Gasto (R$)"
    )

    plt.title(
        "Gastos por Categoria"
    )

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    plt.show()


# ==========================================
# GRÁFICO POR DATA
# ==========================================

def grafico_data(df):

    despesas = validar_despesas(df)

    if despesas is None:
        return

    despesas = despesas.copy()

    despesas["data"] = (
        pd.to_datetime(

            despesas["data"],

            format="%d/%m/%Y"

        )
    )

    gastos_data = (

        despesas
        .groupby("data")[
            "valor"
        ]
        .sum()

    )

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(

        gastos_data.index,

        gastos_data.values

    )

    plt.xlabel(
        "Data"
    )

    plt.ylabel(
        "Gasto (R$)"
    )

    plt.title(
        "Gastos por Data"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    plt.show()


# ==========================================
# EVOLUÇÃO DO SALDO
# ==========================================

def grafico_saldo(df):

    df = df.copy()

    df["data"] = pd.to_datetime(

        df["data"],

        format="%d/%m/%Y"
    )

    df = df.sort_values(
        by="data"
    )

    saldo = 0
    saldos = []

    for _, linha in df.iterrows():

        if linha["tipo"] == "receita":

            saldo += linha["valor"]

        else:

            saldo -= linha["valor"]

        saldos.append(
            saldo
        )

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(

        df["data"],

        saldos
    )

    plt.xlabel(
        "Data"
    )

    plt.ylabel(
        "Saldo (R$)"
    )

    plt.title(
        "Evolução do Saldo"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    plt.show()


# ==========================================
# EXPORTAR EXCEL
# ==========================================

def exportar_excel(df):

    resposta = input(
        "\nDeseja exportar "
        "para Excel? (s/n): "
    ).lower()

    if resposta != "s":
        return

    agora = datetime.now()

    data_exportacao = (
        agora.strftime(
            "%Y-%m-%d_%H-%M"
        )
    )

    nome_arquivo = (

        "relatorio_financeiro_"

        + data_exportacao

        + ".xlsx"
    )

    receitas = df[
        df["tipo"] == "receita"
    ]["valor"].sum()

    despesas = df[
        df["tipo"] == "despesa"
    ]["valor"].sum()

    saldo = (
        receitas - despesas
    )

    resumo = pd.DataFrame({

        "Métrica": [

            "Receitas",
            "Despesas",
            "Saldo"
        ],

        "Valor": [

            receitas,
            despesas,
            saldo
        ]
    })

    with pd.ExcelWriter(
        nome_arquivo
    ) as writer:

        df.to_excel(

            writer,

            sheet_name=
            "Movimentações",

            index=False
        )

        resumo.to_excel(

            writer,

            sheet_name=
            "Resumo",

            index=False
        )

    print(
        f"\nArquivo exportado: "
        f"{nome_arquivo}"
    )
    abrir = input(
        "\nDeseja abrir o arquivo? (s/n): "
    ).lower()

    if abrir == "s":

        os.startfile(
            nome_arquivo
        )

# ==========================================
# MENU GRÁFICOS
# ==========================================

def menu_graficos(df):

    while True:

        print("""
===== GRÁFICOS =====

1 - Pizza
2 - Barras por Categoria
3 - Gastos por Data
4 - Evolução do Saldo
5 - Todos
6 - Voltar
        """)

        opcao = input(
            "Escolha: "
        )

        if opcao == "1":

            grafico_pizza(df)

        elif opcao == "2":

            grafico_barras(df)

        elif opcao == "3":

            grafico_data(df)

        elif opcao == "4":

            grafico_saldo(df)

        elif opcao == "5":

            grafico_pizza(df)
            grafico_barras(df)
            grafico_data(df)
            grafico_saldo(df)

        elif opcao == "6":

            break

        else:

            print(
                "Opção inválida."
            )


# ==========================================
# MENU DASHBOARD
# ==========================================

def iniciar_dashboard():

    df = carregar_dados()

    if df is None:
        return

    while True:

        print("""
===== DASHBOARD =====

1 - Ver Tabela
2 - Estatísticas
3 - Gráficos
4 - Exportar Excel
5 - Voltar
        """)

        opcao = input(
            "Escolha: "
        )

        if opcao == "1":

            mostrar_tabela(df)

        elif opcao == "2":

            mostrar_estatisticas(df)

        elif opcao == "3":

            menu_graficos(df)

        elif opcao == "4":

            exportar_excel(df)

        elif opcao == "5":

            print(
                "\nFechando dashboard..."
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

    iniciar_dashboard()