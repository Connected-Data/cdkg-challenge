import json
import os
from pathlib import Path

import ell
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

filepath = Path("./data")
filenames = [f.name for f in filepath.glob("*")]


MODEL_NAME = "gpt-4o-mini"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
assert OPENAI_API_KEY is not None, "OPENAI_API_KEY is not set"
SEED = 42

openai_client = OpenAI(api_key=OPENAI_API_KEY)


@ell.simple(model=MODEL_NAME, temperature=0.0, client=openai_client, seed=SEED)
def get_entities(text: str) -> str:
    """
    You are a helpful AI assistant that extracts useful entities from a presentation transcript as JSON.

    Three kinds of entities are of interest. You will be given the text, and you will need to
    extract the following entities as JSON.

    Here is an example JSON schema:

    {
        "tag": ["GraphQL", "RDF", "Apollo"]
    }

    Strictly follow the JSON schema provided. Do not return anything other than valid JSON.
    """
    return f"""
    Task: Extract useful entities from the following presentation transcript as JSON.

    Instructions:
      1. Only include technologies or tools/frameworks as a list of "tag" keywords.
      2. Always lowercase the names of the tags (e.g. "GraphQL" should be "graphql").

    Presentation transcript:
    {text}
    """


# Initialize empty list at the start
all_entities = []

with open("entities.json", "w") as f:
    for filename in filenames:
        with open(f"{filepath}/{filename}", "r") as data_file:
            text = data_file.read()

        entities = json.loads(get_entities(text))
        # Append each result to the list
        all_entities.append({"filename": filename, "entities": entities})
        print(f"Finished processing file {filename}")

    # Write the entire list at once
    json.dump(all_entities, f, indent=2)
