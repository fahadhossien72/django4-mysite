import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars_html
from django.urls import reverse_lazy
from . models import Post

class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog-post-list')
    description = 'New post of my blog'

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatechars_html(markdown.markdown(item.body), 30)

    def item_update(self, item):
        return item.publish