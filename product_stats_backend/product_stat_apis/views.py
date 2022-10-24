from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, parsers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from product_stat_apis.constants import SUCCESS, DATA, MESSAGE, ERROR
from product_stat_apis.models import User, Country, City, UserSales
from product_stat_apis.serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
    CountrySerializer,
    CitySerializer,
    UserSaleSerializer,
    UserSalesDataSerializer,
    SaleUpdateSerializer,
    SaleStatSerializer,
    SaleSerializerList,
)
from product_stat_apis.swagger_schemas.custom_schemas import (
    user_login_schema_response,
    user_profile_response_schema,
    update_user_profile_schema_response,
    user_logout_schema_response,
    country_schema_response,
    city_schema_response,
    upload_sale_data_schema_response,
    update_sale_data_response,
    sale_stat_response,
    sale_graph_response,
)


class UserLoginViewSet(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    auto_schema = None

    @swagger_auto_schema(responses=user_login_schema_response)
    def create(self, request, *args, **kwargs):
        """
        This function is used to log in user.
        """
        try:
            data = request.data
            serializer = self.serializer_class(data=data, context={"request": request})
            if serializer.is_valid():
                return Response(
                    {
                        SUCCESS: True,
                        MESSAGE: "User login successfully",
                        DATA: serializer.validated_data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {SUCCESS: False, ERROR: serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    auto_schema = None

    @swagger_auto_schema(responses=user_profile_response_schema)
    def retrieve(self, request, *args, **kwargs):
        """
        This function is used to get user profile.
        """
        try:
            serializer = self.get_serializer(request.user)
            return Response(
                {SUCCESS: True, MESSAGE: "User profile", DATA: serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(responses=update_user_profile_schema_response)
    def update(self, request, *args, **kwargs):
        """
        This function is used to update user profile.
        """
        try:
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        SUCCESS: True,
                        MESSAGE: "User profile updated",
                        DATA: serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {SUCCESS: False, ERROR: serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserLogoutViewSet(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    @swagger_auto_schema(responses=user_logout_schema_response)
    def create(self, request, *args, **kwargs):
        """
        This function is used to log out user.
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {SUCCESS: True, MESSAGE: "User logout successfully"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class CountryViewSet(generics.ListAPIView):
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    queryset = Country.objects.all()

    @swagger_auto_schema(responses=country_schema_response)
    def list(self, request, *args, **kwargs):
        """
        This function is used to get country list.
        """
        try:
            serializer = self.serializer_class(self.queryset.all(), many=True)
            return Response(
                {SUCCESS: True, MESSAGE: "Country list", DATA: serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class CityViewSet(generics.ListAPIView):
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    queryset = City.objects.all()

    @swagger_auto_schema(responses=city_schema_response)
    def list(self, request, *args, **kwargs):
        """
        This function is used to get city list.
        """
        try:
            country_id = request.query_params.get("country_id")
            if country_id:
                self.queryset = self.queryset.filter(country_id=country_id)
                if not self.queryset:
                    return Response(
                        {SUCCESS: False, MESSAGE: "No city found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                serializer = self.serializer_class(self.queryset, many=True)
                return Response(
                    {SUCCESS: True, MESSAGE: "City list", DATA: serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {SUCCESS: False, ERROR: "Country id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class SalesDataViewSet(generics.CreateAPIView):
    serializer_class = UserSaleSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    queryset = UserSales.objects.all()

    @swagger_auto_schema(responses=upload_sale_data_schema_response)
    def create(self, request, *args, **kwargs):
        """
        This function is used to upload sale data.
        """
        try:
            data = request.data
            serializer = self.serializer_class(data=data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {SUCCESS: True, MESSAGE: "Sales data saved", DATA: serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    SUCCESS: False,
                    MESSAGE: "Sales data not saved",
                    DATA: serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserSalesDataViewSet(generics.UpdateAPIView, generics.ListAPIView):
    serializer_class = UserSaleSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserSales.objects.all()

    def list(self, request, *args, **kwargs):
        """
        This function is used to get user sales data.
        """
        try:
            sales = self.queryset.filter(user=request.user).order_by("-sale_date")
            if not sales:
                return Response(
                    {SUCCESS: False, MESSAGE: "No sales data found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = UserSalesDataSerializer(sales, many=True)
            return Response(
                {SUCCESS: True, MESSAGE: "Sales data", DATA: serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses=update_sale_data_response, request_body=SaleUpdateSerializer
    )
    def update(self, request, *args, **kwargs):
        """
        This function is used to update user sales data.
        """
        try:
            sale = get_object_or_404(UserSales, request.data["id"])
            if not sale:
                return Response(
                    {SUCCESS: False, ERROR: "Sale not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = SaleUpdateSerializer(sale, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        SUCCESS: True,
                        MESSAGE: "Sales data updated",
                        DATA: serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {SUCCESS: False, ERROR: serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class SaleStatsViewSet(generics.ListAPIView):
    serializer_class = SaleStatSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserSales.objects.all()

    @swagger_auto_schema(responses=sale_stat_response)
    def list(self, request, *args, **kwargs):
        """
        This function is used to get sale stats.
        """
        try:
            sales = self.queryset.filter().first()
            if not sales:
                return Response(
                    {SUCCESS: False, ERROR: "Sales not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.serializer_class(sales, context={"request": request})
            return Response(
                {SUCCESS: True, MESSAGE: "Sales data", DATA: serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class SaleGraphData(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserSales.objects.all()
    serializer_class = SaleSerializerList

    @swagger_auto_schema(responses=sale_graph_response)
    def list(self, request, *args, **kwargs):
        """
        This function is used to get sale graph data.
        """
        try:
            sales = (
                self.queryset.filter(user=request.user.id)
                .values("sale_date", "product_name")
                .annotate(Count("sale_date"))
                .annotate(Count("product_name"))
                .annotate(no_of_sale=Count("sale_number"))
                .order_by("sale_date")
            )
            if not sales:
                return Response(
                    {SUCCESS: False, MESSAGE: "No sales data found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = SaleSerializerList(sales, many=True)
            return Response(
                {SUCCESS: True, MESSAGE: "Sales data", DATA: serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
