import sys, getopt
import unittest

#convert CNFexpr to set of sets, in each set, either literal or disjunction
def convertSets(CNFexpr,CNFsets):
    if isinstance(CNFexpr, str):
        CNFsets.append([CNFexpr])
    elif isinstance(CNFexpr, list) and CNFexpr[0] == 'not':
        CNFsets.append(CNFexpr)
    elif isinstance(CNFexpr, list) and CNFexpr[0] == 'or':
        CNFsets.append([])
        for i in range(1,len(CNFexpr)):
            CNFsets[-1].append(CNFexpr[i])
    elif isinstance(CNFexpr, list) and CNFexpr[0] == 'and':
        for i in range(1,len(CNFexpr)):
             convertSets(CNFexpr[i],CNFsets)
    return

def getSymbols(CNFsets):
    symbols = []
    for item in CNFsets:
        if len(item) == 1:
            symbols.append(item[0])
        elif len(item) == 2 and item[0] == 'not':
            symbols.append(item[1])
        else:
            for subitem in item:
                if isinstance(subitem, str):
                    symbols.append(subitem)
                else:
                    symbols.append(subitem[1])
    symbols = list(set(symbols))
    return symbols

def modelPropagate(pair,clauses):
    nClauses = []
    for clause in clauses:
        if len(clause) == 1:
            if isinstance(clause[0], str):
                if clause[0] != pair[0]:
                    nClauses.append(clause)
                elif clause[0] == pair[0] and pair[1] == False:
                    nClauses.append([])
            else:
                if clause[0][1]!= pair[0]:
                    nClauses.append(clause)
                elif clause[0][1]==pair[0] and pair[1] == True:
                    nClauses.append([])
        elif len(clause) == 2 and clause[0] == 'not':
            if clause[1] != pair[0]:
                nClauses.append(clause)
            elif clause[1] == pair[0] and pair[1] == True:
                nClauses.append([])
        else:
            nClause = []
            satisfy = False
            for subclause in clause:
                if isinstance(subclause, str):
                    if subclause !=pair[0]:
                        nClause.append(subclause)
                    elif subclause == pair[0] and pair[1] == True:
                        satisfy = True
                        break
                else:
                    if subclause[1] != pair[0]:
                        nClause.append(subclause)
                    elif subclause[1] == pair[0] and pair[1] == False:
                        satisfy = True
                        break
            if not satisfy:
                nClauses.append(nClause)
    return nClauses

def findUnitClause(symbols,clauses,model):
    pair = []
    for clause in clauses:
        if len(clause) == 1:
            if isinstance(clause[0], str):
                pair.append(clause[0])
                pair.append(True)
                break
            else:
                pair.append(clause[0][1])
                pair.append(False)
                break
        elif len(clause) == 2 and clause[0] == "not":
            pair.append(clause[1])
            pair.append(False)
            break
    #unit propagation
    if len(pair)!= 0:
        symbols.remove(pair[0])
        model[pair[0]] = pair[1]
    return pair

def findPureSymbols(symbols,clauses,model):
    symbolTable = {}
    for clause in clauses:
        if len(clause)==1:
            if isinstance(clause[0], str):
                if clause[0] in symbolTable:
                    if symbolTable[clause[0]] == 0:
                        symbolTable[clause[0]] = 2
                else:
                    symbolTable[clause[0]] = 1
            else:
                if clause[0][1] in symbolTable:
                    if symbolTable[clause[0][1]] == 1:
                        symbolTable[clause[0][1]] = 2
                else:
                    symbolTable[clause[0][1]] = 0
        elif len(clause) == 2 and clause[0] == 'not':
            if clause[1] in symbolTable:
                if symbolTable[clause[1]] == 1:
                    symbolTable[clause[1]] = 2
            else:
                symbolTable[clause[1]] = 0
        else:
            for subclause in clause:
                if isinstance(subclause, str):
                    if subclause in symbolTable:
                        if symbolTable[subclause] == 0:
                            symbolTable[subclause] = 2
                    else:
                        symbolTable[subclause] = 1
                else:
                    if subclause[1] in symbolTable:
                        if symbolTable[subclause[1]] == 1:
                            symbolTable[subclause[1]] = 2
                    else:
                        symbolTable[subclause[1]] = 0
    pair = []
    for key in symbolTable:
        if symbolTable[key] != 2:
            if symbolTable[key] == 0:
                pair.append(key)
                pair.append(False)
                break
            else:
                pair.append(key)
                pair.append(True)
                break
    #pure symbol propagation
    if len(pair)!=0:
        symbols.remove(pair[0])
        model[pair[0]] = pair[1]
    return pair
    
