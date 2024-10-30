import requests
from dotenv import load_dotenv
import os
import weaviate
from weaviate.classes.init import Auth
import json

# Create AgentPrompt object with prompt:str, result:bool
class AgentPrompt:
    def __init__(self, prompt: str, result: bool):
        self.prompt = prompt
        self.result = result

# Takes in an AgentPrompt object and uploads the prompt to Weaviate
def log_prompt(prompts_db, prompt: AgentPrompt):
  print("Logging prompt to Weaviate")

  try:
    prompts_db.data.insert({
      "prompt": prompt.prompt,
      "result": prompt.result,
    })
    print("Successfully logged prompt to Weaviate")
  except Exception as e:
    print(f"Error logging prompt to Weaviate: {e}")
    return False

  return True



def check_if_poisoned(prompt: str) -> bool:
    # Add validation for empty prompt
    if not prompt or prompt.strip() == "":
        return False  # or whatever default value makes sense for your use case

    # Query IS_POISONED_ENDPOINT with prompt, return result
    print(f"Checking if prompt is poisoned: {prompt}")
    """
    response = requests.post(IS_POISONED_ENDPOINT, json={"userInput": prompt})
    return response.json()["is_poisoned"]
    """
    load_dotenv()

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

    try:
        is_poisoned = client.collections.get("Is_Poisoned")

        response = is_poisoned.query.near_text(
            query=prompt,
            limit=1,
        )

        for obj in response.objects:
            print(json.dumps(obj.properties, indent=2))

        poisoned = response.objects[0].properties["is_poisoned"]
        if poisoned:
            return True
    except Exception as e:
        print(f"Error checking if prompt is poisoned: {e}")
    finally:
        client.close()

    return False
