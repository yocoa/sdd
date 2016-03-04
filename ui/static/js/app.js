'use strict';

var app = angular.module('uiApp', ['ngRoute', 'ngAnimate']).config(function($sceProvider) {
    $sceProvider.enabled(false);
});

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
    })
    .otherwise({ redirectTo: '/home' });
});

app.controller('RootController', function($rootScope, $location, $window) {
    $rootScope.doSearch = function(query) {
        $location.path('/result/' + query);
    };
    $rootScope.setFocus = function() {
        var element = $window.document.getElementById('queryBox');
        if(element)
            element.focus();
    };
});

app.controller('HomeController', function() {
});

app.controller('ResultController', function($scope, $routeParams, HttpService) {
    $scope.currTab = '带外信息';
    $scope.changeTab = function(tab) {
        $scope.currTab = tab;
    };
    $scope.query = $routeParams.query;

    $scope.data = {
        bgp: null,
        visual: null,
        feature: null,
        relation: null,
    };
    HttpService.getBgp(function(data) {
        $scope.data.bgp = data;
    }, $routeParams.query);
    /*
    HttpService.getVisual(function(data) {
        $scope.data.visual = data;
    }, $routeParams.query);
    HttpService.getFeature(function(data) {
        $scope.data.feature = data;
    }, $routeParams.query);
    HttpService.getRelation(function(data) {
        $scope.data.relation = data;
    }, $routeParams.query);
    */
});

app.factory('HttpService', function($http) {
    return {
        getBgp: function(callback, query) {
            return $http.get('/bgp?query=' + query).success(callback);
        },
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
