from django.urls import path
from .views import (
    VacancyListView,
    VacancyDetailView,
    VacancyCreateView,
    VacancyUpdateView,
    VacancyDeleteView,
    UserVacancyListView,
    SolutionListView,
    ResponseListView,
    NotificationListView,
    NotificationDeleteView,
    SolutionDeleteView,
    ResponseDeleteView
)
from . import views

urlpatterns = [
    path('', VacancyListView.as_view(), name='home'),
    path('received_solutions/', SolutionListView.as_view(), name='received-solutions'),
    path('received_responses/', ResponseListView.as_view(), name='received-responses'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('user/<str:username>', UserVacancyListView.as_view(), name='user-vacancies'),
    path('vacancy/<int:pk>/', VacancyDetailView.as_view(), name='vacancy-detail'),
    path('vacancy/new/', VacancyCreateView.as_view(), name='vacancy-create'),
    path('vacancy/<int:pk>/update/', VacancyUpdateView.as_view(), name='vacancy-update'),
    path('vacancy/<int:pk>/delete/', VacancyDeleteView.as_view(), name='vacancy-delete'),
    path('vacancy/<int:pk>/upload/', views.upload_file, name='upload'),
    path('received_solutions/<int:pk>/respond/', views.create_response, name='respond'),
    path('notifications/<int:pk>/delete/', NotificationDeleteView.as_view(), name='notification-delete'),
    path('received_solutions/<int:pk>/delete/', SolutionDeleteView.as_view(), name='solution-delete'),
    path('received_responses/<int:pk>/delete/', ResponseDeleteView.as_view(), name='response-delete'),
    path('about/', views.about, name='about'),
]