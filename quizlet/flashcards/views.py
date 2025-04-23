from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Deck, Flashcard
from .serializers import UserDeckSerializer, FlashcardSerializer
from django.db.models import Count

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_decks(request):
    user = request.user
    decks = Deck.objects.filter(user=user).annotate(flashcard_count = Count('flashcard'))

    result = [
        {
            "deck_id": d.id,
            "deck_title": d.title,
            "flashcard_count": d.flashcard_count
        } for d in decks
    ]

    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_flashcard(request):
    serializer = FlashcardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response (serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeckListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        decks = Deck.objects.filter(user=request.user)
        serializer = UserDeckSerializer(decks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserDeckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeckDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Deck.objects.get(pk=pk, user=user)
        except Deck.DoesNotExist:
            return None
    
    def get(self, request, pk):
        deck = self.get_object(pk, request.user)
        if deck is None:
            return Response({'error': 'Not found'}, status=404)
        serializer = UserDeckSerializer(deck)
        return Response(serializer.data)
    
    def put(self, request, pk):
        deck = self.get_object(pk, request.user)
        if deck is None:
            return Response({'error': 'Not found'}, status=404)
        serializer = UserDeckSerializer(deck, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        deck = self.get_object(pk, request.user)
        if deck is None:
            return Response({'error': 'Not found'}, status=404)
        deck.delete()
        return Response(status=204)
