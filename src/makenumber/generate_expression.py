import random
import ast
import itertools

def _remove_unnecessary_parentheses(expression):
    try:
        tree = ast.parse(expression)
        return ast.unparse(tree).strip()
    except SyntaxError:
        return expression

def _generate_expr_and_num():
    nums = random.sample(range(1, 70), 4) + [random.randint(70, 80), random.randint(80, 120)]
    nums_backup = nums.copy()
    nums_backup.sort()
    ops = ['+', '-', '*', '/']
    init_paren = True if random.random() < 0.2 else False
    firstnum = random.choice(nums)
    nums.remove(firstnum)
    numops = 5
    expr = ('(' if init_paren else '') + str(firstnum)
    lastnum = firstnum
    prev_div = False
    in_paren = init_paren
    for _ in range(numops):
        op = random.choice(ops)
        expr += op
        paren = True if random.random() < 0.4 and not in_paren and not op in {'+', '-'} else False
        nextnum = random.choice([x for x in nums])
        nums.remove(nextnum)
        expr += ('(' if paren else '') + str(nextnum)
        if paren:
            in_paren = True
        closeparen = True if random.random() < 0.6 and in_paren and not paren else False
        expr += (')' if closeparen else '')
        if closeparen:
            in_paren = False
        lastnum = nextnum
    if in_paren:
        expr += ')'
    try:
        return _remove_unnecessary_parentheses(expr), eval(expr), nums_backup
    except ZeroDivisionError:
        return "", 1000000, []

def generate_expression():
    res = _generate_expr_and_num()
    while (
        abs(res[1]) > 300
        or abs(res[1] - int(res[1])) > 1e-13
        or ('*' not in res[0] and '/' not in res[0])
        or ('(' not in res[0])
        or ('* 1') in res[0]
        or ('1 *') in res[0]
        or res[1] in res[2]
        or any(
            abs(res[1] / r - int(res[1] / r)) < 1e-13 and r > res[1] / 4
            for r in res[2]
        )
        or res[1] in itertools.chain.from_iterable(
            [i + j, i - j, i * j, i / j]
            if ind != indd
            else []
            for indd, i in enumerate(res[2])
            for ind, j in enumerate(res[2])
        )
        or any(
            k not in (i, j) and (
                abs(op1 + res[2][k] - res[1]) < 1e-13
                or abs(op1 - res[2][k] - res[1]) < 1e-13
                or abs(res[2][k] - op1 - res[1]) < 1e-13
                or abs(op1 * res[2][k] - res[1]) < 1e-13
                or (res[2][k] != 0 and abs(op1 / res[2][k] - res[1]) < 1e-13)
                or (op1 != 0 and abs(res[2][k] / op1 - res[1]) < 1e-13)
            )
            for i, a in enumerate(res[2])
            for j, b in enumerate(res[2]) if i != j
            for op1 in [a + b, a - b, b - a, a * b]
            for k, c in enumerate(res[2])
        )
    ):
        res = _generate_expr_and_num()

    return res

if __name__ == '__main__':
    print(generate_expression())
