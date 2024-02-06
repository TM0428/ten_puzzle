# 演算子のための定数
LEFT_ASSOC = 0
RIGHT_ASSOC = 1

# 対応する演算子
OPERATORS = {
    '+': (0, LEFT_ASSOC),
    '-': (0, LEFT_ASSOC),
    '*': (5, LEFT_ASSOC),
    '/': (5, LEFT_ASSOC),
    '%': (5, LEFT_ASSOC)
}

# 演算子かどうかの確認
def is_operator(token):
    return token in OPERATORS.keys()

# 結合性の確認
def is_associative(token, assoc):
    if not is_operator(token):
        raise ValueError('Invalid token: %s' % token)
    return OPERATORS[token][1] == assoc

# 二つの記号の優先順位を確認
def cmp_precedence(token1, token2):
    if not is_operator(token1) or not is_operator(token2):
        raise ValueError('Invalid tokens: %s %s' % (token1, token2))
    return OPERATORS[token1][0] - OPERATORS[token2][0]

# 中置記法を逆ポーランド記法に変換する
def infix_to_RPN(tokens):
    out = []
    stack = []
    for token in tokens:
        if is_operator(token):
            while len(stack) != 0 and is_operator(stack[-1]):
                if (is_associative(token, LEFT_ASSOC)
                        and cmp_precedence(token, stack[-1]) <= 0) or (
                        is_associative(token, RIGHT_ASSOC)
                        and cmp_precedence(token, stack[-1]) < 0):
                    out.append(stack.pop())
                    continue
                break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while len(stack) != 0 and stack[-1] != '(':
                out.append(stack.pop())
            stack.pop()
        else:
            out.append(token)
    while len(stack) != 0:
        out.append(stack.pop())
    return out

# リストの要素をタブ区切りの文字列にする
def list_to_str_with_space(lst):
    str_w_space = '\t'.join([i for i in lst])
    return str_w_space


ops = {
    "+": (lambda a, b: a + b),
    "-": (lambda a, b: a - b),
    "*": (lambda a, b: a * b),
    "/": (lambda a, b: a / b)
}

# 逆ポーランド記法の数式を計算する
def calc_RPN(expression):
    tokens_RPN = expression.split()
    stack = []

    for token in tokens_RPN:
        if token in ops:
            arg2 = stack.pop()
            arg1 = stack.pop()
            result = ops[token](arg1, arg2)
            stack.append(result)
        else:
            stack.append(int(token))
    return stack.pop()

# 入力と出力のための関数
def in_and_out(input_equation: str) -> float:
    output = infix_to_RPN(list(input_equation.replace(" ", "")))
    stri = list_to_str_with_space(output)
    # print(stri)
    result = calc_RPN(stri)
    print("[calc] result is", result)
    return result


if __name__ == '__main__':
    in_and_out("3*5-5*1")