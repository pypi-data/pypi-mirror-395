from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "file_explorer"

# REST API 路由
router = DefaultRouter()
router.register(r"files", views.FileUploadViewSet, basename="file")

# API URLs
api_urls = [
    path("api/", include(router.urls)),
    # 直接的文件上传端点（支持curl）
    path("api/upload/", views.api_upload_file, name="api_upload_file"),
]

# 模板视图 URLs
template_urls = [
    # 文件列表
    path("", views.FileListView.as_view(), name="file_list"),
    # 文件详情
    path("file/<int:pk>/", views.FileDetailView.as_view(), name="file_detail"),
    # 文件上传
    path("upload/", views.FileUploadView.as_view(), name="file_upload"),
    # 文件编辑
    path("file/<int:pk>/edit/", views.FileUpdateView.as_view(), name="file_update"),
    # 文件删除
    path("file/<int:pk>/delete/", views.FileDeleteView.as_view(), name="file_delete"),
    # 文件下载
    path("file/<int:file_id>/download/", views.download_file, name="download_file"),
    # 文件搜索
    path("search/", views.search_files, name="search_files"),
]

# 合并所有URLs
urlpatterns = api_urls + template_urls
