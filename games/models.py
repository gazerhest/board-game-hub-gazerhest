from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=150, unique=True)
    country = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
            ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.country})"


class Designer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    class Meta:
            ordering = ['first_name', 'last_name']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class BoardGame(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_players = models.PositiveIntegerField(default=1)
    max_players = models.PositiveIntegerField(default=4)
    play_time_minutes = models.PositiveIntegerField()
    min_age = models.PositiveIntegerField(default=10)
    release_year = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    image_url = models.URLField(blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='games'
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.PROTECT,
        related_name='games'
    )
    designer = models.ForeignKey(
        Designer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='games'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
