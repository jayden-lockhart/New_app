from django.shortcuts import render, redirect
from accounts.models import (
    JournalistProfile,
    Publisher,
    Article,
    Newsletter,
    ReaderProfile,
    EditorProfile,
    User
)
from .forms import ArticleForm, NewsletterForm, PublisherForm, ReaderForm, EditorForm, JournalistForm
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users
from django.contrib import messages
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Create your views here.


def log_approved_article(api_url, article_id, title):
    '''    Sends a POST request to log an approved article.'''
    payload = {
        "article_id": article_id,
        "title": title.strip(),
        "status": "approved"
    }
    try:
        request = Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=10) as response:
            response_text = response.read().decode("utf-8")
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {
                "message": "Success, but no JSON returned.",
                "raw_response": response_text,
            }
    except (HTTPError, URLError, TimeoutError) as e:
        return {"error": str(e)}


def send_article_to_subscribers(article):
    author = article.author
    publisher = article.publisher
    readers = ReaderProfile.objects.all()
    for reader in readers:
        if author in reader.journalists.all():
            for user in User.objects.all():
                if user == reader.user:
                    email = EmailMessage(
                        subject=f"New Article: {article.title}",
                        body=(
                            f"Dear {reader.full_name},\n\n"
                            f"A new article titled '{article.title}' "
                            f"has been published by "
                            f"{article.author.full_name}"
                            f"You can read the article here: "
                            f"http://yourwebsite.com/articles/"
                            f"{article.title}\n\n"
                            f"Best regards,\nNews App Team"
                        ),
                        to=[user.email],
                    )
                    email.send()
        if publisher in reader.publishers.all():
            for user in User.objects.all():
                if user == reader.user:
                    email = EmailMessage(
                        subject=f"New Article: {article.title}",
                        body=(
                            f"Dear {reader.full_name},\n\n"
                            f"A new article titled '{article.title}' "
                            f"has been published by "
                            f"{article.author.full_name}"
                            f"Best regards,\nNews App Team"
                        ),
                        to=[user.email],
                    )
                    email.send()


def send_newsletter_to_subscribers(newsletter):
    author = newsletter.author
    publisher = newsletter.publisher
    readers = ReaderProfile.objects.all()
    for reader in readers:
        if author in reader.journalists.all():
            for user in User.objects.all():
                if user == reader.user:
                    email = EmailMessage(
                        subject=f"New Newsletter: {newsletter.title}",
                        body=(
                            f"Dear {reader.full_name},\n\n"
                            f"A new article titled '{newsletter.title}' "
                            f"has been published by {newsletter.author} "
                            f"{newsletter.editor}"
                            f"from {newsletter.publisher}.\n\n"
                            f"Best regards,\nNews App Team"
                        ),
                        to=[user.email],
                    )
                    email.send()
            if publisher in reader.publishers.all():
                for user in User.objects.all():
                    if user == reader.user:
                        email = EmailMessage(
                            subject=f"New Article: {newsletter.title}",
                            body=(
                                f"Dear {reader.full_name},\n\n"
                                f"A new article titled '{newsletter.title}' "
                                f"has been published by {newsletter.author} "
                                f"{newsletter.editor}"
                                f"from {newsletter.publisher}.\n\n"
                                f"Best regards,\nNews App Team"
                            ),
                            to=[user.email],
                        )
                        email.send()


@login_required(login_url='login')
def publisher_summary(request):
    publishers = Publisher.objects.all()
    context = {'publishers': publishers}
    return render(
        request,
        'content/publisher_summary.html',
        context
    )


@login_required(login_url='login')
def newsletter_sum(request):
    newsletters = Newsletter.objects.all()
    return render(
        request,
        'content/newsletter_sum.html',
        {'newsletters': newsletters}
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor'])
def unapproved_article(request):
    unapproved_articles = Article.objects.filter(approved=False)
    return render(
        request,
        'content/unapproved_articles.html',
        {'articles': unapproved_articles}
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['journalist'])
def add_article(request):
    journalist = JournalistProfile.objects.get(user__id=request.user.id)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = journalist
            form.save()
            return redirect('home')
    else:
        form = ArticleForm()
    return render(
        request,
        'content/add_article.html',
        {'form': form}
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor'])
def approve_article(request, id):
    article = Article.objects.get(id=id)
    article.approved = True
    article.save()
    send_article_to_subscribers(article)
    log_approved_article('http://127.0.0.1:8000/api/articles/', article.id, article.title)
    return redirect('unapproved_articles')


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'journalist'])
def edit_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ArticleForm(instance=article)
    return render(
        request,
        'content/edit_article.html',
        {'form': form, 'article': article}
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'journalist'])
def delete_article(request, id):
    article = Article.objects.get(id=id)
    article.delete()
    return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'journalist'])
