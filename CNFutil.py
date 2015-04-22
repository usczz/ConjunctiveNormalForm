def mySort(expr):
    if isinstance(expr, str):
        return expr
    result = list(expr)
    for i in range(len(result)):
        if isinstance(result[i], list):
            result[i] = sorted(result[i])
    result = sorted(result)
    for i in range(len(result)):
        if isinstance(result[i], list):
            result[i].reverse()
    result.reverse()   
    return result

def mylen(expr):
    if isinstance(expr, str):
        return 1
    elif isinstance(expr, list) and expr[0] == 'not':
        return 1
    else:
        return len(expr)
    
def myCmp(x,y):
    if mylen(x) != mylen(y):
        return mylen(x) - mylen(y)
    else:
        return x > y

def sortByLen(expr):
    return sorted(expr,cmp=myCmp) 

def getCompliment(expr):
    if isinstance(expr, str):
        return ["not",expr]
    else:
        return expr[1]
    
def subClause(expr1,expr2):
    if isinstance(expr1, str) and isinstance(expr2, str):
        if expr1 == expr2:
            return True
        else:
            return False
    elif isinstance(expr1, str) and isinstance(expr2, list):
        if expr2[0] == "not" and expr1 == expr2[1]:
            return False
        if expr1 in expr2:
            return True
        else:
            return False
    elif isinstance(expr1, list) and isinstance(expr2, str):
        if expr1[0] == "not" and expr1[1] == expr2:
            return False
        if expr2 in expr1:
            return True
        else:
            return False
    else:
        sub = True
        minexpr =[]
        larexpr =[]
        if len(expr1) <= len(expr2):
            minexpr = expr1
            larexpr = expr2
        else:
            minexpr = expr2
            larexpr = expr1
        for item in minexpr:
            if item in larexpr:
                continue
            else:
                sub = False
                break
        return sub

def equal(expr1, expr2):
    if type(expr1) != type(expr2):
        return False
    if isinstance(expr1, str):
        if expr1 == expr2:
            return True
        else:
            return False
    if len(expr1) != len(expr2):
        return False
    sortedExpr1 = mySort(expr1)
    sortedExpr2 = mySort(expr2)
    for i in range(len(sortedExpr1)):
        if equal(sortedExpr1[i], sortedExpr2[i]):
            continue
        else:
            return False
    return True
    
def test():
    print sortByLen(['and', ['or', 'P', ['not', 'Q']], ['or', ['not', 'R'], ['not', 'Q'], 'P'], ['or', 'P', ['not', 'R']], ['or', 'P', ['not', 'Q'], 'R']])
    
if __name__ == "__main__":
    test()
                   