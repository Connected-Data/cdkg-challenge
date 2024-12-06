"""
This script creates a lexical graph from the transcripts of the Connected Data Knowledge Graph Challenge.

Run this script _after_ creating the domain graph, i.e., after running `create_domain_graph.py`.
"""

import json
from pathlib import Path

import kuzu
import polars as pl

db = kuzu.Database("cdl_db")
conn = kuzu.Connection(db)


def load_data(filepath: str) -> pl.DataFrame:
    """Load and clean data from the metadata CSV file"""
    df = (
        pl.read_csv(filepath)
        .drop_nulls()
        .select("Title", "File")
        .with_columns(
            pl.col("File")
            .map_elements(lambda x: Path(x).stem, return_dtype=pl.String)
            .alias("filename")
        )
        .rename({"Title": "title"})
        .drop("File")
        .select("filename", "title")
    )
    return df


# Read the metadata file to associate filenames with speakers
df = load_data(
    "../../Transcripts/Connected Data Knowledge Graph Challenge - Transcript Metadata.csv"
)
# Read entities from entities.json and insert into the lexical subgraph
with open("entities.json", "r") as f:
    entities = json.load(f)

# Create the necessary node and relationship tables for the lexical graph
# In this case, the lexical graph is a subgraph that attaches to the domain graph
conn.execute("CREATE NODE TABLE IF NOT EXISTS Tag(keyword STRING, PRIMARY KEY(keyword));")
conn.execute("CREATE REL TABLE IF NOT EXISTS IS_DESCRIBED_BY(FROM Talk TO Tag);")

for data in entities:
    filename = Path(data["filename"]).stem
    talk = df.filter(pl.col("filename") == filename).select("title").to_series().to_list()
    if talk:
        title = talk[0]
        conn.execute(
            """
            MATCH (talk:Talk {title: $title})
            UNWIND $data.entities.tag AS keyword
            MERGE (tag:Tag {keyword: keyword})
            MERGE (tag)<-[:IS_DESCRIBED_BY]-(talk)
            """,
            parameters={"data": data, "title": title},
        )
