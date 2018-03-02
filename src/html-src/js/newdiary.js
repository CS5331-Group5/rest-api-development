$(function() {

  if (!sessionStorage.getItem("token")) {
    sessionStorage.setItem("message", "Please log in!");
    location.href = "login.html";
  }

  var newdiaryForm = new Vue({
    el: "#newdiaryForm",
    data: {
      title: "",
      isPublic: false,
      text: "",
      hasSubmission: false,
      error: undefined
    },
    methods: {
      onSubmit: function() {
        this.error = undefined;
        this.hasSubmission = true;

        var data = {
          "token": sessionStorage.getItem("token"),
          "title": this.title,
          "public": this.isPublic,
          "text": this.text
        };

        $.post(HOST + "/diary/create", JSON.stringify(data), function(data) {
          if (data.status) {
            sessionStorage.setItem("message", "You have created a new diary successfully!");
            location.href = "mydiary.html";
          } else {
            this.error = data.error;
          }

          this.hasSubmission = false;
        }.bind(this));
      }
    }
  });

});
