angular.module('searcherApp').controller('InputController', function ($scope, AppointmentService) {
    var vm = this;
    vm.submit = function () {
        AppointmentService.getAppointment($scope.registrationNumber).then(function (response) {
            console.log(response);
        });
    }
});
