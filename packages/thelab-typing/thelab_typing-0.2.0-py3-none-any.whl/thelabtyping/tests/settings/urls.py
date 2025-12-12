from django.urls import include, path

from thelabtyping.api.routing import Router

from ..sampleapp.views import (
    router_users_detail,
    router_users_list,
    router_users_post,
)

# Alternate method of building a router
unnamespaced_router = Router(basename="unnamespaced-router")
unnamespaced_router.route(
    "users/",
    name="users-list",
    get=router_users_list,
    post=router_users_post,
)
unnamespaced_router.route(
    "users/<int:pk>/",
    name="users-detail",
    get=router_users_detail,
)

urlpatterns = [
    path("api/", include("thelabtyping.tests.sampleapp.urls")),
    path("unnamespaced-router/", include(unnamespaced_router.urls)),
]
