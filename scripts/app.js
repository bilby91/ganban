(function() {

  var Ganban = (function () {

    function cardToHtml(card) {
      return `<div class="card panel panel-default" id='` + card['id'] + `' data-board-id='` + card['board_id'] + `'>
        <div class="panel-body">
          <p><strong>#` + card['id'] + `</strong></p>
          <p class='content'>` + card['content'] + `</p>
          <div class='pull-left'>
            <span class="text-muted">` + card['author_email'] + `</span>
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

    function getCard(id, callback) {
      $.get('/api/cards/' + id, callback);
    };

    function createCard(board_id, content) {
      var params = {
        board_id: board_id,
        content: content
      };

      $.post('/api/cards', params, function (card) {
        var cardHtml = cardToHtml(card);
        $('.cards-board#' + card['board_id']).prepend(cardHtml);
      });
    };

    function updateCard(id, board_id, content) {
      $.ajax({
        method: "PUT",
        url: '/api/cards/' + id,
        data: {
          board_id: board_id,
          content: content
        },
        success: function(card) {
          var cardHtml = cardToHtml(card);
          $('.card#' + card['id']).replaceWith(cardHtml);
        }
      })
    };

    function deleteCard(id) {
      $.ajax({
        method: "DELETE",
        url: '/api/cards/' + id,
        success: function () {
          $('.card#' + id).remove();
        }
      })
    };

    return {
      getCard: getCard,
      createCard: createCard,
      updateCard: updateCard,
      deleteCard: deleteCard
    };

  })();

  var getCardFormValues = function () {
    var $form = $('#cardForm');

    return {
      id: $form.find('#id').val(),
      board_id: $form.find('#board').val(),
      content: $form.find('#content').val()
    }
  };

  var setCardFormValues = function (id, board_id, content) {
    var $form = $('#cardForm');

    $form.find('#id').val(id),
    $form.find('#board').val(board_id),
    $form.find('#content').val(content)
  };

  var resetCardFormValues = function (board_id) {
    setCardFormValues(null, board_id, null);
  };

  $(document).ready(function () {

    var drake = dragula({
      containers: $('.cards-board').toArray()
    });

    drake.on('drop', function (el, target, source, sibling) {
      var cardId = $(el).attr('id');
      var newBoardId = $(target).attr('id');

      Ganban.updateCard(cardId, newBoardId);
    });

    $('.new-card').on('click', function(e) {
      var board = $(e.target).closest('.panel').find('.cards-board');
      var boardId = board.attr('id');

      resetCardFormValues(boardId);
      $('#cardModal').modal('show');
    });

    $('.save-card').on('click', function() {
      var cardParams = getCardFormValues();

      if (cardParams['id'] === '') {
        Ganban.createCard(cardParams['board_id'], cardParams['content']);
      } else {
        Ganban.updateCard(cardParams['id'], cardParams['board_id'], cardParams['content']);
      }
      $('#cardModal').modal('hide');
    });

    $('.cards-board').on('click', '.edit-card', function(e) {
      var card = $(e.target).closest('.card');

      var id = card.attr('id');
      var board_id = card.data('board-id');
      var content = card.find('.content').html();

      setCardFormValues(id, board_id, content);
      $('#cardModal').modal('show');

      Ganban.getCard(id, function(card){
        setCardFormValues(card['id'], card['board_id'], card['content']);
      });
    });

    $('.cards-board').on('click', '.delete-card', function(e) {
      var card = $(e.target).closest('.card');
      var cardId = card.attr('id');
      Ganban.deleteCard(cardId);
    });

  });

})();
