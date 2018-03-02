$(function() {

  if (sessionStorage.getItem("token")) {
    location.href = "mydiary.html";
  }

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
          "username": this.username,
          "password": this.password,
        };

        $.post(HOST + "/users/authenticate", JSON.stringify(data), function(data) {
          if (data.status && data.result) {
            sessionStorage.setItem("token", data.result.token);
            location.href = "mydiary.html";
          } else {
            this.error = data.error || "Invalid username or password";
          }

          this.hasSubmission = false;
        }.bind(this));
      }
    }
  });

});
