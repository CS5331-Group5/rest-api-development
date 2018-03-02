$(function() {

  if (!sessionStorage.getItem("token")) {
    sessionStorage.setItem("message", "Please log in!");
    location.href = "login.html";
  }

  var diaries = new Vue({
    el: "#diaries",
    data: {
      entries: []
    }
  });

  $.post(HOST + "/diary", JSON.stringify({
    "token": sessionStorage.getItem("token")
  }), function(data) {
    if (data.status) {
      diaries.entries = data.result;
    }
  });

});
