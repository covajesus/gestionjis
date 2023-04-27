import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import locale
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots



# Establecer la configuración regional
locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')

# Configuración de la conexión a la base de datos utilizando SQLAlchemy
engine = create_engine('mysql+pymysql://jysparki_jis:Jis2020!@103.72.78.28/jysparki_jis') 


# # Configuración de la conexión a la base de datos
# connection = pymysql.connect(
#     host='103.72.78.28',
#     user='jysparki_jis',
#     password='Jis2020!',
#     db='jysparki_jis',
#     charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor
# )

st.header("Reporte de Ventas") 
st.markdown("---") 


# Crear la consulta con la sintaxis de SQLAlchemy y obtener los resultados como un DataFrame de Pandas
query_actual = text("""
SELECT
    DAY(date) as dia,
    'actual' as Version,
	SUM(DASH_INGRESOS_ACUMULADO_ACTUAL.ticket_number) AS ticket_number, 
	SUM(DASH_INGRESOS_ACUMULADO_ACTUAL.Ingresos) AS Ingresos_actual, 	
	SUM(DASH_INGRESOS_ACUMULADO_ACTUAL.Ingresos_SSS) AS Ingresos_SSS_actual
FROM
	DASH_INGRESOS_ACUMULADO_ACTUAL
	GROUP BY
	DASH_INGRESOS_ACUMULADO_ACTUAL.date
""")

# Ejecutar la consulta a través del motor
with engine.connect() as conn:
    df_actual = pd.read_sql(query_actual, conn)


query_anterior = """
SELECT
    DAY(date) as dia,
    'Anterior' as Version,
	SUM(ticket_number) AS ticket_number,
	SUM(Ingresos) AS Ingresos_anterior,
	SUM(Ingresos_SSS) AS Ingresos_SSS_anterior
FROM
	DASH_INGRESOS_ACUMULADO_ANTERIOR
	GROUP BY
	date
"""
df_anterior = pd.read_sql(query_anterior, engine)


query_ppto = """
SELECT
    DAY(date) as dia,
	date, 
	SUM(ppto) AS ppto
FROM
	DASH_INGRESOS_ACUMULADO_PPTO
	GROUP BY
	date
"""
df_ppto = pd.read_sql(query_ppto, engine)


query_evo_actual = """
SELECT
	MONTH(date)as mes,
	sum(DASH_INGRESOS_ACTUAL.ticket_number) as ticket_number, 
	sum(DASH_INGRESOS_ACTUAL.Venta_Neta) as Venta_Neta, 
	sum(DASH_INGRESOS_ACTUAL.Ingresos) as Ingresos_actual, 
	sum(DASH_INGRESOS_ACTUAL.Venta_SSS) as Venta_SSS, 
	sum(DASH_INGRESOS_ACTUAL.Ingresos_SSS) as Ingresos_SSS_actual
FROM
	DASH_INGRESOS_ACTUAL
GROUP BY MONTH(date)
"""
df_evo_actual = pd.read_sql(query_evo_actual, engine)


query_evo_anterior = """
SELECT
	MONTH(date)as mes,
	sum(DASH_INGRESOS_ANTERIOR.ticket_number) as ticket_number, 
	sum(DASH_INGRESOS_ANTERIOR.Venta_Neta) as Venta_Neta, 
	sum(DASH_INGRESOS_ANTERIOR.Ingresos) as Ingresos_anterior, 
	sum(DASH_INGRESOS_ANTERIOR.Venta_SSS) as Venta_SSS, 
	sum(DASH_INGRESOS_ANTERIOR.Ingresos_SSS) as Ingresos_SSS_anterior
FROM
	DASH_INGRESOS_ANTERIOR
GROUP BY MONTH(date)
"""
df_evo_anterior = pd.read_sql(query_evo_anterior, engine)


query_evo_ppto = """
SELECT
	MONTH(date)as mes,
	sum(DASH_INGRESOS_PPTO.ppto) as Ingresos_ppto
FROM
	DASH_INGRESOS_PPTO
GROUP BY MONTH(date)
"""
df_evo_ppto = pd.read_sql(query_evo_ppto, engine)

