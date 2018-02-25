var gulp = require("gulp");
var pug = require("gulp-pug");
var uglify = require('gulp-uglify');
var livereload = require('gulp-livereload');
var http = require('http');
var st = require('st');

gulp.task("html", function() {
  gulp.src("pages/*.pug")
    .pipe(pug())
    .pipe(gulp.dest("../html/"))
    .pipe(livereload());
});

gulp.task("js", function() {
  gulp.src("js/*.js")
    .pipe(uglify())
    .pipe(gulp.dest("../html/js"))
    .pipe(livereload());
});

gulp.task("server", function(done) {
  http.createServer(
    st({
      path: "../html",
      cache: false
    })
  ).listen(1889, done);
});

gulp.task("watch", ["default", "server"], function() {
  livereload.listen({
    basePath: "../html/"
  });

  gulp.watch(["layouts/**/*.pug", "pages/**/*.pug"], ["html"]);
  gulp.watch(["js/**/*.js"], ["js"]);
});

gulp.task("default", ["js", "html"]);
