# this script gets the data stored in /dataset, and ingests it into weaviate
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, DataType, Property
from dotenv import load_dotenv
import os
from pathlib import Path
import pprint


def load_chunked_prompts() -> list[dict]:
    """
    load chunked prompts from directory.
    returns list of dicts with
    content
    is poisoned flag
    tag_name
    use_case
    """

    # Get the directory of the current script and construct path to data
    current_dir = Path(__file__).parent
    base_dir = current_dir / "data"

    prompts = []

    # get all files that start with chunk
    for file_path in Path(base_dir).glob('chunk-*'):
        tag_name = file_path.stem
        # determine if poisoned from file name
        is_poisoned = "poison" in tag_name.lower()

        #read content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        prompt_data = {
            "content": content,
            "is_poisoned": is_poisoned,
            "tag_name": tag_name,
            "use_case": "auto_grader",
        }
        prompts.append(prompt_data)

    return prompts


if __name__ == "__main__":
    # Load environment variables
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)

    # Retrieve API keys from environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    wcd_url = os.environ["WCD_URL"]
    wcd_api_key = os.environ["WCD_API_KEY"]

    # Connect to Weaviate
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=wcd_url,
        auth_credentials=Auth.api_key(wcd_api_key),
        headers={"X-OpenAI-Api-Key": openai_key},
    )

    print(client.is_ready())

    # Define collection with named vector for the `content` field
    is_poisoned = client.collections.create(
        "Is_Poisoned",
        vectorizer_config=[
            Configure.NamedVectors.text2vec_openai(
                name="content_vector",
                source_properties=["content"]
            )
        ],
        properties=[
            Property(name="content", data_type=DataType.TEXT),  # Change "text" to DataType.TEXT
            Property(name="is_poisoned", data_type=DataType.BOOL),
            Property(name="tag_name", data_type=DataType.TEXT),
            Property(name="use_case", data_type=DataType.TEXT),
        ]
    )

    is_poisoned = client.collections.get("Is_Poisoned")

    chunks_data = load_chunked_prompts()
    pp = pprint.PrettyPrinter(indent=2)
    print("Loaded chunks:")
    pp.pprint(chunks_data)

    # Insert data into Weaviate
    with is_poisoned.batch.dynamic() as batch:
        for d in chunks_data:
            batch.add_object(d)

    client.close()
