from django import template
from ..models import Post

register = template.Library()

# Creating the custom template function

@register.inclusion_tag('blog/latest_post.html')
def show_latest_post(count=5):
    latest_post = Post.published.order_by('-publish')[:count]
    return { 'latest_post':latest_post }
