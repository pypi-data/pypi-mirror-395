# __NAME__ - Rust 编写的 Python 扩展包

这是一个使用 Rust 和 PyO3 编写的 Python 扩展包示例。

## 功能特性

- **数学工具**: 加法、减法、乘法、除法、幂运算
- **字符串工具**: 反转字符串、大小写转换、字符统计
- **数据处理**: DataProcessor 类，提供数据统计和处理功能

## 安装要求

- Rust (最新稳定版)
- Python 3.7+
- maturin (用于构建 Python 扩展)

## 安装 maturin

```bash
# 使用 pip 安装
pip install maturin
# 或者使用 cargo
cargo install maturin
```

## 构建和安装

### 开发模式（推荐用于开发）

```bash
# 在 __NAME__ 目录下
maturin develop

### 发布模式
maturin build --release 
pip install target/wheels/__NAME__-*.whl

### 直接安装
maturin develop --release
```

## 使用方法

安装后，可以在 Python 中这样使用：

```python
import __NAME__

# 使用数学工具
result = __NAME__.add(10, 5)
print(f"10 + 5 = {result}")

result = __NAME__.multiply(4, 7)
print(f"4 * 7 = {result}")

result = __NAME__.power(2, 8)
print(f"2^8 = {result}")

# 使用字符串工具
reversed = __NAME__.reverse_string("Hello, World!")
print(f"反转: {reversed}")

upper = __NAME__.to_uppercase("hello")
print(f"大写: {upper}")

count = __NAME__.count_chars("Python")
print(f"字符数: {count}")

# 使用数据处理类
processor = __NAME__.DataProcessor([1.0, 2.0, 3.0, 4.0, 5.0])
print(f"总和: {processor.sum()}")
print(f"平均值: {processor.average()}")
print(f"最大值: {processor.max()}")
print(f"最小值: {processor.min()}")
print(f"数量: {processor.count()}")

# 添加数据
processor.add_data(6.0)
print(f"添加后总和: {processor.sum()}")
```

## 项目结构

```
__NAME__/
├── Cargo.toml          # Rust 项目配置
├── pyproject.toml      # Python 包配置
├── src/
│   └── lib.rs          # Rust 源代码
├── README.md           # 说明文档
└── example.py          # 使用示例
```

## 开发

### 运行测试

```bash
# 运行 Rust 测试
cargo test

# 运行 Python 测试（需要先安装）
maturin develop
pytest
```

### 清理构建文件

```bash
cargo clean
```
 
## 更多信息

- [PyO3 文档](https://pyo3.rs/)
- [maturin 文档](https://maturin.rs/)
- [Rust 官方文档](https://www.rust-lang.org/)

