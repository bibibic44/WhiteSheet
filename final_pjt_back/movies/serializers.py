from django.db.models import fields
from rest_framework import serializers
from .models import Comment, Movie, Review


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class ReviewDetailSerializer(serializers.ModelSerializer):
    comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comment_count = serializers.IntegerField(
        source='comment_set.count', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'content', 'rank', 'comment_set',
                  'comment_count', 'movie', 'movie_title', 'created_at', 'updated_at')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'content') #, 'user', 'username', 'created_at', 'updated_at')
        read_only_fields = ('review',)


class CommentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
