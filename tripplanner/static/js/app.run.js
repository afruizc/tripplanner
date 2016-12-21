"use strict";

(function () {
    angular.module('tripplanner')
        .run(checkRouting);

    checkRouting.$inject = ['$rootScope','$http', '$location', 'AuthService'];

    function checkRouting($rootScope, $http, $location, AuthService) {
        var routesNoAuth = ['/login'];

        var requiresAuth = function(route) {
            if (route == '/') {
                return false;
            }
            var needsAuth = true;
            routesNoAuth.forEach(function (elt) {
                if (route.startsWith(elt)) {
                    needsAuth = false;
                }
            });
            return needsAuth;
        };

        $rootScope.$on('$routeChangeStart', function (event, next, current) {
            console.log($location.url());
            if (requiresAuth($location.url()) && !AuthService.userLoggedIn()) {
                $location.path('/login');
            }
        });

        $http.defaults.headers.common['Content-Type'] = 'application/json'
    }
})();