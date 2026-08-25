from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Follow, Image


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "profile_picture",
            "bio",
            "post_count",
            "is_following",
            "posts",
        ]

    def get_profile_picture(self, obj):
        request = self.context.get("request")

        if not hasattr(obj, "profile"):
            return None

        if not obj.profile.profile_picture:
            return None

        if request:
            return request.build_absolute_uri(
                obj.profile.profile_picture.url
            )

        return obj.profile.profile_picture.url

    def get_bio(self, obj):
        if not hasattr(obj, "profile"):
            return ""

        return obj.profile.bio

    def get_post_count(self, obj):
        return Image.objects.filter(
            user=obj
        ).count()

    def get_is_following(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return False

        if request.user == obj:
            return False

        return Follow.objects.filter(
            follower=request.user,
            following=obj
        ).exists()

    def get_posts(self, obj):
        posts = Image.objects.filter(
            user=obj
        ).order_by("-date")

        return ProfilePostSerializer(
            posts,
            many=True,
            context=self.context
        ).data

class ImageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    image = serializers.SerializerMethodField()

    likes = serializers.IntegerField(
        source="likes.count",
        read_only=True
    )

    liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = [
            "id",
            "username",
            "image",
            "date",
            "likes",
            "liked_by_me",
        ]

    def get_liked_by_me(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return False

        return obj.likes.filter(
            user=request.user
        ).exists()
    
    def get_image(self, obj):
        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(obj.photo.url)

        return obj.photo.url


class CreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["photo"]

class ProfilePostSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = [
            "id",
            "image",
            "date",
        ]

    def get_image(self, obj):
        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(
                obj.photo.url
            )

        return obj.photo.url
    
class SearchUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "profile_picture",
            "bio",
        ]

    def get_profile_picture(self, obj):
        request = self.context.get("request")

        if not hasattr(obj, "profile"):
            return None

        if not obj.profile.profile_picture:
            return None

        if request:
            return request.build_absolute_uri(
                obj.profile.profile_picture.url
            )

        return obj.profile.profile_picture.url

    def get_bio(self, obj):
        if not hasattr(obj, "profile"):
            return ""

        return obj.profile.bio