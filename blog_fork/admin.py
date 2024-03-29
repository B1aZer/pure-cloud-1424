
from copy import deepcopy

from django.contrib import admin

from .models import BlogPost, BlogCategory
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin
from .models import Blogroll, Link


blogpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
blogpost_fieldsets[0][1]["fields"].insert(1, "categories")
blogpost_fieldsets[0][1]["fields"].extend(["content", "allow_comments", "show_poll"])
blogpost_list_display = ["title", "user", "status", "admin_link"]
if settings.BLOG_USE_FEATURED_IMAGE:
    blogpost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    blogpost_list_display.insert(0, "admin_thumb")


class BlogPostAdmin(DisplayableAdmin, OwnableAdmin):
    """
    Admin class for blog posts.
    """

    fieldsets = blogpost_fieldsets
    list_display = blogpost_list_display
    filter_horizontal = ("categories",)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class BlogCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for blog categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "blog.BlogCategory" in items:
                return True
        return False



class LinksInline(TabularDynamicInlineAdmin):
    model = Link

class BlogrollAdmin(PageAdmin):
    inlines = (LinksInline,)
    readonly_fields = ['dob']
    fieldsets = ((None, {'fields': ('dob',)}),)

admin.site.register(Blogroll, BlogrollAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
