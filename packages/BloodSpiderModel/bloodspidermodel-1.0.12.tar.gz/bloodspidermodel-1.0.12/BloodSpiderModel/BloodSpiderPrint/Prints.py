class Prints:

    def colored_print(self, text, color='white'):
        """
        带颜色输出的print函数

        参数:
            text (str): 要打印的文本
            color (str): 文本颜色，可选值如下:
                'black' - 黑色
                'red' - 红色
                'green' - 绿色
                'yellow' - 黄色
                'blue' - 蓝色
                'magenta' - 洋红色(紫色)
                'cyan' - 青色
                'white' - 白色(默认)
        """
        # ANSI颜色代码字典
        color_codes = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m'
        }

        # 重置颜色的ANSI代码
        reset_code = '\033[0m'

        # 获取对应的颜色代码，如果颜色不存在则使用默认白色
        color_code = color_codes.get(color.lower(), color_codes['white'])

        # 打印带颜色的文本
        print(f"{color_code}{text}{reset_code}")