
# from django.contrib import admin
from django.urls import path, include
from.views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', index, name='index'),
    path('add_todo/', add, name='add_todo'),   
    path('delete_todo/<uuid:todo_id>/', delete_todo, name='delete_todo'),
    path('complete_todo/<uuid:todo_id>/', complete_todo, name='complete_todo'),
    # path('learn', Learnmore,name='learn' ),
    # path("upload/", upload, name="upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        
    ]