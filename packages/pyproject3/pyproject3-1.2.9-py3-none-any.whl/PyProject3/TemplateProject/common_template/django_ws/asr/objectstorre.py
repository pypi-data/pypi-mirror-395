""" "封装对象存储服务."""

import logging
import threading
from queue import Queue
from typing import BinaryIO, override

from django.conf import settings
from minio import Minio
from minio.error import MinioException
from minio.helpers import MIN_PART_SIZE

logger = logging.getLogger("common.logger")


class StreamIO(BinaryIO):
    """音频 io，为 minio 上传文件特意准备的."""

    def __init__(self):
        self.buff_q = Queue()

    @override
    def readable(self) -> bool:
        return True

    @override
    def writable(self) -> bool:
        return True

    @override
    def read(self) -> bytes:
        """读取数据.
        返回读取到的字节数据。如果当前流已无数据可读，则返回一个空 bytes，即 b''。
        """
        part_size = 0
        part_data = bytearray()
        while part_size < MIN_PART_SIZE:
            one_data = self.buff_q.get()
            if len(one_data) == 0:
                break
            part_data.extend(one_data)
        # 因为返回 b"" 时表示结束标志，为了避免结束标志被错误的消费掉，需要补齐
        if 0 < len(part_data) < MIN_PART_SIZE:
            self.buff_q.put(b"")
        return bytes(part_data)

    @override
    def write(self, data: bytes):
        """写入数据.
        写入一个空 bytes（b''）表示后面再无数据写入了。
        """
        self.buff_q.put(data)


class StreamUploadThread(threading.Thread):
    """流式上传线程，上传数据到 minio."""

    def __init__(self, obj_name: str):
        """流式上传线程.

        args:
            obj_name:目标对象名.
        """
        super().__init__()
        self.obj_name = obj_name
        self.obj_size = 0
        self.io_q = StreamIO()
        self.minio_client = Minio(
            endpoint=settings.MINIO_ADDR,
            access_key=settings.MINIO_AK,
            secret_key=settings.MINIO_SK,
            secure=False,
        )

    def run(self):
        try:
            self.minio_client.stream_put_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=self.obj_name,
                data=self.io_q,
            )
        except MinioException:
            logger.error("上传音频数据出错", exc_info=True)
        except:  # noqa: E722
            logger.error("上传音频未预料到的错误", exc_info=True)

    def append(self, data: bytes):
        """添加需要上传的数据.
        data 为空 bytes（b''）表示后面再无数据需要上传了。
        """
        self.io_q.write(data)
        self.obj_size += len(data)


def down_obj(bucket_name: str, object_name: str) -> bytes:
    """从 minio 下载对象并返回."""
    minio_client = Minio(
        endpoint=settings.MINIO_ADDR,
        access_key=settings.MINIO_AK,
        secret_key=settings.MINIO_SK,
        secure=False,
    )
    response = None
    try:
        response = minio_client.get_object(
            bucket_name=bucket_name, object_name=object_name
        )
        data = response.data
        return data
    finally:
        if response:
            response.close()
            response.release_conn()
