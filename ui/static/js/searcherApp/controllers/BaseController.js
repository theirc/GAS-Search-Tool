angular.module('searcherApp').controller('BaseController', function ($rootScope, LoadingOverlayService, languages) {
    var vm = this;
    vm.languages = languages;

    var deregisterStateChangeStartHandler = $rootScope.$on('$stateChangeStart', function () {
        LoadingOverlayService.start();
    });

    var deregisterStateChangeEndHandler = $rootScope.$on('$stateChangeSuccess', function () {
        LoadingOverlayService.stop();
    });

    $rootScope.$on('$destroy', function () {
        deregisterStateChangeStartHandler();
        deregisterStateChangeEndHandler();
    });
});
