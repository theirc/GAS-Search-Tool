angular.module('searcherApp').directive('languageChoice', function($state, $cookies) {
    return {
        restrict: 'E',
        scope: {
            language: '='
        },
        templateUrl: '/partials/directives/language-choice.html',
        link: function(scope) {
            scope.chooseLangage = function(language) {
                $cookies.put('language', language);
            };
        }
    };
});
