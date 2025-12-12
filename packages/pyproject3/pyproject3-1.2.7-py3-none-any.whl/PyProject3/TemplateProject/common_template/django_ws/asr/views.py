import logging
import wave
import zipfile
from io import BytesIO

from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib import auth
from django.core.handlers.asgi import ASGIRequest
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ninja import NinjaAPI, Query, Redoc
from ninja.renderers import JSONRenderer

from . import objectstorre
from .forms import WavForms
from .models import AsrRecord

logger = logging.getLogger("common.logger")


async def async_auth(request: ASGIRequest):
    request_user = await sync_to_async(auth.get_user)(request)
    return request_user.is_authenticated


json_render = JSONRenderer()

json_render.json_dumps_params = {"ensure_ascii": False}
api = NinjaAPI(
    title="asr api",
    version="2.0",
    description="",
    openapi_url="openapi.json" if settings.DEBUG else "",
    docs_url="docs" if settings.DEBUG else "",
    docs=Redoc(
        settings={
            "expandResponses": "all",
            "jsonSampleExpandLevel": "all",
            "expandSingleSchemaField": True,
            "showObjectSchemaExamples": True,
            "onlyRequiredInSamples": True,
            "showSecuritySchemeType": True,
            "generateCodeSamples": True,
        }
    ),
    renderer=json_render,
    auth=async_auth,
)


@api.get("download_index", summary="获取下载页")
async def download_index(request: ASGIRequest):
    """下载页."""
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin/login/")
    form = WavForms()
    return render(request, "asr/download_wav.html", {"form": form})


@api.get("download", summary="下载 asr 结果")
async def download(request: ASGIRequest, app_id: Query[int], session_id: Query[str]):
    """下载 asr 结果（音频和识别结果的压缩包）.

    :param request:session_id, app_id
    :return:
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin/login/")

    record = await AsrRecord.objects.filter(
        app__id=app_id, session_id=session_id
    ).afirst()
    if not record:
        return HttpResponse("没有找到对应会话！")

    # 创建一个内存流对象，用于写入 ZIP 数据
    memory_file = BytesIO()

    with zipfile.ZipFile(memory_file, "w") as zip_file:
        # 从 minio 下载声音
        for i, spe in enumerate(record.speeches):
            pcm_data = objectstorre.down_obj(spe["bucket_name"], spe["object_name"])
            f = BytesIO()
            wav_obj = wave.Wave_write(f=f)
            wav_obj.setnchannels(1)
            wav_obj.setsampwidth(2)
            wav_obj.setframerate(16000)
            wav_obj.writeframes(pcm_data)
            f.seek(0)
            if len(record.speeches) == 1:
                # 只有一个音频文件就没必要在名称里加序号了
                zip_file.writestr(f"{session_id}.wav", f.read())
            else:
                # 如果有多个音频文件，就在文件名中加序号进行区分
                zip_file.writestr(f"{session_id}-{i}.wav", f.read())
            wav_obj.close()
            f.close()

        # 识别的结果文本也得给
        text_list = "\n".join([r["text"] for r in record.asr_results])
        posts = "\n".join(
            [r.get("post_text") or "" for r in record.asr_results]
        ).strip()
        zip_file.writestr(f"{session_id}.txt", text_list)
        if posts:
            zip_file.writestr(f"{session_id}-词替换后.txt", posts)

    # 将内存流对象指针定位到起始位置，并创建响应对象
    memory_file.seek(0)
    res = FileResponse(
        as_attachment=True,
        streaming_content=memory_file.read(),
        content_type="application/zip",
    )
    memory_file.close()
    res["Content-Disposition"] = "attachment; " f"filename={session_id}.zip"
    res["Access-Control-Allow-Origin"] = "*"
    res["Access-Control-Expose-Headers"] = "content-disposition"
    res["Server"] = "*"
    return res
