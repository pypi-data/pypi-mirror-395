"""
my_awesome_tool - 一个正在开发中的工具。
此为一个名称预留包，项目正在积极开发。
"""

__version__ = "0.0.1"
__author__ = "CoolBlue-ww <3520352176@qq.com>"

# 当有人直接导入这个包时，可以给出提示（可选）
import sys
if not hasattr(sys, '_called_from_setup'):
    print(
        f"Note: You have imported the placeholder package for `CerebraX` (version {__version__}).\n"
        "The actual project is under active development.\n"
        "For more information, visit: https://github.com/CoolBlue-ww/CerebraX",
        file=sys.stderr
    )
