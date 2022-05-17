from django.urls import path

from .views import JobTaskSave, JobTaskEdit


urlpatterns = [
    path('', JobTaskSave.as_view()),
    path('/<str:pk>', JobTaskEdit.as_view()),
]
