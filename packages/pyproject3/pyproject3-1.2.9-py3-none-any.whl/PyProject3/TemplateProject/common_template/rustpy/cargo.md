Cargo 使用说明
==============

Cargo 是 Rust 的官方包管理器和构建工具。它负责构建代码、下载依赖、编译项目等任务。

一、安装 Cargo
--------------
Cargo 通常随 Rust 一起安装。如果已安装 Rust，Cargo 应该已经可用。

检查 Cargo 是否安装：
    cargo --version

如果没有安装，请访问 https://www.rust-lang.org/ 安装 Rust。

二、创建新项目
--------------
创建新的二进制项目（可执行程序）：
    cargo new project_name

创建新的库项目：
    cargo new --lib library_name

在当前目录初始化项目：
    cargo init

三、项目结构
-----------
一个标准的 Cargo 项目包含以下文件：

    project_name/
    ├── Cargo.toml      # 项目配置文件
    ├── Cargo.lock      # 依赖锁定文件（自动生成）
    ├── src/            # 源代码目录
    │   └── main.rs     # 主程序入口（二进制项目）
    │   └── lib.rs      # 库入口（库项目）
    └── target/         # 编译输出目录（自动生成）

四、常用命令
-----------

1. 构建项目
   cargo build
   - 编译项目，生成可执行文件在 target/debug/ 目录
   - 首次运行会下载依赖

2. 运行项目
   cargo run
   - 编译并运行项目
   - 等同于 cargo build && ./target/debug/project_name

3. 检查代码（不编译）
   cargo check
   - 快速检查代码是否有错误，不生成可执行文件
   - 比 cargo build 更快

4. 运行测试
   cargo test
   - 运行项目中的所有测试

5. 构建发布版本
   cargo build --release
   - 生成优化后的发布版本
   - 可执行文件在 target/release/ 目录
   - 编译时间更长，但运行速度更快

6. 运行发布版本
   cargo run --release

7. 添加依赖
   cargo add package_name
   - 添加依赖到 Cargo.toml 并安装

8. 更新依赖
   cargo update
   - 更新 Cargo.lock 中的依赖版本

9. 清理构建文件
   cargo clean
   - 删除 target/ 目录，释放磁盘空间

10. 查看项目信息
    cargo tree
    - 显示依赖树

11. 查看文档
    cargo doc
    - 生成项目文档
    - 文档在 target/doc/ 目录

    cargo doc --open
    - 生成并打开文档

五、Cargo.toml 配置文件
-----------------------
Cargo.toml 是项目的配置文件，包含项目元数据和依赖信息。

示例：

    [package]
    name = "my_project"
    version = "0.1.0"
    edition = "2021"

    [dependencies]
    serde = "1.0"
    tokio = { version = "1.0", features = ["full"] }

主要字段说明：
- name: 项目名称
- version: 项目版本
- edition: Rust 版本（2015, 2018, 2021）
- dependencies: 项目依赖

六、工作空间（Workspace）
------------------------
多个相关项目可以组织在一个工作空间中：

    workspace/
    ├── Cargo.toml      # 工作空间配置
    ├── project1/
    │   └── Cargo.toml
    └── project2/
        └── Cargo.toml

工作空间 Cargo.toml 示例：

    [workspace]
    members = ["project1", "project2"]

七、常用技巧
-----------

1. 使用环境变量
   RUST_LOG=debug cargo run
   - 设置日志级别

2. 指定特性（features）
   cargo build --features feature_name

3. 并行编译
   cargo build -j N
   - N 为并行任务数

4. 详细输出
   cargo build --verbose
   - 显示详细的编译信息

5. 只编译特定包（工作空间中）
   cargo build -p package_name

八、常见问题
-----------

1. 编译速度慢
   - 使用 cargo check 进行快速检查
   - 使用 cargo build --release 只在需要时使用
   - 考虑使用 sccache 缓存编译结果

2. 依赖下载慢
   - 配置国内镜像源（如清华大学、中科大镜像）

3. 清理缓存
   cargo clean
   - 清理编译缓存

九、获取帮助
-----------
查看所有可用命令：
    cargo --help

查看特定命令的帮助：
    cargo build --help
    cargo run --help

更多信息请访问：
- 官方文档: https://doc.rust-lang.org/cargo/
- Cargo 手册: https://doc.rust-lang.org/cargo/guide/

