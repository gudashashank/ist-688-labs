import streamlit as st
from openai import OpenAI, OpenAIError
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb
from chromadb.utils import embedding_functions
import os
import PyPDF2
from PyPDF2 import PdfReader

# Function to create ChromaDB collection and embed PDF documents
def create_chromadb_collection(pdf_files):
    if 'Lab4_vectorDB' not in st.session_state:
        # Initialize ChromaDB client with persistent storage
        client = chromadb.PersistentClient(path="./chroma_db")
        st.session_state.Lab4_vectorDB = client.get_or_create_collection(name="Lab4Collection")
        
        # Set up OpenAI embedding function
        openai_embedder = embedding_functions.OpenAIEmbeddingFunction(api_key=st.secrets["openai_key"], model_name="text-embedding-3-small")
        
        # Loop through provided PDF files, convert to text, and add to the vector database
        for file in pdf_files:
            try:
                # Read PDF file and extract text
                pdf_text = ""
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    pdf_text += page.extract_text()
                
                # Add document to ChromaDB collection with embeddings
                st.session_state.Lab4_vectorDB.add(
                    documents=[pdf_text],
                    metadatas=[{"filename": file.name}],
                    ids=[file.name]
                )
            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")
        
        # Add a remark saying the database is created
        st.success("ChromaDB collection has been created successfully!")

# Function to test vector database with a search query
def test_vector_db(query):
    if 'Lab4_vectorDB' in st.session_state:
        # Perform a similarity search on the query
        results = st.session_state.Lab4_vectorDB.query(
            query_texts=[query],
            n_results=3,
            include=["metadatas", "distances"]
        )
        
        # Display the top 3 document names (filenames) and distances
        st.write(f"Search results for '{query}':")
        for i, (metadata, distance) in enumerate(zip(results['metadatas'][0], results['distances'][0])):
            st.write(f"{i+1}. Filename: {metadata['filename']}")
            st.write(f"   Distance: {distance:.4f}")
            st.write("---")

# Streamlit application
st.title("Lab 4 - ChromaDB and OpenAI Embeddings")

# Load PDF files (example file uploader)
pdf_files = st.file_uploader("Upload your PDF files", accept_multiple_files=True, type=["pdf"])

# Create ChromaDB collection and embed documents if not already created
if st.button("Create ChromaDB Collection") and pdf_files:
    create_chromadb_collection(pdf_files)

# Test the vector database
test_query = st.text_input("Enter a search query (e.g., 'Generative AI')")
if test_query:
    test_vector_db(test_query)