from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

# Blog home page for listing all published blogs

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginated_by = 3
    template_name = 'blog/blog_list.html'   

# Detailed post for individual blog

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status='published', publish__year=year, publish__month=month, publish__day=day, slug=post)
    context = { 'post':post }
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
        
