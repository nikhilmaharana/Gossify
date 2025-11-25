from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Like, Comment


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    readonly_fields = ('user', 'created_at')
    can_delete = True


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('user', 'created_at')
    fields = ('user', 'text', 'created_at')
    can_delete = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('display_author', 'caption_preview', 'created_at', 'anonymous', 'total_likes', 'total_comments', 'image_tag')
    list_filter = ('anonymous', 'created_at', 'author')
    search_fields = ('author__username', 'caption')
    readonly_fields = ['image_tag', 'created_at', 'updated_at']
    inlines = [LikeInline, CommentInline]

    def display_author(self, obj):
        """Show 'Anonymous' if the post is anonymous, else show actual username."""
        return "Anonymous" if obj.anonymous else obj.author.username
    display_author.short_description = 'Author'

    def caption_preview(self, obj):
        """Truncate long captions for readability."""
        return obj.caption[:50] + "..." if len(obj.caption) > 50 else obj.caption
    caption_preview.short_description = 'Caption'

    def total_likes(self, obj):
        """Count likes."""
        return obj.likes.count()
    total_likes.short_description = 'Likes'

    def total_comments(self, obj):
        """Count comments."""
        return obj.comments.count()
    total_comments.short_description = 'Comments'

    def image_tag(self, obj):
        """
        Show a clickable thumbnail of the post image in the admin panel that opens the full image in a new tab.
        """
        if hasattr(obj, 'image') and obj.image:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" style="max-height:100px;"/></a>',
                obj.image.url
            )
        return "-"
    image_tag.short_description = 'Image'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__caption')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'short_text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'text', 'post__caption')

    def short_text(self, obj):
        """
        Show a truncated preview of the comment with a max of 50 characters,
        replacing newlines with spaces for cleaner display.
        """
        text = obj.text.replace("\n", " ").strip()
        return (text[:50] + "...") if len(text) > 50 else text
    short_text.short_description = 'Comment Preview'
