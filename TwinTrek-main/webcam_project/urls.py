# """webcam_project URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/3.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# # from django.contrib import admin
# # from django.urls import path, include
# # from django.views.generic import TemplateView
# # from django.conf import settings
# # from django.conf.urls.static import static
# # from webcam_app import views

# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# #     path('api/webcam-image/', views.webcam_image_view, name='webcam-image-view'),  # Updated view reference
# #     # path('api/webcam-image/<int:image_id>/', get_webcam_image, name='get-webcam-image'),
# #     path('', views.manual, name='webcam'),
# #     path('buggy_feed/',views.buggy_feed,name='buggy_feed'),
# #     path('api/get-coordinates/', views.get_coordinates, name='get_coordinates'),
# #     path('api/post-coordinates/', views.post_coordinates, name='post-coordinates'),
# #     path('api/get-buggy-coordinates/',views.getBuggyPosition,name = 'get-buggy-coordinates'),
# #     path('api/get-smoke-level/',views.getSmokeLevel,name = 'get-smoke-level'),
# #     path('api/get-gas-sensor-value/', views.get_gas_sensor_value, name='get_gas_sensor_value'),
# #     path('api/get-direction/',views.getDirection,name = 'get-direction'),
# #     path('api/get-obstacle-distance/',views.getUltrasonicDistance ,name = 'get-ultrasonic-distance'),
# #     path('manual-mode/', views.manual, name='manual-mode'),
# #     path('auto/', views.automatic, name='auto'),
    


# # ]

# # if settings.DEBUG:
# #     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# from django.contrib import admin
# from django.urls import path, re_path, include
# from django.views.generic import TemplateView
# from django.conf import settings
# from django.conf.urls.static import static
# from webcam_app import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/webcam-image/', views.webcam_image_view, name='webcam-image-view'),
#     path('api/get-coordinates/', views.get_coordinates, name='get_coordinates'),
#     path('api/post-coordinates/', views.post_coordinates, name='post_coordinates'),
#     path('api/get-buggy-coordinates/', views.getBuggyPosition, name='get-buggy-coordinates'),
#     path('api/get-smoke-level/', views.getSmokeLevel, name='get-smoke-level'),
#     path('api/get-gas-sensor-value/', views.get_gas_sensor_value, name='get_gas_sensor_value'),
#     path('api/get-direction/', views.getDirection, name='get-direction'),
#     path('api/get-obstacle-distance/', views.getUltrasonicDistance, name='get-ultrasonic-distance'),
#     path('buggy_feed/', views.buggy_feed, name='buggy_feed'),
#     path('api/get-detection/', views.get_detection, name = 'get-detection'),

#     # Serve the React frontend
#     re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html')),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('webcam_app.urls')),  # Include API URLs from webcam_app
    path('', TemplateView.as_view(template_name='index.html')),  # Serve the React frontend
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
