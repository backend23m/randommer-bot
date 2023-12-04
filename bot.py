from settings import URL, API_KEY, cart_msg
import requests
from time import sleep
from randommer import card
from datetime import datetime


welcome_msg = '''
Hello and welcome to Randommer Bot!

🎉 Get ready for a diverse range of randomness with our exciting features. Here's a quick guide on how to use this bot:

1. /start: Use this command to receive a warm welcome message and get instructions on how to interact with the bot.

2. /card: Feeling lucky? Use this command to draw a random card and see what fortune it holds for you.

3. /finance: Looking for some crypto randomness? Type this command to get a random crypto address.

4. /misc: Explore the richness of various cultures! Use this command to receive information on 5 randomly selected cultures.

5. /name: Need a name on the spot? Type this command for a completely random full name.

6. /phone: If you're in need of phone numbers, use this command to get 5 randomly generated Uzbekistan phone numbers.

7. /social_number: Curious about social numbers? Use this command to get a randomly generated social number.

8. /text: Want some Lorem Ipsum text? Type this command to receive 20 words of normal Lorem Ipsum text.

9. /busywork: Need something to keep yourself occupied? Use this command for advice on productive and engaging tasks.
'''


def get_last_update(url: str) -> dict:
    endpoint = '/getUpdates'
    url += endpoint # https://api.telegram.org/bot{TOKEN}/getUpdates

    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()['result']
        if len(result) == 0:
            return 404
        last_update = result[-1]
        return last_update

    return response.status_code

def send_message(url: str, chat_id: str, text: str, mode=False):
    endpoint = '/sendMessage'
    url += endpoint

    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if mode:
        payload["parse_mode"] = "HTML"

    requests.get(url, params=payload)



def main(url: str):
    last_update_id = -1
    c = card.Card()

    while True:
        current_update = get_last_update(url)
        if current_update['update_id'] != last_update_id:
            user = current_update['message']['from']
            text = current_update['message'].get('text')

            if text is None:
                send_message(url, user['id'], 'send a message.')

            elif text == '/start':
                send_message(url, user['id'], welcome_msg)

            elif text == '/card':
                cart_data = c.get_card(api_key=API_KEY)
                date_object = datetime.fromisoformat(cart_data['date'])
                msg = cart_msg.format(
                    bank=cart_data['type'],
                    fullname=cart_data['fullName'],
                    number=cart_data['cardNumber'],
                    pin=cart_data['pin'],
                    cvv=cart_data['cvv'],
                    date=date_object.strftime('%Y-%m-%d')
                    )
                send_message(url, user['id'], msg, mode=True)

            elif text == '/busywork':
                advice = bored.get_activity_by_type('busywork')['activity']
                send_message(url, user['id'], advice)

            else:
                send_message(url, user['id'], 'error message.')

            last_update_id = current_update['update_id']

        sleep(0.5)

main(URL)
