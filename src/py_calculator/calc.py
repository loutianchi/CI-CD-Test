import re


def calculate(expression: str) -> float:
    """
    安全地计算字符串数学表达式（支持+、-、*、/）。

    该函数首先将中缀表达式转换为后缀表达式（RPN），
    然后计算后缀表达式得出结果。
    """

    # 1. 中缀表达式转后缀表达式 (Shunting-yard algorithm)
    def infix_to_postfix(tokens):
        # 运算符优先级
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []  # 输出队列
        operators = []  # 运算符栈

        for token in tokens:
            if token.replace('.', '', 1).isdigit():  # 判断是否为数字（包括浮点数）
                output.append(float(token))
            elif token in precedence:
                # 当运算符栈不为空，且栈顶运算符优先级更高或相同时，弹出
                while (operators and precedence.get(operators[-1], 0) >= precedence[token]):
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
            if isinstance(token, float):  # 如果是数字，入栈
                stack.append(token)
            else:  # 如果是运算符
                if len(stack) < 2:
                    raise ValueError("无效的表达式：运算符缺少操作数")
                
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
                        raise ZeroDivisionError("错误：除数为零")
                    stack.append(operand1 / operand2)
        
        if len(stack) != 1:
            raise ValueError("无效的表达式：操作数过多")
            
        return stack[0]

    # --- 主逻辑 ---
    # 使用正则表达式将表达式分割为数字和运算符
    # 这个正则表达式可以处理整数、浮点数和运算符
    tokens = re.findall(r'(\d+\.?\d*|[\+\-\*\/])', expression.replace(" ", ""))
    if not tokens:
        raise ValueError("表达式为空或无效")

    postfix_expr = infix_to_postfix(tokens)
    result = evaluate_postfix(postfix_expr)
    return result


# --- 示例 ---
print("--- 使用安全方法计算 ---")
expr1 = "3 + 5 * 2"
print(f"'{expr1}' 的计算结果是: {calculate(expr1)}")  # 预期: 13.0

expr2 = "10 + 2 * 6 - 4 / 2"
print(f"'{expr2}' 的计算结果是: {calculate(expr2)}")  # 预期: 20.0

expr3 = "2.5 * 4 + 10.5"
print(f"'{expr3}' 的计算结果是: {calculate(expr3)}")  # 预期: 20.5
