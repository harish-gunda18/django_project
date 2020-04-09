from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Words
from random import randint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    levels = Words.objects.order_by().values('level').distinct()
    level_fraction = {}
    for l in levels:
        level_fraction[l['level']] = 0
    level_count = {}
    if request.user.is_authenticated:
        for word_id in request.user.profile.get_mastered_list():
            low = Words.objects.get(pk=word_id).level
            level_count[low] = level_count.get(low, 0) + 1
    for key, value in level_count.items():
        level_fraction[key] = int(value/len(Words.objects.filter(level=key))*100)
    return render(request, 'words/home.html', context={'level_fraction': level_fraction})


@login_required
def level(request):
    if request.method == 'POST':
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
                profile.set_mastered_list(temp_mlist)
        else:
            if reviewed == "r":
                pass
            elif reviewed == "m":
                temp_mlist.remove(word_id)
                profile.set_mastered_list(temp_mlist)
                temp_rlist.append(word_id)
                profile.set_reviewed_list(temp_rlist)
            else:
                temp_rlist.append(word_id)
                profile.set_reviewed_list(temp_rlist)
        profile.save()
        return redirect(reverse('words-level') + f'?level={word_level}')
    req_level = request.GET.get('level')
    req_level = int(req_level)
    filter_words = Words.objects.filter(level=req_level).values('pk')
    rand = randint(1, len(filter_words))
    prk = 0
    for idx, p in enumerate(filter_words):
        if idx+1 == rand:
            prk = p['pk']
            break
    word = Words.objects.filter(level=req_level).get(pk=prk)
    user = User.objects.get(pk=request.user.id)
    profile = user.profile
    if word.pk in profile.get_reviewed_list():
        reviewed = "r"
    elif word.pk in profile.get_mastered_list():
        reviewed = "m"
    else:
        reviewed = "n"
    return render(request, 'words/level.html', {'word': word, 'reviewed': reviewed, 'sidebar': word.level})


def about(request):
    return render(request, 'words/about.html', {'title': 'about'})


class AllWordsListView(LoginRequiredMixin, ListView):
    allow_empty = False
    model = Words
    template_name = 'words/words.html'
    context_object_name = 'words'
    paginate_by = 10

    def get_queryset(self):
        return Words.objects.filter(level=self.kwargs.get('level')).order_by('word')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['sidebar'] = self.kwargs.get('level')
        return context


class MasteredWordsListView(LoginRequiredMixin, ListView):
    model = Words
    template_name = 'words/words.html'
    context_object_name = 'words'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        all_master = Words.objects.filter(pk__in=user.profile.get_mastered_list())
        return all_master.filter(level=self.kwargs.get('level')).order_by('word')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['sidebar'] = self.kwargs.get('level')
        return context


class ReviewedWordsListView(LoginRequiredMixin, ListView):
    model = Words
    template_name = 'words/words.html'
    context_object_name = 'words'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        all_review = Words.objects.filter(pk__in=user.profile.get_reviewed_list())
        return all_review.filter(level=self.kwargs.get('level')).order_by('word')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['sidebar'] = self.kwargs.get('level')
        return context


class SearchWordsListView(LoginRequiredMixin, ListView):
    model = Words
    template_name = 'words/words.html'
    context_object_name = 'words'
    paginate_by = 10

    def get_queryset(self):
        return Words.objects.filter(word__contains=self.request.GET.get('search_word')).order_by('word')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['search'] = 'search'
        return context
