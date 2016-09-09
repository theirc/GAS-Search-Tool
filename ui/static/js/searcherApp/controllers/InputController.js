angular.module('searcherApp').controller('InputController', function ($scope, AppointmentService, $state, $rootScope) {
    var vm = this;
    vm.submit = function () {
        AppointmentService.getAppointment($scope.registrationNumber).then(function (response) {
            if (response.data) {
                $rootScope.appointment = response.data;
                $state.go('results', {appointmentId: $scope.registrationNumber});
            }
            else {
                vm.noData = true;
            }
        });
    }
});
