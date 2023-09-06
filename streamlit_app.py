#streamlit app link: https://jtstream.streamlit.app/
import streamlit as st, streamlit as streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner')

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal 🥣')
st.text('🥗 Kale, Spinach & Rocket Smoothie 🥗')
st.text('🐔 Hard-Boiled Free-Range Egg 🐔')
st.text('🥑🍞 Avacoda Toast 🥑🍞')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)

#----------------------------fruityvice_api_response
#streamlit.header("Fruityvice Fruit Advice!")
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json()) #just writes the data to the screen

# take the json version of the response and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output to the screen as a table
#----------------------------streamlit.dataframe(fruityvice_normalized)

#----------------------------create the repeatable code block (called an API using a function which takes in fruit as an argument and 'requests' package)
def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
          # take the json version of the response and normalize it with pandas
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized
  
#----------------------------New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)    # -------- output to the screen as a table
except URLError as e:
    streamlit.error()
        
#--------------------------------------------------------------------create a function that will query snowflake table when click on a button
streamlit.header("The fruit load list contains:")
#Snowflake-related functions
def get_fruit_load_list():
        with my_cnx.cursor() as my_cur:
             my_cur.execute("select * from fruit_load_list")
             return my_cur.fetchall() #fetchall means to print all row from the output of the select statement

# Add a button to load the fruit table
if st.button('Get Fruit Load List'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_data_rows = get_fruit_load_list() #---- function being called here
        st.dataframe(my_data_rows) #displays table nicely using st.dataframe

#dont run anything past here while we troubleshoot
streamlit.stop()

# Allow end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
        with my_cnx.cursor() as my_cur:
             my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
             return "Thanks for adding" + new_fruit
             
#text entry box
try:
    add_my_fruit = streamlit.text_input('What fruit would you like to add?')
    if not add_my_fruit:
        streamlit.error("Please add a fruit")
    else:
        add_fruit_function_output = insert_row_snowflake(add_my_fruit)
except URLError as e:
    streamlit.error()
