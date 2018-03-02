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
        $.post(HOST + "/users/expire", JSON.stringify({
          "token": sessionStorage.getItem("token")
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
      user: {},
      message: sessionStorage.getItem("message")
    }
  });

  if (sessionStorage.getItem("message")) {
    sessionStorage.removeItem("message");
    setTimeout(function() { greeting.message = undefined; }, 10000);
  }

  if (sessionStorage.getItem("token")) {
    $.post(HOST + "/users", JSON.stringify({
      "token": sessionStorage.getItem("token")
    }), function(data) {
      if (data.status) {
        navbar.loggedIn = true;
        navbar.user = data.result;

        greeting.loggedIn = true;
        greeting.user = data.result;
      } else {
        sessionStorage.removeItem("token");
      }
    });
  }

  // Health check
  var healthCheck = new Vue({
    el: "#health-check",
    data: {
      status: false
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

  // Dairy
  //
  // {
  //   "id": 1,
  //   "title": "My First Project",
  //   "author": "ashrugged",
  //   "publish_date": "2013-02-27T13:37:00+00:00",
  //   "public": true,
  //   "text": "If you don't know, the thing to do is not to get scared, but to learn."
  // }
  //
  Vue.component("diary-entry", {
    props: ["diary", "editable"],
    data: function() {
      return {
        error: undefined
      };
    },
    template: '<div class="card mb-5">' +
      '<div class="card-header">' +
      '<span class="text-secondary">{{ moment(diary.publish_date).format("lll") }}</span> by ' +
      '<strong>{{ diary.author }}</strong> ' +
      '<span class="badge badge-primary" v-if="!diary.public">Private</span>' +
      '</div>' +
      '<div class="card-body">' +
      '<h2 class="card-title">{{ diary.title }}</h2>' +
      '<p class="card-text">{{ diary.text }}</p>' +
      '</div>' +
      '<div class="card-footer" v-if="editable && !error">' +
      '<a href="#" class="card-link text-danger" v-on:click="deleteDiary">Delete</a>' +
      '<a href="#" class="card-link" v-on:click="togglePermission">{{ diary.public ? "Make Private" : "Make Public" }}</a>' +
      '</div>' +
      '<div class="card-footer text-danger" v-if="editable && error">{{ error }}</div>' +
      '</div>',
    methods: {
      togglePermission: function() {
        $.post(HOST + "/diary/permission", JSON.stringify({
          "token": sessionStorage.getItem("token"),
          "id": this.diary.id,
          "public": !this.diary.public
        }), function(data) {
          if (data.status) {
            location.reload();
          }

          this.error = data.error;
        });
      },
      deleteDiary: function() {
        $.post(HOST + "/diary/delete", JSON.stringify({
          "token": sessionStorage.getItem("token"),
          "id": this.diary.id
        }), function(data) {
          if (data.status) {
            location.reload();
          }

          this.error = data.error;
        });
      }
    }
  });

});
