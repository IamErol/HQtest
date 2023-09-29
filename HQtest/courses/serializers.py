from rest_framework import serializers
from .models import ProductAccess, Product, Lesson, LessonView


class LessonViewSerializer(serializers.ModelSerializer):
    """Serializer for lesson views."""

    class Meta:
        model = LessonView
        fields = ['viewed_time_seconds', 'watched', 'last_viewed_time']


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for lessons."""

    lesson_view = LessonViewSerializer(source='lessonview_set',
                                       many=True,
                                       read_only=True)
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_link', 'duration_seconds', 'lesson_view']


class ProductAccessSerializer(serializers.ModelSerializer):
    """Serializer for Product accesses."""

    lesson = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = ProductAccess
        fields = ['id', 'user', 'product', 'lesson']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product."""

    class Meta:
        model = Product
        fields = ['id', 'owner', 'name']