# Cerrar la conexión a la base de datos
engine.dispose()




# Calcular la sumatoria de la columna "Ingresos_actual"
ingresos_actual_sum = df_actual["Ingresos_actual"].sum()

# Calcular la sumatoria de la columna "ticket_number"
ticket_actual_sum = df_actual["ticket_number"].sum()

# Calcular la sumatoria de la columna "Ingresos_anterior"
ingresos_anterior_sum = df_anterior["Ingresos_anterior"].sum()

# Calcular la sumatoria de la columna "Ingresos_ppto"
ingresos_ppto_sum = df_ppto["ppto"].sum()

# Calcular la sumatoria de la columna "Ingresos_sss_actual"
ingresos_actual_SSS_sum = df_actual["Ingresos_SSS_actual"].sum()

# Calcular la sumatoria de la columna "Ingresos_sss_anterior"
ingresos_anterior_SSS_sum = df_anterior["Ingresos_SSS_anterior"].sum()



# Crear 3 columnas
uno_column, dos_column, tres_column = st.columns(3)


# muestra los totales Acumulado Actual mes
with uno_column:
    st.metric(label="Actual", value=locale.currency(ingresos_actual_sum, grouping=True))

# muestra los totales Acumulado Anterior mes
with dos_column:
    # Mostrar la sumatoria en Streamlit
    st.metric(label="Año Anterior", value=locale.currency(ingresos_anterior_sum, grouping=True))

# muestra los totales Acumulado Ppto mes
with tres_column:
    # Mostrar la sumatoria en Streamlit
    st.metric(label="Presupuesto", value=locale.currency(ingresos_ppto_sum, grouping=True))

# Crear 3 columnas
cuatro_column, cinco_column, seis_column = st.columns(3)

# muestra Variacion SSS Acumulado mes
with cuatro_column:
    # Mostrar la sumatoria en Streamlit
    st.metric(label="VAR %", value=(round(float((float(ingresos_actual_SSS_sum) / float(ingresos_anterior_SSS_sum) - 1) * 100),2)))

# muestra Desviacion % Acumulado mes
with cinco_column:
    # Mostrar la sumatoria en Streamlit
    st.metric(label="DESV %", value=(round(float((float(ingresos_actual_sum) / float(ingresos_ppto_sum) - 1) * 100),2)))

# muestra Ticket Promedio Acumulado mes    
with seis_column:
    # Mostrar la sumatoria en Streamlit
    st.metric(label="Ticket Promedio", value=locale.currency((float(ingresos_actual_sum) / float(ticket_actual_sum)) , grouping=True))

# Crear 3 columnas
siete_column, ocho_column, nueve_column = st.columns(3)

# muestra Ticket Pagados Acumulado mes
with siete_column:
    # Mostrar la sumatoria en Streamlit
    st.metric(label="Ticket Pagados", value=locale.currency(ticket_actual_sum , grouping=True))

# muestra total Visitas Acumulado mes
with ocho_column:
    # Mostrar la sumatoria en Streamlit
    st.metric(label="Visitas", value=locale.currency((ticket_actual_sum *3) , grouping=True)) 

# muestra Cantidad de Sucursales Mes
with nueve_column:
    # Mostrar la sumatoria en Streamlit
    st.metric(label="Sucursales", value="65")
    

#st.markdown("---")

# Unir los dataframes por la columna "dia"
#df_union = df_actual.merge(df_anterior, on="dia", how="outer").merge(df_ppto, on="dia", how="outer")

## Seleccionar las columnas que queremos mostrar y renombrarlas
#df_union = df_union[["dia", "Ingresos_actual", "Ingresos_anterior", "ppto"]]
#df_union = df_union.rename(columns={"Ingresos_actual": "Actual", "Ingresos_anterior": "Anterior"})


