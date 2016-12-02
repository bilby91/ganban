import webapp2, json, logging, helper
import settings

from models.card import Card

json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if hasattr(obj, 'isoformat') else None)


class ApiHandler(helper.Entity, helper.Mailer, helper.Channel, webapp2.RequestHandler):
    def dispatch(self):
        super(ApiHandler, self).dispatch()
        self.response.headers['Content-Type'] = 'application/json'


class GetCardHandler(ApiHandler):
    def get(self, card_id):
        card = self.get_card(card_id)

        self.response.out.write(json.dumps(card.to_dict()))


class UpdateCardHandler(ApiHandler):
    def put(self, card_id):
        card = self.get_card(card_id)
        content = self.request.get('content')
        board_id = self.request.get('board_id')

        if content:
            card.content = content

        if board_id:
            card.board_key = self.get_board(board_id).key

        card.put()

        logging.info("Card with id: %s updated.", card.key.id())

        self.send_channel_message('update', card)
        self.response.out.write(json.dumps(card.to_dict()))


class CardHandler(ApiHandler):
    def get(self):
        ''' Get all cards '''
        cards = [card.to_dict() for card in Card.query()]
        self.response.out.write(json.dumps(cards))

    def post(self):
        ''' Create new card '''
        board = self.get_board(self.request.get('board_id'))

        card = Card(board_key=board.key,
                    content=self.request.get('content'),
                    author_key=self.current_ganban_user().key)
        card.put()

        if settings.SEND_EMAILS:
            self.send_new_card_email(card)

        logging.info("Card with id: %s created.", card.key.id())

        self.send_channel_message('create', card)
        self.response.out.write(json.dumps(card.to_dict()))


class DestroyCardHandler(ApiHandler):
    def delete(self, card_id):
        card = self.get_card(card_id)

        card.key.delete()

        logging.info("Card with id: %s deleted.", card_id)

        self.send_channel_message('destroy', card)
        self.response.out.write(json.dumps({}))
