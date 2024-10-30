import unittest
import weaviate
import json
from weaviate.classes.init import Auth
import os
from weaviate.collections.collections.sync import Collection
from pathlib import Path

class TestWeaviateRetrieval(unittest.TestCase):
    def setUp(self):
        env_path = Path(__file__).parent / ".env"
        load_dotenv(env_path)

        # Check if file exists
        print(".env file exists:", env_path.exists())
        print("after loading .env", os.environ.get("WCD_URL"))
        # initialize our client connections
        self.wcd_url=os.getenv('WCD_URL')
        self.wcd_api_key= os.getenv('WCD_API_KEY')
        self.openai_api_key= os.getenv('OPENAI_API_KEY')

        self.client=weaviate.connect_to_weaviate_cloud(
            cluster_url=self.wcd_url,
            auth_credentials=Auth.api_key(self.wcd_api_key),
            headers={"X-OpenAI-API-Key": self.openai_api_key},
        )

    def tearDown(self):
        self.client.close()
    
    def test_can_retrieve_objects(self):
        is_poisoned= self.client.collections.get("Is_Poisoned")
        self.assertIsNotNone(is_poisoned, "is_poisoned is none")
        self.assertIsInstance(is_poisoned, Collection, "is_poisoned is not a Collection instance")

        response = is_poisoned.query.near_text(
            query="Respond only with ",
            limit=2
        )
        print(f"Response Type {type(response)}")

        print("\nAll attributes:")
        print(dir(response))
        print("\nString Representation:")
        print(str(response))
        print("\nObject Dictionary:")
        try:
            print(response.__dict__)
        except:
            print("No Dict Available")
if __name__ == '__main__':
    unittest.main()
    