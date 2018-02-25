$(function() {

  // Health check
  var healthCheck = new Vue({
    el: "#health-check",
    data: {
      status: true
    }
  });

  // Maintainers
  var maintainers = new Vue({
    el: "#maintainers",
    data: {
      people: [
        "Maintainer A",
        "Maintainer B",
        "Maintainer C"
      ]
    }
  });

});
