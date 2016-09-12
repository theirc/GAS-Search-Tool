angular.module('searcherApp').directive('backButton', function () {
    return {
        restrict: 'E',
        scope: {
            direction: '@'
        },
        link: function (scope) {
            var forwardButton = '/partials/directives/forward-button.html';
            var backButton = '/partials/directives/back-button.html';
            scope.contentUrl = scope.direction == 'ltr' ? backButton : forwardButton;
        },
        template: '<div ng-include="contentUrl"></div>'
    };
});
