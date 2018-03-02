$(function() {

  var diaries = new Vue({
    el: "#diaries",
    data: {
      entries: []
    }
  });

  $.getJSON(HOST + "/diary", function(data) {
    if (data.status) {
      diaries.entries = data.result;
    }
  });

});
