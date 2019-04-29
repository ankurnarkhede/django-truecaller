from django.urls import path
from truecaller import views

urlpatterns = [
    path('contacts/', views.ContactsList.as_view()),
    path('signup/', views.SignupList.as_view()),
    path('login/', views.LoginList.as_view()),
    path('spam/', views.SpamList.as_view()),
    path('search_name/', views.SearchNameList.as_view()),
    path('search_phone/', views.SearchPhoneList.as_view())
]
