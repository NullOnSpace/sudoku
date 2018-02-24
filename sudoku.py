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
            while True:
                flag2 = 1
                for ele in line:
                    if type(ele) is set:
                        notme_set = set()
                        for other_set in filter(lambda x:type(x) is set, line):
                            if other_set is not ele:
                                notme_set = notme_set | other_set
                        if len(ele - notme_set) == 1:
                            line[line.index(ele)] = list(ele - notme_set)[0]
                            flag2 = 0
                            break
                if flag2:break
            if flag1 and flag2:break

def iso_check(to_check_mt):
    for line in to_check_mt:
        all_set = list(filter(lambda x: type(x) is set, line))
        if len(all_set) > 2:
            for i in range(2,len(all_set)):
                for sublist in itertools.combinations(all_set, i):
                    set_sublist = functools.reduce((lambda x,y: set(x)|set(y)),
                                                   sublist)
                    if len(set_sublist) == i:
                        for ele in line:
                            if type(ele) is set and not ele <= set_sublist:
                                print('%s counter %s ' %
                                      (str(ele),str(set_sublist)))
                                if ele & set_sublist:
                                    line[line.index(ele)] = ele - set_sublist

def validation(to_check_mt):
    for line in to_check_mt:
        try:
            assert functools.reduce((lambda x,y: x+y), line) == 45
        except (TypeError, AssertionError):
            return False
    else:
        return True

def is_solved(to_judge_mt):
    for line in to_judge_mt:
        for ele in line:
            if type(ele) == set:
                return False
    else:
        return True

def mt_iter(line_mt):
    while True:
        mut_ex(line_mt)
        contrast_mt = copy.deepcopy(line_mt)
        column_mt = line_to_column(line_mt)
        mut_ex(column_mt)
        original_mt = column_to_ori(column_mt)
        mut_ex(original_mt)
        line_mt = ori_to_line(original_mt)
        mut_ex(line_mt)
        print_mt(line_mt)
        if contrast_mt == line_mt:
            print('iso check')
            iso_check(line_mt)
            column_mt = line_to_column(line_mt)
            iso_check(column_mt)
            original_mt = column_to_ori(column_mt)
            iso_check(original_mt)
            line_mt = ori_to_line(original_mt)
            if contrast_mt == line_mt:
                return (line_mt, 1)
        #time.sleep(1)
        if is_solved(line_mt):
            return (line_mt, 0)

def choose_one(line_mt):
    print('choose one')
    for i in range(9):
        for j in range(9):
            if type(line_mt[i][j]) == set:
                for v in line_mt[i][j]:
                    exp_line_mt = copy.deepcopy(line_mt)
                    exp_line_mt[i][j] = v
                    result_tup = mt_iter(exp_line_mt)
                    if result_tup[1]:
                        choose_one(result_tup[0])
                    elif (validation(result_tup[0])and
                          validation(line_to_column(result_tup[0])) and
                          validation(column_to_ori(line_to_column(result_tup[0])))):
                        return result_tup[0]
                    else:
                        continue


line_mt = read_mt()
while True:
    result_tuple = mt_iter(line_mt)
    if result_tuple[1]:
        line_mt = choose_one(line_mt)
        if validation(line_mt):
            break
    else:
        line_mt = result_tuple[0]
        break

write_mt(line_mt)