def DPLL(clauses,symbols,model):
    #empty sentence, sentence is satisfiable
    if len(clauses) == 0:
        for sym in symbols:
            model[sym] = True
        return [True,model]
    for item in clauses:
        #empty clause, sentence is unsatisfiable
        if len(item) == 0:
            return [False,model]
    pair = findPureSymbols(symbols, clauses, model)
    if len(pair)!=0:
        clauses = modelPropagate(pair, clauses)
        return DPLL(clauses,symbols,model)
    pair = findUnitClause(symbols, clauses, model)
    if len(pair)!=0:
        clauses = modelPropagate(pair, clauses)
        return DPLL(clauses,symbols,model)
    pair = []
    pair.append(symbols[0])
    pair.append(True)
    clausesT = modelPropagate(pair, clauses)
    pair[1] = False
    clausesF = modelPropagate(pair, clauses)
    symbolsT = list(symbols)
    modelT = model.copy()
    symbolsT.remove(pair[0])
    modelT[pair[0]] = True
    result = DPLL(clausesT,symbolsT,modelT)
    if result[0] == True:
        return result
    symbolsF = list(symbols)
    symbolsF.remove(pair[0])
    modelF = model.copy()
    modelF[pair[0]] = False
    return DPLL(clausesF, symbolsF, modelF)

#def DPLL(CNFsets,symbols,assignedValue):
def solveSAT(CNFexpr):
    CNFsets = []
    convertSets(CNFexpr, CNFsets)
    symbols = getSymbols(CNFsets)
    model = {}
    [satisfieable,model] = DPLL(CNFsets, symbols, model)
#     print model
    return [satisfieable,model]

def main(argv):
    inputFile = ""
    outputFile = "CNF_satisfiability.txt"
    try:
        opts,args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print "python CNFsolve.py -i <inputfile>"
        sys.exit(2)
    for opt,arg in opts:
        if opt == "-i":
            inputFile = arg

    fin = open(inputFile,"r")
    fout = open(outputFile,"w")
    count = int(fin.readline())
#     fout.write(str(count)+"\n")
    for i in range(0,count):
        expr = fin.readline()
        exprList = eval(expr)
        [sat,model] =  solveSAT(exprList)
        if not sat:
            fout.write('['+"\"false\""+']'+"\n")
        else:
            fout.write('[')
            answer = []
            answer.append("\"true\"")
            for key in model:
                if model[key] == True:
                    answer.append("\""+str(key)+"="+"true\"")
                else:
                    answer.append("\""+str(key)+"="+"false\"")
            astr = ",".join(answer)
            fout.write(astr)
            fout.write(']'+"\n")
    fin.close()
    fout.close()

def test():
    print solveSAT(['and', ['or', 'A', 'B'], ['or', ['not', 'A'], 'C'], ['or', ['not', 'B'], 'C'], ['or', ['not', 'C'], 'B']])
    print solveSAT(["and",["or","P","Q"],["or",["not","P"],"R"],["or",["not","P"],["not","R"]],["or",["not","Q"],"S",["not","T"]],"T"])
    print solveSAT(["and",["or",["not","P"],"Q"],["or",["not","P"],["not","Q"]],["or","P",["not","Q"]]])
if __name__ == "__main__":
#     main(sys.argv[1:])
    test()