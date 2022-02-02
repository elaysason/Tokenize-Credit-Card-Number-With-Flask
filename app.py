import luhn as fl
from uuid import uuid4
from schema import And, Or, Schema, Use, SchemaError
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, abort
from waitress import serve

app = Flask(__name__)
api = Api(app)
credit_cards = {}


class APIError(Exception):
    """All custom API Exceptions."""
    pass


class BadInput(APIError):
    """Custom User Input Error Class."""
    code = 400


@app.errorhandler(APIError)
def handle_exception(err):
    """Returns error as JSON if APIError or a child of it is raised."""
    message = err.args[0]
    method = err.args[1]
    app.logger.warning('| ' + method + ' request refused.' + message)
    if len(err.args) == 2:
        return jsonify({'error_message': message}), err.code
    return jsonify({'error_message': err.args[2]}), err.code


def card_check(input, method):
    """Checks if the input is legal and making small transitions on it.
    :param input: The input given to be a credit card and needs to be checked and transformed.
    :param method: The method which the credit card check is called from.
    :return: card: The input is valid credit card and didn't exist before, the card.
    """
    card = input.replace(' ', '')
    try:
        card_parts = [digits for digits in card.split('-')]
        json_input_parts = {"credit-card": card_parts}
        is_valid = Schema({"credit-card": And([str], lambda x: (
                all([len(part) == 4 for part in card_parts]) and len(x) == 4))}).validate(json_input_parts)
        is_valid_number = fl.verify(card.replace('-', ''))
        if is_valid_number:
            if card in list(credit_cards.values()):
                raise BadInput('Credit card number already exists', method)
            return card
        else:
            raise BadInput('Invalid credit card number', method, "Credit card number isn't valid")
    except KeyError as err:
        raise BadInput('Invalid JSON', 'POST')
    except SchemaError:
        raise BadInput('Invalid credit card number', method, "Credit card number structure isn't valid")


class Welcome(Resource):
    def get(self):
        return "Welcome to the toknizer app! Feel free to enter your credit card."


class PostCard(Resource):
    """Enter a new credit card into the system"""

    def post(self):
        """Add the new credit card
        :return JSON with "token" as key and the token value if the card is valid else "error_message" as
        key and the reason as value.
        """
        json_input = request.get_json()
        token = uuid4()
        card = card_check(json_input['credit-card'], 'POST')
        credit_cards[str(token)] = card
        app.logger.info(' | Created new credit card. [credit_card = ' + card + ', token = ' + str(token) + ']')
        return jsonify({"token": token})


class Card(Resource):
    """Used to access an existing credit card in the system."""

    def get(self, card_token):
        """Returns the credit card which is assigned to the token.
        :param card_token: The token which the credit card with that token should be changed
        :return JSON with "credit-card" as key and the credit card itself as value
        """
        try:
            app.logger.debug(' |  Get credit card. [token = ' + card_token + ']')
            return jsonify({'credit-card': credit_cards[card_token]})
        except KeyError:
            raise BadInput('No credit matching this token', 'GET')

    def put(self, card_token):
        """Change the card which is assigned to the token.
        :param card_token: The token which the credit card with that token should be changed
        :return JSON with "token" with the token which was changed , and "credit-card"
        as key and the credit card itself as value if the new card is valid.
        """
        json_input = request.get_json()
        card_number = ''
        app.logger.debug(' |  Get credit card. [token = ' + card_token + ']')
        try:
            old = credit_cards[card_token]
        except KeyError:
            raise BadInput('No credit matching this token', 'PUT')
        card = card_check(json_input['credit-card'], 'PUT')
        credit_cards[card_token] = card
        return jsonify({'token': card_token, 'credit-card': credit_cards[card_token]})


api.add_resource(Welcome, '/')
api.add_resource(PostCard, '/creditcard')
api.add_resource(Card, '/creditcard/<string:card_token>')

if __name__ == "__main__":
    app.debug = True
    serve(app, host='localhost', port=8081, threads=1)
