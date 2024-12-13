from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chat'),
    path('process/', views.process_message, name='process_message'),
    # path('', views.chat_view, name='chat'),
    
]



from django.views.generic import RedirectView

# urlpatterns = [
#     path('', RedirectView.as_view(url='/login/')),  # Redirect root URL to /login/
#     path('admin/', admin.site.urls),
#     path('chat/', include('chat_app.urls')),
#     path('login/', views.user_login, name='login'),
# ]


