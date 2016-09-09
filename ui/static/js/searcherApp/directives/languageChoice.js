angular.module('searcherApp').directive('languageChoice', function($state, $cookies) {
    return {
        restrict: 'E',
        scope: {
            language: '=',
            changeLanguage: '&'
        },
        templateUrl: '/partials/directives/language-choice.html'
    };
});
