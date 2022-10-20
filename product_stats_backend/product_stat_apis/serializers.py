from django.db.models import Avg, Count
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _
from product_stat_apis.models import *
import pandas as pd


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.
    """

    email = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=True,
        max_length=128,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def validate(self, attrs) -> dict:
        data = self.context["request"].data
        email = data["email"]
        password = data["password"]
        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if not user.check_password(password):
                    raise serializers.ValidationError("Incorrect password")
            else:
                raise serializers.ValidationError("User does not exist")
        else:
            raise serializers.ValidationError("Email and password required")
        data_dict = dict()
        data_dict["user_id"] = user.id
        token = RefreshToken.for_user(user)
        data_dict["access_token"] = str(token.access_token)
        data_dict["refresh_token"] = str(token)
        return data_dict


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """

    class Meta:
        model = User
        fields = ["id", "name", "email", "country", "city", "age", "gender"]


class UserSaleSerializer(serializers.ModelSerializer):
    """
    Serializer for user sale.
    """

    user_id = serializers.IntegerField(required=False, read_only=True)
    sale_date = serializers.DateField(required=False, read_only=True)
    product_name = serializers.CharField(required=False, max_length=100, read_only=True)
    sale_number = serializers.IntegerField(required=False, read_only=True)
    revenue = serializers.FloatField(required=False, read_only=True)
    sale_data = serializers.FileField(write_only=True)

    class Meta:
        model = UserSales
        fields = "__all__"

    def create(self, validated_data) -> object:
        request = self.context["request"]
        data = request.data
        df = pd.read_csv(data["sale_data"])
        data_values = df.to_dict("records")
        for obj in data_values:
            obj["sale_date"] = pd.to_datetime(obj["date"]).date()
            obj["sale_number"] = obj["sales_number"]
            obj["product_name"] = obj["product"]
            UserSales.objects.create(
                user_id=request.user,
                sale_date=obj["sale_date"],
                product_name=obj["product_name"],
                sale_number=obj["sale_number"],
                revenue=obj["revenue"],
            )
        return data


class SaleSerializerList(serializers.ModelSerializer):
    """
    Serializer for sale list.
    """

    revenue = serializers.FloatField(required=False, write_only=True)
    sale_number = serializers.FloatField(required=False, write_only=True)
    no_of_sale = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = UserSales
        fields = "__all__"


class UserSalesDataSerializer(serializers.ModelSerializer):
    """
    Serializer for user sales data.
    """

    class Meta:
        model = UserSales
        fields = "__all__"


class SaleUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=False, read_only=True)
    """
    Serializer for sale update.
    """

    class Meta:
        model = UserSales
        fields = "__all__"

    def update(self, instance, validated_data) -> object:
        instance.sale_number = validated_data.get("sale_number", instance.sale_number)
        instance.revenue = validated_data.get("revenue", instance.revenue)
        instance.product_name = validated_data.get(
            "product_name", instance.product_name
        )
        instance.sale_date = validated_data.get("sale_date", instance.sale_date)
        instance.save()
        return instance


class SaleStatSerializer(serializers.ModelSerializer):
    """
    Serializer for sale stat.
    """

    average_sales_for_current_user = serializers.SerializerMethodField(
        "get_average_sales_for_current_user"
    )
    average_sale_all_user = serializers.SerializerMethodField(
        "get_average_sale_all_user"
    )
    max_revenue_for_one_sale_current_user = serializers.SerializerMethodField(
        "get_max_sale_for_one_sale_current_user"
    )
    highest_revenue_product_for_user = serializers.SerializerMethodField(
        "get_highest_revenue_product_for_user"
    )
    most_sold_product_for_user = serializers.SerializerMethodField(
        "get_most_sold_product_for_user"
    )

    class Meta:
        model = UserSales
        exclude = ["id", "sale_date", "product_name", "sale_number", "revenue"]

    def get_average_sales_for_current_user(self, obj):
        """
        Get average sales for current user.
        """
        try:
            user = self.context["request"].user
            sales = UserSales.objects.filter(user_id=user).aggregate(
                avg_sale=Avg("revenue")
            )
            return round(sales["avg_sale"], 2)
        except KeyError:
            return None

    def get_average_sale_all_user(self, obj):
        """
        Get average sale for all user.
        """
        try:
            sales = UserSales.objects.aggregate(avg_sale=Avg("revenue"))
            return round(sales["avg_sale"], 2)
        except KeyError:
            return None

    def get_max_sale_for_one_sale_current_user(self, obj):
        """
        Get max sale for one sale current user.
        """
        try:
            user = self.context["request"].user
            sales = UserSales.objects.filter(user_id=user).order_by("-revenue").first()
            data_dict = {
                "user_id": sales.user_id.id,
                "revenue": sales.revenue,
                "sale_id": sales.id,
            }
            return data_dict
        except KeyError:
            return None

    def get_highest_revenue_product_for_user(self, obj):
        """
        Get the highest revenue product for user.
        """
        try:
            user = self.context["request"].user
            sales = UserSales.objects.filter(user_id=user).order_by("-revenue").first()
            data_dict = {
                "user_id": sales.user_id.id,
                "revenue": sales.revenue,
                "product_name": sales.product_name,
            }
            return data_dict
        except KeyError:
            return None

    def get_most_sold_product_for_user(self, obj):
        """
        Get the most sold product for user.
        """
        try:
            user = self.context["request"].user
            sale = (
                UserSales.objects.filter(user_id=user)
                .values("product_name")
                .annotate(count=Count("product_name"))
            )
            sale = sorted(sale, key=lambda x: x["count"], reverse=True)
            data_dict = {
                "user_id": user.id,
                "product_name": sale[0]["product_name"],
                "count": sale[0]["count"],
            }
            return data_dict
        except KeyError:
            return None


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer for country.
    """

    class Meta:
        model = Country
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    """
    Serializer for city.
    """

    class Meta:
        model = City
        fields = "__all__"
