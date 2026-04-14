import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard de Queimadas", layout="wide", page_icon="🔥")

@st.cache_data
def load_data():
    # Lê o arquivo CSV considerando o separador ; e a codificação correta para acentuação
    df = pd.read_csv('Queimadas.csv', sep=';', encoding='latin1')
    
    # Substitui os traços "-" por 0 e converte as colunas para o tipo numérico
    df['2017'] = pd.to_numeric(df['2017'].replace('-', 0))
    df['2018'] = pd.to_numeric(df['2018'].replace('-', 0))
    df['2019'] = pd.to_numeric(df['2019'].replace('-', 0))
    
    return df

df = load_data()

st.title("🔥 Dashboard de Focos de Queimadas (2017 - 2019)")
st.markdown("Visualização dos focos de queimadas nos municípios (Goiás).")

# Barra lateral para filtros
st.sidebar.header("Filtros")
cidades = st.sidebar.multiselect(
    "Selecione as Localidades:",
    options=df["Localidade"].unique(),
    default=df["Localidade"].unique()[:5]  # Seleciona as primeiras 5 cidades por padrão
)

if not cidades:
    st.warning("Por favor, selecione ao menos uma localidade para exibir os gráficos.")
else:
    # Filtrar dados com base nas cidades selecionadas
    df_filtered = df[df["Localidade"].isin(cidades)]
    
    # Exibir a tabela
    st.subheader("Visualização dos Dados")
    st.dataframe(df_filtered)

    # Preparar dados para os gráficos (derretendo as colunas de ano para as linhas)
    df_melted = df_filtered.melt(
        id_vars=['Localidade', 'Variável'], 
        value_vars=['2017', '2018', '2019'], 
        var_name='Ano', 
        value_name='Número de Focos'
    )

    st.subheader("Análises Gráficas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras
        fig_bar = px.bar(
            df_melted, 
            x="Localidade", 
            y="Número de Focos", 
            color="Ano", 
            barmode="group",
            title="Focos de Queimada por Localidade"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Gráfico de evolução anual
        df_total_ano = df_melted.groupby("Ano")["Número de Focos"].sum().reset_index()
        fig_line = px.line(
            df_total_ano, 
            x="Ano", 
            y="Número de Focos", 
            markers=True,
            title="Evolução Total (Localidades Selecionadas)"
        )
        st.plotly_chart(fig_line, use_container_width=True)
