import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Cuisines", page_icon="🍽️", layout="wide")

#--------------------------------------
#Funções
#--------------------------------------
def top_cuisines():
    cuisines = {
        "Italian": "",
        "American": "",
        "Arabian": "",
        "Japanese": "",
        "Brazilian": "",
    }

    cols = [
        "restaurant_id",
        "restaurant_name",
        "country",
        "city",
        "cuisines",
        "average_cost_for_two",
        "currency",
        "aggregate_rating",
        "votes",
    ]

    for key in cuisines.keys():

        lines = df2["cuisines"] == key

        cuisines[key] = (
            df2.loc[lines, cols]
            .sort_values(["aggregate_rating", "restaurant_id"], ascending=[False, True])
            .iloc[0, :]
            .to_dict()
        )

    return cuisines

def top_restaurants(countries, cuisines, top_n):
    cols = [
        "restaurant_id",
        "restaurant_name",
        "country",
        "city",
        "cuisines",
        "average_cost_for_two",
        "aggregate_rating",
        "votes",
    ]

    lines = (df2["cuisines"].isin(cuisines)) & (df2["country"].isin(countries))

    dataframe = df2.loc[lines, cols].sort_values(
        ["aggregate_rating", "restaurant_id"], ascending=[False, True]
    )

    return dataframe.head(top_n)


def top_best_cuisines(countries, top_n):
    lines = df2["country"].isin(countries)

    grouped_df = (
        df2.loc[lines, ["aggregate_rating", "cuisines"]]
        .groupby("cuisines")
        .mean()
        .sort_values("aggregate_rating", ascending=False)
        .reset_index()
        .head(top_n)
    )

    fig = px.bar(
        grouped_df.head(top_n),
        x="cuisines",
        y="aggregate_rating",
        text="aggregate_rating",
        text_auto=".2f",
        title=f"Top {top_n} Melhores Tipos de Culinárias",
        labels={
            "cuisines": "Tipo de Culinária",
            "aggregate_rating": "Média da Avaliação Média",
        },
    )

    return fig

def top_worst_cuisines(countries, top_n):
    lines = df2["country"].isin(countries)

    grouped_df = (
        df2.loc[lines, ["aggregate_rating", "cuisines"]]
        .groupby("cuisines")
        .mean()
        .sort_values("aggregate_rating")
        .reset_index()
        .head(top_n)
    )

    fig = px.bar(
        grouped_df.head(top_n),
        x="cuisines",
        y="aggregate_rating",
        text="aggregate_rating",
        text_auto=".2f",
        title=f"Top {top_n} Piores Tipos de Culinárias",
        labels={
            "cuisines": "Tipo de Culinária",
            "aggregate_rating": "Média da Avaliação Média",
        },
    )

    return fig
#--------------------------------------
# Import Dataset
#--------------------------------------
df_raw = pd.read_csv('data/processed/data.csv')
#--------------------------------------
# Criando uma copia
#--------------------------------------
df2 = df_raw.copy()
#==================================================
# Barra Lateral
#==================================================
st.sidebar.markdown("## Filtros")

countries = st.sidebar.multiselect(
    "Escolha os Paises que Deseja visualizar as Informações",
    df2.loc[:, "country"].unique().tolist(),
    default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
)

top_n = st.sidebar.slider(
    "Selecione a quantidade de Restaurantes que deseja visualizar", 1, 20, 10
)

cuisines = st.sidebar.multiselect(
    "Escolha os Tipos de Culinária ",
    df2.loc[:, "cuisines"].unique().tolist(),
    default=[
        "Home-made",
        "BBQ",
        "Japanese",
        "Brazilian",
        "Arabian",
        "American",
        "Italian",
    ],
)

#==================================================
# Layout no Streamlit
#==================================================
st.header("🏙️ Visão - Tipos Culinários")
st.markdown(f"## Melhores Restaurantes dos Principais tipos Culinários")
cuisines = top_cuisines()

italian, american, arabian, japonese, brazilian = st.columns(len(cuisines))

with italian:
    st.metric(
        label=f'Italiana: {cuisines["Italian"]["restaurant_name"]}',
        value=f'{cuisines["Italian"]["aggregate_rating"]}/5.0',
        help=f"""
        País: {cuisines["Italian"]['country']}\n
        Cidade: {cuisines["Italian"]['city']}\n
        Média Prato para dois: {cuisines["Italian"]['average_cost_for_two']} ({cuisines["Italian"]['currency']})
        """,
    )

with american:
    st.metric(
        label=f'Italiana: {cuisines["American"]["restaurant_name"]}',
        value=f'{cuisines["American"]["aggregate_rating"]}/5.0',
        help=f"""
        País: {cuisines["American"]['country']}\n
        Cidade: {cuisines["American"]['city']}\n
        Média Prato para dois: {cuisines["American"]['average_cost_for_two']} ({cuisines["American"]['currency']})
        """,
    )

with arabian:
    st.metric(
        label=f'Italiana: {cuisines["Arabian"]["restaurant_name"]}',
        value=f'{cuisines["Arabian"]["aggregate_rating"]}/5.0',
        help=f"""
        País: {cuisines["Arabian"]['country']}\n
        Cidade: {cuisines["Arabian"]['city']}\n
        Média Prato para dois: {cuisines["Arabian"]['average_cost_for_two']} ({cuisines["Arabian"]['currency']})
        """,
    )

with japonese:
    st.metric(
        label=f'Italiana: {cuisines["Japanese"]["restaurant_name"]}',
        value=f'{cuisines["Japanese"]["aggregate_rating"]}/5.0',
        help=f"""
        País: {cuisines["Japanese"]['country']}\n
        Cidade: {cuisines["Japanese"]['city']}\n
        Média Prato para dois: {cuisines["Japanese"]['average_cost_for_two']} ({cuisines["Japanese"]['currency']})
        """,
    )

with brazilian:
    st.metric(
        label=f'Italiana: {cuisines["Brazilian"]["restaurant_name"]}',
        value=f'{cuisines["Brazilian"]["aggregate_rating"]}/5.0',
        help=f"""
        País: {cuisines["Brazilian"]['country']}\n
        Cidade: {cuisines["Brazilian"]['city']}\n
        Média Prato para dois: {cuisines["Brazilian"]['average_cost_for_two']} ({cuisines["Brazilian"]['currency']})
        """,
    )

with st.container():
    df_restaurants = top_restaurants(countries, cuisines, top_n)
    st.markdown(f"## Top {top_n} Restaurantes")
    st.dataframe(df_restaurants)

    best, worst = st.columns(2)
    with best:
        fig = top_best_cuisines(countries, top_n)
        st.plotly_chart(fig, use_container_width=True)
    with worst:
        fig = top_worst_cuisines(countries, top_n)

        st.plotly_chart(fig, use_container_width=True)
    
    
    