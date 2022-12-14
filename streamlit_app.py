import streamlit

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Pongamos una lista de selección aquí para que puedan escoger la fruta que quieren incluir
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Mostrar la tabla en la página.
streamlit.dataframe(fruits_to_show)

#Nueva sección para mostrar la respuesta api de fruityvice
streamlit.header("Fruityvice Fruit Advice!")
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")
#streamlit.text(fruityvice_response.json()) #Solo escribe los datos en la pantalla

#Tome la versión json de la respuesta y normalícela.
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#Mostrarlo en la pantalla como una tabla
streamlit.dataframe (fruityvice_normalized)
