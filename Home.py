import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(
    page_title = "Home",
    page_icon = '📊'
)
#--------------------------------------
#Funções
#--------------------------------------
def create_map(dataframe):
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in dataframe.iterrows():

        name = line["restaurant_name"]
        price_for_two = line["average_cost_for_two"]
        cuisine = line["cuisines"]
        currency = line["currency"]
        rating = line["aggregate_rating"]
        color = f'{line["color_name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)

def qty_restaurants(dataframe):
    return dataframe.shape[0]


def qty_countries(dataframe):
    return dataframe.loc[:, "country"].nunique()


def qty_cities(dataframe):
    return dataframe.loc[:, "city"].nunique()


def qty_ratings(dataframe):
    return dataframe.loc[:, "votes"].sum()


def qty_cuisines(dataframe):
    return dataframe.loc[:, "cuisines"].nunique()

def create_sidebar(df):
    image = Image.open("logo.png")

    col1, col2 = st.sidebar.columns([1, 4], gap="small")
    col1.image(image, width=35)
    col2.markdown("# Fome Zero")

    st.sidebar.markdown("## Filtros")

    countries = st.sidebar.multiselect(
        "Escolha os Paises que Deseja visualizar os Restaurantes",
        df2.loc[:, "country"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

    st.sidebar.markdown("### Dados Tratados")
    st.sidebar.download_button(
        label="Download",
        data=df2.to_csv(index=False, sep=";"),
        file_name="data.csv",
        mime="text/csv",
    )
    return list(countries)
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
selected_countries = create_sidebar(df2)

#==================================================
# Layout no Streamlit
#==================================================
st.markdown("# Fome Zero!")

st.markdown("## O Melhor lugar para encontrar seu mais novo restaurante favorito!")

st.markdown("### Temos as seguintes marcas dentro da nossa plataforma:")

restaurants, countries, cities, ratings, cuisines = st.columns(5)

restaurants.metric(
    "Restaurantes Cadastrados",
    qty_restaurants(df2),
)

countries.metric(
    "Países Cadastrados",
    qty_countries(df2),
)

cities.metric(
    "Cidades Cadastrados",
   qty_cities(df2),
)

ratings.metric(
    "Avaliações Feitas na Plataforma",
    f"{qty_ratings(df2):,}".replace(",", "."),
)

cuisines.metric(
    f"Tipos de Culinárias\nOferecidas",
    f"{qty_cuisines(df2):,}",
)

map_df = df2.loc[df2["country"].isin(selected_countries), :]

create_map(map_df)