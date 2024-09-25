from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from authors.forms import LoginForm, RegisterForm
from authors.models import Profile
from posts.forms import PostForm
from posts.models import Tweet
# Create your views here.


class AuthorsLogin(View):
    def get(self, request):
        if request.method != 'GET':
            messages.error(request, 'Requisição inválida.')
            return redirect('home')

        form = LoginForm()

        return render(
            request,
            'authors/pages/login.html',

            context={
                'form': form,
                'form_action': reverse('authors:login'),
                'btn_text': 'Entrar'
            })

    def post(self, request):
        if not request.POST:
            raise Http404()

        form = LoginForm(request.POST)

        if form.is_valid():
            authenticate_user = authenticate(
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', '')
            )

        if authenticate_user is not None:
            login(request, authenticate_user)
            messages.success(request, "Login feito com sucesso")
            return redirect(reverse('authors:feed'))
        messages.error(request, "Credenciais não autorizadas.")
        return redirect(reverse('authors:login'))


@method_decorator(
    login_required(
        login_url='authors:login',
        redirect_field_name='next'), name='dispatch')
class AuthorsLogout(View):
    def post(self, request):
        if not request.POST:
            messages.error(request, 'Requisição inválida.')
            return redirect('home')

        if request.POST.get('username') != request.user.username:
            messages.error(request, 'Requisição inválida.')
            return redirect(reverse('authors:feed'))
        logout(request)
        messages.success(request, 'Logout feito com sucesso.')

        return redirect(reverse('authors:login'))


class AuthorsRegister(View):
    def get(self, request):
        if request.method != 'GET':
            messages.error(request, 'Requisição inválida.')
            return redirect('home')

        register_form_data = request.session.get(
            'register_form_data', None)
        form = RegisterForm(register_form_data)

        return render(
            request,
            'authors/pages/register.html',
            context={
                'form': form,
                'form_action': reverse('authors:register'),
                'btn_text': 'Cadastrar'
            })

    def post(self, request):
        if not request.POST:
            messages.error(request, 'Requisição inválida.')
            return redirect('home')

        POST = request.POST
        request.session['register_form_data'] = POST
        form = RegisterForm(POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            del (request.session['register_form_data'])
            messages.success(request, 'Usuário cadastrado com sucesso.')
            return redirect('authors:login')

        messages.error(request, 'Existem erros no formulário.')
        return redirect('authors:register')


@method_decorator(
    login_required(
        login_url='authors:login',
        redirect_field_name='next'), name='dispatch')
class AuthorsFeed(ListView):
    model = Tweet
    context_object_name = 'tweets'

    ordering = ['created_at']

    def get_queryset(self, *args, **kwargs):
        current_user = self.request.user
        current_profile = Profile.objects.filter(author=current_user).first()

        tweets = Tweet.objects.filter(
            author__in=current_profile.following.all())
        return tweets

    def get(self, request):
        if request.method != 'GET':
            messages.error(request, 'Requisição inválida.')
            return redirect('home')

        tweets = self.get_queryset()
        form = PostForm()
        return render(
            request,
            'authors/pages/feed.html',
            context={
                'tweets': tweets,
                'form': form,
                'btn_text': 'Tweet',
                'form_action': reverse('posts:post'),
            }
        )


class AuthorsSearch(ListView):
    model = Profile
    context_object_name = 'profiles'
    ordering = ['Profile.author.user.username']

    def post(self, request, *args, **kwargs):
        if request.method != 'POST':
            messages.error(request, 'Requisição inválida.')
            return redirect('home')

        search_term = request.POST.get('search_term', '')

        usuarios = Profile.objects.filter(
            Q(author__username__icontains=search_term)
        )
        return render(
            request,
            template_name='authors/pages/search.html',
            context={
                'search_term': search_term,
                'usuarios': usuarios
            }
        )


class ProfilePage(ListView):
    model = Tweet

    def get(self, request, pk):
        if request.method != 'GET':
            messages.error(request, 'Requisição inválida.')
            return redirect('home')

        tweets = Tweet.objects.filter(author__id=pk)
        profile_from_page = Profile.objects.get(author__id=pk)
        btn_text = ''
        btn_action = ''
        logged = False

        if request.user.is_authenticated:
            logged = True
            current_user_profile = Profile.objects.get(
                author__username=request.user.username)
            if current_user_profile.following.filter(id=profile_from_page.id).exists():
                btn_text = 'Deixar de seguir'
                btn_action = 'unfollow'
            else:
                btn_text = 'Seguir'
                btn_action = 'follow'
            return render(
                request,
                'authors/pages/profile.html',
                context={
                    'tweets': tweets,
                    'logged': logged,
                    'profile': profile_from_page,
                    'btn_text': btn_text,
                    'btn_action': reverse(
                        'authors:followers',
                        kwargs={
                            'pk': profile_from_page.id,
                            'action': btn_action})
                }
            )
        return render(
            request,
            'authors/pages/profile.html',
            context={
                'tweets': tweets,
                'logged': logged,
                'profile': profile_from_page,

            }
        )


class ProfileFollowMethods(View):
    def get(self, request, action,  pk):
        if request.method != 'GET':
            messages.error(request, 'Requisição inválida.')
            return redirect('home')

        current_user_logged = Profile.objects.filter(
            author__username=request.user.username).first()

        to_follow_profile = Profile.objects.filter(id=pk).first()

        if action == 'follow':
            current_user_logged.following.add(to_follow_profile.id)
            messages.success(request, f'Seguindo @{to_follow_profile}.')
        elif action == 'unfollow':
            current_user_logged.following.remove(to_follow_profile.id)
            messages.warning(
                request, f'Deixou de seguir @{to_follow_profile}.')

        return redirect(request.META.get("HTTP_REFERER"))
