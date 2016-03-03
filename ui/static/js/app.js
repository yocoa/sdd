'use strict';

var app = angular.module('uiApp', ['ngRoute', 'ngAnimate']);

app.config(function($routeProvider) {
  $routeProvider
  .when('/home',
  {
    controller: 'HomeController',
    templateUrl: '/static/partials/home.html'
  })
  .when('/result',
  {
    controller: 'ResultController',
    templateUrl: '/static/partials/result.html'
  })
  .otherwise({ redirectTo: '/home' });
});

app.controller('RootController', function($rootScope) {
});

app.controller('ResultController', function($scope) {
});
