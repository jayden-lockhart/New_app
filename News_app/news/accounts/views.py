from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group

from accounts.decorators import allowed_users
from .forms import SignUpForm
from .models import (
    ReaderProfile,
    EditorProfile,
    JournalistProfile,
    Article,
    Newsletter,
    User
)
from django.contrib.auth.decorators import login_required
# Create your views here.


def has_group(user, group_name):
    """Check if a user belongs to a given group."""
    return user.groups.filter(name=group_name).exists()


@login_required(login_url='login')
def home(request):
    articles = Article.objects.filter(approved=True)
    newsletters = Newsletter.objects.all()
    return render(request, 'accounts/home.html', {
        'articles': articles, 'newsletters': newsletters})


def login_user(request):
    '''logs user in'''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout_user(request):
    '''logs out user'''
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


def register_reader(request):
    '''registers a new user'''
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            ReaderProfile.objects.create(
                user=user, full_name=form.cleaned_data.get('full_name'))
            reader, created = Group.objects.get_or_create(name='reader')
            current_user = User.objects.get(id=request.user.id)
            current_user.groups.add(reader)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                return render(
                        request,
                        'accounts/register.html',
                        {'form': form}
                    )
    else:
        return render(request, 'accounts/register.html', {'form': form})


def register_editor(request):
    '''registers a new user'''
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            EditorProfile.objects.create(
                user=user, full_name=form.cleaned_data.get('full_name'))
            editor, created = Group.objects.get_or_create(name='editor')
            current_user = User.objects.get(id=request.user.id)
            current_user.groups.add(editor)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                return render(
                       request,
                       'accounts/register_editor.html',
                       {'form': form}
                   )
    else:
        return render(request, 'accounts/register_editor.html', {'form': form})


def register_journalist(request):
    '''registers a new user'''
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            JournalistProfile.objects.create(
                user=user, full_name=form.cleaned_data.get('full_name'))
            journalist, created = Group.objects.get_or_create(
                name='journalist')
            current_user = User.objects.get(id=request.user.id)
            current_user.groups.add(journalist)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                return render(
                       request,
                       'accounts/register_journalist.html',
                       {'form': form}
                   )
    else:
        return render(request, 'accounts/register_journalist.html', {
            'form': form})


@login_required(login_url='login')
def view_journalist(request):
    journalist = JournalistProfile.objects.get(user__id=request.user.id)
    articles = Article.objects.filter(author=journalist)
    newsletters = Newsletter.objects.filter(author=journalist)
    context = {
        'journalist': journalist,
        'articles': articles,
        'newsletters': newsletters,
    }
    return render(request, 'accounts/view_journalist.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['reader'])
def view_reader(request):
    reader = ReaderProfile.objects.get(user__id=request.user.id)
    publishers = reader.publishers.all()
    journalists = reader.journalists.all()
    return render(
        request,
        'accounts/view_reader.html',
        {
            'reader': reader,
            'publishers': publishers,
            'journalists': journalists,
        },
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor'])
def view_editor(request):
    editor = EditorProfile.objects.get(user__id=request.user.id)
    publisher = editor.publisher
    articles = Article.objects.filter(publisher=publisher, approved=False)
    newsletters = Newsletter.objects.filter(editor=editor)
    return render(
        request,
        'accounts/view_editor.html',
        {
            'editor': editor,
            'publisher': publisher,
            'articles': articles,
            'newsletters': newsletters,
        },
    )
