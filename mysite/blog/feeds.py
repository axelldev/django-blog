import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from .models import Post


class LatestPostsFeed(Feed):
    title = "My Blog"
    link = reverse_lazy("blog:post_list")
    description = "New posts of my blog."

    def items(self):
        return Post.published.all()[:5]

    def item_tilte(self, item: Post):
        return item.title

    def item_description(self, item: Post):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item: Post):
        return item.publish
