$(function() {

  var loginForm = new Vue({
    el: "#loginForm",
    data: {
      username: "",
      password: "",
      hasSubmission: false,
      error: undefined
    },
    methods: {
      onSubmit: function() {
        this.error = undefined;
        this.hasSubmission = true;

        var data = {
          username: this.username,
          password: this.password,
        };

        $.post(HOST + "/users/authenticate", JSON.stringify(data), function(data) {
          if (data.status) {
            sessionStorage.setItem("token", data.token);

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
