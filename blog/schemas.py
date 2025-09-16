from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
)
from .serializers import (
    PostInputSerializer, PostOutputSerializer,
    CommentInputSerializer, CommentOutputSerializer,
    CategoryInputSerializer, CategoryOutputSerializer
)

# Shared parameters
SEARCH_PARAM = OpenApiParameter(
    name="search",
    location=OpenApiParameter.QUERY,
    description="Search text (title/body). Supported if selector implements it.",
    required=False,
    type=OpenApiTypes.STR,
)

PAGE_PARAM = OpenApiParameter(
    name="page",
    location=OpenApiParameter.QUERY,
    description="Page number (if pagination enabled).",
    required=False,
    type=OpenApiTypes.INT,
)

# -----------------------
# Posts
# -----------------------
post_list_schema = extend_schema(
    summary="List posts",
    description="Return a list of posts serialized with `PostOutputSerializer`.",
    tags=["Posts"],
    operation_id="blog_posts_list",
    parameters=[SEARCH_PARAM, PAGE_PARAM],
    responses={
        200: OpenApiResponse(
            response=PostOutputSerializer(many=True),
            description="A list of posts"
        )
    }
)

post_create_schema = extend_schema(
    summary="Create post",
    description="Create a new post. Authenticated users only. Request must conform to PostInputSerializer.",
    tags=["Posts"],
    request=PostInputSerializer,
    responses={
        200: OpenApiResponse(  # matches current view (returns 200); consider changing to 201 in code
            response=PostOutputSerializer,
            description="Created post representation"
        ),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Validation error"),
        401: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Authentication required"),
    },
)

post_detail_schema = extend_schema(
    summary="Retrieve a post",
    description="Return a single post by `id` using `PostOutputSerializer`.",
    tags=["Posts"],
    operation_id="blog_posts_detail",
    request=None,
    parameters=[
        OpenApiParameter(name="id", location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT),
    ],
    
    responses={
        200: OpenApiResponse(response=PostOutputSerializer, description="Post detail"),
        404: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Not found"),
    }
)

post_update_schema = extend_schema(
    summary="Update a post",
    description="Update an existing post. `PUT` expects full payload; `PATCH` allows partial. Author-only.",
    tags=["Posts"],
    parameters=[OpenApiParameter(name="id", location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT)],
    request=PostInputSerializer,
    responses={
        200: OpenApiResponse(response=PostOutputSerializer, description="Updated post representation"),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Validation error"),
        403: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Permission denied"),
        404: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Not found"),
    },
)

post_delete_schema = extend_schema(
    summary="Delete a post",
    description="Delete the specified post (author only). Returns 204 No Content.",
    tags=["Posts"],
    parameters=[OpenApiParameter(name="id", location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT)],
    responses={204: OpenApiResponse(response=OpenApiTypes.NONE, description="Deleted")},

)

# -----------------------
# Comments
# -----------------------
comment_list_schema = extend_schema(
    summary="List comments for a post",
    description="Return all comments for the post identified by `id`.",
    tags=["Comments"],
    parameters=[OpenApiParameter(name="id", location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT)],
    responses={200: OpenApiResponse(response=CommentOutputSerializer(many=True), description="List of comments")}
)

comment_create_schema = extend_schema(
    summary="Create comment",
    description="Create a comment on the post identified by `id`. Authenticated users only.",
    tags=["Comments"],
    parameters=[OpenApiParameter(name="id", location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT)],
    request=CommentInputSerializer,
    responses={
        201: OpenApiResponse(response=CommentOutputSerializer, description="Created comment"),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Validation error"),
        401: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Authentication required"),
        404: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Post not found"),
    },

)

comment_delete_schema = extend_schema(
    summary="Delete comment",
    description="Delete a comment. Admin-only (current implementation).",
    tags=["Comments"],
    parameters=[
        OpenApiParameter(name="post_pk", location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT),
        OpenApiParameter(name="comment_pk", location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT),
    ],
    responses={204: OpenApiResponse(response=OpenApiTypes.NONE, description="Deleted")},

)

# -----------------------
# Categories
# -----------------------
category_list_schema = extend_schema(
    summary="List categories",
    operation_id="blog_categories_list",
    description="Return list of categories (CategoryOutputSerializer).",
    tags=["Categories"],
    responses={200: OpenApiResponse(response=CategoryOutputSerializer(many=True), description="List of categories")}
)

category_detail_schema = extend_schema(
    summary="Retrieve a category",
    description="Return a single category by `pk`.",
    operation_id="blog_categories_detail",
    tags=["Categories"],
    parameters=[OpenApiParameter(name="pk", location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT)],
    responses={200: OpenApiResponse(response=CategoryOutputSerializer, description="Category detail"),
               404: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Not found")}
)

category_create_schema = extend_schema(
    summary="Create category",
    description="Create a new category. Admin-only (current implementation).",
    tags=["Categories"],
    request=CategoryInputSerializer,
    responses={
        200: OpenApiResponse(response=CategoryOutputSerializer, description="Created category (view currently returns 200)"),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Validation error"),
        403: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Admin required"),
    },
)

category_update_schema = extend_schema(
    summary="Update category",
    description="Update a category (Admin-only). PUT = full update, PATCH = partial update.",
    tags=["Categories"],
    parameters=[OpenApiParameter(name="pk", location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT)],
    request=CategoryInputSerializer,
    responses={
        200: OpenApiResponse(response=CategoryOutputSerializer, description="Updated category"),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Validation error"),
        403: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Admin required"),
        404: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Not found"),
    },
)

category_delete_schema = extend_schema(
    summary="Delete category",
    description="Delete the category (Admin-only).",
    tags=["Categories"],
    parameters=[OpenApiParameter(name="pk", location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT)],
    responses={204: OpenApiResponse(response=OpenApiTypes.NONE, description="Deleted")},
)

# -----------------------
# Like
# -----------------------
like_create_schema = extend_schema(
    summary="Like a post",
    description="Create a like for the post identified by `id`. Requires authentication. "
                "No request body is required — the authenticated user will be recorded as the liker.",
    tags=["Like"],
    parameters=[
        OpenApiParameter(
            name="id",
            location=OpenApiParameter.PATH,
            required=True,
            description="Primary key of the post to like",
            type=OpenApiTypes.INT,
        )
    ],
    request=OpenApiTypes.NONE,
    responses={
        201: OpenApiResponse(response=OpenApiTypes.NONE, description="Like created (no response body)"),
        400: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Bad request"),
        401: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Authentication required"),
        404: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Post not found"),
    },
)
