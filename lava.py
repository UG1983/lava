import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.


import pandas as pd
import math
import altair as alt



st.set_page_config(
    page_title="Listado de lavadoras",
    #page_icon="🧊",
    #layout="wide",
    initial_sidebar_state="expanded",
    )


data = pd.read_csv("Lavadoras.csv", header=0)

lista_marcas = data.sort_values('Marca')['Marca'].unique().tolist()

#st.title('Encuentra la mejor lavadora calidad / precio')
st.title('Encuentra tu lavadora con la mejor relación calidad - precio')
#st.header('Usa los filtros de tu izquierda para encontrar la lavadora que mejor se adapte a tus necesidades')



lista_kg = data['Kg'].unique().tolist()
lista_kg.sort()
#lista_kg 

lista_Vel = data['Vel Centrifugado'].unique().tolist()
lista_Vel.sort()
#lista_Vel

lista_Ene = data['Consumo Energía'].unique().tolist()
lista_Ene.sort(reverse=True)
#lista_Ene

lista_Agu = data['Consumo Agua'].unique().tolist()
lista_Agu.sort(reverse=True)
#lista_Agu

lista_Rui = data['Nivel de Ruido'].unique().tolist()
lista_Rui.sort(reverse=True)
#lista_Rui

punt_max = 100

punt_min_kg = punt_max / len(lista_kg)
#punt_min_kg

punt_min_Vel = punt_max / len(lista_Vel)
#punt_min_Vel

punt_min_Ene = punt_max / len(lista_Ene)
#punt_min_Ene

punt_min_Agu = punt_max / len(lista_Agu)
#punt_min_Agu

punt_min_Rui = punt_max / len(lista_Rui)
#punt_min_Rui

data['punt_kg'] = 0
data['punt_Vel'] = 0
data['punt_Ene'] = 0
data['punt_Agu'] = 0
data['punt_Rui'] = 0


for i in range (len(data)):
    #data['punt_kg'][i] = (lista_kg.index(data['Kg'][i])+15)*punt_min_Agu
    data['punt_Vel'][i] = (lista_Vel.index(data['Vel Centrifugado'][i])+17)*punt_min_Agu
    data['punt_Ene'][i] = (lista_Ene.index(data['Consumo Energía'][i])+6)*punt_min_Agu
    data['punt_Agu'][i] = (lista_Agu.index(data['Consumo Agua'][i])+1)*punt_min_Agu
    data['punt_Rui'][i] = (lista_Rui.index(data['Nivel de Ruido'][i])+6)*punt_min_Agu 
    
data['Puntuacion'] =  (data['punt_Vel'] + data['punt_Ene'] + data['punt_Agu'] + data['punt_Rui']) / 4

data['punt_Precio'] = data['Precio'] / data['Puntuacion']

data.sort_values('punt_Precio')

chosen_TP = st.sidebar.radio(
    'TIPO DE CARGA',
    (data['Carga'].unique()))



# Add a slider to the sidebar:
slider_KG = st.sidebar.slider(
    'CAPACIDAD DE LAVADO KG',
    data['Kg'].unique().tolist()[0], data['Kg'].unique().tolist()[-1], (data['Kg'].unique().tolist()[0], data['Kg'].unique().tolist()[-1])
)

# Add a slider to the sidebar:
slider_PC = st.sidebar.slider(
    'RANGO DE PRECIO',
    data['Precio'].unique().tolist()[0], data['Precio'].unique().tolist()[-1], (data['Precio'].unique().tolist()[0], data['Precio'].unique().tolist()[-1])
)


options_MA = st.sidebar.multiselect(
    'MARCAS',
    lista_marcas, lista_marcas
    )



st.info('La información contenida en esta página no está actualizada')


#data[(data.Kg.isin([6,7])) & (data['Carga'] == chosen_TP)]



a = data[(data['Kg'] >= slider_KG[0]) & (data['Kg'] <= slider_KG[-1]) & (data['Carga'] == chosen_TP) & (data['Precio'] >= slider_PC[0]) & (data['Precio'] <= slider_PC[-1]) & (data.Marca.isin(options_MA))]

a.reset_index()




st.text('Resultados: ' + str(len(a)))

 




