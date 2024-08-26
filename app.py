import streamlit as st
import pymysql
from sqlalchemy import create_engine
import pandas as pd


# Configuración de la conexión a la base de datos utilizando SQLAlchemy
engine = create_engine('mysql+pymysql://jysparki_admin:Admin2024$!@216.137.190.82/jysparki_jis')

# Configuración de la conexión a la base de datos
connection = pymysql.connect(
    host='216.137.190.82',
    user='jysparki_admin',
    password='Admin2024$',
    db='jysparki_jis',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Función para obtener los meses, año, responsable, status y agregar a un selectbox
def obtener_mes():
    with connection.cursor() as cursor:
        sql = "select mes from DM_Periodos GROUP BY mes"
        cursor.execute(sql)
        results = cursor.fetchall()
    mes_list = [result['mes'] for result in results]
    mes_list.insert(0, "Todos")  # Agregar opción "Todos" al principio de la lista
    return mes_list

def obtener_anio():
    with connection.cursor() as cursor:
        sql = "select `Año` from DM_Periodos GROUP BY `Año`"
        cursor.execute(sql)
        results = cursor.fetchall()
    anio_list = ["Todos"] + [result['Año'] for result in results]
    return anio_list

def obtener_responsable():
    with connection.cursor() as cursor:
        sql = "select names as responsable from QRY_BRANCH_OFFICES where names is not null GROUP BY names "
        cursor.execute(sql)
        results = cursor.fetchall()
    responsable_list = ["Todos"] + [result['responsable'] for result in results]
    return responsable_list

def obtener_status():
    with connection.cursor() as cursor:
        sql = "select `status` FROM statuses where status_id > 17 and status_id < 20"
        cursor.execute(sql)
        results = cursor.fetchall()
    status_list = ["Todos"] + [result['status'] for result in results]
    return status_list


st.header("Reporte de Abonados") 

col1, col2 = st.columns(2)

with col1:
    # Obtener el mes seleccionado por el usuario  
    option_mes = st.selectbox(
    'Seleccionar Mes:', obtener_mes())

    # Obtener el responsable seleccionado por el usuario
    option_responsable = st.selectbox(
    'Seleccionar Responsable:', obtener_responsable())

with col2:
    # Obtener el Año seleccionado por el usuario
    option_anio = st.selectbox(
    'Seleccionar Año:', obtener_anio())

    # Obtener el mes seleccionado por el usuario
    option_status = st.selectbox(
    'Seleccionar Estado:', obtener_status())

# Función para obtener los datos de la tabla ST_DTE_EMITIDOS
def obtener_datos(mes, anio, responsable, status):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM ST_DTE_EMITIDOS"
        if mes != "Todos" and anio != "Todos" and responsable != "Todos" and status != "Todos":
            sql += f" WHERE Mes = '{mes}' and `Año` = '{anio}' and responsable = '{responsable}' and status = '{status}'"
        elif mes != "Todos" and anio != "Todos" and responsable != "Todos":
            sql += f" WHERE Mes = '{mes}' and `Año` = '{anio}' and responsable = '{responsable}'"
        elif mes != "Todos" and status != "Todos" and responsable != "Todos":
            sql += f" WHERE Mes = '{mes}' and status = '{status}' and responsable = '{responsable}'"
        elif anio != "Todos" and status != "Todos" and responsable != "Todos":
            sql += f" WHERE `Año` = '{anio}' and status = '{status}' and responsable = '{responsable}'"
        elif mes != "Todos" and responsable != "Todos":
            sql += f" WHERE Mes = '{mes}' and responsable = '{responsable}'"
        elif anio != "Todos" and responsable != "Todos":
            sql += f" WHERE `Año` = '{anio}' and responsable = '{responsable}'"
        elif status != "Todos" and responsable != "Todos":
            sql += f" WHERE status = '{status}' and responsable = '{responsable}'"
        elif mes != "Todos" and anio != "Todos":
            sql += f" WHERE Mes = '{mes}' and `Año` = '{anio}'"
        elif mes != "Todos" and status != "Todos":
            sql += f" WHERE Mes = '{mes}' and status = '{status}'"
        elif anio != "Todos" and status != "Todos":
            sql += f" WHERE `Año` = '{anio}' and status = '{status}'"
        elif mes != "Todos":
            sql += f" WHERE Mes = '{mes}'"
        elif anio != "Todos":
            sql += f" WHERE `Año` = '{anio}'"
        elif status != "Todos":
            sql += f" WHERE status = '{status}'"
        cursor.execute(sql)
        results = cursor.fetchall()
    df = pd.DataFrame.from_records(results)
    return df


# Obtener los datos de la tabla y mostrarlos en Streamlit
df = obtener_datos(option_mes, option_anio, option_responsable, option_status)


st.markdown("---") 

left_column, right_column = st.columns(2)

# Calcular la suma total de la columna 'amount'
with left_column:
    sum_total = df['amount'].sum()
    st.write(f'Suma total:  {sum_total}')

# Calcular la cantidad de folios
with right_column:
    count_total = df['amount'].count()
    st.write(f'Cantidad total:  {count_total}')
    
st.markdown('---')
st.dataframe(df)







