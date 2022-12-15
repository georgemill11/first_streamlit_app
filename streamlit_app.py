import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Snowflake Badge')

streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑 Hard-Boiled Free-Range Egg 🍞')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')




# Let's put a pick list here so they can pick the fruit they want to include
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Pear', 'Peach'])

fruit_to_show = my_fruit_list.loc[fruit_selected]

# Display the table on the page.
streamlit.dataframe(fruit_to_show)
streamlit.dataframe(my_fruit_list)

def get_fruit_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruit_normalaized = pandas.json_normalize(fruityvice_response.json())
  return fruit_normalaized

def get_fruit_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        my_data_rows = my_cur.fetchall()
        return my_data_rows

def add_fruid(new_fruid):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('" + new_fruid + "')")
         return "Thanks for adding " + new_fruid

fruit_choice = streamlit.text_input("Whats fruit would you like information about", "kiwi")
streamlit.write("Ypu Chose: " + fruit_choice)

streamlit.header("Fruityvice Fruit Advice!")

try:
  if not fruit_choice:
    streamlit.error("Please select a fruit to get info")
  else:
    streamlit.dataframe(get_fruit_data(fruit_choice))

except URLError as e:
    streamlit.error()

fruit_add = streamlit.text_input("Whats fruit would you like to add?")

if streamlit.button("Fruit for adding"):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     streamlit.text(add_fruid(fruit_add))
     my_cnx.close()

if streamlit.button("Get fruit load list"):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     data_rows = get_fruit_list()
     my_cnx.close()
     streamlit.dataframe(data_rows)
#https://pavlin84-snowflake-myfirspytonfile-x5zgv7.streamlit.app/
