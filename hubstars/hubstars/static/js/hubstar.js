var hubstar = angular.module('HubStar', ['ngMaterial', 'ngMessages']);

hubstar.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

hubstar.controller("AppController", function ($scope, GithubService, $mdDialog) {
  $scope.form = {};
  $scope.url_pattern = /https:\/\/github\.com\/\S+\/\S+/;
  $scope.results = null;
  $scope.working = false;
  $scope.errors = {};
  
  $scope.do_battle = function () {
    if ($scope.addForm.$valid) {
      $scope.working = true;
      
      GithubService.do_battle($scope.form)
        .success(function (data) {
          $scope.results = data;
        })
        .error(function (data) {
          $scope.errors = data.errors || {};
          $scope.addForm.url1.$error = {};
          $scope.addForm.url2.$error = {};
          
          if ($scope.errors.url1) {
            $scope.addForm.url1.$error = {custom: true};
          }
          
          if ($scope.errors.url2) {
            $scope.addForm.url2.$error = {custom: true};
          }
          
          $mdDialog.show(
            $mdDialog.alert()
              .title('Error')
              .content('There was an error collecting battle data.')
              .ariaLabel('Error')
              .ok('OK')
          );
        })
        .finally(function () {
          $scope.working = false;
        });
    }
  };
});

hubstar.service("GithubService", function ($http) {
  var GithubService = this;
  
  GithubService.do_battle = function (form_data) {
    return $http.post('/api/github-battle', form_data);
  };
  
  return GithubService;
});