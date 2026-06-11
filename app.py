import streamlit as st
import pandas as pd
import gdown
import os
import numpy as np
st.title("Análisis de Transacciones de Tarjetas de Crédito")
st.write("Este es un análisis de las transacciones de tarjetas de crédito utilizando Streamlit.")
CSV_PATH = "credit_card_transactions.csv"
FILE_ID = "1TfgsRgXStBjNbWer0ZQ9Zki0vycBVlVp"

if not os.path.exists(CSV_PATH):
    gdown.download(id=FILE_ID, output=CSV_PATH, quiet=False)

df = pd.read_csv(CSV_PATH)
st.dataframe(df.head())
st.write(df.shape)
st.write(df.describe())
st.subheader("Valores faltantes")
st.write(df.isnull().sum())
st.metric("Total Transacciones", len(df))
st.metric("Monto Total", f"$ {df['amt'].sum():,.2f}")
import plotly.express as px
fig = px.histogram(df, x="amt")
st.plotly_chart(fig)
import plotly.express as px 
st.subheader("Distribución de Montos") 
fig = px.histogram(df, x="amt", nbins=50, title= "Distribución de montos de transacciones") 
st.plotly_chart(fig)
st.subheader("Top Categorías") 
categoria = (df["category"].value_counts().head(10).reset_index()) 
categoria.columns = ["Categoria", "Cantidad"] 
fig = px.bar(categoria, x="Categoria", y="Cantidad") 
st.plotly_chart(fig)
st.subheader("Monto Total por Categoría")

montos = (
    df.groupby("category")["amt"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    montos,
    x="category",
    y="amt"
)

st.plotly_chart(fig)
st.subheader("Fraudes por Categoría")

fraudes = (
    df[df["is_fraud"] == 1]
    .groupby("category")
    .size()
    .sort_values(ascending=False)
    .reset_index(name="fraudes")
)

fig = px.bar(
    fraudes,
    x="category",
    y="fraudes"
)

st.plotly_chart(fig)
st.subheader("Transacciones por Género")

fig = px.pie(
    df,
    names="gender"
)

st.plotly_chart(fig)
df["trans_date_trans_time"] = pd.to_datetime(
    df["trans_date_trans_time"]
)

df["mes"] = (
    df["trans_date_trans_time"]
    .dt.to_period("M")
    .astype(str)
)

mensual = (
    df.groupby("mes")
    .size()
    .reset_index(name="transacciones")
)

fig = px.line(
    mensual,
    x="mes",
    y="transacciones"
)

st.plotly_chart(fig)
st.header("Indicadores Principales") 
col1, col2, col3, col4 = st.columns(4) 
with col1: st.metric("Total Transacciones", f"{len(df):,}") 
with col2: st.metric("Monto Total", f"$ {df['amt'].sum():,.2f}") 
with col3: st.metric("Ticket Promedio", f"$ {df['amt'].mean():,.2f}") 
with col4: fraude_pct = df ['is_fraud'].mean()*100 
st.metric("% Fraude", f"{fraude_pct:.2f}%")
# Indicadores para conclusiones automáticas

total_transacciones = len(df)

monto_total = df["amt"].sum()

ticket_promedio = df["amt"].mean()

porcentaje_fraude = (df["is_fraud"].mean()) * 100

categoria_top = df["category"].value_counts().idxmax()

cantidad_categoria_top = df["category"].value_counts().max()

categoria_mayor_monto = (
    df.groupby("category")["amt"]
    .sum()
    .idxmax()
)

monto_categoria_mayor = (
    df.groupby("category")["amt"]
    .sum()
    .max()
)
st.header("Conclusiones")
st.info(
    f"""
    1. El dataset contiene un total de {total_transacciones:,} transacciones,
    proporcionando una muestra amplia para el análisis del comportamiento de los usuarios.
    """
)

st.info(
    f"""
    2. La categoría con mayor cantidad de operaciones es '{categoria_top}',
    registrando {cantidad_categoria_top:,} transacciones.
    """
)

st.info(
    f"""
    3. El monto total procesado en el conjunto de datos asciende a
    ${monto_total:,.2f}, con un ticket promedio de
    ${ticket_promedio:,.2f} por transacción.
    """
)

st.info(
    f"""
    4. La categoría que genera el mayor volumen económico es
    '{categoria_mayor_monto}', acumulando aproximadamente
    ${monto_categoria_mayor:,.2f}.
    """
)

st.info(
    f"""
    5. La tasa de fraude observada es de {porcentaje_fraude:.2f}%,
    lo que evidencia la necesidad de mantener controles y mecanismos
    de monitoreo para prevenir operaciones fraudulentas.
    """
)
st.success(f"✅ Total de transacciones analizadas: {total_transacciones:,}")

st.success(f"✅ Monto total procesado: ${monto_total:,.2f}")

st.success(f"✅ Ticket promedio: ${ticket_promedio:,.2f}")

st.warning(
    f"⚠️ Tasa de fraude detectada: {porcentaje_fraude:.2f}%"
)

st.success(
    f"✅ Categoría con más transacciones: {categoria_top}"
)

st.success(
    f"✅ Categoría con mayor monto acumulado: {categoria_mayor_monto}"
)

 