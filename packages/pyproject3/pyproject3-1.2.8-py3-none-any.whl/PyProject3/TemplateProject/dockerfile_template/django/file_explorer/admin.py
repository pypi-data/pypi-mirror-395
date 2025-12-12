from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import FileUpload


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    """文件上传管理界面"""

    list_display = [
        "id",
        "original_name",
        "file_type",
        "file_size_display",
        "uploaded_by",
        "is_public",
        "uploaded_at",
        "download_count",
    ]

    list_filter = ["file_type", "is_public", "uploaded_at", "uploaded_by"]

    search_fields = ["original_name", "description", "tags", "uploaded_by__username"]

    readonly_fields = [
        "file_name",
        "file_size",
        "file_type",
        "mime_type",
        "uploaded_by",
        "uploaded_at",
        "updated_at",
        "download_count",
        "last_downloaded",
        "file_size_display",
        "file_extension",
    ]

    fieldsets = [
        (
            "文件信息",
            {
                "fields": [
                    "original_name",
                    "file_path",
                    "file_size_display",
                    "file_type",
                    "mime_type",
                ]
            },
        ),
        ("元数据", {"fields": ["description", "tags", "is_public"]}),
        ("用户信息", {"fields": ["uploaded_by", "uploaded_at", "updated_at"]}),
        ("统计信息", {"fields": ["download_count", "last_downloaded"]}),
    ]

    ordering = ["-uploaded_at"]

    list_per_page = 25

    actions = ["make_public", "make_private", "delete_selected_files"]

    def file_size_display(self, obj):
        """显示人类可读的文件大小"""
        return obj.get_file_size_display()

    file_size_display.short_description = "文件大小"

    def file_extension(self, obj):
        """显示文件扩展名"""
        return obj.get_file_extension()

    file_extension.short_description = "文件扩展名"

    def download_link(self, obj):
        """显示下载链接"""
        if obj.file_path:
            url = reverse("file_explorer:download_file", args=[obj.id])
            return format_html('<a href="{}" target="_blank">下载</a>', url)
        return "无文件"

    download_link.short_description = "下载链接"

    def make_public(self, request, queryset):
        """批量设置为公开"""
        updated = queryset.update(is_public=True)
        self.message_user(request, f"成功将 {updated} 个文件设置为公开")

    make_public.short_description = "设置为公开"

    def make_private(self, request, queryset):
        """批量设置为私有"""
        updated = queryset.update(is_public=False)
        self.message_user(request, f"成功将 {updated} 个文件设置为私有")

    make_private.short_description = "设置为私有"

    def delete_selected_files(self, request, queryset):
        """批量删除文件"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"成功删除 {count} 个文件")

    delete_selected_files.short_description = "删除选中的文件"

    def get_queryset(self, request):
        """自定义查询集"""
        qs = super().get_queryset(request)
        return qs.select_related("uploaded_by")

    def has_add_permission(self, request):
        """是否允许添加"""
        return True

    def has_change_permission(self, request, obj=None):
        """是否允许修改"""
        return True

    def has_delete_permission(self, request, obj=None):
        """是否允许删除"""
        return True

    def has_view_permission(self, request, obj=None):
        """是否允许查看"""
        return True
