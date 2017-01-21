'use strict';   // See note about 'use strict'; below

var myApp = angular.module('myApp', [
 'ngRoute',
 'ngCookies'
]);


myApp.config(['$routeProvider',
     function($routeProvider) {
         $routeProvider.
             when('/', {
                 templateUrl: '/static/partials/index.html',
                 controller: 'IndexCtrl'  
             }).
             when('/home', {
                 templateUrl: '../static/partials/home.html',
                 controller: 'HomeCtrl'                                  
             }).
            when('/signin', {
                 templateUrl: '../static/partials/signin.html',
                 controller: 'SignInCtrl'
             }).             
            when('/signup', {
                 templateUrl: '../static/partials/signup.html',
                 controller: 'SignUpCtrl'

             }).
            when('/logout', {
                 templateUrl: '../static/partials/logout.html',
             }).                           
             otherwise({
                 redirectTo: '/'
             });
    }]);


myApp.controller('IndexCtrl',['$scope', '$cookies', function($scope,$cookies) {
       $scope.cookievalue = $cookies.get('sessionkey');
       console.log($scope.cookievalue)
}]);

myApp.controller('SignInCtrl', ['$window', '$scope', '$http','$cookies',function($window,$scope, $http,$cookies) {
        console.log("in Sign In ");
       // $scope.error = "Hello World boy2";

        // if user already loggedin, redirect him to home.
        if($cookies.get("sessionkey")){
            window.location.href = '/#/home';
            return;
        }


       $scope.signIn = function signIn($event) {
           console.log("Sign In call");
           var email  = $scope.email;
           var password = $scope.password;
           if(!email && !password)
                return

           console.log("email is "+ email+"  , "+password);                      
           // $event.preventDefault();        
            $http({
                method:'POST',
                url:'/signin',
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                },
                data:{email: email,password: password, sessionkey: 'someinvalid'}
            })
            .then(function(resp){
                console.log(resp);
                if(resp['status']==200 && resp['data']['status'] == "success" &&
                    resp['data']['sessionkey']){
                    var sessionkey = resp['data']['sessionkey']
                    $cookies.put("sessionkey",sessionkey);
                    window.location.href = '/#/home';
                }else if(resp['data']){
                    console.log(resp['data']['error']);
                    $scope.error = resp['data']['error'];
                }else
                    console.log("Some Error");
            },function(error){
                console.log(error);
            });


           // Call Flask Sign up here.
       };
}]);
myApp.controller('SignUpCtrl', ['$window', '$scope','$http','$cookies',function($window,$scope, $http,$cookies) {
        console.log("in Sign Up ");

        // if user already loggedin, redirect him to home.
        if($cookies.get("sessionkey")){
            window.location.href = '/#/home';
            return;
        }

       $scope.signUp = function signUp($event) {
           console.log("Sign Up call");
           // Call Flask Sign up here.
           var email  = $scope.email;
           var password = $scope.password;
            var username = $scope.username;

           if(!email || !password || !username)
                return           

            $http({
                method:'POST',
                url:'/signup',
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                },
                data:{username:username, email:email, password:password}
            })
            .then(function(resp){
                console.log("Responce is : ");                
                console.log(resp);
                if(resp['status']==200 && resp['data']['status'] == "success" &&
                    resp['data']['sessionkey']){
                    var sessionkey = resp['data']['sessionkey']
                    $cookies.put("sessionkey",sessionkey);
                    window.location.href = '/#/home';
                }else if(resp['data']){
                    console.log(resp['data']['error']);
                    $scope.error = resp['data']['error'];
                }else
                    console.log("Some Error");

            },function(error){
                console.log(error);
            });
       };
}]);

myApp.controller('HomeCtrl', ['$window', '$scope', '$http','$cookies', function($window,$scope,$http,$cookies) {
        console.log("in Homeee");

        $scope.listofnames = null;
        $scope.listofdummy = null;

        var sessionValue = $cookies.get("sessionkey");
        if (!sessionValue){

            window.location.href = '/#/signin';
            $scope.greeting = "You need to log in";

        }
        console.log("Inside getdummydata2");
        $http({
                method:'POST',
                url:'/getallusers',
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                },
                data:{ sessionkey: sessionValue}
             
        }).then(function(resp){
            // console.log(resp);
            if(resp['status'] == 200 && resp['data']['status'] == "success" &&
                resp['data']['users']){
                $scope.listofusers = resp['data']['users'];
            }else if(resp['data'] && !resp['data']['sessionkey']){
                console.log(resp['data']['error']);
                $scope.error = "Some error "+resp['data']['error'];
                // window.location.href = '/#/signin';
            }else
                console.log("Some Error");
        },function(error){
            console.log(error);
            $scope.listofusers = null;
        });


        $scope.signOut = function signOut($event) {
            console.log("Signing Out");
            // 1. Remove session. 
            // 2. Tell server to remove its session. 
            // if user already loggedin, redirect him to home.
            
            $http({
                method:'POST',
                url:'/signout',
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                },
                data : {sessionkey:sessionValue}
            })
            .then(function(resp){
                console.log(resp);
            },function(error){
                console.log(error);
            });
        

            $cookies.remove("sessionkey");            
            window.location.href = '/#/';

        }   

        $scope.timeTable = function timeTable($event) {




            $scope.listofdummy = null; 
            $scope.listofusers = null;

            $http({
                method:'GET',
                url:'/getviewtable',
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                },
                data : {sessionkey:sessionValue}
            })
            .then(function(resp){
                $scope.listofnames = resp['data'];
            },function(error){
                console.log(error);
                $scope.listofnames = null;
            });            
        }        

        $scope.dummyData = function dummyData($event) {
            $scope.listofnames = null; 
            $scope.listofusers = null;                       
            $http({
                method:'GET',
                url:'/getdummydata',
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                },
                data : {sessionkey:sessionValue}
            })
            .then(function(resp){
                console.log(resp);
                $scope.listofdummy = resp['data'];
            },function(error){
                console.log(error);
                $scope.listofdummy = null;
            });            
        }

}]);
