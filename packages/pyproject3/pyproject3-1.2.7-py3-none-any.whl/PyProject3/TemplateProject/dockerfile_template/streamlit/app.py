#! .venv/bin/python
#coding: utf-8
import datetime
import streamlit as st
st.title("Hello World")
col1, col2 = st.columns([1, 2])
with col1:
    choice = st.selectbox("Select an option", ["Option 1", "Option 2", "Option 3"])
    if choice == "Option 1":
        st.write("You selected Option 1")
    elif choice == "Option 2":
        st.write("You selected Option 2")
    else:
        st.write("You selected Option 3")
with col2:
    st.json({
        "name": "John",
        "age": 30,
        "city": "New York"
    })

    st.markdown("""
    # Hello World
    This is a test
    This is a test  
    This is a test
    This is a test
    """)

    st.code("print('Hello, World!')", language="python")

    st.latex("$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$")
    
    st.graphviz_chart("""
    digraph {
        A -> B;
        A -> C;
        B -> D;
        C -> D;
    }
    """)
    
    st.divider()
    st.progress(0.3)
    st.progress(0.7, text="Loading...")

    st.text_input("Enter your name", value="John")
    st.text_area("Enter your bio", value="I am a software engineer")
    st.number_input("Enter your age", value=30, min_value=0, max_value=100)
    st.date_input("Enter your birth date", value=datetime.date(1990, 1, 1))
    st.time_input("Enter your birth time", value=datetime.time(12, 0, 0))
    st.file_uploader("Upload a file", type=["jpg", "png", "pdf"])
    st.color_picker("Select a color", value="#000000")
    st.button("Click me")

    st.checkbox("Select this option")



