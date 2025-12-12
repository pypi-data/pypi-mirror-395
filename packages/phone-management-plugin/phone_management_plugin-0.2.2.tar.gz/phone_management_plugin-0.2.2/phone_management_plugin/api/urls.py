from netbox.api.routers import NetBoxRouter
from .views import PhoneManagementPluginRootView, PhoneNumberViewSet, PhoneNumberRangeViewSet, SimViewSet, SimAdminViewSet

router = NetBoxRouter()
router.APIRootView = PhoneManagementPluginRootView

router.register("phonenumbers", PhoneNumberViewSet)
router.register("phonenumberranges", PhoneNumberRangeViewSet)
router.register("sims", SimViewSet)
router.register("simadmins", SimAdminViewSet)

urlpatterns = router.urls