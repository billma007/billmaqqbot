
# from verify import *
import random
from itertools import permutations
ops = ["+","-","*","/"]
def get24(res_1):
    if len(res_1[0]) == 1:
        return res_1
    else:
        result = []
        for j in res_1:
            per_num = list(permutations(j,2))
            for i in per_num:
                for op in ops:
                    tmp = j[:]
                    tmp.remove(i[0])
                    tmp.remove(i[1])
                    tmp.append("(" + i[0] + op + i[1] + ")")
                    result.append(tmp)
    return get24(result)
def verify(number):
    for i in number:
        try:
            if eval(i[0]) == 24.0:
                return True
        except:
            pass
    return False
# res_1 = get24(number)
# print(verify(res_1))
def generate():
	num = []
	num_2 = []
	num_list = [1,2,3,4,5,6,7,8,9]
	for i in range(4):
		ranint = random.choice(num_list)
		num.append(str(ranint))
		num_list.remove(int(ranint))
	num_2.append([str(i) for i in num])
	res = get24(num_2)
	if verify(res) == True:
		return num
	else:
		generate()
	return num

def returnnum(strlistt) -> list:
    try :
        kkkk=''.join(filter(str.isdigit, str(strlistt))).replace(" ","").replace("+","").replace(" ","")
        if len(kkkk)!=4:return [-1]
        kkk=list(set(kkkk))
        kkkkk=list(generate())
        kk="".join(kkkkk)
        num=0
        for i in kkk:
            if i in kk:num=num+1
        return [num]+kkkkk

    except:return [-2]

if __name__=="__main__":
    print(returnnum(".bot signin guess 2 3 3 3"))