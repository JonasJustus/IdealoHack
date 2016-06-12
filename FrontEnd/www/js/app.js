// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.services' is found in services.js
// 'starter.controllers' is found in controllers.js
angular.module('app', ['ionic', 'app.controllers', 'app.routes', 'app.services', 'app.directives', 'backand'])

.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if (window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleDefault();
    }
  });
})

.config(function (BackandProvider) {
  BackandProvider.setAppName('ideal');
  BackandProvider.setAnonymousToken('828a4c68-8f1f-42cc-8517-ad95dbfe4844');
})

.controller('AppCtrl', function($scope, listService) {
  $scope.lists = [];
  $scope.input = {};

  function getAlllists() {
    listService.getlists()
    .then(function (result) {
      $scope.lists = result.data.data;
    });
  }

  $scope.addlist = function() {
    listService.addlist($scope.input)
    .then(function(result) {
      $scope.input = {};
      // Reload our lists, not super cool
      getAlllists();
    });
  }

  $scope.deletelist = function(id) {
    listService.deletelist(id)
    .then(function (result) {
      // Reload our lists, not super cool
      getAlllists();
    });
  }

  getAlllists();
})

.service('listService', function ($http, Backand) {
  var baseUrl = '/1/objects/';
  var objectName = 'lists/';

  function getUrl() {
    return Backand.getApiUrl() + baseUrl + objectName;
  }

  function getUrlForId(id) {
    return getUrl() + id;
  }

  getlists = function () {
    return $http.get(getUrl());
  };

  addlist = function(list) {
    return $http.post(getUrl(), list);
  }

  deletelist = function (id) {
    return $http.delete(getUrlForId(id));
  };

  return {
    getlists: getlists,
    addlist: addlist,
    deletelist: deletelist
  }
});
