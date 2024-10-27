import requests

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


IS_POISONED_ENDPOINT = "https://ferrets.b28.dev/is_poisoned"

def check_if_poisoned(prompt: str) -> bool:
    # Query IS_POISONED_ENDPOINT with prompt, return result
    print(f"Checking if prompt is poisoned: {prompt}")

    response = requests.post(IS_POISONED_ENDPOINT, json={"userInput": prompt})
    return response.json()["is_poisoned"]
