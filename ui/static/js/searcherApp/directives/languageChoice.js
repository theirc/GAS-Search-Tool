angular.module('searcherApp').directive('languageChoice', function() {
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
