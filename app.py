from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    try:
        data = request.get_json()
        # print("Received JSON:", data)

        parameters = data['queryResult']['parameters']

        source_currency = parameters['unit-currency']['currency']
        amount = parameters['unit-currency']['amount']
        target_currency = parameters['currency-name']

        print(source_currency)
        print(amount)
        print(target_currency)


        conversion_rate = fetch_conversion_factor(source_currency, target_currency)
        final_amount = amount * conversion_rate
        final_amount = round(final_amount, 2)

        response_text = f"{amount} {source_currency} is equal to {final_amount:.2f} {target_currency}"

        print(response_text)

        return jsonify({"fulfillmentText": response_text})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"fulfillmentText": "Sorry, I couldn't process your request right now."})

def fetch_conversion_factor(source, target):
    url = f"https://v6.exchangerate-api.com/v6/86adce36353e3e8797f6cba1/pair/{source}/{target}"
    response = requests.get(url).json()
    # print("API response:", response)

    if response.get("result") == "success":
        return response["conversion_rate"]
    else:
        raise ValueError("Conversion API failed")

if __name__ == '__main__':
    app.run(debug=True)
