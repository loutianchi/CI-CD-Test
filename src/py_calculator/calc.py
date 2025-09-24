import re


def calculate(expression: str) -> float:
    """
    安全地计算字符串数学表达式 (支持+, -, *, /).

    该函数首先将中缀表达式转换为后缀表达式 (RPN),
    然后计算后缀表达式得出结果.
    """

    # 1. 中缀表达式转后缀表达式 (Shunting-yard algorithm)
    def infix_to_postfix(tokens):
        # 运算符优先级
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []  # 输出队列
        operators = []  # 运算符栈

        for token in tokens:
            if token.replace('.', '', 1).isdigit():  # 判断是否为数字 (包括浮点数)
                output.append(float(token))
            elif token in precedence:
                # 当运算符栈不为空, 且栈顶运算符优先级更高或相同时, 弹出
                while (
                    operators
                    and precedence.get(operators[-1], 0) >= precedence[token]
                ):
                    output.append(operators.pop())
                operators.append(token)

        # 将剩余的运算符全部弹出到输出队列
        while operators:
            output.append(operators.pop())

        return output

    # 2. 计算后缀表达式
    def evaluate_postfix(postfix_tokens):
        stack = []
        for token in postfix_tokens:
            if isinstance(token, float):  # 如果是数字, 入栈
                stack.append(token)
            else:  # 如果是运算符
                if len(stack) < 2:
                    raise ValueError("无效的表达式: 运算符缺少操作数")

                # 弹出两个操作数
                operand2 = stack.pop()
                operand1 = stack.pop()

                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("错误: 除数为零")
                    stack.append(operand1 / operand2)

        if len(stack) != 1:
            raise ValueError("无效的表达式: 操作数过多")

        return stack[0]

    # --- 主逻辑 ---
    # 1. 预处理: 移除所有空格
    sanitized_expr = expression.replace(" ", "")

    # 如果处理后为空字符串, 直接认为是无效表达式
    if not sanitized_expr:
        raise ValueError("表达式为空或无效")

    # 2. 词法分析: 提取所有 token
    tokens = re.findall(r'(\d+\.?\d*|[\+\-\*\/])', sanitized_expr)

    # 3. 验证步骤
    # 检查所有 token 拼接后是否等于预处理过的字符串
    if "".join(tokens) != sanitized_expr:
        raise ValueError("表达式包含无效字符或格式错误")

    # 4. 转换并计算
    postfix_expr = infix_to_postfix(tokens)
    result = evaluate_postfix(postfix_expr)

    return result
