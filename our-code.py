from translate_rm import Translator

operators = {
    '+':'Add',
    '*':'Mul',
    'expt':'Pow'
    
}

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
    t = Translator()
    t.parse(string)
    print(to_string(t.program[-1])) 

if __name__ == '__main__':
    t = Translator()
    t.parse_file('add-3.ss')
    print(t.program)
    for x in t.program:
        print(to_string(x))
