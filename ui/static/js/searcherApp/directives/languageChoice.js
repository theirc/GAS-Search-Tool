angular.module('searcherApp').directive('languageChoice', function($state, $cookies) {
    return {
        restrict: 'E',
        scope: {
            language: '=',
            changeLanguage: '&',
            navigateTo: '&'
        },
        templateUrl: '/partials/directives/language-choice.html'
    };
});
