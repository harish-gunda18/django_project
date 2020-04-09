from rest_framework import serializers
from words.models import Words


class WordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        fields = ['pk', 'word', 'meaning', 'example_sentence']
