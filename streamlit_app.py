import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Pongamos una lista de selección aquí para que puedan escoger la fruta que quieren incluir
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Mostrar la tabla en la página.
streamlit.dataframe(fruits_to_show)


#Creación Funcion repetible.
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
#Nueva sección para mostrar la respuesta api de fruityvice
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input ('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data (fruit_choice)
    #Mostrarlo en la pantalla como una tabla
    streamlit.dataframe (back_from_function)
    
except URLError as e:
    streamlit.error()

#detenemos esta parte para que no se ejecute.
streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Permitir que el usuario final agregue una fruta a la lista
add_my_fruit = streamlit.text_input ('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks fro adding: ', add_my_fruit)

# Seguir puede que no funcione por ahora.
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
