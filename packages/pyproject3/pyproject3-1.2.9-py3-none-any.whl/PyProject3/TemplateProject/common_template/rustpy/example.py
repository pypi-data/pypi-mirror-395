#!/usr/bin/env python3
"""
__NAME__ 使用示例

演示如何使用 Rust 编写的 Python 扩展包。
"""

import __NAME__


def main():
    print("=" * 50)
    print("__NAME__ 使用示例")
    print("=" * 50)

    # 数学工具示例
    print("\n【数学工具】")
    print(f"10 + 5 = {__NAME__.add(10, 5)}")
    print(f"10 - 5 = {__NAME__.subtract(10, 5)}")
    print(f"10 * 5 = {__NAME__.multiply(10, 5)}")
    print(f"10 / 5 = {__NAME__.divide(10, 5)}")
    print(f"2 ^ 8 = {__NAME__.power(2, 8)}")

    # 测试除零错误处理
    try:
        result = __NAME__.divide(10, 0)
    except ValueError as e:
        print(f"除零错误: {e}")

    # 字符串工具示例
    print("\n【字符串工具】")
    text = "Hello, World!"
    print(f"原字符串: {text}")
    print(f"反转: {__NAME__.reverse_string(text)}")
    print(f"大写: {__NAME__.to_uppercase(text)}")
    print(f"小写: {__NAME__.to_lowercase(text)}")
    print(f"字符数: {__NAME__.count_chars(text)}")

    # 数据处理示例
    print("\n【数据处理】")
    data = [1.0, 2.5, 3.7, 4.2, 5.9]
    processor = __NAME__.DataProcessor(data)

    print(f"数据: {processor.get_data()}")
    print(f"总和: {processor.sum()}")
    print(f"平均值: {processor.average():.2f}")
    print(f"最大值: {processor.max()}")
    print(f"最小值: {processor.min()}")
    print(f"数量: {processor.count()}")

    # 添加新数据
    print("\n添加新数据 6.5...")
    processor.add_data(6.5)
    print(f"更新后的数据: {processor.get_data()}")
    print(f"新的总和: {processor.sum()}")
    print(f"新的平均值: {processor.average():.2f}")

    print("\n" + "=" * 50)
    print("示例运行完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
