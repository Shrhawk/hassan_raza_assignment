from django.urls import path

from product_stat_apis.views import *

urlpatterns = [
    path("user_login", UserLoginViewSet.as_view({"post": "create"}), name="user_login"),
    path(
        "user_logout", UserLogoutViewSet.as_view({"post": "create"}), name="user_logout"
    ),
    path(
        "get_profile",
        UserProfileViewSet.as_view({"get": "retrieve"}),
        name="get_profiles",
    ),
    path(
        "update_profile",
        UserProfileViewSet.as_view({"put": "update"}),
        name="update_user_profile",
    ),
    path("countries", CountryViewSet.as_view({"get": "list"}), name="countries"),
    path("city", CityViewSet.as_view({"get": "list"}), name="city"),
    # Sale
    path(
        "upload_sale_data",
        SalesDataViewSet.as_view({"post": "create"}),
        name="upload_sales_data",
    ),
    path(
        "user_sale_data",
        UserSalesDataViewSet.as_view({"get": "list"}),
        name="get_user_sales",
    ),
    path(
        "update_sale_data",
        UserSalesDataViewSet.as_view({"put": "update"}),
        name="update_sale_data",
    ),
    # Sale Stat
    path("sale_stats", SaleStatsViewSet.as_view({"get": "list"}), name="sale_stats"),
    # Graph
    path(
        "graph_sale_data",
        SaleGraphData.as_view({"get": "list"}),
        name="graph_sale_data",
    ),
]
