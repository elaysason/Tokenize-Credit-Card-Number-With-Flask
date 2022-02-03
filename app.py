import luhn as fl
from uuid import uuid4
from schema import And, Or, Schema, Use, SchemaError
from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource
from waitress import serve

app = Flask(__name__)
api = Api(app)
credit_cards = {}


def card_check(input, method):
    """Checks if the input is legal and making small transitions on it.
    :param input: The input given to be a credit card and needs to be checked and transformed.
    :param method: The method which the credit card check is called from.
    :return: card: if the input is valid credit card and didn't exist before, the card.
    """

    try:
        if "credit-card" in list(input.keys()):
            card = input["credit-card"].replace(' ', '')
        else:
            app.logger.warning('| ' + method + ' request refused.' + 'Invalid JSON')
            raise abort(400, """Invlaid JSON, "credit-card" should be the key of your card""")
        card_parts = [digits for digits in card.split('-')]
        ## Assums structure of 4 part and '-' separting between them.
        is_valid = Schema(And([str], lambda x: (
                all([len(part) == 4 for part in card_parts]) and len(x) == 4))).validate(card_parts)
        is_valid_number = fl.verify(card.replace('-', ''))
        if is_valid_number:
            if card in list(credit_cards.values()):
                app.logger.warning('| ' + method + ' request refused.' + 'Credit card number already exists')
                abort(400, 'Credit card number already exists')
            return card
        else:
            app.logger.warning('| ' + method + ' request refused.' + 'Invalid credit card number according to '
                                                                     'Luhn Algorithm')
            abort(400, "Credit card number isn't valid according to Luhn Algorithm")
    except KeyError as err:
        app.logger.warning('| ' + method + ' request refused.' + 'Invalid JSON')
        raise abort(400, 'Invlaid JSON.')
    except SchemaError:
        app.logger.warning('| ' + method + ' request refused.' + 'Invalid credit card number')
        abort(400, "Credit card number structure isn't valid,Make sure your card is 16 digits long and separted to 4 equal part by -.")

        
class PostCard(Resource):
    """Enter a new credit card into the system"""

    def post(self):
        """Add the new credit card
        :return JSON with "token" as key and the token value if the card is valid else "message" as
        key and the key is the reason why.
        """
        json_input = request.get_json()
        token = uuid4()
        card = card_check(json_input, 'POST')
        credit_cards[str(token)] = card
        app.logger.info(' | Created new credit card. [credit_card = ' + credit_cards[str(token)] + ', token = ' + str(token) + ']')
        return jsonify({"token": token})

class Card(Resource):
    """Used to access an existing credit card in the system,"""

    def get(self, card_token):
        """Returns the credit card which is assigned to the token.
        :param card_token: The token which the credit card with that token should be changed
        :return JSON with "credit-card" as key and the credit card itself as value if the card is valid,
        else "message" with the reason why.
        """
        app.logger.debug(' |  Get credit card. [token = ' + card_token + ']')
        if str(card_token) in list(credit_cards.keys()):
            return jsonify({'credit-card': credit_cards[str(card_token)]})
        app.logger.warning(' | ' + 'GET' + ' request refused.' + 'No credit matching this token')
        abort(400,'No credit matching this token')

    def put(self, card_token):
        """Change the card which is assigned to the token.
        :param card_token: The token which the credit card with that token should be changed
        :return JSON with "token" with the token which was changed , and "credit-card"
        as key and the credit card itself as value if the new card is valid else "message" with
        the reason why the new card isn't valid.
        """
        json_input = request.get_json()
        card_number = ''
                app.logger.debug(' |  Get credit card. [token = ' + card_token + ']')
        if card_token not in credit_cards in list(credit_cards.keys()):
            app.logger.warning('| ' + 'PUT' + ' request refused.' + 'No credit matching this token')
            abort(400, 'No credit matching this token')
        card = card_check(json_input, 'PUT')
        credit_cards[card_token] = card
        return jsonify({'token': card_token, 'credit-card': credit_cards[card_token]})


api.add_resource(PostCard, '/creditcard')
api.add_resource(Card, '/creditcard/<string:card_token>')

if __name__ == "__main__":
    app.debug = True
    serve(app, host='localhost', port=8081, threads=1)
