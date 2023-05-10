import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Countries", page_icon="🌍", layout="wide")

#--------------------------------------
#Funções
#--------------------------------------
def countries_restaurants(countries):
    grouped_df = (
        df2.loc[df2["country"].isin(countries), ["restaurant_id", "country"]]
        .groupby("country")
        .count()
        .sort_values("restaurant_id", ascending=False)
        .reset_index()
    )

    fig = px.bar(
        grouped_df,
        x="country",
        y="restaurant_id",
        text="restaurant_id",
        title="Quantidade de Restaurantes Registrados por País",
        labels={
            "country": "Paises",
            "restaurant_id": "Quantidade de Restaurantes",
        },
    )

    return fig


def countries_cities(countries):
    grouped_df = (
        df2.loc[df2["country"].isin(countries), ["city", "country"]]
        .groupby("country")
        .nunique()
        .sort_values("city", ascending=False)
        .reset_index()
    )

    fig = px.bar(
        grouped_df,
        x="country",
        y="city",
        text="city",
        title="Quantidade de Cidades Registrados por País",
        labels={
            "country": "Paises",
            "city": "Quantidade de Cidades",
        },
    )

    return fig


def countries_mean_votes(countries):
    grouped_df = (
        df2.loc[df2["country"].isin(countries), ["votes", "country"]]
        .groupby("country")
        .mean()
        .sort_values("votes", ascending=False)
        .reset_index()
    )

    fig = px.bar(
        grouped_df,
        x="country",
        y="votes",
        text="votes",
        text_auto=".2f",
        title="Média de Avaliações feitas por País",
        labels={
            "country": "Paises",
            "votes": "Quantidade de Avaliações",
        },
    )

    return fig


def countries_average_plate(countries):
    grouped_df = (
        df2.loc[df2["country"].isin(countries), ["average_cost_for_two", "country"]]
        .groupby("country")
        .mean()
        .sort_values("average_cost_for_two", ascending=False)
        .reset_index()
    )

    fig = px.bar(
        grouped_df,
        x="country",
        y="average_cost_for_two",
        text="average_cost_for_two",
        text_auto=".2f",
        title="Média de Preço de um prato para duas pessoas por País",
        labels={
            "country": "Paises",
            "average_cost_for_two": "Preço de prato para duas Pessoas",
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
#==================================================
# Layout no Streamlit
#==================================================

st.header("🌍 Visão - Países")
with st.container():
        fig = countries_restaurants(countries)
        st.plotly_chart(fig , use_container_width = True)
with st.container():
        fig = countries_cities(countries)
        st.plotly_chart(fig , use_container_width = True)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fig = countries_mean_votes(countries)
        st.plotly_chart(fig, use_container_width = True)
    with col2:
        fig = countries_average_plate(countries)
        st.plotly_chart(fig, use_container_width = True)