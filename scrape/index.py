import requests
from bs4 import BeautifulSoup
import time

# Telegram Bot details
telegram_bot_token = '6549242285:AAHbDavPesyC-FnwDBIMrKJQkDHIR-JJ_1Y'
telegram_channel_username = '@jobbbaw'

# Function to send messages to Telegram
def send_message_to_telegram(message):
    send_message_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {
        "chat_id": telegram_channel_username,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(send_message_url, data=data)
    if response.status_code != 200:
        print("Failed to send message to Telegram channel.")

def get_products():
    response = requests.get('https://www.sheger.net/computers').text
    soup = BeautifulSoup(response, 'html.parser')

    products = soup.find_all('div', class_='col-product')
    message_count = 0  # Counter for the number of messages sent
    message_limit = 5  # Limit of messages to send

    for product in products:
        if message_count >= message_limit:
            break  # Stop sending messages if the limit is reached

        product_name = product.find('h3', class_='product-title').text.strip()
        product_provider = product.find('p', class_='product-user').text.strip()
        product_price = product.find('span', class_='price').text.strip()
        product_image = product.find_all('img', class_='img-product')
        product_image_url = product_image[0]['data-src'] if product_image else "Image not available"
        product_url_tag = product.find('a', href=True)
        product_url = product_url_tag['href'] if product_url_tag else "URL not available"

        # Creating message for Telegram
        message = f"<b>Product Name:</b> {product_name}\n\n"
        message += f"<b>Provider:</b> {product_provider}\n\n"
        message += f"<b>Price:</b> {product_price}\n\n"
        message += f"<b>Image URL:</b> {product_image_url}\n\n"
        message += f"<b>Product URL:</b> {product_url}\n"
        send_message_to_telegram(message)
        time.sleep(10)  # Wait for 10 seconds before sending the next message

        message_count += 1  # Increment the message counter

get_products()
