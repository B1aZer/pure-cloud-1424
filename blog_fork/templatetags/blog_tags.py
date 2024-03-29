
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Count

from blog_fork.forms import BlogPostForm
from blog_fork.models import BlogPost, BlogCategory, Blogroll
from mezzanine import template


register = template.Library()


@register.as_tag
def blog_months(*args):
    """
    Put a list of dates for blog posts into the template context.
    """
    dates = BlogPost.objects.published().values_list("publish_date", flat=True)
    date_dicts = [{"date": datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for i, date_dict in enumerate(month_dicts):
        month_dicts[i]["post_count"] = date_dicts.count(date_dict)
    return month_dicts


@register.as_tag
def blog_categories(*args):
    """
    Put a list of categories for blog posts into the template context.
    """
    posts = BlogPost.objects.published()
    categories = BlogCategory.objects.filter(blogposts__in=posts)
    return list(categories.annotate(post_count=Count("blogposts")))


@register.as_tag
def blog_authors(*args):
    """
    Put a list of authors (users) for blog posts into the template context.
    """
    blog_posts = BlogPost.objects.published()
    authors = User.objects.filter(blogposts__in=blog_posts)
    return list(authors.annotate(post_count=Count("blogposts")))




@register.as_tag
def blog_recent_posts(limit=5):
    """
    Put a list of recently published blog posts into the template context.
    """
    return list(BlogPost.objects.published()[:limit])


@register.inclusion_tag("admin/includes/quick_blog.html", takes_context=True)
def quick_blog(context):
    """
    Admin dashboard tag for the quick blog form.
    """
    context["form"] = BlogPostForm()
    return context


@register.as_tag
def blog_upvotes(limit=3):
    upvotes = []
    blog_posts = BlogPost.objects.published()[:limit]
    for post in blog_posts:
        upv = post.upvote
        dnv = post.downvote
        if upv > dnv:
            upvotes.append(post)
    return upvotes

@register.as_tag
def blog_downvotes(limit=3):
    downvotes = []
    blog_posts = BlogPost.objects.published()[:limit]
    for post in blog_posts:
        upv = post.upvote
        dnv = post.downvote
        if dnv > upv:
            downvotes.append(post)
    return downvotes

@register.as_tag
def blog_blogroll(*args):
    return Blogroll.objects.get(id=9).link_set.all() 

@register.inclusion_tag('blog/includes/poll.html')
def show_poll(post):
    proc = 0.0
    proc_up = proc
    proc_down = proc
    upvotes = post.upvote
    downvotes = post.downvote
    summ = float(float(upvotes) + float(downvotes))
    if summ > 0:
        proc = upvotes/summ*100
        proc_up = proc
        proc_down = downvotes/summ*100
    return {'proc': proc,
            'proc_up': int(proc_up),
            'proc_down': int(proc_down),
            'up': int(upvotes),
            'down': int(downvotes),
            'sum': int(summ)}

