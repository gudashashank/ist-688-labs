import streamlit as st
from openai import OpenAI, OpenAIError

# Display title and introduction
st.title("MY Lab3 Question Answering Chatbot")

# Model selection via sidebar
openAI_model = st.sidebar.selectbox("Which Model?", ("mini", "regular"))
model_to_use = "gpt-4o-mini" if openAI_model == "mini" else "gpt-4o"

# Initialize OpenAI client in session state if not already done
if 'client' not in st.session_state:
    api_key = st.secrets["OPENAI_API_KEY"] 
    st.session_state.client = OpenAI(api_key=api_key)

# Initialize messages in session state if not already done
if 'messages' not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages from the session state
for msg in st.session_state.messages:
    chat_msg = st.chat_message(msg["role"])
    chat_msg.write(msg["content"])

# Input for the user to type messages
if prompt := st.chat_input("What is up?"):
    # Append user's message to the session state messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user's message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using OpenAI's API
    client = st.session_state.client
    try:
        stream = client.chat.completions.create(
            model=model_to_use,
            messages=st.session_state.messages,
            stream=True,
        )

        # Stream and display the assistant's response
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
    except OpenAIError as e:
        st.error(f"An error occurred: {e}")
