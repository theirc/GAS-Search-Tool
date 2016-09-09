angular.module('searcherApp').directive('inputForm', function () {
    return {
        restrict: 'E',
        scope: false,
        templateUrl: '/partials/directives/input-form.html'
    };
});
