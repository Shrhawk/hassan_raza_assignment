from django.urls import path

from product_stat_apis.views import (
    UserLoginViewSet,
    UserLogoutViewSet,
    UserProfileViewSet,
    CountryViewSet,
    CityViewSet,
    SalesDataViewSet,
    UserSalesDataViewSet,
    SaleStatsViewSet,
    SaleGraphData,
)

urlpatterns = [
    path("user_login", UserLoginViewSet.as_view(), name="user_login"),
    path("user_logout", UserLogoutViewSet.as_view(), name="user_logout"),
    path(
        "get_profile",
        UserProfileViewSet.as_view(),
        name="get_profiles",
    ),
    path(
        "update_profile",
        UserProfileViewSet.as_view(),
        name="update_user_profile",
    ),
    path("countries", CountryViewSet.as_view(), name="countries"),
    path("city", CityViewSet.as_view(), name="city"),
    # Sale
    path(
        "upload_sale_data",
        SalesDataViewSet.as_view(),
        name="upload_sales_data",
    ),
    path(
        "user_sale_data",
        UserSalesDataViewSet.as_view(),
        name="get_user_sales",
    ),
    path(
        "update_sale_data",
        UserSalesDataViewSet.as_view(),
        name="update_sale_data",
    ),
    # Sale Stat
    path("sale_stats", SaleStatsViewSet.as_view(), name="sale_stats"),
    # Graph
    path(
        "graph_sale_data",
        SaleGraphData.as_view(),
        name="graph_sale_data",
    ),
]
