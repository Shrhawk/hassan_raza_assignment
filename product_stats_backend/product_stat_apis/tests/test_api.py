import json
import unittest
import pytest
from django.db.models import Avg, Count
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from product_stat_apis.models import User, Country, City, UserSales


def api_client():
    """
    Create a new API client.
    """
    country = Country.objects.create(name="US")
    city = City.objects.create(name="New York", country=country)
    user = User.objects.create(
        email="test1@gmail.com",
        password="test",
        country=country,
        city=city,
        gender="Male",
        name="Test",
        role="User",
        age=20,
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client


class TestProductStats(unittest.TestCase):
    @pytest.mark.django_db
    def test_user_manager(self):
        """
        Test user manager.
        """
        user = User.objects.create_user(
            email="test@gmail.com",
            password="test",
            name="Test",
            role="User",
            age=20,
            gender="Male",
        )
        assert user.email == "test@gmail.com"
        assert user.name == "Test"
        assert user.role == "User"
        assert user.age == 20

    @pytest.mark.django_db
    def test_user_migrations(self):
        """
        Test user migrations.
        """
        self.email = "test@gmail.com"
        user = self.create_user()
        assert user.email == "test@gmail.com"
        assert user.name == "Test"
        assert user.role == "User"
        assert user.age == 20

    @pytest.mark.django_db
    def test_user_sale_migration(self):
        """
        Test user sale migration.
        """
        self.email = "test@gmail.com"
        user = self.create_user()
        self.user = user
        user_sale = self.create_sale()
        assert user_sale.user.id == user.id
        assert user_sale.product_name == "Test"

    @pytest.mark.django_db
    def test_average_sales_for_current_user(self):
        """
        Test average sales for current user.
        """
        self.email = "test@gmail.com"
        user = self.create_user()
        self.user = user
        self.create_sale()
        sales = UserSales.objects.filter(user=user).aggregate(avg_sale=Avg("revenue"))
        assert sales["avg_sale"] == 100

    @pytest.mark.django_db
    def test_average_sale_all_user(self):
        """
        Test average sale all user.
        """
        self.email = "test@gmail.com"
        user = self.create_user()
        self.user = user
        self.create_sale()
        sale = UserSales.objects.all().aggregate(avg_sale=Avg("revenue"))
        assert sale["avg_sale"] == 100

    @pytest.mark.django_db
    def test_get_max_sale_for_one_sale_current_user(self):
        """
        Test get max sale for one sale current user.
        """
        self.email = "test@gmail.com"
        user = self.create_user()
        self.user = user
        self.create_sale()
        user_sale = UserSales.objects.create(
            user=self.user,
            product_name="Test",
            revenue=500,
            sale_date="2021-01-01",
            sale_number=1,
        )
        sale = UserSales.objects.filter(user=user).order_by("-revenue").first()
        assert sale.revenue == 500
        assert sale.product_name == "Test"
        assert sale.id == user_sale.id

    @pytest.mark.django_db
    def test_get_highest_revenue_product_for_user(self):
        """
        Test get highest revenue product for user.
        """
        self.email = "test@gmail.com"
        user = self.create_user()
        self.user = user
        self.create_sale()
        user_sale = UserSales.objects.create(
            user=self.user,
            product_name="TOY",
            revenue=500,
            sale_date="2021-01-01",
            sale_number=1,
        )
        sale = UserSales.objects.filter(user=user).order_by("-revenue").first()
        assert sale.revenue == 500
        assert sale.product_name == sale.product_name
        assert sale.id == user_sale.id

    @pytest.mark.django_db
    def test_get_most_sold_product_for_user(self):
        """
        Test get most sold product for user.
        """
        self.email = "test@gmail.com"
        user = self.create_user()
        self.user = user
        self.create_sale()
        UserSales.objects.create(
            user=self.user,
            product_name="Test",
            revenue=500,
            sale_date="2021-01-01",
            sale_number=2,
        )
        sale = (
            UserSales.objects.filter(user=user)
            .values("product_name")
            .annotate(count=Count("product_name"))
        )
        sale = sorted(sale, key=lambda x: x["count"], reverse=True)
        assert sale[0]["product_name"] == "Test"
        assert sale[0]["count"] == 2

    @pytest.mark.django_db
    def test_login(self):
        """
        Test login.
        """
        self.email = "alpha99@gmail.com"
        user = self.create_user()
        user.set_password("test")
        user.save()
        valid_payload = {"email": "alpha99@gmail.com", "password": "test"}
        url = reverse("user_login")
        response = api_client().post(
            url,
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        api_response = response.json()
        assert response.status_code == 200
        assert api_response["success"]

    @pytest.mark.django_db
    def test_login_email_fail(self):
        """
        Test login email fail.
        """
        self.email = "alpha99@gmail.com"
        user = self.create_user()
        user.set_password("test")
        user.save()
        valid_payload = {"email": "alpha991@gmail.com", "password": "test1"}
        url = reverse("user_login")
        response = api_client().post(
            url,
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        api_response = response.json()
        assert response.status_code == 400
        assert not api_response["success"]

    @pytest.mark.django_db
    def test_login_password_fail(self):
        """
        Test login password fail.
        """
        self.email = "alpha99@gmail.com"
        user = self.create_user()
        user.set_password("test")
        user.save()
        valid_payload = {"email": "alpha99@gmail.com", "password": "test1"}
        url = reverse("user_login")
        response = api_client().post(
            url,
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        api_response = response.json()
        assert response.status_code == 400
        assert not api_response["success"]

    @pytest.mark.django_db
    def test_logout(self):
        """
        Test logout.
        """
        self.email = "log@gmail.com"
        user = self.create_user()
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        valid_payload = {"refresh_token": str(refresh)}

        url = reverse("user_logout")
        response = client.post(
            url,
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        api_response = response.json()
        assert response.status_code == 205
        assert api_response["success"]

    @pytest.mark.django_db
    def test_logout_fail(self):
        """
        Test logout fail.
        """
        url = reverse("user_logout")
        response = api_client().post(
            url,
            data={},
            content_type="application/json",
        )
        api_response = response.json()
        assert response.status_code == 400
        assert not api_response["success"]

    @pytest.mark.django_db
    def test_get_profile(self):
        """
        Test get profile.
        """
        url = reverse("get_profiles")
        response = api_client().get(url)
        api_response = response.json()
        assert response.status_code == 200
        assert api_response["data"]["email"] == "test1@gmail.com"
        assert api_response["data"]["gender"] == "Male"
        assert api_response["success"]

    @pytest.mark.django_db
    def test_get_profile_fail(self):
        """
        Test get profile fail.
        """
        url = reverse("get_profiles")
        client = APIClient()
        response = client.get(url)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_update_profile(self):
        """
        Test update profile.
        """
        url = reverse("update_user_profile")
        valid_payload = {
            "name": "Test",
            "email": "test11@gmail.com",
            "age": 20,
        }
        response = api_client().put(
            url,
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        api_response = response.json()
        assert response.status_code == 200
        assert api_response["success"]
        assert api_response["data"]["email"] == "test11@gmail.com"
        assert api_response["data"]["gender"] == "Male"

    @pytest.mark.django_db
    def test_update_profile_fail(self):
        """
        Test update profile fail.
        """
        url = reverse("update_user_profile")
        valid_payload = {
            "name": "Test",
            "email": "test11@gmail.com",
            "age": 20,
        }
        client = APIClient()
        response = client.put(
            url, data=json.dumps(valid_payload), content_type="application/json"
        )
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_countries(self):
        """
        Test countries.
        """
        url = reverse("countries")
        response = api_client().get(url)
        api_response = response.json()
        assert response.status_code == 200
        assert api_response["success"]
        assert api_response["data"][0]["name"] == "US"

    @pytest.mark.django_db
    def test_city(self):
        """
        Test city.
        """
        country_id = Country.objects.create(name="US")
        city = City.objects.create(name="New York", country=country_id)
        url = reverse("city")
        url = url + "?country_id=" + str(city.country.id)
        response = api_client().get(url)
        api_response = response.json()
        assert response.status_code == 200
        assert api_response["success"]
        assert api_response["data"][0]["name"] == "New York"

    @pytest.mark.django_db
    def test_city_fail(self):
        """
        Test city fail.
        """
        country_id = 33
        url = reverse("city")
        url = url + "?country_id=" + str(country_id)
        response = api_client().get(url)
        api_response = response.json()
        assert response.status_code == 404
        assert not api_response["success"]

    @pytest.mark.django_db
    def test_upload_sale_data(self):
        """
        Test upload sale data.
        """
        url = reverse("upload_sales_data")
        payload = {}
        files = [
            (
                "sale_data",
                (
                    "product_stat_apis/tests/sale.csv",
                    open("product_stat_apis/tests/sale.csv", "rb"),
                    "text/csv",
                ),
            )
        ]
        response = api_client().post(url, data=payload, files=files)
        api_response = response.json()
        assert response.status_code == 400
        assert not api_response["success"]

    @pytest.mark.django_db
    def test_get_user_sale_data(self):
        """
        Test get user sale data.
        """
        self.email = "testsale@gmail.com"
        user = self.create_user()
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        UserSales.objects.create(
            user=user,
            product_name="Test",
            revenue=100,
            sale_date="2021-01-01",
            sale_number=1,
        )
        url = reverse("get_user_sales")
        response = client.get(url)
        api_response = response.json()
        assert response.status_code == 200
        assert api_response["success"]
        assert api_response["data"][0]["product_name"] == "Test"
        assert api_response["data"][0]["revenue"] == 100
        assert api_response["data"][0]["sale_date"] == "2021-01-01"

    @pytest.mark.django_db
    def test_get_user_sale_data_fail(self):
        """
        Test get user sale data fail.
        """
        url = reverse("get_user_sales")
        response = api_client().get(url)
        api_response = response.json()
        assert response.status_code == 404
        assert not api_response["success"]

    @pytest.mark.django_db
    def test_update_user_sale_data(self):
        """
        Test update user sale data.
        """
        self.email = "updatesale@gmail.com"
        user = self.create_user()
        self.user = user
        client = self.create_test_client()
        user_sale = self.create_sale()
        url = reverse("update_sale_data")
        valid_payload = {
            "product_name": "Test1",
            "revenue": 200,
            "sale_date": "2021-01-01",
            "sale_number": 4,
            "id": user_sale.id,
        }
        response = client.put(
            url,
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        api_response = response.json()
        assert response.status_code == 200
        assert api_response["success"]
        assert api_response["data"]["product_name"] == "Test1"
        assert api_response["data"]["revenue"] == 200
        assert api_response["data"]["sale_date"] == "2021-01-01"
        assert api_response["data"]["sale_number"] == 4

    @pytest.mark.django_db
    def test_update_user_sale_data(self):
        """
        Test update user sale data.
        """
        url = reverse("update_sale_data")
        valid_payload = {
            "product_name": "Test1",
            "revenue": 200,
            "sale_date": "2021-01-01",
            "sale_number": 4,
            "id": 5,
        }
        response = api_client().put(
            url,
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        api_response = response.json()
        assert response.status_code == 400
        assert not api_response["success"]

    @pytest.mark.django_db
    def test_sale_stats(self):
        """
        Test sale stats.
        """
        self.email = "test99@gmail.com"
        user1 = self.create_user()
        UserSales.objects.create(
            user=user1,
            product_name="Test",
            revenue=100,
            sale_date="2021-01-01",
            sale_number=1,
        )
        client = APIClient()
        refresh = RefreshToken.for_user(user1)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.email = "test100@gmail.com"
        user2 = self.create_user()
        UserSales.objects.create(
            user=user2,
            product_name="Test",
            revenue=50,
            sale_date="2021-01-01",
            sale_number=1,
        )
        url = reverse("sale_stats")
        response = client.get(url)
        api_response = response.json()
        assert response.status_code == 200
        assert api_response["success"]
        assert api_response["data"]["average_sales_for_current_user"] == 100.0
        assert api_response["data"]["average_sale_all_user"] == 75.0
        assert (
            api_response["data"]["max_revenue_for_one_sale_current_user"]["revenue"]
            == 100.0
        )

    @pytest.mark.django_db
    def test_graph_sale_data(self):
        """
        Test graph sale data.
        """
        self.email = "test@gmail.com"
        user = self.create_user()
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        UserSales.objects.create(
            user=user,
            product_name="Test",
            revenue=100,
            sale_date="2021-01-01",
            sale_number=1,
        )
        url = reverse("graph_sale_data")
        response = client.get(url)
        api_response = response.json()
        assert response.status_code == 200
        assert api_response["success"]
        assert api_response["data"][0]["sale_date"] == "2021-01-01"
        assert api_response["data"][0]["no_of_sale"] == 1

    @pytest.mark.django_db
    def test_graph_sale_data_fail(self):
        """
        Test graph sale data fail.
        """
        url = reverse("graph_sale_data")
        response = api_client().get(url)
        api_response = response.json()
        assert response.status_code == 404
        assert not api_response["success"]

    def create_user(self) -> User:
        """
        Create user.
        return: User
        """
        country = Country.objects.create(name="US")
        city = City.objects.create(name="New York", country=country)
        user = User.objects.create(
            email=self.email,
            country=country,
            city=city,
            gender="Male",
            name="Test",
            role="User",
            age=20,
        )
        return user

    def create_sale(self) -> UserSales:
        """
        Create sale.
        return: UserSales object.
        """
        sale = UserSales.objects.create(
            user=self.user,
            product_name="Test",
            revenue=100,
            sale_date="2021-01-01",
            sale_number=1,
        )
        return sale

    def create_test_client(self) -> APIClient:
        """
        Create test client.
        return: client
        """
        client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        return client
