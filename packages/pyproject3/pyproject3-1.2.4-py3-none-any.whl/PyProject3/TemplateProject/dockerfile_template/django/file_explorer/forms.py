from django import forms

from .models import FileUpload


class FileUploadForm(forms.ModelForm):
    """文件上传表单"""

    class Meta:
        model = FileUpload
        fields = ["file_path", "description", "tags", "is_public"]
        widgets = {
            "file_path": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.gif,.zip,.rar,.txt",
                }
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "请输入文件描述（可选）"}
            ),
            "tags": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "请输入标签，用逗号分隔（可选）"}
            ),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_tags(self):
        """清理标签字段，将逗号分隔的标签转换为空格分隔"""
        tags = self.cleaned_data.get("tags", "")
        if tags:
            # 将逗号分隔的标签转换为空格分隔
            tags = tags.replace(",", " ").replace("，", " ")
            # 移除多余的空格
            tags = " ".join(tags.split())
        return tags

    def clean_file_path(self):
        """验证上传的文件"""
        file_path = self.cleaned_data.get("file_path")
        if file_path:
            # 检查文件大小 (10MB)
            if file_path.size > 10 * 1024 * 1024:
                raise forms.ValidationError("文件大小不能超过10MB")

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
            file_extension = file_path.name.lower().split(".")[-1]
            if file_extension not in [ext[1:] for ext in allowed_extensions]:
                raise forms.ValidationError("不支持的文件类型")

        return file_path


class FileUpdateForm(forms.ModelForm):
    """文件更新表单"""

    class Meta:
        model = FileUpload
        fields = ["description", "tags", "is_public"]
        widgets = {
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "请输入文件描述..."}
            ),
            "tags": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "请输入标签，用空格分隔..."}
            ),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_tags(self):
        """清理标签字段"""
        tags = self.cleaned_data.get("tags", "")
        if tags:
            # 移除多余的空格
            tags = " ".join(tags.split())
        return tags
