from django.contrib.auth.models import User
from rest_framework import serializers

from .models import FileUpload


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class FileUploadSerializer(serializers.ModelSerializer):
    """文件上传序列化器"""

    uploaded_by = UserSerializer(read_only=True)
    file_size_display = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = FileUpload
        fields = [
            "id",
            "file_name",
            "original_name",
            "file_path",
            "file_size",
            "file_size_display",
            "file_type",
            "mime_type",
            "description",
            "tags",
            "uploaded_by",
            "is_public",
            "uploaded_at",
            "updated_at",
            "download_count",
            "last_downloaded",
            "file_extension",
            "download_url",
        ]
        read_only_fields = [
            "id",
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
            "download_url",
        ]

    def get_file_size_display(self, obj):
        """获取人类可读的文件大小"""
        return obj.get_file_size_display()

    def get_file_extension(self, obj):
        """获取文件扩展名"""
        return obj.get_file_extension()

    def get_download_url(self, obj):
        """获取下载URL"""
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/files/{obj.id}/download/")
        return None


class FileUploadCreateSerializer(serializers.ModelSerializer):
    """文件上传创建序列化器"""

    file = serializers.FileField(write_only=True, help_text="要上传的文件")

    class Meta:
        model = FileUpload
        fields = ["file", "description", "tags", "is_public"]

    def validate_file(self, value):
        """验证上传的文件"""
        # 检查文件大小 (10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("文件大小不能超过10MB")

        # 检查文件类型 (可选的安全检查)
        allowed_extensions = [
            ".txt",
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".zip",
            ".rar",
        ]
        file_extension = value.name.lower().split(".")[-1]
        if file_extension not in [ext[1:] for ext in allowed_extensions]:
            raise serializers.ValidationError("不支持的文件类型")

        return value

    def create(self, validated_data):
        """创建文件上传记录"""
        file_obj = validated_data.pop("file")

        # 获取当前用户
        user = self.context["request"].user

        # 创建文件记录
        file_upload = FileUpload.objects.create(
            file_name=file_obj.name,
            original_name=file_obj.name,
            file_path=file_obj,
            file_size=file_obj.size,
            file_type=file_obj.name.split(".")[-1].lower(),
            mime_type=file_obj.content_type,
            uploaded_by=user,
            **validated_data,
        )

        return file_upload


class FileUploadUpdateSerializer(serializers.ModelSerializer):
    """文件上传更新序列化器"""

    class Meta:
        model = FileUpload
        fields = ["description", "tags", "is_public"]

    def update(self, instance, validated_data):
        """更新文件记录"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
