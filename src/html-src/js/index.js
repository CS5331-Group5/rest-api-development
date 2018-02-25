$(function() {

  // {
  //   "id": 1,
  //   "title": "My First Project",
  //   "author": "ashrugged",
  //   "publish_date": "2013-02-27T13:37:00+00:00",
  //   "public": true,
  //   "text": "If you don't know, the thing to do is not to get scared, but to learn."
  // }
  Vue.component("diary-entry", {
    props: ["diary"],
    template: '<div class="card mb-5">' +
      '<div class="card-header">' +
      '<span class="text-secondary">{{ moment(diary.publish_date).format("lll") }}</span> by ' +
      '<strong>{{ diary.author }}</strong> ' +
      '<span class="badge badge-primary" v-if="!diary.public">Secret</span>' +
      '</div>' +
      '<div class="card-body">' +
      '<h2 class="card-title">{{ diary.title }}</h2>' +
      '<p class="card-text">{{ diary.text }}</p>' +
      '</div>' +
      '</div>'
  });

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
