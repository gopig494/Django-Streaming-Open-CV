from django.shortcuts import get_object_or_404, render,redirect
from streaming.forms import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout as logout_user,login as login_user
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from streaming.video_streaming import *
from django.contrib import messages

# Create your views here.

def check_authentication(func):
    def validate_auth(request, video_id = None):
        if request.user.is_authenticated:
            if video_id:
                return func(request,video_id)
            else:
                return func(request)
        else:
            return redirect('/streaming/login/')
    return validate_auth

@check_authentication
def index(request):
    return render(request, 'streaming/index.html',{"header":1})
    
def signup(request):
    if request.method == "POST": 
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password,
                                            first_name=form.cleaned_data.get('first_name'),
                                            last_name=form.cleaned_data.get('last_name'),
                                            email=form.cleaned_data.get('email'))
            user.save()
            return redirect('/streaming/login/')
    else:
        form = SignUpForm()
    return render(request, 'streaming/signup.html',{"signup_form":form})

def login(request):
    if request.method == "POST": 
        form = LogInForm(request.POST)
        if form.is_valid():
            token,already_created = Token.objects.get_or_create(user = form.auth_info)
            login_user(request, form.auth_info)
            messages.success(request, "Log in successfully.")
            return redirect("/")
    else:
        form = LogInForm()
    return render(request, 'streaming/login.html',{"login_from":form})

@check_authentication
def logout(request):
    logout_user(request)
    messages.success(request, "Log out successfully.")
    return redirect("/streaming/login/")

@check_authentication
def create_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST,request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.userid = request.user
            video.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('/')
    else:
        form = VideoForm()
    return render(request, 'streaming/create_video.html', {'form': form,"header":1,"method":"POST"})

@check_authentication
def edit_video(request,video_id):
    my_object = get_object_or_404(Video, pk=video_id)
    form = VideoForm(instance=my_object)
    return render(request, 'streaming/create_video.html', {'form': form,"header":1,"video_id":video_id})

@check_authentication
def update_video(request,video_id):
    my_object = Video.objects.get(pk=video_id)
    form = VideoForm(request.POST,request.FILES,instance=my_object)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        form = VideoForm(instance=my_object)
        return render(request, 'streaming/create_video.html', {'form': form,"header":1,"video_id":video_id})


@check_authentication
def delete_video(request,video_id):
    exe_video = Video.objects.get(pk = video_id)
    exe_video.delete()
    return redirect('/')

class VideoListView(LoginRequiredMixin,generic.ListView):
    model = Video
    template_name = 'streaming/index.html'
    context_object_name = 'videos'
    paginate_by = 3

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/streaming/login/")
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(userid = self.request.user)
        search_txt = self.request.GET.get('search_txt')
        if search_txt:
            # queryset = queryset.filter(name = search_txt)
            queryset = queryset.filter(name__contains=search_txt)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_txt'] = self.request.GET.get('search_txt') or ''
        context['header'] = 1
        return context