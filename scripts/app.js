var Ganban = (function () {

  function cardToHtml(card) {
    return `<div class="card panel panel-default" id='` + card.id + `'>
      <input type="hidden" id="id" value='` + card.id + `'></input>
      <input type="hidden" id="board" value='` + card.board_id + `'></input>
      <input type="hidden" id="content" value='` + card.content + `'></input>
      <div class="panel-body">
        <p><strong>#` + card.id + `</strong></p>
        <p class='content'>` + card.content + `</p>
        <div class='pull-left'>
          <span class="text-muted">` + card.author_email + `</span>
        </div>
        <div class='pull-right'>
          <button type="button" class="btn btn-xs btn-default edit-card">
            <span class='glyphicon glyphicon-pencil' aria-hidden="true"></span>
          </button>
          <button type="button" class="btn btn-xs btn-default delete-card">
            <span class='glyphicon glyphicon-trash' aria-hidden="true"></span>
          </button>
        </div>
      </div>
    </div>`;
  };

  function initCards() {
    $.get('/api/cards', function(cards){
        for(card in cards) {
            addCard(cards[card]);
        }
    });
  }

  function getCard(id, callback) {
    $.get('/api/cards/' + id, callback);
  };

  function createCard(card) {
    $.post('/api/cards', card, addCard);
  };

  function addCard(card) {
    var cardHtml = cardToHtml(card);
    $('.cards-board#' + card['board_id']).prepend(cardHtml);
  };

  function updateCard(card) {
    $.ajax({
      method: "PUT",
      url: '/api/cards/' + card.id,
      data: card,
      success: replaceCard
    })
  };

  function replaceCard(card) {
    var $card = $('.card#' + card.id);

    if ($card.data('board-id') == card.board_id) {
      var cardHtml = cardToHtml(card);
      $card.replaceWith(cardHtml);
    } else {
      $('.card#' + card['id']).remove();
      addCard(card);
    }
  };

  function deleteCard(id) {
    $.ajax({
      method: "DELETE",
      url: '/api/cards/' + id,
      success: function () { removeCard(id) }
    })
  };

  function removeCard(id) {
    $('.card#' + id).remove();
  };

  function onChannelMessage(message) {
    var message = JSON.parse(message.data);

    switch(message.action) {
      case 'create':
        addCard(message.card);
        break;
      case 'update':
        replaceCard(message.card);
        break;
      case 'destroy':
        removeCard(message.card.id);
        break;
    }
  };

  return {
    initCards: initCards,
    getCard: getCard,
    createCard: createCard,
    updateCard: updateCard,
    deleteCard: deleteCard,
    onChannelMessage: onChannelMessage
  };

})();

function Card(board_id, id, content) {
    this.board_id = board_id;
    this.id = id;
    this.content = content;
}

Card.getCardFromElement = function(el) {
    // We're putting this function on Card because if we make any changes to
    // Card (by adding new properties), we HAVE to update this function as well

    $form = $(el);
    return new Card(
        $form.find('#board').val(),
        $form.find('#id').val(),
        $form.find('#content').val()
    );
}

var setCardFormValues = function (card) {
  var $form = $('#cardForm');

  $form.find('#id').val(card.id),
  $form.find('#board').val(card.board_id),
  $form.find('#content').val(card.content)
};


var resetCardFormValues = function (board_id) {
  setCardFormValues(new Card(board_id, null, null));
};

$(document).ready(function () {

  var drake = dragula({
    containers: $('.cards-board').toArray()
  });

  drake.on('drop', function (el, target, source, sibling) {
    var card = Card.getCardFromElement(el);
    card.board_id = $(target).attr('id');

    Ganban.updateCard(card);
  });

  $('.new-card').on('click', function(e) {
    var board = $(e.target).closest('.panel').find('.cards-board');
    var boardId = board.attr('id');

    resetCardFormValues(boardId);
    $('#cardModal').modal('show');
  });

  $('.save-card').on('click', function() {
    var card = Card.getCardFromElement($('#cardForm'));

    if (card.id === '') {
      Ganban.createCard(card);
    } else {
      Ganban.updateCard(card);
    }
    $('#cardModal').modal('hide');
  });

  $('.cards-board').on('click', '.edit-card', function(e) {
    var cardEl = $(e.target).closest('.card');

    card = Card.getCardFromElement(cardEl);

    setCardFormValues(card);
    $('#cardModal').modal('show');

    Ganban.getCard(card.id, function(card){
      setCardFormValues(card);
    });
  });

  $('.cards-board').on('click', '.delete-card', function(e) {
    var cardEl = $(e.target).closest('.card');
    card = Card.getCardFromElement(cardEl);
    Ganban.deleteCard(card.id);
  });

  Ganban.initCards();
});
