var app = angular.module('application',[]);


app.controller('LoginCtrl',function($scope, $http) {

  $scope.error = 0;

  $scope.connect = function(){
    $scope.error = 0;
    $http({method: 'POST', url:'http://spacink.xyz:5000/login', data: $scope.payload}).then(
      function (response){
        window.location = '/';
      },
      function (response){
        if (response.status == 403)
          window.location = '/auth/password';
        else
          $scope.error = response.status;
      });
  }

  $scope.change = function(){
    // TODO: handle token
    $scope.error = 0;
    $http({method: 'POST', url: '/api/password', data: $scope.payload}).then(
      function (response){
        window.location = '/auth/login';
      },
      function (response){
        $scope.error = response.status;
      }
    )
  }

});
/*
var app = angular.module('application',[]);


app.controller('MainCtrl',function($scope, $http) {

  $scope.error = 0;

  $scope.connect = function(){
    $scope.error = 0;
    console.log($scope.payload);
    var dataObj = {
				username : $scope.payload.user,
				password : $scope.payload.password,
		};
    //$http.post('https://127.0.0.1:5000/login').then(
    $http({method: 'POST', url: 'http://127.0.0.1:5000/login', data: dataObj}).then(
      function (response){
        //window.location = '/';
          console.log("Log ma");
      },
      function (response){
        if (response.status == 403)
          window.location = '/auth/password';
        else
            console.log(response.status == 403, response.headers);
            $scope.error = response.status;
      });
  }

  $scope.change = function(){
    // TODO: handle token
    $scope.error = 0;
    $http({method: 'POST', url: '/api/password', data: $scope.payload}).then(
      function (response){
        window.location = '/auth/login';
      },
      function (response){
        $scope.error = response.status;
      }
    )
  }

});
*/