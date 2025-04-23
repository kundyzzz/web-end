from rest_framework import serializers
from .models import Flashcard, Deck, Tag
from django.contrib.auth.models import User

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ['id', 'title', 'description', 'user']
        read_only_fields = ['user']

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'question', 'answer', 'deck', 'tags']

class TagSerializer(serializers.Serializer):
    class Meta:
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField(max_length=50)


class UserDeckSerializer(serializers.Serializer):
    class Meta:
        deck_id = serializers.IntegerField()
        deck_title = serializers.CharField()
        flashcard_count = serializers.IntegerField()
        