## Unir los dataframes evo por la columna "mes"
df_union_evo = df_evo_actual.merge(df_evo_anterior, on="mes", how="outer").merge(df_evo_ppto, on="mes", how="outer")

## Seleccionar las columnas que queremos mostrar y renombrarlas
df_union_evo = df_union_evo[["mes", "Ingresos_actual", "Ingresos_anterior", "Ingresos_ppto", "Ingresos_SSS_actual", "Ingresos_SSS_anterior"]]
df_union_evo = df_union_evo.rename(columns={"Ingresos_actual": "Actual_E", "Ingresos_anterior": "Anterior_E", "Ingresos_ppto": "Ppto_E", "Ingresos_SSS_actual": "SSS_actual" , "Ingresos_SSS_anterior": "SSS_anterior"})


varsss = (round(float((float(ingresos_actual_SSS_sum) / float(ingresos_anterior_SSS_sum) - 1) * 100),2))
print(varsss)

#agregar la columna varSSS =(round(float((float(ingresos_actual_SSS_sum) / float(ingresos_anterior_SSS_sum) - 1) * 100),2)))
# y luego agregar al dataframe
#st.dataframe(df_union_evo)


# st.markdown("---")

# # Crear la figura del gráfico de barras
# fig = go.Figure(data=[
#     go.Bar(name='Actual', x=df_union['dia'], y=df_union['Actual']),
#     go.Bar(name='Anterior', x=df_union['dia'], y=df_union['Anterior']),
#     go.Bar(name='Ppto', x=df_union['dia'], y=df_union['ppto'])
# ])

# # Configurar el diseño del gráfico
# fig.update_layout(barmode='group', xaxis_title='Día', yaxis_title='Ingresos Acumulados')

# # Mostrar el gráfico en Streamlit
# st.plotly_chart(fig)

st.markdown("---")

# Guarda la posicion del mes a reemplazar
mes_pos = datetime.datetime.now().month

df_nuevo = df_union_evo
df_nuevo.loc[mes_pos -1, ['mes', "Actual_E", "Anterior_E", "Ppto_E", "SSS_actual", "SSS_anterior"]] = [mes_pos, ingresos_actual_sum, ingresos_anterior_sum, ingresos_ppto_sum, ingresos_actual_SSS_sum, ingresos_anterior_SSS_sum]
df_nuevo = df_nuevo.sort_values(by=['mes'], ignore_index=True)

st.dataframe(df_nuevo)

# Crear la figura del gráfico de barras evolutivo
fig_evo = go.Figure(data=[
    go.Bar(name='Actual', x=df_nuevo['mes'], y=df_nuevo['Actual_E']),
    go.Bar(name='Anterior', x=df_nuevo['mes'], y=df_nuevo['Anterior_E']),
    go.Bar(name='Ppto', x=df_nuevo['mes'], y=df_nuevo['Ppto_E']),
	#go.Bar(name='varsss', x=df_nuevo['mes'], y=df_nuevo['varsss'])
])

# Configurar el diseño del gráfico
fig_evo.update_layout(barmode='group', xaxis_title='mes', yaxis_title='Ingresos Evolutivo')

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_evo)


st.markdown("---")
# Definir los datos
x  = df_nuevo['mes']
y1 = df_nuevo['Actual_E']
y2 = df_nuevo['Anterior_E']
y3 = df_nuevo['Ppto_E']
y9 = df_nuevo['SSS_anterior']

# Crear la figura del gráfico con dos ejes
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Agregar la barra al eje primario en la trama principal
fig.add_bar(x=x, y=y1, name='Ingresos actual', marker=dict(color='#F78F1E'))

# Agregar la línea al eje secundario en la trama secundaria
fig.add_trace(go.Scatter(x=x, y=y9, name='PPTO', line=dict(color='#5D5C5C')), secondary_y=True)

# Actualizar el diseño de la figura
fig.update_layout(title='Ingresos', xaxis_title='mes', yaxis_title='Ingresos', legend=dict(x=0, y=1, traceorder="normal"))

# Mostrar la figura
fig.show()




