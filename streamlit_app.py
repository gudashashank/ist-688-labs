import streamlit as st

lab_1 = st.Page("Lab_1.py", title = 'Lab 1')
lab_2 = st.Page("Lab_2.py", title = 'Lab 2')
lab_3 = st.Page("Lab_3.py", title = 'Lab 3')
lab_4 = st.Page("Lab_4.py", title = 'Lab 4')


pg = st.navigation([lab_1,lab_2,lab_3,lab_4])

st.set_page_config(page_title = "IST-688 Labs - Shashank Guda")

pg.run()
