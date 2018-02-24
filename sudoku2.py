import sys
import time
import itertools
import functools
import copy

def print_mt(tp_mt):
    for line in tp_mt:
        print(line)
    print()

def read_mt():
    tr_mt = []
    with open('puzzle', 'r') as f1:
        for line in f1:
            newline = [int(x) for x in line.split()]
            tr_mt.append(newline)
    return tr_mt

def write_mt(tp_mt):
    with open('solution', 'w') as f1:
        for i in tp_mt:
            for j in i:
                f1.write('%s\t' % j)
            f1.write('\n')

def ori_to_line(original_mt):
    line_mt = []
    for i in range(9):
        newline = []
        for j in range(3):
            for k in range(3):
                newline.append(original_mt[i//3*3+j][i%3*3+k])
        line_mt.append(newline)
    return line_mt

def line_to_column(line_mt):
    column_mt = []
    for i in range(9):
        newcolumn = []
        for j in range(9):
            newcolumn.append(line_mt[j][i])
        column_mt.append(newcolumn)
    return column_mt

def column_to_ori(column_mt):
    original_mt = []
    for i in range(9):
        newsquare = []
        for j in range(3):
            for k in range(3):
                newsquare.append(column_mt[i%3*3+k][i//3*3+j])
        original_mt.append(newsquare)
    return original_mt

def mut_ex(to_handle_mt):
    for line in to_handle_mt:
        while True:
            flag1 = 1
            ex_set=set([x for x in line if type(x)==int and x])
            for ele in line:
                if ele:
                    if type(ele) != int:
                        if ele & ex_set:
                            idx = line.index(ele)
                            ele = ele - ex_set
                            line[idx] = ele
                            flag1 = 0
                else:
                    line[line.index(ele)] = set(range(1,10)) - ex_set
                    flag1 = 0
                if type(ele)==set and len(ele) == 1:
                    try:
                        line[idx] = list(ele)[0]
                    except UnboundLocalError:
                        line[line.index(ele)] = list(ele)[0]
                    ex_set = ex_set | ele
                    flag1 = 0
            if flag1:break

def validation(to_check_mt):
    for line in to_check_mt:
        num_iter = filter(lambda x:type(x) is int, line)
        num_list = list(num_iter)
        if len(num_list) != len(set(num_list)):
            return False
    else:
        return True

def is_solved(to_judge_mt):
    for line in to_judge_mt:
        for ele in line:
            if type(ele) != int:
                return False
    else:
        return True

def mt_iter(line_mt):
    while True:
        contrast_mt = copy.deepcopy(line_mt)
        mut_ex(line_mt)
        column_mt = line_to_column(line_mt)
        mut_ex(column_mt)
        original_mt = column_to_ori(column_mt)
        mut_ex(original_mt)
        line_mt = ori_to_line(original_mt)
        mut_ex(line_mt)
        if is_solved(line_mt):
            return (line_mt, 0)
        if contrast_mt == line_mt:
            return (contrast_mt, 1)

def choose_one(line_mt):
    for i in range(9):
        for j in range(9):
            if type(line_mt[i][j]) == set:
                for v in line_mt[i][j]:
                    exp_line_mt = copy.deepcopy(line_mt)
                    exp_line_mt[i][j] = v
                    result_tup = mt_iter(exp_line_mt)
                    if (validation(result_tup[0])and
                        validation(line_to_column(result_tup[0])) and
                        validation(column_to_ori(line_to_column(result_tup[0])))):
                        if not result_tup[1]:
                            return result_tup[0]
                        else:
                            mbcor_mt = choose_one(result_tup[0])
                            if is_solved(mbcor_mt):
                                return mbcor_mt
                else:
                    return line_mt


line_mt = read_mt()
result_tuple = mt_iter(line_mt)
if result_tuple[1]:
    line_mt = choose_one(result_tuple[0])
else:
    line_mt = result_tuple[0]

print_mt(line_mt)
write_mt(line_mt)
