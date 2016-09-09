angular.module('searcherApp').factory('AppointmentService', function ($http, apiUrl) {
    return {
        getAppointment: function (registrationNumber) {
            return $http({
                method: 'POST',
                url: apiUrl + '/appointments/search',
                data: {'registration_number': registrationNumber}
            });
        }
    };
});
