OPERATORS = ['NOT', 'AND', 'OR']
OPERATOR_PRECEDENCE = {
    ')': 4,
    '(': 4,
    'NOT': 3,
    'AND': 2,
    'OR': 1,
}

def is_operator(token):
    return token in OPERATORS


def is_brace(token):
    return token in ['(', ')']


def is_operand(token):
    return not (is_operator(token) or is_brace(token))


def compare_operators(op1, op2):
    if OPERATOR_PRECEDENCE[op1] == OPERATOR_PRECEDENCE[op2]:
        return 0
    elif OPERATOR_PRECEDENCE[op1] > OPERATOR_PRECEDENCE[op2]:
        return 1
    else:
        return -1


def infix_to_prefix(query):
    # https://www.youtube.com/watch?v=fUxnb5eTRS0
    query = query.replace('(', ' ( ')
    query = query.replace(')', ' ) ')
    tokens = [token for token in query.split(' ') if token]
    tokens.reverse()

    output = []
    stack = []
    for token in tokens:
        if is_operand(token):
            output.append(token)
        elif token == ')':
            stack.append(token)
        elif is_operator(token):
            while (len(stack) and not is_brace(stack[-1])):
                if compare_operators(token, stack[-1]) <= 0:
                    output.append(stack[-1])
                    stack = stack[:-1]
                else:
                    break
            stack.append(token)
        elif token == '(':
            while (len(stack) and stack[-1] != ')'):
                output.append(stack[-1])
                stack = stack[:-1]
            stack = stack[:-1]

    while (len(stack)):
        output.append(stack[-1])
        stack = stack[:-1]

    output.reverse()
    return output


def process_infix_query(infix_list):
    stack = []

    if len(infix_list) == 1:
        return Query(tuple(infix_list))

    while (len(infix_list) != 1 or len(stack)):
        token = infix_list[-1]
        infix_list = infix_list[:-1]

        if is_operand(token):
            stack.append(token)
        else:
            if token == 'NOT':
                q = Query((token, stack[-1]))
                stack = stack[:-1]
            else:
                # token is AND or OR
                q = Query((token, stack[-1], stack[-2]))
                stack = stack[:-2]

            infix_list.append(q)

    return infix_list[0]


class Query(object):
    """Wraper object for queries."""
    def __init__(self, query_tuple):
        # Sort operands to make caching easier.
        if len(query_tuple) == 3:
            operator = query_tuple[0]
            o1 = query_tuple[1]
            o2 = query_tuple[2]
            if o1 > o2:
                query_tuple = (operator, o2, o1)
            else:
                query_tuple = (operator, o1, o2)

        self.query_tuple = query_tuple

    def __repr__(self):
        return 'Query(%s)' % str(self.query_tuple)
