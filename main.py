from translate_rm import Translator

def to_string(lyst):
    result = ''
    if type(lyst[0]) is list : 
        print('you done fucked up')
    result += repr(lyst[0])
    for e in lyst[1:]:
        if type(e) is list:
            print('this is a list')
            result += to_string(e)
    return result
t = Translator()
t.parse_file('add-3.ss')
print(t.program)
to_string(t.program)
