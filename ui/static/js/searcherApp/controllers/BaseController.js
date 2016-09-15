angular.module('searcherApp').controller('BaseController', function ($rootScope, LoadingOverlayService, $state,
                                                                     languages, $translate, $cookies, $sce, $translate) {
    var vm = this;
    vm.isCookiePolicyAccepted = $cookies.get('cookiePolicy');
    vm.languages = languages;
    vm.language = $translate.proposedLanguage() || $translate.use();
    vm.isRTL = vm.language && !(vm.language === 'en' || vm.language === 'el' || vm.language === 'kmr' || vm.language === 'pan');
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
        vm.isRTL = !(language.code === 'en' || language.code === 'el' || language.code === 'kmr' || language.code === 'pan');
        vm.language = language;
        $translate.use(language.code);
    };

    vm.navigateTo = function (name) {
        $state.go(name);
    };

    vm.getDirection = function () {
        return vm.isRTL ? 'rtl' : 'ltr'
    }

    $rootScope.translateToHtml = function(value) {
      console.log($translate.instant(value));
        // Defaults to treating trusted text as `html`
        return $sce.trustAsHtml($translate.instant(value));
    };
});
