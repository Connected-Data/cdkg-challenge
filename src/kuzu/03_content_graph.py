"""
This script creates a lexical graph from the transcripts of the Connected Data Knowledge Graph Challenge.

Run this script _after_ creating the domain graph, i.e., after running `create_domain_graph.py`.
"""
import polars as pl
from pathlib import Path
import json
import kuzu

db = kuzu.Database("cdl_db")
conn = kuzu.Connection(db)


def load_data(filepath: str) -> pl.DataFrame:
    """Load and clean data from the metadata CSV file"""
    df = (
        pl.read_csv(filepath)
        .drop_nulls()
        .select("Speaker", "File")
        .with_columns(pl.col("Speaker").str.replace_all(" & ", " and "))
        .with_columns(pl.col("Speaker").str.split(" and "))
        .explode("Speaker")
        .with_columns(pl.col("Speaker").str.strip_chars())
        .with_columns(
            pl.col("File").map_elements(lambda x: Path(x).stem, return_dtype=pl.String).alias("filename")
        )
        .rename({"Speaker": "speaker"})
        .drop("File")
        .select("filename", "speaker")
    )
    return df

# Read the metadata file to associate filenames with speakers
df = load_data(
    "../../Transcripts/Connected Data Knowledge Graph Challenge - Transcript Metadata.csv"
)
df.select("filename").to_series().to_list()

# Extract speakers for each filename as a list from dataframe
speakers = df.group_by("filename").agg(pl.col("speaker").alias("speakers"))

# Create the necessary node and relationship tables for the lexical graph
# In this case, the lexical graph is a subgraph that attaches to the domain graph
conn.execute("CREATE NODE TABLE IF NOT EXISTS Topic(name STRING, PRIMARY KEY(name));")
conn.execute("CREATE REL TABLE IF NOT EXISTS DISCUSSES(FROM Speaker TO Topic);")

# Read entities from entities.json and insert into the lexical subgraph
with open("entities.json", "r") as f:
    entities = json.load(f)

for data in entities:
    filename = Path(data["filename"]).stem
    # lookup speaker name from filename
    speaker = df.filter(pl.col("filename") == filename).select("speaker").to_series().to_list()
    
    if speaker:
        speaker = speaker[0]
        conn.execute(
            """
            MATCH (s:Speaker {name: $speaker})
            UNWIND $data.entities.topic AS topic
            MERGE (t:Topic {name: topic})
            MERGE (s)-[:DISCUSSES]->(t)
            """,
            parameters={"data": data, "speaker": speaker}
        )
