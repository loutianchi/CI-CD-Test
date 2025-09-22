# test_calculator.py

import pytest
from py_calculator.calc import calculate


# 1. 使用 @pytest.mark.parametrize 来测试多组合法的表达式
# 这是 pytest 最强大的功能之一
@pytest.mark.parametrize("expression, expected", [
    # 简单运算
    ("5 + 3", 8.0),
    ("10 - 4", 6.0),
    ("7 * 3", 21.0),
    ("20 / 5", 4.0),
    # 无空格
    ("3+5*2", 13.0),
    # 运算符优先级
    ("3 + 5 * 2", 13.0),
    ("10 - 8 / 4", 8.0),
    # 长表达式
    ("10 + 2 * 6 - 4 / 2", 20.0),
    ("100 - 5 * 10 + 20 / 2", 60.0),
    # 单个数字
    ("7", 7.0)
])
def test_valid_expressions(expression, expected):
    """
    测试各种合法的表达式
    """
    assert calculate(expression) == expected


# 2. 单独测试浮点数，使用 pytest.approx 来处理精度问题
@pytest.mark.parametrize("expression, expected", [
    ("2.5 * 4", 10.0),
    ("10.5 / 2", 5.25),
    ("3.1 + 4.2 * 2", 11.5),
    ("0.1 + 0.2", 0.3)  # 经典的浮点数精度问题
])
def test_float_expressions(expression, expected):
    """
    测试包含浮点数的表达式
    """
    assert calculate(expression) == pytest.approx(expected)


# 3. 使用 pytest.raises 来测试预期的异常
@pytest.mark.parametrize("expression, error", [
    # 除零错误
    ("10 / 0", ZeroDivisionError),
    # 无效表达式
    ("5 * + 3", ValueError),
    ("", ValueError),
    ("5 +", ValueError),
])
def test_invalid_expressions(expression, error):
    """
    测试会引发异常的无效表达式
    """
    with pytest.raises(error):
        calculate(expression)


# 也可以写一些独立的、不带参数的测试函数
def test_simple_case_without_param():
    """
    一个独立的简单测试用例
    """
    assert calculate("1 + 1") == 2
