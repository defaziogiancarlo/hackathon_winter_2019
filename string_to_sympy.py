operators = {
    '+':'Add',
    '*':'Mul',
    'expt':'Pow'
    
}

def lexer(text):
    """
    Lexer for Scheme code. Takes a string of Scheme code and breaks it
    up into a flat list of the important parts.

    > lexer("(define x (lambda (x) (cond ((test? x) (func x)) (else return))))"))
    ['(', 'define', 'x', '(', 'lambda', '(', 'x', ')', '(', 'cond', '(', '(', 'test?',
     'x', ')', '(', 'func', 'x', ')', ')', '(', 'else', 'return', ')', ')', ')', ')']
    """
    state = None
    current = ""
    retval = []
    i = 0
    while i < len(text):
        c = text[i]
        if state == "in-comment":
            if c == "\n":
                state = None
            # else, ignore
        elif state == "in-string":
            if c == '\\':
                current += c
                i += 1
                c = text[i]
                current += c
            elif c == '"':
                state = None
                current += c
                retval.append(current)
                current = ""
            else:
                current += c
        else:
            if c in ["(", ")", "'"]:
                if current:
                    retval.append(current)
                    current = ""
                retval.append(c)
            elif c == "#":
                if current:
                    retval.append(current)
                    current = ""
                i += 1
                if text[i] != "\\":
                    current = "#" + text[i]
                else:
                    i += 1
                    current = "#\\" + text[i]
                    i += 1
                    while (not text[i] in [' ', ')']) and i < len(text):
                        current += text[i]
                        i += 1
                    i -= 1
            elif c == ";":
                if current:
                    retval.append(current)
                    current = ""
                state = "in-comment"
            elif c == '"':
                if current:
                    retval.append(current)
                    current = ""
                current = '"'
                state = "in-string"
            elif c in [" ", "\n"]:
                if current:
                    retval.append(current)
                    current = ""
            else:
                current += c
        i += 1
    if current:
        retval.append(current)
    return retval

def parser(lexed):
    """
    Take a lexed list and parse it into a tree of s-expressions represented
    as lists. Side-effect: collects and replaces symbols.

    > parser(lexer("(define x (lambda (x) (cond ((test? x) (func x)) (else return))))"))
    [['define', 'x', ['lambda', ['x'], ['cond', [['test?', 'x'],
                                                 ['func', 'x']], ['else', 'return']]]]]
    """
    retval = []
    stack = []
    current = None
    i = 0
    while i < len(lexed):
        item = lexed[i]
        if item == "(": ## (define x 1)   ((test? 1) 1)
            if current is not None:
                stack.append(current)
            current = []
        elif item == ")":
            if len(stack) > 0:
                temp = stack.pop()
                if current is not None:
                    temp.append(current)
                current = temp
            else:
                if current is not None:
                    retval.append(current)
                current = None
        elif item == "'": ## quoted
            if i + 1 < len(lexed):
                if lexed[i + 1] != "(":
                    i += 1
                    current.append(self.make_symbol_name(lexed[i]))
                else:
                    i += 2
                    current.append("symbol_emptylist")
            else: # same as any item
                current.append(item)
        else:
            current.append(item)
        i += 1
    if current:
        retval.append(current)
    if stack:
        raise Exception("stack:", stack)
    return retval
def get_func(name):
    if name in operators:
        return operators[name]
    return name

def is_int(symbol):
    if symbol != '':
        return symbol.isdigit() or symbol[0] == '-' and symbol[1:].isdigit()
    else :
        return False
def is_float(symbol):
    try :
        float(symbol)
        return True
    except ValueError :
        return False

def to_string(lyst):
    result = ''
    if not lyst:
        print('Error: Empty list')
        return ''
    if type(lyst[0]) is list : 
        print('Error: first element is list')
        return ''
    if type(lyst) is list :
        result += get_func(lyst[0]) + '(' + ','.join(list(map(to_string,lyst[1:]))) + ')'
    elif is_int(lyst) :
        result += 'Integer(' + lyst + ')'
    elif is_float(lyst) :
        result += 'Float(' + lyst + ')'
    else:
        result += 'Symbol(\'' + lyst + '\')'
    return result

def string_to_sympy(string):
    program_list = parser(lexer(string))
    return to_string(program_list[-1])

if __name__ == '__main__':
    print(string_to_sympy('(+ 1 a (* 2 4 5))'))
    
