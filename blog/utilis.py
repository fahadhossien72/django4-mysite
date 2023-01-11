from . models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginatorPost(request, posts, results):
    page = request.GET.get('page')
    results = 3
    paginator = Paginator(posts, results)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page=1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)

    left_index = (int(page)- 3)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 4)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages 

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index)
    return posts, paginator, custom_range