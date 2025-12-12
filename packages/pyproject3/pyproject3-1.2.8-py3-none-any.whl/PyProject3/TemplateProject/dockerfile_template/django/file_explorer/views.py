import json
import mimetypes
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .forms import FileUpdateForm, FileUploadForm
from .models import FileUpload
from .serializers import (
    FileUploadCreateSerializer,
    FileUploadSerializer,
    FileUploadUpdateSerializer,
)

# ==================== Django REST Framework Views ====================


class FileUploadViewSet(viewsets.ModelViewSet):
    """文件上传视图集"""

    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """根据用户权限过滤查询集"""
        user = self.request.user

        # 如果是超级用户，可以看到所有文件
        if user.is_superuser:
            return FileUpload.objects.all()

        # 普通用户只能看到自己的文件和公开文件
        return FileUpload.objects.filter(Q(uploaded_by=user) | Q(is_public=True))

    def get_serializer_class(self):
        """根据操作类型选择序列化器"""
        if self.action == "create":
            return FileUploadCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return FileUploadUpdateSerializer
        return FileUploadSerializer

    def perform_create(self, serializer):
        """创建文件记录"""
        serializer.save(uploaded_by=self.request.user)

    def perform_update(self, serializer):
        """更新文件记录"""
        serializer.save()

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        """下载文件"""
        file_upload = self.get_object()

        # 检查权限
        if not file_upload.is_public and file_upload.uploaded_by != request.user:
            return Response({"error": "没有权限下载此文件"}, status=status.HTTP_403_FORBIDDEN)

        # 检查文件是否存在
        if not file_upload.file_path or not os.path.exists(file_upload.file_path.path):
            return Response({"error": "文件不存在"}, status=status.HTTP_404_NOT_FOUND)

        # 增加下载次数
        file_upload.increment_download_count()

        # 准备下载响应
        file_path = file_upload.file_path.path
        file_name = file_upload.original_name

        # 获取MIME类型
        content_type, _ = mimetypes.guess_type(file_name)
        if content_type is None:
            content_type = "application/octet-stream"

        # 读取文件并返回
        try:
            with open(file_path, "rb") as f:
                response = HttpResponse(f.read(), content_type=content_type)
                response["Content-Disposition"] = f'attachment; filename="{file_name}"'
                return response
        except Exception as e:
            return Response(
                {"error": f"文件读取失败: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def my_files(self, request):
        """获取当前用户的文件"""
        queryset = self.get_queryset().filter(uploaded_by=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def public_files(self, request):
        """获取公开文件"""
        queryset = self.get_queryset().filter(is_public=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """搜索文件"""
        query = request.query_params.get("q", "")
        if not query:
            return Response({"error": "请提供搜索关键词"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset().filter(
            Q(original_name__icontains=query)
            | Q(description__icontains=query)
            | Q(tags__icontains=query)
            | Q(file_type__icontains=query)
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="upload-file")
    def upload_file(self, request):
        """通过API上传文件（支持curl）"""
        try:
            # 检查是否有文件上传
            if "file" not in request.FILES:
                return Response(
                    {"error": "请提供文件，使用 'file' 作为字段名"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            uploaded_file = request.FILES["file"]

            # 验证文件
            if uploaded_file.size > 10 * 1024 * 1024:  # 10MB限制
                return Response(
                    {"error": "文件大小不能超过10MB"}, status=status.HTTP_400_BAD_REQUEST
                )

            # 检查文件类型
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
            file_extension = uploaded_file.name.lower().split(".")[-1]
            if file_extension not in [ext[1:] for ext in allowed_extensions]:
                return Response(
                    {"error": "不支持的文件类型"}, status=status.HTTP_400_BAD_REQUEST
                )

            # 获取其他参数
            description = request.data.get("description", "")
            tags = request.data.get("tags", "")
            is_public = request.data.get("is_public", False)

            # 处理标签（将逗号分隔转换为空格分隔）
            if tags:
                tags = tags.replace(",", " ").replace("，", " ")
                tags = " ".join(tags.split())

            # 创建文件记录
            file_upload = FileUpload.objects.create(
                file_name=uploaded_file.name,
                original_name=uploaded_file.name,
                file_path=uploaded_file,
                file_size=uploaded_file.size,
                file_type=file_extension,
                mime_type=uploaded_file.content_type or "application/octet-stream",
                description=description,
                tags=tags,
                is_public=is_public,
                uploaded_by=request.user,
            )

            # 返回成功响应
            serializer = self.get_serializer(file_upload)
            return Response(
                {"message": "文件上传成功", "file": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": f"文件上传失败: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==================== Django Template Views ====================


class FileListView(LoginRequiredMixin, ListView):
    """文件列表视图"""

    model = FileUpload
    template_name = "file_explorer/file_list.html"
    context_object_name = "files"
    paginate_by = 20

    def get_queryset(self):
        """根据用户权限过滤文件"""
        user = self.request.user

        if user.is_superuser:
            return FileUpload.objects.all()

        return FileUpload.objects.filter(Q(uploaded_by=user) | Q(is_public=True))

    def get_context_data(self, **kwargs):
        """添加上下文数据"""
        context = super().get_context_data(**kwargs)
        context["total_files"] = self.get_queryset().count()
        context["my_files_count"] = FileUpload.objects.filter(
            uploaded_by=self.request.user
        ).count()
        context["public_files_count"] = FileUpload.objects.filter(
            is_public=True
        ).count()
        return context


class FileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """文件详情视图"""

    model = FileUpload
    template_name = "file_explorer/file_detail.html"
    context_object_name = "file"

    def test_func(self):
        """检查用户是否有权限查看文件"""
        file_obj = self.get_object()
        user = self.request.user

        # 超级用户可以查看所有文件
        if user.is_superuser:
            return True

        # 文件所有者可以查看
        if file_obj.uploaded_by == user:
            return True

        # 公开文件可以查看
        if file_obj.is_public:
            return True

        return False


class FileUploadView(LoginRequiredMixin, CreateView):
    """文件上传视图"""

    model = FileUpload
    template_name = "file_explorer/file_upload.html"
    form_class = FileUploadForm
    success_url = reverse_lazy("file_explorer:file_list")

    def form_valid(self, form):
        """表单验证成功后的处理"""
        try:
            print("=== File Upload Debug Info ===")
            print(f"Form data keys: {form.cleaned_data.keys()}")
            print(f"Form files: {self.request.FILES}")

            form.instance.uploaded_by = self.request.user

            # 获取上传的文件对象
            uploaded_file = form.cleaned_data["file_path"]
            print(f"Uploaded file: {uploaded_file}")
            print(f"File type: {type(uploaded_file)}")
            print(f"File attributes: {dir(uploaded_file)}")

            # 检查是否是InMemoryUploadedFile或TemporaryUploadedFile
            from django.core.files.uploadedfile import (
                InMemoryUploadedFile,
                TemporaryUploadedFile,
            )

            if isinstance(uploaded_file, (InMemoryUploadedFile, TemporaryUploadedFile)):
                print("File is InMemoryUploadedFile or TemporaryUploadedFile")
            else:
                print("File is not a standard uploaded file type")

            # 验证文件对象
            if not uploaded_file:
                messages.error(self.request, "没有选择文件")
                return self.form_invalid(form)

                # 设置文件属性
            form.instance.file_name = uploaded_file.name
            form.instance.original_name = uploaded_file.name

            # 获取文件大小
            try:
                if hasattr(uploaded_file, "size"):
                    form.instance.file_size = uploaded_file.size
                    print(f"File size from size attribute: {uploaded_file.size}")
                else:
                    # 如果size属性不存在，尝试其他方法
                    print("Size attribute not found, trying alternative method")
                    uploaded_file.seek(0, 2)  # 移动到文件末尾
                    form.instance.file_size = uploaded_file.tell()
                    uploaded_file.seek(0)  # 重置到文件开头
                    print(f"File size from seek/tell: {form.instance.file_size}")
            except Exception as size_error:
                print(f"File size error: {size_error}")
                form.instance.file_size = 0

            print(f"File name: {uploaded_file.name}")

            # 获取文件扩展名
            if "." in uploaded_file.name:
                form.instance.file_type = uploaded_file.name.split(".")[-1].lower()
            else:
                form.instance.file_type = "unknown"

            print(f"File extension: {form.instance.file_type}")

            # 获取MIME类型
            try:
                print("Checking content_type attribute...")
                if hasattr(uploaded_file, "content_type"):
                    form.instance.mime_type = uploaded_file.content_type
                    print(f"MIME type from content_type: {uploaded_file.content_type}")
                else:
                    print("content_type attribute not found, using mimetypes")
                    # 使用mimetypes模块来猜测MIME类型
                    import mimetypes

                    guessed_type, _ = mimetypes.guess_type(uploaded_file.name)
                    form.instance.mime_type = guessed_type or "application/octet-stream"
                    print(f"MIME type from mimetypes: {form.instance.mime_type}")
            except Exception as mime_error:
                print(f"MIME type error: {mime_error}")
                form.instance.mime_type = "application/octet-stream"

            print("=== End Debug Info ===")

            messages.success(self.request, "文件上传成功！")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"文件上传处理失败: {str(e)}")
            # 记录详细错误信息用于调试
            import traceback

            print(f"File upload error: {str(e)}")
            print(traceback.format_exc())
            return self.form_invalid(form)

    def form_invalid(self, form):
        """表单验证失败后的处理"""
        # 记录详细的表单错误
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")

        messages.error(self.request, "文件上传失败，请检查输入信息！")
        return super().form_invalid(form)


class FileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """文件更新视图"""

    model = FileUpload
    template_name = "file_explorer/file_update.html"
    form_class = FileUpdateForm
    success_url = reverse_lazy("file_explorer:file_list")

    def test_func(self):
        """检查用户是否有权限编辑文件"""
        file_obj = self.get_object()
        user = self.request.user

        # 超级用户可以编辑所有文件
        if user.is_superuser:
            return True

        # 文件所有者可以编辑
        return file_obj.uploaded_by == user


class FileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """文件删除视图"""

    model = FileUpload
    template_name = "file_explorer/file_confirm_delete.html"
    success_url = reverse_lazy("file_explorer:file_list")

    def test_func(self):
        """检查用户是否有权限删除文件"""
        file_obj = self.get_object()
        user = self.request.user

        # 超级用户可以删除所有文件
        if user.is_superuser:
            return True

        # 文件所有者可以删除
        return file_obj.uploaded_by == user

    def delete(self, request, *args, **kwargs):
        """删除文件"""
        messages.success(request, "文件删除成功！")
        return super().delete(request, *args, **kwargs)


@login_required
def download_file(request, file_id):
    """文件下载视图"""
    file_upload = get_object_or_404(FileUpload, id=file_id)

    # 检查权限
    if not file_upload.is_public and file_upload.uploaded_by != request.user:
        if not request.user.is_superuser:
            messages.error(request, "没有权限下载此文件！")
            return redirect("file_explorer:file_list")

    # 检查文件是否存在
    if not file_upload.file_path or not os.path.exists(file_upload.file_path.path):
        messages.error(request, "文件不存在！")
        return redirect("file_explorer:file_list")

    # 增加下载次数
    file_upload.increment_download_count()

    # 准备下载响应
    file_path = file_upload.file_path.path
    file_name = file_upload.original_name

    # 获取MIME类型
    content_type, _ = mimetypes.guess_type(file_name)
    if content_type is None:
        content_type = "application/octet-stream"

    # 读取文件并返回
    try:
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type=content_type)
            response["Content-Disposition"] = f'attachment; filename="{file_name}"'
            return response
    except Exception as e:
        messages.error(request, f"文件读取失败: {str(e)}")
        return redirect("file_explorer:file_list")


@login_required
def search_files(request):
    """文件搜索视图"""
    try:
        query = request.GET.get("q", "")
        if not query:
            return redirect("file_explorer:file_list")

        user = request.user

        if user.is_superuser:
            files = FileUpload.objects.filter(
                Q(original_name__icontains=query)
                | Q(description__icontains=query)
                | Q(tags__icontains=query)
                | Q(file_type__icontains=query)
            )
        else:
            files = FileUpload.objects.filter(
                (Q(uploaded_by=user) | Q(is_public=True))
                & (
                    Q(original_name__icontains=query)
                    | Q(description__icontains=query)
                    | Q(tags__icontains=query)
                    | Q(file_type__icontains=query)
                )
            )

        # 分页
        paginator = Paginator(files, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "files": page_obj,
            "query": query,
            "total_results": files.count(),
        }

        return render(request, "file_explorer/search_results.html", context)
    except Exception as e:
        messages.error(request, f"搜索失败: {str(e)}")
        return redirect("file_explorer:file_list")


@csrf_exempt
def api_upload_file(request):
    """通过API上传文件（支持curl，无需认证）"""
    if request.method != "POST":
        return JsonResponse({"error": "只支持POST方法"}, status=405)

    try:
        # 检查是否有文件上传
        if "file" not in request.FILES:
            return JsonResponse(
                {
                    "error": "请提供文件，使用 'file' 作为字段名",
                    "example": "curl -X POST -F 'file=@your_file.txt' -F 'description=文件描述' -F 'tags=标签1,标签2' -F 'is_public=true' http://localhost:8000/files/api/upload/",
                },
                status=400,
            )

        uploaded_file = request.FILES["file"]

        # 验证文件
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB限制
            return JsonResponse({"error": "文件大小不能超过10MB"}, status=400)

        # 检查文件类型
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
        file_extension = uploaded_file.name.lower().split(".")[-1]
        if file_extension not in [ext[1:] for ext in allowed_extensions]:
            return JsonResponse(
                {"error": "不支持的文件类型", "allowed_types": allowed_extensions}, status=400
            )

        # 获取其他参数
        description = request.POST.get("description", "")
        tags = request.POST.get("tags", "")
        is_public = request.POST.get("is_public", "false").lower() == "true"

        # 获取或创建默认用户（用于API上传）
        try:
            # 尝试获取admin用户，如果不存在则创建
            user = User.objects.filter(is_superuser=True).first()
        except Exception as user_error:
            return JsonResponse({"error": f"缺少用户: {str(user_error)}"}, status=500)

        # 处理标签（将逗号分隔转换为空格分隔）
        if tags:
            tags = tags.replace(",", " ").replace("，", " ")
            tags = " ".join(tags.split())

        # 创建文件记录
        file_upload = FileUpload.objects.create(
            file_name=uploaded_file.name,
            original_name=uploaded_file.name,
            file_path=uploaded_file,
            file_size=uploaded_file.size,
            file_type=file_extension,
            mime_type=uploaded_file.content_type or "application/octet-stream",
            description=description,
            tags=tags,
            is_public=is_public,
            uploaded_by=user,
        )

        # 返回成功响应
        return JsonResponse(
            {
                "message": "文件上传成功",
                "file_id": file_upload.id,
                "file_name": file_upload.original_name,
                "file_size": file_upload.file_size,
                "file_type": file_upload.file_type,
                "uploaded_at": file_upload.uploaded_at.isoformat(),
                "download_url": f"/files/file/{file_upload.id}/download/",
                "view_url": f"/files/file/{file_upload.id}/",
            },
            status=201,
        )

    except Exception as e:
        return JsonResponse({"error": f"文件上传失败: {str(e)}"}, status=500)