def add_newsletter(request):
    if JournalistProfile.objects.get(user__id=request.user.id):
        if request.method == 'POST':
            form = NewsletterForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = JournalistProfile.objects.get(user__id=request.user.id)
                form.save()
                send_newsletter_to_subscribers(form.instance)
                return redirect('home')
        else:
            form = NewsletterForm()
        return render(
            request,
            'content/add_newsletter.html',
            {'form': form}
        )
    if EditorProfile.objects.get(user__id=request.user.id):
        if request.method == 'POST':
            form = NewsletterForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.editor = EditorProfile.objects.get(user__id=request.user.id)
                form.save()
                send_newsletter_to_subscribers(form.instance)
                return redirect('home')
        else:
            form = NewsletterForm()
        return render(
            request,
            'content/add_newsletter.html',
            {'form': form}
        )


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'journalist'])
def edit_newsletter(request, id):
    newsletter = Newsletter.objects.get(id=id)
    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewsletterForm(instance=newsletter)
    return render(
        request,
        'content/edit_newsletter.html',
        {'form': form, 'newsletter': newsletter}
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'journalist'])
def delete_newsletter(request, id):
    newsletter = Newsletter.objects.get(id=id)
    newsletter.delete()
    return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'journalist'])
def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PublisherForm()
    return render(
        request,
        'content/add_publisher.html',
        {'form': form}
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'journalist'])
def edit_publisher(request, id):
    publisher = Publisher.objects.get(id=id)
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PublisherForm(instance=publisher)
    return render(
        request,
        'content/edit_publisher.html',
        {'form': form, 'publisher': publisher}
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'journalist'])
def delete_publisher(request, id):
    publisher = Publisher.objects.get(id=id)
    publisher.delete()
    return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['reader'])
def subscribe_publisher(request, id):
    publisher = Publisher.objects.get(id=id)
    user = ReaderProfile.objects.get(user=request.user)
    user.publishers.add(publisher)
    return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['reader'])
def subscribe_journalist(request, pk):
    journalist = JournalistProfile.objects.get(int(pk))
    user = ReaderProfile.objects.get(user=request.user)
    user.journalists.add(journalist)
    return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['reader'])
def unsubscribe_publisher(request, id):
    publisher = Publisher.objects.get(id=id)
    user = ReaderProfile.objects.get(user=request.user)
    user.publishers.remove(publisher)
    return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['reader'])
def unsubscribe_journalist(request, pk):
    journalist = JournalistProfile.objects.get(id=int(pk))
    user = ReaderProfile.objects.get(user=request.user)
    user.journalists.remove(journalist)
    return redirect('home')


@login_required(login_url='login')
def view_article(request, id):
    article = Article.objects.get(id=id)
    journalist = article.author
    return render(
        request,
        'content/view_article.html',
        {'article': article, 'journalist': journalist}
    )


@login_required(login_url='login')
def view_newsletter(request, id):
    try:
        newsletter = Newsletter.objects.get(id=id)
        articles = newsletter.articles.all()
        return render(
            request,
            'content/view_newsletter.html',
            {'newsletter': newsletter, 'articles': articles}
        )
    except Newsletter.DoesNotExist:
        messages.success(request, "Newsletter not found.")
        return redirect('home')


@login_required(login_url='login')
def view_publisher(request, id):
    try:
        publisher = Publisher.objects.get(id=id)
        articles = Article.objects.filter(publisher=publisher)
        newsletters = Newsletter.objects.filter(publisher=publisher)
        return render(
            request, 'content/view_publisher.html',
            {
                'publisher': publisher,
                'articles': articles,
                'newsletters': newsletters
            }
            )
    except Publisher.DoesNotExist:
        messages.success(request, "Publisher not found.")
        return redirect('home')


@login_required(login_url='login')
def journalist_summary(request):
    journalists = JournalistProfile.objects.all()
    return render(
        request,
        'content/journalist_summary.html',
        {'journalists': journalists}
    )


@login_required(login_url='login')
def journalist_coverage(request, full_name):
    journalist = JournalistProfile.objects.get(full_name=full_name)
    articles = Article.objects.filter(author=journalist)
    newsletters = Newsletter.objects.filter(author=journalist)
    return render(
        request,
        'content/journalist_coverage.html',
        {
            'journalist': journalist,
            'articles': articles,
            'newsletters': newsletters
        }
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'journalist'])
def join_publisher(request):
    user = request.user
    if user.groups.filter(name='editor').exists():
        editor_profile = EditorProfile.objects.get(user__id=request.user.id)
        form = EditorForm(request.POST or None, instance=editor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your info has been updated.")
            return redirect('home')
        return render(request, 'content/join_publisher.html', {'form': form})
    elif user.groups.filter(name='journalist').exists():
        journalist_profile = JournalistProfile.objects.get(
            user__id=request.user.id)
        form = JournalistForm(
            request.POST or None, instance=journalist_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your info has been updated.")
            return redirect('home')
        return render(request, 'content/join_publisher.html', {'form': form})


def article_summry(request):
    articles = Article.objects.filter(approved=True)
    return render(
        request, 'content/article_summary.html', {'articles': articles})


def subscribe(request):
    reader = ReaderProfile.objects.get(user__id=request.user.id)
    form = ReaderForm(request.POST or None, instance=reader)
    if form.is_valid():
        form.save()
        messages.success(request, "Your info has been updated.")
        return redirect('home')
    return render(request, 'content/subscribe.html', {'form': form})
