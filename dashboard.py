# ==========================================
# DASHBOARD FINANCEIRO - DASHBOARD.PY
# ==========================================

# Biblioteca para trabalhar com tabelas
import pandas as pd

# Biblioteca para criar gráficos
import matplotlib.pyplot as plt

# Biblioteca para trabalhar com datas
from datetime import datetime

# Biblioteca para verificar arquivos
import os


# ==========================================
# CARREGAR DADOS
# ==========================================

def carregar_dados():
    """
    Lê o arquivo dados.json
    e transforma em DataFrame
    """

    try:

        # Lê JSON e converte para tabela
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
        "\n========== TABELA ==========\n"
    )

    print(df)


# ==========================================
# ESTATÍSTICAS
# ==========================================

def mostrar_estatisticas(df):

    print(
        "\n========== ESTATÍSTICAS ==========\n"
    )

    receitas = df[
        df["tipo"] == "receita"
    ]["valor"].sum()

    despesas = df[
        df["tipo"] == "despesa"
    ]["valor"].sum()

    saldo = receitas - despesas

    media = df["valor"].mean()

    maior = df["valor"].max()

    menor = df["valor"].min()

    print(
        f"Receitas: R$ {receitas:.2f}"
    )

    print(
        f"Despesas: R$ {despesas:.2f}"
    )

    print(
        f"Saldo: R$ {saldo:.2f}"
    )

    print(
        f"Média: R$ {media:.2f}"
    )

    print(
        f"Maior movimentação: R$ {maior:.2f}"
    )

    print(
        f"Menor movimentação: R$ {menor:.2f}"
    )


# ==========================================
# FILTRAR DESPESAS
# ==========================================

def apenas_despesas(df):

    return df[
        df["tipo"] == "despesa"
    ]


# ==========================================
# GRÁFICO PIZZA
# ==========================================

def grafico_pizza(df):

    despesas = apenas_despesas(df)

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

    despesas = apenas_despesas(df)

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

    despesas = apenas_despesas(df)

    # transforma texto em data
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
        "Valor Gasto"
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
# EXPORTAR PARA EXCEL
# ==========================================

def exportar_excel(df):

    resposta = input(
        "\nDeseja exportar para Excel? (s/n): "
    ).lower()

    if resposta != "s":
        return

    # gera data/hora
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

    # exporta Excel
    df.to_excel(

        nome_arquivo,

        index=False

    )

    print(
        f"\nArquivo exportado: {nome_arquivo}"
    )


# ==========================================
# MENU DE GRÁFICOS
# ==========================================

def menu_graficos(df):

    while True:

        print("""
========== GRÁFICOS ==========

1 - Pizza
2 - Barras por Categoria
3 - Gastos por Data
4 - Todos
5 - Voltar
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

            grafico_pizza(df)

            grafico_barras(df)

            grafico_data(df)

        elif opcao == "5":
            break

        else:
            print(
                "Opção inválida."
            )


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def iniciar_dashboard():

    # carrega tabela
    df = carregar_dados()

    if df is None:
        return

    # mostra tabela
    mostrar_tabela(df)

    # mostra estatísticas
    mostrar_estatisticas(df)

    # perguntar gráficos
    resposta = input(
        "\nDeseja visualizar gráficos? (s/n): "
    ).lower()

    if resposta == "s":

        menu_graficos(df)

    # perguntar exportação
    exportar_excel(df)

    print(
        "\nDashboard encerrado."
    )


# ==========================================
# INICIAR
# ==========================================

if __name__ == "__main__":

    iniciar_dashboard()