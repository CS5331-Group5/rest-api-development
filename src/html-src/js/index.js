$(function() {

  var diaries = new Vue({
    el: "#diaries",
    data: {
      entries: [{
        "id": 1,
        "title": "My First Project",
        "author": "ashrugged",
        "publish_date": "2013-02-27T13:37:00+00:00",
        "public": true,
        "text": "If you don't know, the thing to do is not to get scared, but to learn."
      }, {
        "id": 2,
        "title": "My Second Project",
        "author": "ashrugged",
        "publish_date": "2013-02-27T13:37:00+00:00",
        "public": true,
        "text": "If you don't know, the thing to do is not to get scared, but to learn."
      }]
    }
  });

});
