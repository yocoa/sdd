'use strict';

var app = angular.module('uiApp', ['ngRoute', 'ngAnimate']);

app.config(function($routeProvider) {
    $routeProvider
    .when('/home',
    {
        controller: 'HomeController',
        templateUrl: '/static/partials/home.html'
    })
    .when('/result/:query',
    {
        controller: 'ResultController',
        templateUrl: '/static/partials/result.html'
    });
    //.otherwise({ redirectTo: '/home' });
});

app.controller('RootController', function($rootScope, $location) {
    $rootScope.searchClickHandler = function(query) {
        $location.path('/result/' + query);
    };
});

app.controller('HomeController', function() {
});

app.controller('ResultController', function($scope, $routeParams, HttpService) {
    $scope.data = {
        info: null,
        visual: null,
        feature: null,
        relation: null,
    };
    /*
    HttpService.getInfo(function(data) {
        $scope.data.info = data;
    }, $routeParams.query);
    */
    HttpService.getVisual(function(data) {
        $scope.data.visual = data;
    }, $routeParams.query);
    HttpService.getFeature(function(data) {
        $scope.data.feature = data;
    }, $routeParams.query);
    HttpService.getRelation(function(data) {
        $scope.data.relation = data;
    }, $routeParams.query);
});

app.factory('HttpService', function($http) {
    return {
        getVisual: function(callback, query) {
            return $http.get('/visual?query=' + query).success(callback);
        },
        getFeature: function(callback, query) {
            return $http.get('/feature?query=' + query).success(callback);
        },
        getRelation: function(callback, query) {
            return $http.get('/relation?query=' + query).success(callback);
        }
    };
});
