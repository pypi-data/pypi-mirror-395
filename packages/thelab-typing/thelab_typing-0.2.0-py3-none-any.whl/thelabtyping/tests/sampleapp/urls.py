from django.urls import include, path

from thelabtyping.api.routing import Router

from .views import (
    UserView,
    router,
    router_users_detail,
    router_users_list,
    router_users_post,
)

# Alternate method of building a router
alt_router = Router(basename="alt-router", enable_index=False)
alt_router.route(
    "users/",
    name="users-list",
    get=router_users_list,
    post=router_users_post,
)
alt_router.route(
    "users/<int:pk>/",
    name="users-detail",
    get=router_users_detail,
)

app_name = "sampleapp"
urlpatterns = [
    path("users/", UserView.as_view(), name="users-list"),
    path("router/", include(router.urls)),
    path("alt-router/", include(alt_router.urls)),
]
