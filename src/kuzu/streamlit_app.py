import streamlit as st

from rag import GraphRAG

st.set_page_config(page_title="Graph RAG Q&A", layout="wide")
st.title("Graph RAG using Kuzu")

if "messages" not in st.session_state:
    st.session_state.messages = []


# Initialize the GraphRAG system
@st.cache_resource
def init_rag():
    return GraphRAG("cdl_db.kuzu")


rag = init_rag()

# Create the input box
question = st.text_input(
    "Ask a question to the CDL Knowledge Graph built on top of Kuzu, an embedded graph database:",
    placeholder="e.g., Can you tell me about Connected Data World 2021?",
)

if question:
    with st.spinner("Generating answer..."):
        # Get the Cypher query
        output = rag.run(question)

        # Show the Cypher query in an expander
        with st.expander("View Cypher Query", expanded=True):
            st.code(output["cypher"], language="sql")

        # Get and show the response
        st.write("### Answer")
        st.write(output["response"])
        # Append the question and answer to the history
        st.session_state.messages.append({"question": question, "answer": output["response"]})

# Display history
for msg in reversed(st.session_state.messages):
    with st.container(border=True):
        st.write("**Q:** " + msg["question"])
        st.write("**A:** " + msg["answer"])
