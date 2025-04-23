from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import get_user_decks, create_flashcard, DeckListCreateAPIView, DeckDetailAPIView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/decks/user/', get_user_decks, name='get_user_decks'),
    path('api/flashcards/create/', create_flashcard, name='create_flashcard'),

    path('api/decks/', DeckListCreateAPIView.as_view(), name='deck_list_create'),
    path('api/decks/<int:pk>/', DeckDetailAPIView.as_view(), name='deck_detail'),
]
