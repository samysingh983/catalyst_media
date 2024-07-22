from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'),
    path('delete/', views.delete, name='delete'),
    path('upload/', views.upload_file, name='upload_file'),
    path('query_builder/', views.query_builder, name='query_builder'),
    path('upload_chunk/', views.process_file_chunk, name='process_file_chunk'),
    path('process/<int:file_id>/', views.process_file, name='process_file'),
    path('query_data/', views.query_data, name='query_data'),
]