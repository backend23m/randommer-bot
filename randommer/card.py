import requests
from .randommer import Randommer


class Card(Randommer):
    def get_card(self, api_key: str, type=None) -> dict:
        '''get card from randommer
        
        Args:
            api_key (str): api key
            type (str): card type

        Returns:
            dict: card data
        '''
        endpoint = "Card"
        url = self.get_url() + endpoint # https://randommer.io/api/Card

        headers = {
            "X-Api-Key": api_key
        }

        if type is not None:
            payload = {
                "type": type
            }
            response = requests.get(url, params=payload, headers=headers)
        else:
            response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        
        return response.status_code

    def get_card_types(self, api_key: str) -> list:
        '''get cars types from randommer

        Args:
            api_key (str): api key
            
        Returns:
            list: list of types
        '''
        endpoint = "Card/Types"
        url = self.get_url() + endpoint # https://randommer.io/api/Card/Types

        headers = {
            "X-Api-Key": api_key
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()

        return response.status_code
