angular.module('searcherApp').directive('forwardButton', function() {
    return {
        restrict: 'E',
        scope: {
            direction: '@'
        },
        templateUrl: '/partials/directives/forward-button.html'
    };
});
