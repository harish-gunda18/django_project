from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from words.api.serializers import WordsSerializer
from random import randint
from words.models import Words
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters


@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_words(request, level):
    if request.method == 'GET':
        filter_words = Words.objects.filter(level=level).values('pk')
        rand = randint(1, len(filter_words))
        prk = 0
        for idx, p in enumerate(filter_words):
            if idx + 1 == rand:
                prk = p['pk']
                break
        word = Words.objects.filter(level=level).get(pk=prk)
        serializer = WordsSerializer(instance=word)
        user = request.user
        profile = user.profile
        if word.pk in profile.get_reviewed_list():
            reviewed = "r"
        elif word.pk in profile.get_mastered_list():
            reviewed = "m"
        else:
            reviewed = "n"
        data = {'reviewed': reviewed, 'level': word.level}
        data.update(serializer.data)
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        word_id = request.POST.get("wordid")
        word_level = Words.objects.get(pk=word_id).level
        known = request.POST.get("known")
        reviewed = request.POST.get("reviewed")
        user = User.objects.get(pk=request.user.id)
        profile = user.profile
        temp_rlist = profile.get_reviewed_list()
        temp_mlist = profile.get_mastered_list()
        word_id = int(word_id)
        if known == "yes":
            if reviewed == "r":
                temp_mlist.append(word_id)
                profile.set_mastered_list(temp_mlist)
                temp_rlist.remove(word_id)
                profile.set_reviewed_list(temp_rlist)
            elif reviewed == "n":
                temp_mlist.append(word_id)
                profile.set_reviewed_list(temp_mlist)
        else:
            if reviewed == "r":
                pass
            elif reviewed == "m":
                temp_mlist.remove(word_id)
                profile.set_mastered_list(temp_mlist)
                temp_rlist.append(word_id)
                profile.set_reviewed_list(temp_rlist)
        profile.save()
        data = {"url": reverse('api-words', kwargs={'level': word_level}, request=request)}
        return Response(data, status=status.HTTP_201_CREATED)


class ApiAllWordsView(ListAPIView):
    serializer_class = WordsSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination
    page_size = 10

    def get_queryset(self):
        return Words.objects.filter(level=self.kwargs.get('level')).order_by('word')


class ApiReviewedWordsView(ListAPIView):
    serializer_class = WordsSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination
    page_size = 10

    def get_queryset(self):
        all_review = Words.objects.filter(pk__in=self.request.user.profile.get_reviewed_list())
        return all_review.filter(level=self.kwargs.get('level')).order_by('word')


class ApiMasteredWordsView(ListAPIView):
    serializer_class = WordsSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination
    page_size = 10

    def get_queryset(self):
        all_master = Words.objects.filter(pk__in=self.request.user.profile.get_mastered_list())
        return all_master.filter(level=self.kwargs.get('level')).order_by('word')


class ApiSearchWordsView(ListAPIView):
    queryset = Words.objects.all()
    serializer_class = WordsSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = [filters.SearchFilter]
    search_fields = ['word']
