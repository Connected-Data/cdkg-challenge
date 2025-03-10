// --- Data models ---
class Cypher {
  query string
}

class Answer {
  question string
  answer string
}

// --- Functions ---

function RAGText2Cypher(schema: string, question: string) -> Cypher {
  client CustomGPT4oMini
  prompt #"
    You are an expert in translating natural language questions into Cypher statements.
    You will be provided with a question and a graph schema.
    Use only the provided relationship types and properties in the schema to generate a Cypher
    statement.
    The Cypher statement could retrieve nodes, relationships, or both.
    Do not include any explanations or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a
    Cypher statement.
    Answer in no more than 5 sentences

    {{ _.role("user") }}
    Task: Generate a Cypher statement to query a graph database.

    {{ schema}}

    The question is:
    {{ question }}

    Instructions:
    1. Use only the provided node and relationship types and properties in the schema.
    2. When returning results, return property values rather than the entire node or relationship.
    3. ALWAYS use the WHERE clause to compare string properties, and compare them using the
       LOWER() function.

    {{ ctx.output_format }}
  "#
}

function RAGAnswerQuestion(question: string, context: string) -> Answer {
  client CustomGPT4oMini
  prompt #"
    You are an AI assistant using Retrieval-Augmented Generation (RAG).
    RAG enhances your responses by retrieving relevant information from a knowledge base.
    You will be provided with a question and relevant context. Use only this context to answer
    the question.
    Do not make up an answer. If you don't know the answer, say so clearly.
    Always strive to provide concise, helpful, and context-aware answers.

    {{ _.role("user") }}
    QUESTION: {{ question }}
    RELEVANT CONTEXT: {{ context }}

    {{ ctx.output_format }}

    RESPONSE:
  "#
}


test Text2Cypher1 {
  functions [RAGText2Cypher]
  args {
    schema #"
    ALWAYS RESPECT THE EDGE DIRECTIONS:
    ---
    (:Talk) -[:IS_DESCRIBED_BY]-> (:Tag)
    (:Speaker) -[:GIVES_TALK]-> (:Talk)
    (:Talk) -[:IS_PART_OF]-> (:Event)
    (:Talk) -[:IS_CATEGORIZED_AS]-> (:Category)
    ---

    Node properties:
    - Tag
        - keyword: string
    - Talk
        - title: string
        - category: string
        - url: string
        - description: string
        - type: string
    - Speaker
        - name: string
    - Event
        - name: string
        - description: string
    - Category
        - name: string

    Edge properties:
    - GIVES_TALK
        - date: date
    "#
    question "Who are the speakers whose talks have the tag 'rdf'? Return the speaker names as a numbered list."
  }
  @@assert(has_return_clause, {{ 'RETURN' in this.query }})
}

test RAGAnswer1 {
  functions [RAGAnswerQuestion]
  args {
    question "Who are the speakers whose talks have the tag 'rdf'? Return the speaker names as a numbered list."
    context #"
        ['Marcus Nölke', 'Veronika Heimsbakk', 'Dave Duggal', 'Kurt Cagle', 'Sebastian Schmidt', 'Veronique Moore', 'Atanas Kiryakov', 'Ora Lassila']
    "#
  }
}

test RAGMissingContext {
  functions [RAGAnswerQuestion]
  args {
    question "What did Paco Nathan say about RDF?"
    context ""
  }
}
