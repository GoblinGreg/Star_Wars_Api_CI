from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)


def get_characters(search_name=None):
    api_url = "https://swapi.dev/api/people/"

    if search_name:
        api_url += f"?search={search_name}"

    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except (requests.ConnectionError, requests.Timeout, requests.RequestException) as e:
        print(f"API Error: {e}. Loading from local file...")
        try:
            with open('characters.json', 'r') as f:
                data = json.load(f)

            if search_name:
                results = [char for char in data if search_name.lower()
                           in char['name'].lower()]
                return results
            return data
        except FileNotFoundError:
            print("Local file not found!")
            return []


@app.route("/")
def index():
    search_name = request.args.get('name', '')
    characters = get_characters(search_name if search_name else None)
    return render_template('index.html', characters=characters, search_name=search_name)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        message = request.form.get('message')

        print(f"Email: {email}")
        print(f"Message: {message}")

        return render_template('thanks.html', email=email)

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
