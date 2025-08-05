import json
import os
from pathlib import Path

# Updated imports using the src package
from dotenv import load_dotenv

from baml_client import b

load_dotenv()
os.environ["BAML_LOG"] = "WARN"


def get_filenames(directory_path):
    """Get all filenames from the specified directory."""
    path = Path(directory_path)
    return [f.name for f in path.glob("*")]


def extract_entities_from_file(file_path):
    """Extract entities from a single file using BAML."""
    with open(file_path, "r") as data_file:
        text = data_file.read()

    entity = b.ExtractTags(text)
    # Convert Entity object to a dictionary using Pydantic's model_dump method
    return entity.model_dump()


def process_files(directory_path):
    """Process all files in the directory and extract entities."""
    all_entities = []
    filenames = get_filenames(directory_path)

    for filename in filenames:
        full_path = f"{directory_path}/{filename}"
        entities = extract_entities_from_file(full_path)
        all_entities.append({"filename": filename, "entities": entities})
        print(f"Finished processing file {filename}")

    return all_entities


def save_entities_to_json(entities, output_file):
    """Save extracted entities to a JSON file."""
    with open(output_file, "w") as f:
        json.dump(entities, f, indent=2)


def main():
    """Main function to orchestrate the entity extraction process."""
    directory_path = "./data"
    output_file = "entities.json"

    all_entities = process_files(directory_path)
    save_entities_to_json(all_entities, output_file)
    print(f"Extraction complete. Results saved to {output_file}")


if __name__ == "__main__":
    main()
