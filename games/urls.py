from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailAPIView.as_view(), name='category-detail'),
    path('publishers/', views.PublisherListCreateAPIView.as_view(), name='publisher-list-create'),
    path('publishers/<int:pk>/', views.PublisherDetailAPIView.as_view(), name='publisher-detail'),
    path('designers/', views.DesignerListCreateAPIView.as_view(), name='designer-list-create'),
    path('designers/<int:pk>/', views.DesignerDetailAPIView.as_view(), name='designer-detail'),
    path('games/', views.BoardGameListCreateAPIView.as_view(), name='game-list-create'),
    path('games/<int:pk>/', views.BoardGameDetailAPIView.as_view(), name='game-detail'),
]