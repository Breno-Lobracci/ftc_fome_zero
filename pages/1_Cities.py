import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image


st.set_page_config(page_title = 'Cidades', page_icon = '🏙️', layout = 'wide')

#--------------------------------------
#Funções
#--------------------------------------

def top_cities_restaurants(countries):
    grouped_df = (
        df2.loc[df2["country"].isin(countries), ["restaurant_id", "country", "city"]]
        .groupby(["country", "city"])
        .count()
        .sort_values(["restaurant_id", "city"], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(10),
        x="city",
        y="restaurant_id",
        text="restaurant_id",
        text_auto=".2f",
        color="country",
        title="Top 10 Cidades com mais Restaurantes na Base de Dados",
        labels={
            "city": "Cidade",
            "restaurant_id": "Quantidade de Restaurantes",
            "country": "País",
        },
    )

    return fig

def top_best_restaurants(countries):
    grouped_df = (
        df2.loc[
            (df2["aggregate_rating"] >= 4) & (df2["country"].isin(countries)),
            ["restaurant_id", "country", "city"],
        ]
        .groupby(["country", "city"])
        .count()
        .sort_values(["restaurant_id", "city"], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(7),
        x="city",
        y="restaurant_id",
        text="restaurant_id",
        text_auto=".2f",
        color="country",
        title="Top 7 Cidades com Restaurantes com média de avaliação acima de 4",
        labels={
            "city": "Cidade",
            "restaurant_id": "Quantidade de Restaurantes",
            "country": "País",
        },
    )

    return fig



def top_worst_restaurants(countries):
    grouped_df = (
        df2.loc[
            (df2["aggregate_rating"] <= 2.5) & (df2["country"].isin(countries)),
            ["restaurant_id", "country", "city"],
        ]
        .groupby(["country", "city"])
        .count()
        .sort_values(["restaurant_id", "city"], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(7),
        x="city",
        y="restaurant_id",
        text="restaurant_id",
        text_auto=".2f",
        color="country",
        title="Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5",
        labels={
            "city": "Cidade",
            "restaurant_id": "Quantidade de Restaurantes",
            "country": "País",
        },
    )

    return fig

def most_cuisines(countries):
    grouped_df = (
        df2.loc[df2["country"].isin(countries), ["cuisines", "country", "city"]]
        .groupby(["country", "city"])
        .nunique()
        .sort_values(["cuisines", "city"], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(10),
        x="city",
        y="cuisines",
        text="cuisines",
        color="country",
        title="Top 10 Cidades mais restaurantes com tipos culinários distintos",
        labels={
            "city": "Cidades",
            "cuisines": "Quantidade de Tipos Culinários Únicos",
            "country": "País",
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
st.header("🏙️ Visão - Cidades")

with st.container():
        fig = top_cities_restaurants( countries )
        st.plotly_chart(fig , use_container_width = True)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fig = top_best_restaurants( countries )
        st.plotly_chart(fig, use_container_width = True)
    with col2:
        fig = top_worst_restaurants( countries )
        st.plotly_chart(fig, use_container_width = True)
with st.container():
        fig = most_cuisines( countries )
        st.plotly_chart(fig, use_container_width = True)