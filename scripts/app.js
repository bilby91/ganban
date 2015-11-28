(function() {

  var Ganban = (function () {

    function newCard() {
      $('#cardModal').modal();
    };

    function createCard() {
      alert('not implemented yet.');
    };

    function editCard() {
      alert('not implemented yet.');
    };

    function updateCard() {
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
      newCard: newCard,
      createCard: createCard,
      editCard: editCard,
      updateCard: updateCard,
      updateCardStatus: updateCardStatus,
      deleteCard: deleteCard
    };

  })();

  $(document).ready(function () {

    var drake = dragula({
      containers: [
        document.getElementById('to-do'),
        document.getElementById('in-progress'),
        document.getElementById('done')
      ]
    });

    drake.on('drop', Ganban.updateCardStatus);
    $('.new-card').on('click', Ganban.newCard);
    $('.edit-card').on('click', Ganban.editCard);
    $('.delete-card').on('click', Ganban.deleteCard);

  });

})();
