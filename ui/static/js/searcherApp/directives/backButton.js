angular.module('searcherApp').directive('backButton', function() {
    return {
        restrict: 'E',
        scope: {
            direction: '@'
        },
        templateUrl: '/partials/directives/back-button.html'
    };
});
