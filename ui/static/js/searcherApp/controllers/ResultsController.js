angular.module('searcherApp').controller('ResultsController', function (appointment, $filter) {
    var vm = this;
    vm.appointment = appointment;
    if(appointment.datetime) {
        m = moment(appointment.datetime).tz('Europe/Athens');
        appointment.am_pm = '';
        appointment.hour = m.format('LT');
        appointment.date = m.format('L');
    }

    vm.translationData = {
        number: appointment.registration_number,
        hour: appointment.hour,
        am_pm: appointment.am_pm,
        time_of_day: $filter('translate')(appointment.time_of_day),
        date: appointment.date,
        office: appointment.office_name
    };
});
