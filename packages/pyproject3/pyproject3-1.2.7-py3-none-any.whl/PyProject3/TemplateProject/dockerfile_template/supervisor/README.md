
# xmov_benchmark


## 测试ASR性能
```bash
cd app/asr
python benchmark.py
```

### 开发配置

```bash

# 安装开发依赖
pip install -e ".[dev]"

# 手动修改修改__init__.py中的__version__， 然后打包
make build

# 上传到xmov-pypi, 需要安装twine， 配置~/.pypirc
make upload
```

    