angular.module('searcherApp').controller('ResultsController', function (appointment, $filter) {
    var vm = this;
    vm.appointment = appointment;
    vm.translationData = {
        number: appointment.registration_number,
        hour: appointment.hour,
        am_pm: appointment.am_pm,
        time_of_day: $filter('translate')(appointment.time_of_day),
        date: appointment.date,
        office: appointment.office_name
    };
});
