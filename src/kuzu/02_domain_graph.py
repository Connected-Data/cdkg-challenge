from pathlib import Path

import kuzu
import polars as pl


def load_data(filepath: str) -> pl.DataFrame:
    """Load and clean data from CSV"""
    # Drop rows with empty strings
    return (
        pl.read_csv(filepath).drop_nulls().filter(~pl.all_horizontal(pl.all().str.len_chars() == 0))
    )


def extract_speakers(df: pl.DataFrame) -> pl.DataFrame:
    """Extract unique speaker names from dataframe"""
    speakers_df = (
        df.select("Speaker")
        .with_columns(pl.col("Speaker").str.replace_all(" & ", " and "))
        .with_columns(pl.col("Speaker").str.split(" and "))
        .explode("Speaker")
        .with_columns(pl.col("Speaker").str.strip_chars())
        .drop_nulls()
        .unique()
    )
    return speakers_df


def extract_talks(df: pl.DataFrame) -> list[str]:
    """Extract unique talk titles from dataframe"""
    talks_df = (
        df.select(["Title", "Category", "Web", "Description", "Type"])
        .rename(
            {
                "Title": "title",
                "Category": "category",
                "Web": "url",
                "Description": "description",
                "Type": "type",
            }
        )
        .drop_nulls()
        .unique()
    )
    return talks_df


def extract_events(df: pl.DataFrame) -> list[str]:
    """Extract unique event names from dataframe"""
    events_df = df.select("Event").drop_nulls().unique()
    return events_df


def extract_categories(df: pl.DataFrame) -> list[str]:
    """Extract unique event names from dataframe"""
    categories_df = df.select("Category").drop_nulls().unique()
    return categories_df


def get_speaker_talk_category_relationships(df: pl.DataFrame) -> pl.DataFrame:
    """Get relationships between speakers and talks"""
    return (
        df.select("Speaker", "Title", "Date", "Category")
        .with_columns(pl.col("Date").str.to_date(strict=False))
        .with_columns(pl.col("Speaker").str.replace_all(" & ", " and "))
        .with_columns(pl.col("Speaker").str.split(" and "))
        .explode("Speaker")
        .with_columns(pl.col("Speaker").str.strip_chars())
        .rename({"Speaker": "speaker", "Title": "talk", "Date": "date", "Category": "category"})
        .drop_nulls()
        .unique()
    )


def get_talk_category_relationships(df: pl.DataFrame) -> pl.DataFrame:
    """Get relationships between talks and categories"""
    return df.select("Title", "Category").rename({"Title": "from", "Category": "to"})


def create_tables(conn: kuzu.Connection):
    conn.execute("CREATE NODE TABLE IF NOT EXISTS Speaker (name STRING, PRIMARY KEY (name))")
    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS Talk (
            title STRING,
            category STRING, 
            url STRING,
            description STRING,
            type STRING,
            PRIMARY KEY (title)
        )
    """)
    conn.execute(
        """
        CREATE NODE TABLE IF NOT EXISTS Event (
            name STRING,
            description STRING,
            PRIMARY KEY (name)
        )
        """
    )
    conn.execute("CREATE NODE TABLE IF NOT EXISTS Category (name STRING, PRIMARY KEY (name))")
    # Relationships
    conn.execute("CREATE REL TABLE IF NOT EXISTS GIVES_TALK (FROM Speaker TO Talk, date DATE)")
    conn.execute("CREATE REL TABLE IF NOT EXISTS IS_PART_OF (FROM Talk TO Event)")
    conn.execute("CREATE REL TABLE IF NOT EXISTS IS_CATEGORIZED_AS (FROM Talk TO Category)")


def get_talk_event_relationships(df: pl.DataFrame) -> pl.DataFrame:
    """Get relationships between talks and events"""
    return df.select("Title", "Event")


def write_cdl_description(conn: kuzu.Connection, event_name: str) -> None:
    """
    We obtain the conference desrciption for 2021 from the following URL:
    https://2021.connecteddataworld.com/connected-data-world-2021-program-announced/
    """
    description = """
    Connected Data London, the top event for leaders and innovators on all things Knowledge Graphs,
    Graph Data Science and AI, Graph Databases and Semantic Technology, is back as what it has de facto
    become: Connected Data World. Building on our legacy, we are sharing a visionary outlook on Graph
    as a foundational technology stack for the 2020s.
    """
    description_clean = description.replace("\n", " ").strip()
    conn.execute(
        """
        MERGE (e:Event {name: $event_name})
        ON MATCH SET e.description = $description
        """,
        parameters={"event_name": event_name, "description": description_clean},
    )


def write_knowledge_connexions_description(conn: kuzu.Connection, event_name: str) -> None:
    """
    We obtain the conference desrciption for Knowledge Connexions 2020 from the following URL:
    https://knowledge-connexions-conference.heysummit.com/knowledge-connexions-2020-program-announced/
    """
    description = """
    This visionary event featuring a rich array of technological building blocks to support the
    transition to a knowledge-based economy is taking place online. The representation of the
    relationships among data, information, knowledge and --ultimately-- wisdom, known as the data
    pyramid, has long been part of the language of information science. Digital transformation has
    made this relevant beyond the confines of information science. COVID-19 has brought years' worth
    of digital transformation in just a few short months.

    In this new knowledge-based digital world, encoding and making use of business and operational
    knowledge is the key to making progress and staying competitive. So how do we go from data to
    information, and from information to knowledge? This is the key question Knowledge Connexions
    aims to address.
    """
    description_clean = description.replace("\n", " ").strip()
    conn.execute(
        """
        MERGE (e:Event {name: $event_name})
        ON MATCH SET e.description = $description
        """,
        parameters={"event_name": event_name, "description": description_clean},
    )


if __name__ == "__main__":
    # Create the domain graph first - ensure we start with a clean database
    DB_NAME = "cdl_db.kuzu"
    Path(DB_NAME).unlink(missing_ok=True)

    db = kuzu.Database(DB_NAME)
    conn = kuzu.Connection(db)

    # Load data
    df = load_data(
        "../../Transcripts/Connected Data Knowledge Graph Challenge - Transcript Metadata.csv"
    )

    # Extract nodes
    speakers_df = extract_speakers(df)
    talks_df = extract_talks(df)
    events_df = extract_events(df)
    categories_df = extract_categories(df)
    # Get relationships
    speaker_talk_category_df = get_speaker_talk_category_relationships(df)
    is_categorized_as_df = get_talk_category_relationships(df)
    is_part_of_df = get_talk_event_relationships(df)

    # Subset specific DataFrames
    gives_talk_df = speaker_talk_category_df.select("speaker", "talk", "date").rename(
        {"speaker": "from", "talk": "to", "date": "date"}
    )
    relates_to_df = speaker_talk_category_df.select("talk", "category").rename(
        {"talk": "from", "category": "to"}
    )

    # Create tables
    create_tables(conn)

    # Insert nodes
    conn.execute("COPY Speaker FROM speakers_df")
    conn.execute("COPY Talk FROM talks_df")
    conn.execute("COPY Event(name) FROM events_df")
    conn.execute("COPY Category FROM categories_df")
    # Insert relationships
    conn.execute("COPY GIVES_TALK FROM gives_talk_df")
    conn.execute("COPY IS_PART_OF FROM is_part_of_df")
    conn.execute("COPY IS_CATEGORIZED_AS FROM is_categorized_as_df")

    # Write the event descriptions as properties
    write_cdl_description(conn, "Connected Data World 2021")
    write_knowledge_connexions_description(conn, "Knowledge Connexions 2020")
