from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import ImageForm
from .models import Comment, Follow, Image, Like

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ImageSerializer, SearchUserSerializer, UserSerializer, CreateImageSerializer
from rest_framework import status

from rapidfuzz import process, fuzz

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

@login_required
def home(request):
    # -------------------------
    # UPLOAD IMAGE
    # -------------------------
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()

            return redirect("home")
    else:
        form = ImageForm()

    # -------------------------
    # FOLLOWING
    # -------------------------
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list("following_id", flat=True)

    # -------------------------
    # FEED
    # -------------------------
    images = (
        Image.objects
        .filter(
            Q(user=request.user) |
            Q(user_id__in=following_ids)
        )
        .select_related("user")
        .prefetch_related("likes", "comments__user")
        .order_by("-date")
    )

    # -------------------------
    # LIKED POSTS
    # -------------------------
    liked_image_ids = set(
        Like.objects
        .filter(
            user=request.user,
            image__in=images
        )
        .values_list("image_id", flat=True)
    )

    # -------------------------
    # PAGINATION
    # -------------------------
    paginator = Paginator(images, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "myapp/home.html",
        {
            "form": form,
            "img": page_obj,
            "images": page_obj,
            "page_obj": page_obj,
            "liked_image_ids": liked_image_ids,
        }
    )

@login_required
def toggle_like(request, image_id):
    if request.method != "POST":
        return redirect("home")

    image = get_object_or_404(Image, id=image_id)
    like, created = Like.objects.get_or_create(user=request.user, image=image)
    if not created:
        like.delete()

    return redirect(request.META.get("HTTP_REFERER") or "home")


@login_required
def add_comment(request, image_id):
    if request.method == "POST":
        image = get_object_or_404(Image, id=image_id)
        text = request.POST.get("text", "").strip()
        if text:
            Comment.objects.create(user=request.user, image=image, text=text[:500])

    return redirect(request.META.get("HTTP_REFERER") or "home")


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    images = (
        Image.objects
        .filter(user=profile_user)
        .prefetch_related("likes", "comments__user")
        .order_by("-date")
    )

    liked_image_ids = set(
        Like.objects
        .filter(user=request.user, image__in=images)
        .values_list("image_id", flat=True)
    )

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    following_users = User.objects.filter(
        followers__follower=profile_user
    ).order_by("username")

    return render(
        request,
        "myapp/profile.html",
        {
            "profile_user": profile_user,
            "img": images,
            "liked_image_ids": liked_image_ids,
            "is_following": is_following,
            "following_users": following_users,
        },
    )    

@login_required
def search_users(request):
    query = request.GET.get("q", "").strip()

    users = User.objects.filter(
        username__icontains=query
    ) if query else User.objects.none()

    return render(
        request,
        "myapp/search.html",
        {
            "query": query,
            "users": users,
        },
    )

class SearchUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get("q", "").strip()

        if not query:
            return Response([])

        # -------------------------
        # NORMAL SEARCH
        # -------------------------

        users = list(
            User.objects.filter(
                username__icontains=query
            ).order_by("username")
        )

        if users:
            serializer = SearchUserSerializer(
                users,
                many=True,
                context={"request": request}
            )

            return Response(serializer.data)

        # -------------------------
        # FUZZY SEARCH
        # -------------------------

        usernames = list(
            User.objects.values_list(
                "username",
                flat=True
            )
        )

        matches = process.extract(
            query,
            usernames,
            scorer=fuzz.WRatio,
            limit=5,
            score_cutoff=70
        )

        matched_usernames = [
            match[0]
            for match in matches
        ]

        if not matched_usernames:
            return Response([])

        matched_users = User.objects.filter(
            username__in=matched_usernames
        )

        # Preserve fuzzy ranking
        user_map = {
            user.username: user
            for user in matched_users
        }

        ordered_users = [
            user_map[username]
            for username in matched_usernames
            if username in user_map
        ]

        serializer = SearchUserSerializer(
            ordered_users,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

@login_required
def delete_image(request, image_id):
    if request.method != "POST":
        return redirect("home")

    image = get_object_or_404(Image, id=image_id)

    # Only the owner can delete the photo
    if image.user != request.user:
        return redirect("home")

    image.delete()

    return redirect(request.META.get("HTTP_REFERER") or "home")

@login_required
def delete_comment(request, comment_id):
    if request.method != "POST":
        return redirect("home")

    comment = get_object_or_404(Comment, id=comment_id)

    # Only the comment author can delete it
    if comment.user != request.user:
        return redirect("home")

    comment.delete()

    return redirect(request.META.get("HTTP_REFERER") or "home")


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    if user_to_follow != request.user:
        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

    return redirect(
        "profile",
        username=user_to_follow.username
    )

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)

    Follow.objects.filter(
        follower=request.user,
        following=user_to_unfollow
    ).delete()

    return redirect(
        "profile",
        username=user_to_unfollow.username
    )

class FeedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list("following_id", flat=True)

        images = (
            Image.objects
            .filter(
                Q(user=request.user) |
                Q(user_id__in=following_ids)
            )
            .select_related("user")
            .order_by("-date")
        )

        serializer = ImageSerializer(
    images,
    many=True,
    context={"request": request}
)

        return Response(serializer.data)
    
class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(
            request.user,
            context={"request": request}
        )

        return Response(serializer.data)
    
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(
            User,
            username=username
        )

        serializer = UserSerializer(
    user,
    context={"request": request}
)
        return Response(serializer.data)
    
class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)

        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        return Response(
            {"detail": "Following."},
            status=status.HTTP_200_OK
        )


class UnfollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)

        Follow.objects.filter(
            follower=request.user,
            following=user_to_unfollow
        ).delete()

        return Response(
            {"detail": "Unfollowed."},
            status=status.HTTP_200_OK
        )
    
class CreatePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateImageSerializer(
            data=request.data
        )

        if serializer.is_valid():
            image = serializer.save(
                user=request.user
            )

            return Response(
                ImageSerializer(
                    image,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(
            User,
            id=user_id
        )

        if target_user == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=400
            )

        Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        return Response(
            {"following": True}
        )

    def delete(self, request, user_id):
        target_user = get_object_or_404(
            User,
            id=user_id
        )

        Follow.objects.filter(
            follower=request.user,
            following=target_user
        ).delete()

        return Response(
            {"following": False}
        )