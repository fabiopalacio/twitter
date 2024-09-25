from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
# Create your views here.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from authors.models import Profile
from posts.forms import CommentForm, PostForm
from posts.models import Tweet, Comments


@method_decorator(
    login_required(
        login_url='authors:login',
        redirect_field_name='next'), name='dispatch')
class PostsView(View):
    def get(self, request, pk):
        if request.method != 'GET':
            messages.error(request, 'Requisição inválida.')
            return redirect(request.META.get("HTTP_REFERER"))

        form = CommentForm()

        tweet = get_object_or_404(Tweet, id=pk)
        comments = Comments.objects.filter(for_tweet=pk)

        return render(
            request,
            'posts/pages/post.html',
            context={
                'form': form,
                'tweet': tweet,
                'comments': comments,
                'btn_text': 'Enviar comentário',
                'form_action': reverse('posts:add_comment', kwargs={'pk': pk}),
            }
        )

    def post(self, request):
        if request.method != 'POST':
            messages.error(request, 'Requisição inválida.')
            return redirect(request.META.get("HTTP_REFERER"))

        form = PostForm(request.POST)

        if form.is_valid():

            profile = get_object_or_404(Profile, author=request.user)

            tweet = Tweet(
                content=form.cleaned_data.get('content'),
                author=profile
            )
            tweet.save()
            messages.success(request, 'Tweet criado.')
            return redirect(reverse('posts:post', kwargs={'pk': tweet.id}))


class PostList(ListView):

    def get(self, request):
        if request.method != 'GET':
            messages.error(request, 'Requisição inválida.')
            return redirect(request.META.get("HTTP_REFERER"))

        tweets = Tweet.objects.all().order_by('-created_at')
        form = PostForm()
        return render(
            request,
            template_name='posts/pages/post_list.html',
            context={
                'tweets': tweets,
                'form': form,
                'btn_text': 'Tweet',
                'form_action': reverse('posts:post')
            }
        )


@method_decorator(
    login_required(
        login_url='authors:login',
        redirect_field_name='next'), name='dispatch')
class PostDelete(View):
    def post(self, request, pk):
        if request.method != 'POST':
            messages.error(request, 'Requisição inválida.')
            return redirect(request.META.get("HTTP_REFERER"))

        if request.user.is_authenticated:
            tweet = get_object_or_404(Tweet, id=pk)
            if request.user.username == tweet.author.author.username:
                tweet.delete()

                messages.success(request, 'Tweet removido com sucesso.')
                return redirect('authors:feed')
            else:
                messages.warning(
                    request, 'Requisição inválida. Você não é o criador deste tweet.')
                return redirect(request.META.get("HTTP_REFERER"))

        else:
            messages.waning(request, 'Login necessário.')
            return redirect(reverse('authors:login'))


class CommentView(View):
    @method_decorator(
        login_required(
            login_url='authors:login',
            redirect_field_name='next'), name='dispatch')
    def post(self, request, pk):

        if request.method != 'POST':
            messages.error(request, 'Requisição inválida.')
            return redirect(request.META.get("HTTP_REFERER"))

        form = CommentForm(request.POST)

        if form.is_valid():

            profile = get_object_or_404(Profile, author=request.user)
            tweet = get_object_or_404(Tweet, id=pk)
            comment = Comments(
                content=form.cleaned_data.get('content'),
                author=profile,
                for_tweet=tweet
            )

            comment.save()
            messages.success(request, 'Comentário criado com sucesso.')
            return redirect(request.META.get("HTTP_REFERER"))
