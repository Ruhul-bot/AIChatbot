from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatSession, ChatMessage
from .utils import CollegeChatbot
import json

# --------------------------------------------
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
#---------------------------------------------


@login_required
def home(request):
    return render(request, 'chat/home.html')  # Create this template
chatbot = CollegeChatbot()

from django.shortcuts import render
from django.http import HttpResponse

# -------------------------------------------------------
# def user_login(request):
#     # Example login logic
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # Add authentication logic here
#         return HttpResponse(f"Welcome, {username}!")
#     return render(request, 'login.html')  # Ensure 'login.html' exists in templates


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('chat')  # Redirect to chat page after login
    else:
        form = AuthenticationForm()
    
    return render(request, 'chat/login.html', {'form': form})
# -------------------------------------------------------------

@login_required
def chatbot_view(request):
    # Create or get current chat session
    session, created = ChatSession.objects.get_or_create(
        user=request.user, 
        end_time=None
    )
    return render(request, 'chat/chat.html')


# @login_required

#  --------------------------------------------------   
def chat_view(request):
    return render(request, 'chat/chat.html')
    context = {
        'username': request.user.username
    }
    return render(request, 'chat/chat.html', context)
# ---------------------------------------------------




@login_required
def process_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        # Get current active session
        session = ChatSession.objects.filter(
            user=request.user, 
            end_time=None
        ).first()
        
        # Predict intent and get response
        intents = chatbot.predict_class(user_message)
        bot_response = chatbot.get_response(intents, chatbot.intents)
        
        # Save message to database
        chat_message = ChatMessage.objects.create(
            session=session,
            user_message=user_message,
            bot_response=bot_response,
            intent=intents[0]['intent'] if intents else None
        )
        
        return JsonResponse({
            'response': bot_response,
            'intent': intents[0]['intent'] if intents else 'unknown'
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
































































# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
# from .models import ChatSession, ChatMessage
# from .utils import CollegeChatbot
# import json

# # Initialize chatbot
# chatbot = CollegeChatbot()

# def user_login(request):
#     """Handle user login with authentication form."""
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('chat')  # Redirect to chat page after login
#     else:
#         form = AuthenticationForm()
    
#     return render(request, 'chat/login.html', {'form': form})

# @login_required
# def home(request):
#     """Home view - redirects to chat interface."""
#     return redirect('chat')

# @login_required
# def chatbot_view(request):
#     """Main chat interface view."""
#     # Create or get current chat session
#     session, created = ChatSession.objects.get_or_create(
#         user=request.user,
#         end_time=None
#     )
    
#     # Get recent chat history
#     chat_history = ChatMessage.objects.filter(
#         session=session
#     ).order_by('-timestamp')[:10]  # Get last 10 messages
    
#     context = {
#         'username': request.user.username,
#         'chat_history': reversed(chat_history)  # Reverse to show oldest first
#     }
#     return render(request, 'chat/chatbot.html', context)

# @login_required
# def process_message(request):
#     """Handle incoming chat messages and return bot responses."""
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_message = data.get('message', '')
            
#             if not user_message.strip():
#                 return JsonResponse({'error': 'Empty message'}, status=400)
            
#             # Get or create current active session
#             session, created = ChatSession.objects.get_or_create(
#                 user=request.user,
#                 end_time=None
#             )
            
#             # Get chatbot response
#             intents = chatbot.predict_class(user_message)
#             bot_response = chatbot.get_response(intents, chatbot.intents)
            
#             # Save message to database
#             chat_message = ChatMessage.objects.create(
#                 session=session,
#                 user_message=user_message,
#                 bot_response=bot_response,
#                 intent=intents[0]['intent'] if intents else None
#             )
            
#             return JsonResponse({
#                 'response': bot_response,
#                 'intent': intents[0]['intent'] if intents else 'unknown',
#                 'message_id': chat_message.id
#             })
            
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
            
#     return JsonResponse({'error': 'Invalid request method'}, status=400)