"""View for products and lessons."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, F, ExpressionWrapper, fields
from django.db.models.functions import Coalesce, Round
from django.contrib.auth.models import User
from .models import ProductAccess, Product
from .serializers import (ExtendedProductSerializer,
                          ProductLessonSerializer,
                          DetailProductLessonSerializer)


class StudentProduct(viewsets.ViewSet):
    """Get information about products available for students."""

    permission_classes = [IsAuthenticated]
    serializer_class = ProductLessonSerializer

    def get_queryset(self):
        user = self.request.user.pk
        queryset = Product.objects.filter(productaccess__user=user).annotate(
                owner_name=F('owner__username'),
                viewed_time_seconds=F('lesson__lessonview__viewed_time_seconds'),
                watched=F('lesson__lessonview__watched'),
                lesson_name=F('lesson__name')).values('id', 'name',
                                                      'owner_name',
                                                      'lesson_name',
                                                      'viewed_time_seconds',
                                                      'watched',
                                                      )

        return queryset

    def list(self, request):
        """List all products available for a student."""

        queryset = self.get_queryset()
        serializer = ProductLessonSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Get detail information about a product and lessons."""

        product_access = get_object_or_404(ProductAccess.objects,
                                           product_id=pk,
                                           user=request.user)

        lessons = Product.objects.filter(productaccess=product_access).annotate(
                owner_name=F('owner__username'),
                viewed_time_seconds=F('lesson__lessonview__viewed_time_seconds'),
                watched=F('lesson__lessonview__watched'),
                last_viewed_time=F('lesson__lessonview__last_viewed_time'),
                lesson_name=F('lesson__name')).values('id', 'name',
                                                      'owner_name',
                                                      'lesson_name',
                                                      'viewed_time_seconds',
                                                      'last_viewed_time',
                                                      'watched',
                                                )
        serializer = DetailProductLessonSerializer(lessons, many=True)
        return Response(serializer.data)


class AllProducts(viewsets.ViewSet):
    """List all products with statistics."""

    permission_classes = [IsAdminUser]
    serializer_class = ExtendedProductSerializer
    queryset = Product.objects.all().annotate(
            total_lessons_watched=Count('lesson__lessonview',
                                        distinct=True,
                                        filter=F('lesson__lessonview__watched')),
            total_seconds_watched=Sum('lesson__lessonview__viewed_time_seconds',
                                      distinct=True),
            total_students_with_access=Count('productaccess__user',
                                             distinct=True),
            total_users=Coalesce(User.objects.count(), 1),
            #Percentage counts product owners too and includes to total users.
            percentage_of_purchase=ExpressionWrapper(Round(
                (F('total_students_with_access') * 100.00) / F('total_users'), 1),
                output_field=fields.FloatField())).values('id', 'owner', 'name',
                                                          'total_lessons_watched',
                                                          'total_seconds_watched',
                                                          'total_students_with_access',
                                                          'percentage_of_purchase')

    def list(self, request):
        queryset = self.queryset
        serializer = ExtendedProductSerializer(queryset, many=True)
        return Response(serializer.data)

