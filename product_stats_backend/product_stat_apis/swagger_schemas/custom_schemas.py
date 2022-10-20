from drf_yasg import openapi

user_login_schema_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "success": "true",
                "message": "User login successfully",
                "data": {
                    "user_id": 3,
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIj",
                    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjo",
                },
            }
        },
    ),
}

user_logout_schema_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "success": "true",
                "message": "User logout successfully",
            }
        },
    ),
}

user_logout_schema_body = openapi.Parameter(
    name="body",
    in_=openapi.IN_BODY,
    description="body",
    required=True,
    type=openapi.TYPE_OBJECT,
    properties={
        "refresh_token": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="refresh_token",
            example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjo",
        )
    },
)

user_profile_response_schema = {
    "200": openapi.Response(
        description="User Profile",
        examples={
            "application/json": {
                "success": "true",
                "message": "User profile",
                "data": {
                    "id": 1,
                    "name": "test",
                    "email": "test@gmail.com",
                    "country": "Us",
                    "city": "Us",
                    "age": 3,
                    "gender": "Male",
                },
            }
        },
    )
}

update_user_profile_schema_response = {
    "200": openapi.Response(
        description="User profile update response",
        examples={
            "application/json": {
                "success": "true",
                "message": "User updated successfully",
                "data": {
                    "id": 1,
                    "name": "test",
                    "email": "test@gmail.com",
                    "country": 1,
                    "city": 1,
                    "age": 3,
                    "gender": "Male",
                },
            }
        },
    ),
}

country_schema_response = {
    "200": openapi.Response(
        description="Country list",
        examples={
            "application/json": {
                "success": "true",
                "message": "Country list",
                "data": [{"id": 1, "name": "Pakistan"}, {"id": 2, "name": "US"}],
            }
        },
    )
}

city_schema_response = {
    "200": openapi.Response(
        description="City list",
        examples={
            "application/json": {
                "success": "true",
                "message": "City list",
                "data": [
                    {"id": 1, "country": 1, "name": "Lahore"},
                    {"id": 2, "country": 1, "name": "Karachi"},
                ],
            }
        },
    )
}

upload_sale_data_schema_response = {
    "200": openapi.Response(
        description="Upload sale data response",
        examples={
            "application/json": {
                "success": "true",
                "message": "Sale data uploaded successfully",
                "data": {},
            }
        },
    ),
}

update_sale_data_response = {
    "200": openapi.Response(
        description="Update sale data response",
        examples={
            "application/json": {
                "success": "true",
                "message": "Sale data updated successfully",
                "data": {
                    "id": 1,
                    "sale_date": "2022-09-11",
                    "product_name": "Scramble1",
                    "sale_number": 3,
                    "revenue": 12.0,
                },
            }
        },
    ),
}

sale_stat_response = {
    "200": openapi.Response(
        description="Sale stat response",
        examples={
            "application/json": {
                "success": "true",
                "message": "Sale stat",
                "data": {
                    "average_sales_for_current_user": 3.0,
                    "average_sales_for_all_users": 3.0,
                    "max_revenue_for_one_sale_current_user": {
                        "user_id": 1,
                        "revenue": 12.0,
                        "sale_id": 1,
                    },
                    "highest_revenue_product_for_user": {
                        "user_id": 1,
                        "revenue": 12.0,
                        "product_name": "Scramble",
                    },
                    "most_sold_product_for_user": {
                        "user_id": 1,
                        "product_name": "2",
                        "count": 3,
                    },
                },
            }
        },
    ),
}


sale_graph_response = {
    "200": openapi.Response(
        description="Sale graph response",
        examples={
            "application/json": {
                "success": "true",
                "message": "Sale graph",
                "data": [
                    {
                        "no_of_sale": 9,
                        "sale_date": "2022-09-10",
                        "product_name": "Scramble",
                    },
                    {
                        "no_of_sale": 9,
                        "sale_date": "2022-09-10",
                        "product_name": "ALPHA",
                    },
                ],
            }
        },
    ),
}
