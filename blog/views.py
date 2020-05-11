from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count

# Blog home page for listing all published blogs

def post_list(request, tag_slug=None): 
    object_list = Post.published.all() 
    tag = None 
 
    if tag_slug: 
        tag = get_object_or_404(Tag, slug=tag_slug) 
        object_list = object_list.filter(tags__in=[tag]) 
 
    paginator = Paginator(object_list, 9) # 3 posts in each page 
    page = request.GET.get('page') 
    try: 
        posts = paginator.page(page) 
    except PageNotAnInteger: 
        # If page is not an integer deliver the first page 
        posts = paginator.page(1) 
    except EmptyPage: 
        # If page is out of range deliver last page of results 
        posts = paginator.page(paginator.num_pages) 
    return render(request, 'blog/blog_list.html', {'page': page, 'posts': posts, 'tag': tag}) 

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginated_by = 3
#     template_name = 'blog/blog_list.html'   

# Detailed post for individual blog

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status='published', publish__year=year, publish__month=month, publish__day=day, slug=post)

    # Collecting the comments to current post

    comments = post.comments.filter(is_active=True)

    new_comment = None
    if request.method == 'POST':
        # New comment has been made
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Save the comment but do not commit to database as still need to link post object
            new_comment = comment_form.save(commit=False)
            # Add current post to comment
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Suggesting post with similar tags
    post_tag_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]


    comment_form = CommentForm()
    context = { 'post':post,'comments':comments, 'comment_form':comment_form, 'new_comment':new_comment, 'similar_posts':similar_posts }
    return render(request, 'blog/post_detail.html', context)

# Sharing the post throgh Email using Forms

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')

    if request.method == 'POST':
        #Creatng the form from POST data
        form = EmailPostForm(request.POST)
        # Validating the Form
        if form.is_valid():
            # Cleaning the data
            cleaned_Form = form.cleaned_data
            # Sending post throgh mail
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} wants to share "{}"'.format(cleaned_Form['name'], post.title)
            message = '{} wants you read "{}" ({})\n\n Comments {}'.format(cleaned_Form['name'], post.title, post_url, cleaned_Form['comments'])
            send_mail(subject, message, 'kkthunga1@gmail.com', [cleaned_Form['to_email'],])
            sent = True
    else:
        # Displaying the emty form
        form = EmailPostForm()
        sent = False    
    context = { 'form':form, 'post':post, 'sent':sent }
    return render(request, 'blog/blog_share.html',context)
        
# Searching for posts in title and body

def search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            results = Post.objects.annotate(search=SearchVector('title', 'body'), ).filter(search=query)
    
    return render(request, 'blog/search.html', {'form':form, 'query':query, 'results':results})


