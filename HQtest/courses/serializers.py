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
        fields = ['id', 'name']


class ProductViewSerializer(serializers.ModelSerializer):
    lesson_view = LessonViewSerializer(source='lessonview_set',
                                       many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'owner', 'lesson_name', 'lesson_view']


class ProductLessonSerializer(ProductSerializer):
    """Product serializer for products and it's lessons information."""

    viewed_time_seconds = serializers.FloatField()
    watched = serializers.BooleanField()
    owner_name = serializers.CharField()
    lesson_name = serializers.CharField()

    class Meta:
        model = Product
        fields = ProductSerializer.Meta.fields + ['owner_name',
                                                  'lesson_name',
                                                  'viewed_time_seconds',
                                                  'watched',
                                                  ]


class DetailProductLessonSerializer(ProductLessonSerializer):
    """Detail serializer for product and it's lessons information."""

    last_viewed_time = serializers.DateTimeField()

    class Meta:
        model = Product
        fields = ProductLessonSerializer.Meta.fields + ['last_viewed_time']


class ExtendedProductSerializer(ProductSerializer):
    """Serializer with statistics about products and lessons."""

    total_lessons_watched = serializers.IntegerField()
    owner = serializers.IntegerField()
    total_seconds_watched = serializers.IntegerField()
    total_students_with_access = serializers.IntegerField()
    percentage_of_purchase = serializers.FloatField()

    class Meta:
        model = Product
        fields = ProductSerializer.Meta.fields + ['total_lessons_watched',
                                                  'total_seconds_watched',
                                                  'total_students_with_access',
                                                  'percentage_of_purchase',
                                                  'owner']