## todo
-   [x] 完成并发控制。
-   [x] 定义返回给第调用方的状态码。
-   [ ] 重新创建数据库模型，不考虑旧数据，考虑 MongoDB。
    -   [x] App 和 App config 之间考虑用嵌套模型，更符合直觉。
    -   [x] 热词和改写词也内嵌到 app 模型中，更符合直觉。
-   [x] 将 asrapps、hotwords、substitutewords、wavs 四个 app 删除，将它们的功能收归到 asr app 中。
-   [ ] 调研 Django 4.x + 基于 channels 实现的异步 WebSocket 该如何部署。 