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

#fruityvice_api_response
#streamlit.header("Fruityvice Fruit Advice!")
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json()) #just writes the data to the screen

# take the json version of the response and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output to the screen as a table
#streamlit.dataframe(fruityvice_normalized)

#New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # take the json version of the response and normalize it
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # output to the screen as a table
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()
  
#dont run anything past here while we troubleshoot
streamlit.stop()

#  Let's Query Our Trial Account Metadata 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select fruit_name from fruit_load_list")
my_data_row = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains:")
st.dataframe(my_data_row)

#text entry box
add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

#This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