c = alt.Chart(a).mark_circle(size=120).encode(
    x='Puntuacion:N', y='Precio', color='Marca', tooltip=['Marca', 'Modelo', 'Puntuacion', 'Precio'])
st.altair_chart(c, use_container_width=True)


col1, col2 = st.beta_columns(2)

col1, col2 = st.beta_columns((3, 2))

with col1:
    ordenar = st.selectbox(
    'Ordenar por:',
    ('Puntuacion', 'Precio', 'punt_Precio'))

with col2:
    orden = st.selectbox(
    'Ordenar:',
    ('De mayor a menor', 'De menor a mayor'))

if orden == 'De mayor a menor':
    mayor_menor = False
    
if orden == 'De menor a mayor':
    mayor_menor = True


if len(a) == 0:
    st.warning('Revisa los filtros. No hay resultados')
    e = a.sort_values(ordenar, ascending=mayor_menor).reset_index()
else:
    e = a.sort_values(ordenar, ascending=mayor_menor).reset_index()
    


    


calc_col = math.ceil(len(e)/3)

#st.write(calc_col)

contador = 0

for columns in range (0, calc_col):
    if calc_col == 0:
        #st.warning('Revisa los filtros. No hay resultados')
        #st.text(columns)
        break
    else:
        #st.text(columns)
        
        col1, col2, col3 = st.beta_columns(3)

    with col1:
        st.subheader(str(contador+1) + ') ' + str(e['Marca'][contador]) +' | ' + str(e['Kg'][contador]) + 'Kg')
        st.text(str(e['Modelo'][contador]))
        st.text('VC:' + str(e['punt_Vel'][contador]) + '|' +
                'CE:' + str(e['punt_Ene'][contador]) + '|' +
                'CA:' + str(e['punt_Agu'][contador]) + '|' +
                'RL:' + str(e['punt_Rui'][contador])
                )
        st.text( 'Precio: ' + str(e['Precio'][contador]) +' | ' + 'PU: ' + str(e['Puntuacion'][contador]))
        st.image(e['Imagen'][contador], use_column_width=True)        
        st.write(str(e['Enlace'][contador]),unsafe_allow_html=True,)        
        contador = contador + 1
        
    if contador >= len(e):
        break
    else:
    
        with col2:
            st.subheader(str(contador+1) + ') ' + str(e['Marca'][contador]) +' | ' + str(e['Kg'][contador]) + 'Kg')
            st.text(str(e['Modelo'][contador]))
            st.text('VC:' + str(e['punt_Vel'][contador]) + '|' +
                'CE:' + str(e['punt_Ene'][contador]) + '|' +
                'CA:' + str(e['punt_Agu'][contador]) + '|' +
                'RL:' + str(e['punt_Rui'][contador])
                )
            st.text( 'Precio: ' + str(e['Precio'][contador]) + ' | ' + 'PU: ' + str(e['Puntuacion'][contador]))
            st.image(e['Imagen'][contador], use_column_width=True)
            st.write(str(e['Enlace'][contador]),unsafe_allow_html=True,)
            contador = contador + 1

    if contador >= len(e):
        break
    else:

        with col3:
            st.subheader(str(contador+1) + ') ' + str(e['Marca'][contador]) +' | ' + str(e['Kg'][contador]) + 'Kg')
            st.text(str(e['Modelo'][contador]))
            st.text('VC:' + str(e['punt_Vel'][contador]) + '|' +
                'CE:' + str(e['punt_Ene'][contador]) + '|' +
                'CA:' + str(e['punt_Agu'][contador]) + '|' +
                'RL:' + str(e['punt_Rui'][contador])
                )
            st.text( 'Precio: ' + str(e['Precio'][contador]) + ' | ' + 'PU: ' + str(e['Puntuacion'][contador]))
            st.image(e['Imagen'][contador], use_column_width=True)
            st.write(str(e['Enlace'][contador]),unsafe_allow_html=True,)
            contador = contador + 1






#expander = st.beta_expander("FAQ")
#expander.write("Here you could put in some really, really long explanations...")



#st.error('This is an error')
#st.warning('This is a warning')
#st.info('La información contenida en esta página no está actualizada')



