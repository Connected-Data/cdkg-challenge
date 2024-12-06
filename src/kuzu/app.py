import streamlit as st
from rag import GraphRAG

st.set_page_config(page_title="Graph RAG Q&A", layout="wide")
st.title("Graph RAG using Kùzu")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize the GraphRAG system
@st.cache_resource
def init_rag():
    return GraphRAG("./cdl_db")

rag = init_rag()

# Create the input box
question = st.text_input("Ask a question to the CDL Knowledge Graph built on top of Kùzu, an embedded graph database:", 
                        placeholder="e.g., What was discussed in the talk by Paco Nathan?")

if question:
    with st.spinner("Generating answer..."):
        # Get the Cypher query
        cypher = rag.generate_cypher(question)
        
        # Show the Cypher query in an expander
        with st.expander("View Cypher Query"):
            st.code(cypher, language="sql")
        
        # Get and show the response
        response = rag.run(question)
        st.write("### Answer")
        st.write(response)
        # Append the question and answer to the history
        st.session_state.messages.append({"question": question, "answer": response})

# Display history (add before the input box)
for msg in st.session_state.messages:
    st.write("**Q:** " + msg["question"])
    st.write("**A:** " + msg["answer"])
    st.divider()