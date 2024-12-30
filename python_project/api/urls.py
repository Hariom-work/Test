from django.urls import path
from .import views

app_name='api'

urlpatterns = [
    path('projects',views.Projects.as_view(),name='Projects'),
    path('project/<str:id>', views.Project.as_view(), name='project'),
    path('projects/<str:id>/tasks',views.Tasks.as_view(),name='tasks'),
    path('task/<str:id>', views.Task.as_view(), name='task'),
    path('tasks/<str:id>/comments',views.Comments.as_view(),name='comments'),
    path('comment/<str:id>', views.Comment.as_view(), name='comment'),
   
]
