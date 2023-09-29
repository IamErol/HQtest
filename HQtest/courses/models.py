from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    """Product object."""

    owner = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Lesson object."""

    products = models.ManyToManyField(Product)
    name = models.CharField(max_length=255)
    video_link = models.URLField()
    duration_seconds = models.IntegerField()

    def __str__(self):
        return str(self.name)


class ProductAccess(models.Model):
    """Product access object for storing users access to products."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Access to {self.product.name} for {self.user.username}"


    class Meta:
        verbose_name_plural = "accesses"

    def save(self, *args, **kwargs):
        existing_entry = ProductAccess.objects.select_related('Product').filter(user=self.user, product=self.product).exists()
        if not existing_entry: #Prevent duplicate entries.
            super().save(*args, **kwargs)


class LessonView(models.Model):
    """Lesson view object for storing details about lesson and interaction."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_time_seconds = models.IntegerField(default=0)
    watched = models.BooleanField(default=False)
    last_viewed_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set viewed status based on the viewed time compared to the lesson duration.
        if self.viewed_time_seconds >= 0.8 * self.lesson.duration_seconds:
            self.watched = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lesson viewed by {self.user.username}"
