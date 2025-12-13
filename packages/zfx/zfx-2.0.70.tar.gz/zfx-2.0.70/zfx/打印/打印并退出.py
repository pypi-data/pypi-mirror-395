import sys

def 打印并退出(*args, 状态码: int = 0) -> None:
    """
    打印内容后立即结束程序运行,一般常用于日常开发时使用。

    Args:
        *args: 任意数量的要打印的内容，与 print() 参数一致。
        状态码 (int): 退出状态码。0 表示正常退出，非 0 表示异常退出。
    """
    print(*args)
    sys.exit(状态码)
