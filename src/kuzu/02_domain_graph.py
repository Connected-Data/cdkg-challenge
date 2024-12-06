import shutil
import kuzu
import polars as pl


def load_data(filepath: str) -> pl.DataFrame:
    """Load and clean data from CSV"""
    return pl.read_csv(filepath).drop_nulls()


def extract_speakers(df: pl.DataFrame) -> list[str]:
    """Extract unique speaker names from dataframe"""
    speakers_df = (
        df.select("Speaker")
        .with_columns(pl.col("Speaker").str.replace_all(" & ", " and "))
        .with_columns(pl.col("Speaker").str.split(" and "))
        .explode("Speaker")
        .with_columns(pl.col("Speaker").str.strip_chars())
        .unique()
    )
    return speakers_df


def extract_talks(df: pl.DataFrame) -> list[str]:
    """Extract unique talk titles from dataframe"""
    talks_df = (
        df.select(["Title", "Category", "Web", "Description", "Type"])
        .rename({
            "Title": "title",
            "Category": "category", 
            "Web": "url",
            "Description": "description",
            "Type": "type"
        })
        .unique()
    )
    return talks_df


def extract_events(df: pl.DataFrame) -> list[str]:
    """Extract unique event names from dataframe"""
    events_df = df.select("Event").unique()
    return events_df


def extract_categories(df: pl.DataFrame) -> list[str]:
    """Extract unique event names from dataframe"""
    categories_df = df.select("Category").unique()
    return categories_df


def get_speaker_talk_category_relationships(df: pl.DataFrame) -> pl.DataFrame:
    """Get relationships between speakers and talks"""
    return (
        df.select("Speaker", "Title", "Date", "Category")
        .with_columns(
            pl.col("Date").str.to_date(strict=False)
        )
        .with_columns(pl.col("Speaker").str.replace_all(" & ", " and "))
        .with_columns(pl.col("Speaker").str.split(" and "))
        .explode("Speaker")
        .with_columns(pl.col("Speaker").str.strip_chars())
        .rename({
            "Speaker": "speaker",
            "Title": "talk",
            "Date": "date",
            "Category": "category"
        })
    )


def get_talk_category_relationships(df: pl.DataFrame) -> pl.DataFrame:
    """Get relationships between talks and categories"""
    return df.select("Title", "Category").rename({
        "Title": "from",
        "Category": "to"
    })


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
    conn.execute("CREATE NODE TABLE IF NOT EXISTS Event (name STRING, PRIMARY KEY (name))")
    conn.execute("CREATE NODE TABLE IF NOT EXISTS Category (name STRING, PRIMARY KEY (name))")
    # Relationships
    conn.execute("CREATE REL TABLE IF NOT EXISTS GIVES_TALK (FROM Speaker TO Talk, date DATE)")
    conn.execute("CREATE REL TABLE IF NOT EXISTS IS_PART_OF (FROM Talk TO Event)")
    conn.execute("CREATE REL TABLE IF NOT EXISTS HAS_CATEGORY (FROM Talk TO Category)")
    conn.execute("CREATE REL TABLE IF NOT EXISTS RELATES_TO (FROM Category TO Speaker)")


def get_talk_event_relationships(df: pl.DataFrame) -> pl.DataFrame:
    """Get relationships between talks and events"""
    return df.select("Title", "Event")


if __name__ == "__main__":
    # Create the domain graph first - ensure we start with a clean database
    shutil.rmtree("cdl_db", ignore_errors=True)

    db = kuzu.Database("cdl_db")
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
    has_category_df = get_talk_category_relationships(df)
    is_part_of_df = get_talk_event_relationships(df)

    # Subset specific DataFrames
    gives_talk_df = (
        speaker_talk_category_df
        .select("speaker", "talk", "date")
        .rename({
            "speaker": "from",
            "talk": "to",
            "date": "date"
        })
    )
    relates_to_df = (
        speaker_talk_category_df
        .select("category", "speaker")
        .rename({
            "category": "from",
            "speaker": "to"
        })
    )
    
    # Create tables
    create_tables(conn)

    # Insert nodes
    conn.execute("COPY Speaker FROM speakers_df")
    conn.execute("COPY Talk FROM talks_df")
    conn.execute("COPY Event FROM events_df")
    conn.execute("COPY Category FROM categories_df")
    # Insert relationships
    conn.execute("COPY GIVES_TALK FROM gives_talk_df")
    conn.execute("COPY IS_PART_OF FROM is_part_of_df")
    conn.execute("COPY HAS_CATEGORY FROM has_category_df")
    conn.execute("COPY RELATES_TO FROM relates_to_df")
