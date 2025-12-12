import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class FileUpload(models.Model):
    """文件上传模型"""

    # 文件基本信息
    file_name = models.CharField(max_length=255, verbose_name="文件名")
    original_name = models.CharField(max_length=255, verbose_name="原始文件名")
    file_path = models.FileField(upload_to="uploads/%Y/%m/%d/", verbose_name="文件路径")
    file_size = models.BigIntegerField(verbose_name="文件大小(字节)")

    # 文件类型信息
    file_type = models.CharField(max_length=100, blank=True, verbose_name="文件类型")
    mime_type = models.CharField(max_length=100, blank=True, verbose_name="MIME类型")

    # 元数据
    description = models.TextField(blank=True, verbose_name="文件描述")
    tags = models.CharField(max_length=500, blank=True, verbose_name="标签")

    # 用户和权限
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="上传用户",
        related_name="uploaded_files",
    )
    is_public = models.BooleanField(default=False, verbose_name="是否公开")

    # 时间戳
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name="上传时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    # 下载统计
    download_count = models.PositiveIntegerField(default=0, verbose_name="下载次数")
    last_downloaded = models.DateTimeField(null=True, blank=True, verbose_name="最后下载时间")

    class Meta:
        verbose_name = "文件上传"
        verbose_name_plural = "文件上传"
        ordering = ["-uploaded_at"]
        indexes = [
            models.Index(fields=["uploaded_by", "uploaded_at"]),
            models.Index(fields=["file_type", "uploaded_at"]),
            models.Index(fields=["is_public", "uploaded_at"]),
        ]

    def __str__(self):
        return f"{self.original_name} ({self.uploaded_by.username})"

    def get_file_size_display(self):
        """获取人类可读的文件大小"""
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        elif self.file_size < 1024 * 1024 * 1024:
            return f"{self.file_size / (1024 * 1024):.1f} MB"
        else:
            return f"{self.file_size / (1024 * 1024 * 1024):.1f} GB"

    def get_file_extension(self):
        """获取文件扩展名"""
        return os.path.splitext(self.original_name)[1].lower()

    def increment_download_count(self):
        """增加下载次数"""
        self.download_count += 1
        self.last_downloaded = timezone.now()
        self.save(update_fields=["download_count", "last_downloaded"])

    def delete(self, *args, **kwargs):
        """删除文件时同时删除物理文件"""
        if self.file_path:
            if os.path.isfile(self.file_path.path):
                os.remove(self.file_path.path)
        super().delete(*args, **kwargs)
