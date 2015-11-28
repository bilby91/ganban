(function() {

  var Ganban = (function () {

    function createCard(status, content) {
      alert('not implemented yet.');
    };

    function updateCard(id, status, content) {
      alert('not implemented yet.');
    };

    function updateCardStatus(el, target, source, sibling) {
      var $el = $(el);
      var $target = $(target);
      var cardId = $el.data('id');
      var newStatus = target.id;

      console.log('Missing Server Interaction');
    };

    function deleteCard(e) {
      var $el = $(e.target);
      $el.closest('.card').remove();
      console.log('Missing Server Interaction');
    };

    return {
      createCard: createCard,
      updateCard: updateCard,
      updateCardStatus: updateCardStatus,
      deleteCard: deleteCard
    };

  })();

  var getCardFormValues = function () {
    var $form = $('#cardForm');

    return {
      id: $form.find('#id').val(),
      status: $form.find('#status').val(),
      content: $form.find('#content').val()
    }
  };

  var setCardFormValues = function (id, status, content) {
    var $form = $('#cardForm');

    $form.find('#id').val(id),
    $form.find('#status').val(status),
    $form.find('#content').val(content)
  };

  var resetCardFormValues = function (status) {
    setCardFormValues(null, status);
  };

  $(document).ready(function () {

    var drake = dragula({
      containers: [
        document.getElementById('to-do'),
        document.getElementById('in-progress'),
        document.getElementById('done')
      ]
    });

    drake.on('drop', Ganban.updateCardStatus);

    $('.new-card').on('click', function(e) {
      var container = $(e.target).closest('.panel').find('.cards-container');
      var containerId = container.attr('id');

      resetCardFormValues(containerId);
      $('#cardModal').modal();
    });

    $('.edit-card').on('click', function (e) {
      var card = $(e.target).closest('.card');

      var id = card.data('id');
      var status = card.data('status');
      var content = card.find('.content').html();

      setCardFormValues(id, status, content);
      $('#cardModal').modal();
    });

    $('.save-card').on('click', function() {
      var cardParams = getCardFormValues();

      if (cardParams['id'] == null) {
        Ganban.createCard(cardParams['status'], cardParams['content']);
      } else {
        Ganban.updateCard(cardParams['id'], ['status'], cardParams['content']);
      }
    });

    $('.delete-card').on('click', Ganban.deleteCard);

  });

})();
