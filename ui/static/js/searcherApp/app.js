angular.module('searcherApp', ['ui.router', 'ngCookies', 'ngSanitize', 'pascalprecht.translate'])
    .run(function ($rootScope, $state) {
        var unregister = $rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
            $rootScope.previousStateName = fromState.name;
            $rootScope.previousStateParams = fromParams;
        });
        $rootScope.$on('$destroy', function () {
            unregister();
        });
        $rootScope.backToPreviousState = function () {
            $state.go($rootScope.previousStateName, $rootScope.previousStateParams);
        };

	$rootScope.$on('$translateChangeEnd', function(e, l) {
	    moment.locale(l.language);
	});
    })
    .config(function ($stateProvider, $urlRouterProvider, $interpolateProvider, $httpProvider, $translateProvider, staticUrl) {
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        $urlRouterProvider.otherwise('/');
        $translateProvider.useStaticFilesLoader({
            'prefix': staticUrl + 'locale/',
            'suffix': '.json'
        })
            .useCookieStorage()
            .preferredLanguage('en')
            .fallbackLanguage('en')
            .useSanitizeValueStrategy(null);

        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: 'partials/language.html'
            })
            .state('searching', {
                url: '/search',
                templateUrl: 'partials/searching-for.html'
            })
            .state('input', {
                url: '/input',
                templateUrl: 'partials/input.html',
                controller: 'InputController as ctrl'
            })
            .state('results', {
                url: '/search/:appointmentId',
                templateUrl: 'partials/results.html',
                controller: 'ResultsController as ctrl',
                resolve: {
                    appointment: function (AppointmentService, $stateParams, $rootScope) {
                        if ($rootScope.appointment){
                            return $rootScope.appointment;
                        }
                        return AppointmentService.getAppointment($stateParams.appointmentId).then(function (response) {
                            return response.data;
                        });
                    }
                }
            })
    });
