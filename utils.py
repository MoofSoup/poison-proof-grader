import requests

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



def check_if_poisoned(client, prompt: str) -> bool:
    # Query IS_POISONED_ENDPOINT with prompt, return result
    print(f"Checking if prompt is poisoned: {prompt}")
    """
    response = requests.post(IS_POISONED_ENDPOINT, json={"userInput": prompt})
    return response.json()["is_poisoned"]
    """
    # write logic that queries weaviate.
    # if any poisoned chunks are over a similarity threshold, return true
    # else, return false
    similarity_threshold= 0.75

    # construct the query to find similar poisoned chunks
    response = client.query.get("Is_Poisoned", ["content"]) \
      .with_near_text({
         "concepts": [prompt],
         "distance": similarity_threshold,

      }) \
      .with_where({
         "operator": "Equal",
         "path": ["is_poisoned"],
         "valueBoolean": True
      }) \
      .do()
     # Check the response
    poisons = response['data']['Get']['Question']
    if poisons:
        return True

    return False
