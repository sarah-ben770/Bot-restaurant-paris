from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
VERIFY_TOKEN = "mon_token_123"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge'), 200
    return "Erreur", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'messages' in data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}):
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        phone = message['from']
        text = message['text']['body']
        reply = f"Bienvenue au Restaurant Paris! Vous avez dit: {text}"
        send_message(phone, reply)
    return jsonify({'status': 'ok'})

def send_message(phone, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {'Authorization': f'Bearer {WHATSAPP_TOKEN}'}
    data = {"messaging_product": "whatsapp", "to": phone, "text": {"body": text}}
    requests.post(url, headers=headers, json=data)
