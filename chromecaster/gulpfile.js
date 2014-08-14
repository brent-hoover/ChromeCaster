// Chromecaster - created with Gulp Fiction
var gulp = require("gulp");
var livereload = require("livereload");
var concat = require("gulp-concat");
gulp.task("default", [], function () {
    gulp.src([{"path":"./src/**/*.js"},{"path":"./lib/**/*.js"}])
        .pipe(concat("all.js"))
        .pipe(gulp.dest("./build/"));
});


gulp.task("reload", function () {
    gulp.src(["./build/",""])
        .pipe(livereload())
});
gulp.task("watch", ["reload"], function () {
    gulp.watch("./staticsrc/**/*.js", ["default","reload"]);
    gulp.watch("./lib/**/*.js", ["default","reload"]);
});
