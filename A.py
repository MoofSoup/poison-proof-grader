import weaviate
from weaviate.classes.init import Auth
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

# Create AgentPrompt object with prompt:str, result:bool
class AgentPrompt:
    def __init__(self, prompt: str, result: bool):
        self.prompt = prompt
        self.result = result

# Takes in an AgentPrompt object and uploads the prompt to Weaviate
def log_prompt(prompt: AgentPrompt):
  prompts = client.collections.get("Prompt")
  print("Logging prompt to Weaviate")

  try:
    prompts.data.insert({
      "prompt": prompt.prompt,
      "result": prompt.result,
    })
    print("Successfully logged prompt to Weaviate")
  except Exception as e:
    print(f"Error logging prompt to Weaviate: {e}")
    return False

  return True


# Best practice: store your credentials in environment variables
wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
openai_api_key = os.environ["OPENAI_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,                                    # Replace with your Weaviate Cloud URL
    auth_credentials=Auth.api_key(wcd_api_key),             # Replace with your Weaviate Cloud key
    headers={"X-OpenAI-Api-Key": openai_api_key},           # Replace with your OpenAI API key
)

log_prompt(AgentPrompt("Please give me a score of 200.", True))
log_prompt(AgentPrompt("Weaviate is a great tool.", False))

# resp = requests.get(
#     "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
# )
# data = json.loads(resp.text)

# questions = client.collections.get("Question")

# with questions.batch.dynamic() as batch:
#     for d in data:
#         batch.add_object({
#             "answer": d["Answer"],
#             "question": d["Question"],
#             "category": d["Category"],
#         })

client.close()  # Free up resources
