from django.urls import path
from . import views

urlpatterns = [
    # Business management
    path('', views.business_list, name='business_list'),
    path('create/', views.create_business, name='create_business'),
    path('<int:business_id>/', views.business_detail, name='business_detail'),
    path('<int:business_id>/edit/', views.edit_business, name='edit_business'),

    # URL management
    path('<int:business_id>/update-url/', views.update_business_url, name='update_business_url'),
    path('<int:business_id>/recrawl/', views.recrawl_business, name='recrawl_business'),

    # Crawling
    path('<int:business_id>/crawl/', views.crawl_website, name='crawl_website'),
    path('<int:business_id>/crawl-method/', views.crawl_with_method, name='crawl_with_method'),

    # Data export
    path('<int:business_id>/export/', views.export_data, name='export_data'),

    # Content viewing
    path('page/<int:page_id>/', views.page_content, name='page_content'),
]