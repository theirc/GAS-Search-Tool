angular.module('searcherApp').controller('BaseController', function ($rootScope, LoadingOverlayService, $state,
                                                                     languages, $translate, $cookies, $templateCache) {
    var vm = this;
    vm.isCookiePolicyAccepted = $cookies.get('cookiePolicy');
    vm.languages = languages;
    vm.language = $translate.proposedLanguage() || $translate.use();
    vm.isRTL = vm.language && !(vm.language.code === 'en' || vm.language.code === 'el');

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

    vm.acceptCookiePolicy = function () {
        var now = new Date();
        var exp = new Date(now.getFullYear() + 1, now.getMonth(), now.getDate());
        vm.isCookiePolicyAccepted = true;
        $cookies.put('cookiePolicy', 'true', {'expires': exp});
    };

    vm.changeLanguage = function (language) {
        console.log('clicked');
        vm.isRTL = !(language.code === 'en' || language.code === 'el');
        vm.language = language;
        $translate.use(language.code);
        $templateCache.removeAll();
        $state.reload();
    };
});
