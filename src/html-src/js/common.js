var HOST = "http://localhost:8080";

$(function() {

  $.ajaxSetup({
    contentType: "application/json"
  });

  // Navbar
  var navbar = new Vue({
    el: "#navbarToggler",
    data: {
      loggedIn: false,
      user: {},
      items: [{
          "name": "Home",
          "url": "index.html",
          "active": false,
          "annoymous": true,
          "login": true
        },
        {
          "name": "My Diary",
          "url": "mydiary.html",
          "active": false,
          "annoymous": false,
          "login": true
        },
        {
          "name": "New Diary",
          "url": "newdiary.html",
          "active": false,
          "annoymous": false,
          "login": true
        },
        {
          "name": "Register",
          "url": "register.html",
          "active": false,
          "annoymous": true,
          "login": false
        },
        {
          "name": "Login",
          "url": "login.html",
          "active": false,
          "annoymous": true,
          "login": false
        }
      ]
    },
    methods: {
      menu: function(items) {
        var menuItems = [],
          url = location.pathname;

        for (var i = 0, l = items.length; i < l; i++) {
          var v = items[i];

          if (this.loggedIn && v.login) {
            menuItems.push(v);
          } else if (!this.loggedIn && v.annoymous) {
            menuItems.push(v);
          }

          v.active = (url == "/" + v.url);
        }

        return menuItems;
      },
      logout: function() {
        var token = sessionStorage.getItem("token");

        $.post(HOST + "/users/expire", JSON.stringify({
          "token": token
        }), function(data) {
          if (data.status) {
            sessionStorage.setItem("message", "You have logged out!");
          }

          location.href = "index.html";
        });
      }
    }
  });

  var greeting = new Vue({
    el: "#greeting",
    data: {
      loggedIn: false,
      user: {}
    }
  });

  var token = sessionStorage.getItem("token");

  if (token) {
    $.post(HOST + "/users", JSON.stringify({
      "token": token
    }), function(data) {
      if (data.status) {
        navbar.loggedIn = true;
        navbar.user = data;

        greeting.loggedIn = true;
        greeting.user = data;
      } else {
        sessionStorage.removeItem("token");
      }
    });
  }

  // Health check
  var healthCheck = new Vue({
    el: "#health-check",
    data: {
      status: true
    }
  });

  $.getJSON(HOST + "/meta/heartbeat", function(data) {
    healthCheck.status = !!data.status;
  });

  // Maintainers
  var maintainers = new Vue({
    el: "#maintainers",
    data: {
      people: []
    }
  });

  $.getJSON(HOST + "/meta/members", function(data) {
    if (!!data.status) {
      maintainers.people = data.result;
    }
  });

});
