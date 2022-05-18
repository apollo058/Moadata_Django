from django.urls import path

from .views import JobTaskSave, JobTaskEdit, JobTaskRun


urlpatterns = [
    path('', JobTaskSave.as_view()),
    path('/<str:pk>', JobTaskEdit.as_view()),
    path('/<str:pk>/run', JobTaskRun.as_view()),
]
