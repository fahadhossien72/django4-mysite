from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.db.models import Count
from .models import Post, Comment
from . utilis import paginatorPost
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST
from taggit.models import Tag
# Create your views here.
def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    posts, pagination, custom_range = paginatorPost(request, posts, 3)
    context = {'posts':posts, 'pagination':pagination, 'custom_range':custom_range, 'tag':tag}
    return render(request, 'blog/list.html', context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                            status = Post.Status.PUBLISHED,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day,
                            slug=post,
                            )
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # List of similar posts
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    # Form for users to comment
    form = CommentForm()
    context = {'post':post, 'comments':comments, 'form':form, 'similar_posts':similar_posts}
    return render(request, 'blog/details.html', context)



def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'fahadaddin72@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    context = {'form':form, 'post':post, 'sent':sent}
    return render(request, 'blog/share.html', context)

@require_POST
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    context = {'form':form, 'post':post, 'comment':comment}
    return render(request, 'blog/comment.html', context)



