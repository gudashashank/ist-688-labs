import streamlit as st
from openai import OpenAI, OpenAIError

# Show title and description.
st.title("Lab 2 - My Document Question Answering")
st.write(
    "Upload a document below and select how you would like it summarized! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Sidebar for summary options.
st.sidebar.title("Summary Options")
summary_option = st.sidebar.radio(
    "Choose a summary type:",
    (
        "Summarize the document in 100 words",
        "Summarize the document in 2 connecting paragraphs",
        "Summarize the document in 5 bullet points",
    ),
)

# Checkbox for model selection.
use_advanced_model = st.sidebar.checkbox("Use Advanced Model (gpt-4o)")
model_name = "gpt-4o" if use_advanced_model else "gpt-4o-mini"

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)", type=("txt", "md")
)

if uploaded_file:
    # Read the uploaded document.
    document = uploaded_file.read().decode()

    # Create the instruction based on the selected summary option.
    if summary_option == "Summarize the document in 100 words":
        instruction = "Summarize the following document in 100 words."
    elif summary_option == "Summarize the document in 2 connecting paragraphs":
        instruction = "Summarize the following document in 2 connecting paragraphs."
    else:
        instruction = "Summarize the following document in 5 bullet points."

    # Prepare the messages for the LLM.
    messages = [
        {
            "role": "user",
            "content": f"{instruction}\n\n---\n\n{document}",
        }
    ]

    # Generate the summary using the selected model.
    try:
        client = OpenAI(api_key=st.secrets["openai_key"])
        stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)

    except OpenAIError as e:
        st.error(f"An error occurred: {e}")

# Footer
st.markdown(
    """
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; font-size: 12px; color: grey;'>
        IST-688 Shashank Guda
    </div>
    """,
    unsafe_allow_html=True
)
