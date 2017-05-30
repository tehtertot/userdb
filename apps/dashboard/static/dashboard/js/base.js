$(document).ready(function(){
  $('.confirm-delete').click(function(e){
    e.preventDefault();
    var username = this.getAttribute('data-object-name');
    var response = confirm("Are you sure you want to delete user " + username +"?");
    if (response) {
      $.ajax({
        url: e.currentTarget
      })
    }
  })
})
