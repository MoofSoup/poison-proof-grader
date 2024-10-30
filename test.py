import unittest
import weaviate
import json
from weaviate.classes.init import Auth
import os
from weaviate.collections.collections.sync import Collection


class TestWeaviateRetrieval (unittest.TestCase):
    def setUp(self):
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
            
    