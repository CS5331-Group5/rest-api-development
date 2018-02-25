$(function() {

  var registerForm = new Vue({
    el: "#registerForm",
    data: {
      username: "",
      password: "",
      fullname: "",
      age: undefined,
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
          fullname: this.fullname,
          age: this.age
        };

        $.post(HOST + "/users/register", JSON.stringify(data), function(data) {
          if (data.status) {
            sessionStorage.setItem("message", "You have registered successfully!");

            location.href = "login.html";
          } else {
            this.error = data.error;
          }

          console.log(data);

          this.hasSubmission = false;
        }.bind(this));
      }
    }
  });

});
