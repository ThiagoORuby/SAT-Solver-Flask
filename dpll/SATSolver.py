import sys
from copy import deepcopy

assign_true = set()
assign_false = set()
n_props, n_splits = 0, 0

print_list = []
column_list = []
values_list = []
#→¬∧∨

def print_cnf(cnf):
    s = ''
    for i in range(len(cnf)):
        if len(cnf[i]) > 0:
            s += '(' + cnf[i].replace(' ', '+') + ')'
        if(i < len(cnf)-1): s+='∧'
    if s == '':
        s = '()'
    s = s.replace('+', '∨')
    s = s.replace('!', '¬')
    return s


def solve(cnf, literals):
    global print_list
    #print_list.append('\nCNF = ', end='')
    print_list.append(("CNF = " + print_cnf(cnf), 'darkgreen'))
    new_true = []
    new_false = []
    global assign_true, assign_false, n_props, n_splits
    assign_true = set(assign_true)
    assign_false = set(assign_false)
    n_splits += 1
    cnf = list(set(cnf))
    units = [i for i in cnf if len(i)<3]
    units = list(set(units))
    if len(units):
        for unit in units:
            n_props += 1
            if '!' in unit:
                assign_false.add(unit[-1])
                new_false.append(unit[-1])
                i = 0
                while True:
                    if unit in cnf[i]:
                        cnf.remove(cnf[i])
                        i -= 1
                    elif unit[-1] in cnf[i]:
                        cnf[i] = cnf[i].replace(unit[-1], '').strip()
                    i += 1
                    if i >= len(cnf):
                        break
            else:
                assign_true.add(unit)
                new_true.append(unit)
                i = 0
                while True:
                    if '!'+unit in cnf[i]:
                        cnf[i] = cnf[i].replace('!'+unit, '').strip()
                        if '  ' in cnf[i]:
                            cnf[i] = cnf[i].replace('  ', ' ')
                    elif unit in cnf[i]:
                        cnf.remove(cnf[i])
                        i -= 1
                    i += 1
                    if i >= len(cnf):
                        break
    unit_print = 'Units = ' + ', '.join(units)
    unit_print = unit_print.replace('!', '¬')
    print_list.append((unit_print, 'darkblue'))
    #print_list.append('CNF after unit propogation = ', end = '')
    print_list.append(('New CNF = ' + print_cnf(cnf), 'darkorange'))
    print_list.append(("hr", "black"))

    if len(cnf) == 0:
        return True

    if sum(len(clause)==0 for clause in cnf):
        for i in new_true:
            assign_true.remove(i)
        for i in new_false:
            assign_false.remove(i)
        print_list.append(('Null clause found, backtracking...', 'darkred'))
        print_list.append(("hr", "black"))
        return False
    literals = [k for k in list(set(''.join(cnf))) if k.isalpha()]

    x = literals[0]
    if solve(deepcopy(cnf)+[x], deepcopy(literals)):
        return True
    elif solve(deepcopy(cnf)+['!'+x], deepcopy(literals)):
        return True
    else:
        for i in new_true:
            assign_true.remove(i)
        for i in new_false:
            assign_false.remove(i)
        return False


def dpll(info):
    global assign_true, assign_false, n_props, n_splits, print_list, column_list, values_list
    input_cnf = info
    literals = [i for i in list(set(input_cnf)) if i.isalpha()]
    cnf = input_cnf.splitlines()
    print_list = []
    column_list = []
    values_list = []
    result = ''
    n_splits = 0
    n_props = 0
    assign_true = set()
    assign_false = set()
    if solve(cnf, literals):
        print("rolou")
        #print_list.append('Number of Splits = ' + str(n_splits))
        #print_list.append('Unit Propogations = ' + str(n_props))
        #print_list.append('Result: SATISFIABLE')
        result = 'SATISFIABLE'
        #print_list.append('Solution:')
        for i in assign_true:
            column_list.append(i)
            values_list.append(1)
        for i in assign_false:
            column_list.append(i)
            values_list.append(0)
    else:
        """print_list.append('Reached starting node!')
        print_list.append('Number of Splits = ' + str(n_splits))
        print_list.append('Unit Propogations = ' + str(n_props))
        print_list.append('Result: UNSATISFIABLE')"""
        result = 'UNSATISFIABLE'
        print("nao foi")
    #print_list.append()
    return result, print_list, column_list, values_list

#if __name__=='__main__':
#    dpll()
