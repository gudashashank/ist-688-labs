import streamlit as st
from openai import OpenAI, OpenAIError

st.title("My Lab 3 Question Answering Chatbot")

openAI_model = st.sidebar.selectbox("Which Model?", ("mini", "regular"))
model_to_use = "gpt-4o-mini" if openAI_model == "mini" else "gpt-4o"

if 'client' not in st.session_state:
    api_key = st.secrets["openai_key"]
    st.session_state.client = OpenAI(api_key=api_key)

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm a chatbot that can answer questions for you. What would you like to know?"}]

if 'waiting_for_more_info' not in st.session_state:
    st.session_state.waiting_for_more_info = False

for msg in st.session_state.messages:
    chat_msg = st.chat_message(msg["role"])
    chat_msg.write(msg["content"])

if prompt := st.chat_input("Type your message here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = st.session_state.client

    if st.session_state.waiting_for_more_info:
        if prompt.lower() in ['yes', 'y']:
            try:
                stream = client.chat.completions.create(
                    model=model_to_use,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that provides information in a way that a 10-year-old can understand. The user has asked for more information about the previous topic."},
                        {"role": "user", "content": "Please provide more information about the previous topic in a way a 10-year-old can understand."}
                    ] + st.session_state.messages[-4:],
                    stream=True,
                )
                with st.chat_message("assistant"):
                    response = st.write_stream(stream)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.write("DO YOU WANT MORE INFO?")
            except OpenAIError as e:
                st.error(f"An error occurred: {e}")
        else:
            st.session_state.waiting_for_more_info = False
            with st.chat_message("assistant"):
                st.write("Okay! What other question can I help you with?")
            st.session_state.messages.append({"role": "assistant", "content": "Okay! What other question can I help you with?"})
    else:
        try:
            stream = client.chat.completions.create(
                model=model_to_use,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions in a way that a 10-year-old can understand. After answering, always ask 'DO YOU WANT MORE INFO?'"}
                ] + st.session_state.messages,
                stream=True,
            )
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write("DO YOU WANT MORE INFO?")
                st.session_state.waiting_for_more_info = True
        except OpenAIError as e:
            st.error(f"An error occurred: {e}")

    if len(st.session_state.messages) > 6:
        st.session_state.messages = st.session_state.messages[-6:]