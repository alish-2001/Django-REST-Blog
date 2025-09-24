from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenVerifySerializer
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
)
from .serializers import (
    UserCreateInputSerializer,
    UserCreateOutputSerializer,
    UserLoginInputSerializer,
    UserLoginOutputSerializer,
    UserProfileOutputSerializer,
    UserRequestOTPInputSerializer,
    UsersListSerializer,
    UserLogoutInputSerializer,
    UserVerifyAccountInputSerializer,
)

# ---------------------------
# Signup (Create user)
# POST /signup/
# ---------------------------
user_create_schema = extend_schema(
    summary="Create User (Signup)",
    description=(
        "Create a new user account. The request must include `email`, `password` and `confirm_password`.\n\n"
        "On success returns the created user representation (id, email, role, verification flags, etc)."
    ),
    tags=["Users"],
    request=UserCreateInputSerializer,
    responses={
        201: OpenApiResponse(
            response=UserCreateOutputSerializer,
            description="User created successfully"
        ),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Validation error")
    },
)

# ---------------------------
# Request OTP 
# POST /request-otp/
# ---------------------------
user_request_otp_schema = extend_schema(
    summary="Create An OTP",
    description=(
        "Creates an OTP. The request must include `email`.\n\n"
        "The input email must be a valid email address for a registered user in database which is not verified.\n\n"
    ),
    tags=["Users"],
    request=UserRequestOTPInputSerializer,
    responses={
        201: OpenApiResponse(
            response=UserCreateOutputSerializer,
            description="OTP created successfully"
        ),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Validation error")
    },
)



# ---------------------------
# Login
# POST /login/
# ---------------------------
user_login_schema = extend_schema(
    summary="Login (Obtain tokens)",
    description=(
        "Authenticate user using email and password. Returns access and refresh tokens and basic user info."
    ),
    tags=["Users"],
    request=UserLoginInputSerializer,
    responses={
        200: OpenApiResponse(
            response=UserLoginOutputSerializer,
            description="Authentication successful. Returns JWT access & refresh tokens and user info.",
            examples=[
                OpenApiExample(
                    "Login example",
                    value={
                        "access": "eyJhbGciOiJ...<access_token>...",
                        "refresh": "eyJhbGciOiJ...<refresh_token>...",
                        "username": "alice",
                        "first_name": "Alice",
                        "last_name": "Doe"
                    }
                )
            ],
        ),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Validation error"),
        401: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Invalid credentials"),
    },
)

# ---------------------------
# Profile
# GET /profile/
# ---------------------------
user_profile_schema = extend_schema(
    summary="Retrieve current user's profile",
    description="Return the authenticated user's profile information.",
    tags=["Users"],
    responses={
        200: OpenApiResponse(response=UserProfileOutputSerializer, description="User profile"),
        401: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Authentication required"),
    },
)

# ---------------------------
# Users List (admin)
# GET /users/
# ---------------------------
users_list_schema = extend_schema(
    summary="List users (admin only)",
    description="Return a list of users. Requires admin privileges.",
    tags=["Users"],
    parameters=[
        OpenApiParameter(name="page", location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT,
                         description="Page number (if pagination enabled)"),
        OpenApiParameter(name="search", location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.STR,
                         description="Search by username/email (if supported)")
    ],
    responses={
        200: OpenApiResponse(response=UsersListSerializer(many=True), description="List of users"),
        401: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Authentication required"),
        403: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Admin privileges required"),
    },
)

# ---------------------------
# Logout (blacklist refresh)
# POST /logout/
# ---------------------------
user_logout_schema = extend_schema(
    summary="Logout (Blacklist refresh token)",
    description=(
        "Invalidate the provided refresh token (blacklist). The request body must include the `refresh` token.\n\n"
        "Requires authentication."
    ),
    tags=["Users"],
    request=UserLogoutInputSerializer,
    responses={
        205: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Token blacklisted, user logged out",
                             examples=[OpenApiExample("Logout success", value={"message": "User Logged out Successfuly"})]),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Invalid refresh token"),
        401: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Authentication required"),
    },
)

token_refresh_schema = extend_schema(
    summary="Refresh access token",
    description=(
        "Exchange a valid refresh token for a new access token. If refresh token rotation "
        "is enabled the response may also include a new refresh token. This endpoint is "
        "provided by `rest_framework_simplejwt` and is publicly accessible."
    ),
    tags=["Users"],
    request=TokenRefreshSerializer,  # expects {"refresh": "<refresh_token>"}
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="New access token (and optionally a new refresh token).",
            examples=[
                OpenApiExample(
                    "Refresh success",
                    summary="Typical refresh response",
                    value={
                        "access": "eyJ0eXAiOiJKV1QiLCJh...<new_access_token>...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJh...<new_refresh_token>..."  # may be absent if rotation disabled
                    }
                )
            ],
        ),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Bad request (malformed or missing refresh token)"),
        401: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Invalid or expired refresh token"),
    },
    auth=None,  # explicitly mark public (SimpleJWT TokenRefreshView allows anonymous)
)

# ---------------------------
# Token Verify (simplejwt)
# POST /token/verify/
# ---------------------------
token_verify_schema = extend_schema(
    summary="Verify token validity",
    description=(
        "Verify whether a token (access or refresh) is valid. The request body should be "
        '`{"token": "<token_to_verify>"}`. This endpoint is provided by `rest_framework_simplejwt`.'
    ),
    tags=["Users"],
    request=TokenVerifySerializer,  # expects {"token": "<token>"}
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Token is valid (usually returns 200 with empty body).",
            examples=[OpenApiExample("Verify success", summary="Valid token", value={})],
        ),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Bad request (malformed payload)"),
        401: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Token is invalid or expired"),
    },
    auth=None,  # explicitly mark public
)

# ---------------------------
# Verify Account (OTP)
# POST /verify-account/
# ---------------------------
user_verify_account_schema = extend_schema(
    summary="Verify user account (OTP)",
    description=(
        "Verify a newly created user's account using a 5-digit verification code and the user's email."
    ),
    tags=["Users"],
    request=UserVerifyAccountInputSerializer,
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="User verified successfully",
            examples=[OpenApiExample("Verify example", value={"message": "User Verified Successfully"})]
        ),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Invalid code or request"),
        404: OpenApiResponse(response=OpenApiTypes.OBJECT, description="User or OTP not found"),
    }
)
