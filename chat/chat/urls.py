
from django.contrib import admin
from django.urls import path, include
from chatbot import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentification.urls')), 
    path('', include('chatbot.urls')),  # Cela inclut les URLs définies dans l'application chatbot

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
