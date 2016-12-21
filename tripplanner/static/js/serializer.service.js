"use strict";

(function() {
    angular.module('tripplanner')
        .factory('SerializerService', SerializerService);

    function SerializerService() {
        return {
            encodeCredentialsBasicAuth: encodeBasicAuth,
            encodeCredentialsTokenAuth: encodeTokenAuth
        };

        /////////////////////////////

        function encodeBasicAuth(username, password) {
            var userPass = username + ":" + password;
            userPass = btoa(userPass);

            return 'Basic ' + userPass;
        }

        function encodeTokenAuth(token) {
            return ' Token ' + token;
        }
    }
})();