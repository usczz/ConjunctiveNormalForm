#!/usr/bin/python
import sys,getopt
import CNFutil
import unittest

def distribute(propExpr):
    CNFExpr = []
    if len(propExpr) == 3:
        if isinstance(propExpr[1], str) and isinstance(propExpr[2], str):
            if propExpr[1] == propExpr[2]:
                return propExpr[1]
            else:
                CNFExpr = ["or"]
                CNFExpr.append(propExpr[1])
                CNFExpr.append(propExpr[2])
        elif isinstance(propExpr[1], str) and (isinstance(propExpr[2], list) and propExpr[2][0] == "not"):
            CNFExpr.append("or")
            CNFExpr.append(propExpr[1])
            CNFExpr.append(propExpr[2])
        elif (isinstance(propExpr[1], str) or (isinstance(propExpr[1], list) and propExpr[1][0] == "not")) and (isinstance(propExpr[2], list) and propExpr[2][0] == "and"):
            CNFExpr.append("and")
            for i in range(1,len(propExpr[2])):
                nExpr = ["or"]
                nExpr.append(propExpr[1])
                nExpr.append(propExpr[2][i])
                clause = distribute(nExpr)
                exist = False
                for item in CNFExpr:
                    if CNFutil.equal(item, clause):
                        exist = True
                        break
                if not exist:
                    CNFExpr.append(clause)
            if len(CNFExpr) == 2:
                CNFExpr = CNFExpr[1]
        elif (isinstance(propExpr[1], str) or (isinstance(propExpr[1], list) and propExpr[1][0] == "not")) and (isinstance(propExpr[2], list) and propExpr[2][0] == "or"):
            CNFExpr.append("or")
            CNFExpr.append(propExpr[1])
            for i in range(1,len(propExpr[2])):
                exist = False
                for item in CNFExpr:
                    if CNFutil.equal(propExpr[2][i], item):
                        exist = True
                        break
                if not exist:
                    CNFExpr.append(propExpr[2][i])
            if len(CNFExpr) == 2:
                CNFExpr = CNFExpr[1]
        elif (isinstance(propExpr[1], list) and propExpr[1][0] == "not") and isinstance(propExpr[2], str):
            nExpr = ["or"]
            nExpr.append(propExpr[2])
            nExpr.append(propExpr[1])
            CNFExpr = distribute(nExpr)
        elif (isinstance(propExpr[1], list) and propExpr[1][0] == "not") and (isinstance(propExpr[2], list) and propExpr[2][0] == "not"):
            if propExpr[1][1] == propExpr[2][1]:
                return propExpr[1]
            else:
                CNFExpr.append("or")
                CNFExpr.append(propExpr[1])
                CNFExpr.append(propExpr[2])
        elif (isinstance(propExpr[1], list) and propExpr[1][0] == "and") and (isinstance(propExpr[2], str) or (isinstance(propExpr[2], list) and propExpr[2][0] == "not")):
            nExpr = ["or"]
            nExpr.append(propExpr[2])
            nExpr.append(propExpr[1])
            CNFExpr = distribute(nExpr)
        elif (isinstance(propExpr[1], list) and propExpr[1][0] == "and") and (isinstance(propExpr[2], list) and propExpr[2][0] == "and"):
            CNFExpr.append("and")
            for i in range(1,len(propExpr[1])):
                for j in range(1,len(propExpr[2])):
                    nExpr = ["or"]
                    nExpr.append(propExpr[1][i])
                    nExpr.append(propExpr[2][j])
                    clause = distribute(nExpr)
                    exist = False
                    for item in CNFExpr:
                        if CNFutil.equal(item, clause):
                            exist = True
                            break
                    if not exist:
                        CNFExpr.append(clause)
            if len(CNFExpr) == 2:
                CNFExpr = CNFExpr[1]
        elif (isinstance(propExpr[1], list) and propExpr[1][0] == "and") and (isinstance(propExpr[2], list) and propExpr[2][0] == "or"):
            CNFExpr.append("and")
            for i in range(1,len(propExpr[1])):
                nExpr = ["or"]
                nExpr.append(propExpr[1][i])
                nExpr.append(propExpr[2])
                clause = distribute(nExpr)
                exist = False
                for item in CNFExpr:
                    if CNFutil.equal(item,clause):
                        exist = True
                        break
                if not exist:
                    CNFExpr.append(clause)
            if len(CNFExpr) == 2:
                CNFExpr = CNFExpr[1]
        elif (isinstance(propExpr[1], list) and propExpr[1][0] == "or") and (isinstance(propExpr[2], list) and propExpr[2][0] == "or"):
            CNFExpr.append("or")
            for i in range(1,len(propExpr[1])):
                child = propExpr[1][i]
                exist = False
                for item in CNFExpr:
                    if CNFutil.equal(item, child):
                        exist = True
                        break
                if not exist:
                    CNFExpr.append(child)
            for i in range(1,len(propExpr[2])):
                child = propExpr[2][i]
                exist = False
                for item in CNFExpr:
                    if CNFutil.equal(item, child):
                        exist = True
                        break
                if not exist:
                    CNFExpr.append(child)
            if len(CNFExpr) == 2:
                CNFExpr = CNFExpr[1]        
        else:
            nExpr = ["or"]
            nExpr.append(propExpr[2])
            nExpr.append(propExpr[1])
            CNFExpr = distribute(nExpr)
    else:
        nExpr = ["or"]
        for i in range(2,len(propExpr)):
            nExpr.append(list(propExpr[i]))
        clause = distribute(nExpr)
        CNFExpr = ["or"]
        CNFExpr.append(propExpr[1])
        CNFExpr.append(clause)
        CNFExpr = distribute(CNFExpr) 
    return CNFExpr

def propToCNF(propExpr):
    CNFExpr = []
    if isinstance(propExpr,str):
        return propExpr
    elif isinstance(propExpr,list):
        if propExpr[0] == "not":
            if isinstance(propExpr[1], str):
                return propExpr
            elif isinstance(propExpr[1], list) and propExpr[1][0] == "not":
                CNFExpr = propToCNF(propExpr[1][1])
            elif isinstance(propExpr[1], list) and propExpr[1][0] == "and":
                CNFExpr.append("or")
                for i in range(1,len(propExpr[1])):
                    clause = ["not"]
                    clause.append(propExpr[1][i])
                    clause = propToCNF(clause)
                    exist = False
                    for item in CNFExpr:
                        if CNFutil.equal(item, clause):
                            exist = True
                            break
                    if not exist:
                        CNFExpr.append(clause)
                CNFExpr = distribute(CNFExpr)
            elif isinstance(propExpr[1], list) and propExpr[1][0] == "or":
                CNFExpr.append("and")
                for i in range(1,len(propExpr[1])):
                    clause = ["not"]
                    clause.append(propExpr[1][i])
                    clause = propToCNF(clause)
                    exist = False
                    for item in CNFExpr:
                        if CNFutil.equal(item, clause):
                            exist = True
                            break
                    if not exist:
                        CNFExpr.append(clause)
                CNFExpr = propToCNF(CNFExpr)
            elif isinstance(propExpr[1], list) and propExpr[1][0] == "implies":
                CNFExpr.append("and")
                CNFExpr.append(propToCNF(propExpr[1][1]))
                clause = ["not"]
                clause.append(propExpr[1][2])
                clause = propToCNF(clause)
                CNFExpr.append(clause)
                CNFExpr = propToCNF(CNFExpr)
            elif isinstance(propExpr[1], list) and propExpr[1][0] == "iff":
                CNFExpr.append("or")
                leftChild = []
                leftChild.append("implies")
                leftChild.append(propExpr[1][1])
                leftChild.append(propExpr[1][2])
                CNFExpr.append(propToCNF(leftChild))
                rightChild = []
                rightChild.append("implies")
                rightChild.append(propExpr[1][2])
                rightChild.append(propExpr[1][1])
                CNFExpr.append(propToCNF(rightChild))
                CNFExpr = distribute(CNFExpr)
        elif propExpr[0] == "and":
            CNFExpr.append("and")
            for i in range(1,len(propExpr)):
                child = propToCNF(propExpr[i])
                if isinstance(child, str) or (isinstance(child, list) and child[0]!= 'and'):
                    exist = False
                    for item in CNFExpr:
                        if CNFutil.equal(item,child):
                            exist = True
                            break
                    if not exist:
                        CNFExpr.append(child)
                else:
                    for j in range(1,len(child)):
                        tmp = propToCNF(child[j])
                        exist = False
                        for item in CNFExpr:
                            if CNFutil.equal(item, tmp):
                                exist = True
                                break
                        if not exist:
                            CNFExpr.append(tmp)
            if len(CNFExpr) == 2:
                CNFExpr = CNFExpr[1]
        elif propExpr[0] == "or":
            for i in range(1,len(propExpr)):
                propExpr[i] = propToCNF(propExpr[i])
            CNFExpr = distribute(propExpr)
        elif propExpr[0] == "implies":
            leftChild = []
            leftChild.append("not")
            leftChild.append(propExpr[1])
            leftChild = propToCNF(leftChild)
            rightChild = propToCNF(propExpr[2])
            CNFExpr.append("or")
            CNFExpr.append(leftChild)
            CNFExpr.append(rightChild)
            CNFExpr = distribute(CNFExpr)
        elif propExpr[0] == "iff":
            CNFExpr.append("and")
            leftChild = []
            leftChild.append("implies")
            leftChild.append(propExpr[1])
            leftChild.append(propExpr[2])
            CNFExpr.append(propToCNF(leftChild))
            rightChild = []
            rightChild.append("implies")
            rightChild.append(propExpr[2])
            rightChild.append(propExpr[1])
            CNFExpr.append(propToCNF(rightChild))
            CNFExpr = propToCNF(CNFExpr)
    return CNFExpr

class testDistributyCase(unittest.TestCase):
    
    def test_test_case_1(self):
        if not CNFutil.equal(propToCNF(["and",["or","A","A"],"B"]), ["and","A","B"]):
            print "test_case 1 for distribute failed"
    
    def test_test_case_2(self):
        if not CNFutil.equal(propToCNF(["or",["and","A","B","C"], ["and","C","D"]]),["and",["or","A","C"],["or","A","D"],["or","B","C"],["or","B","D"],"C",["or","C","D"]]):
            print "test_case 2 for distribute failed"
            print propToCNF(["or",["and","A","B","C"], ["and","C","D"]])
    def test_test_case_3(self):
        if not CNFutil.equal(propToCNF(['or', ['or', ['not', 'P'], ['not', 'Q']], ['and', ['or', 'P', 'Q'], ['or', ['not', 'Q'], ['not', 'P']]]]), ["and",["or",["not","P"],["not","Q"],"P","Q"],["or",["not","P"],["not","Q"]]]):
            print "test_case 3 for distribute failed"
            print propToCNF(['or', ['or', ['not', 'P'], ['not', 'Q']], ['and', ['or', 'P', 'Q'], ['or', ['not', 'Q'], ['not', 'P']]]])
    def test_test_case_4(self):
        if not CNFutil.equal(propToCNF(["or",["and","P","Q"],["and","P","Q"]]), ["and","P","Q"]):
            print "test_case for distribute failed"
            print propToCNF(["or",["and","P","Q"],["and","P","Q"]])

class testAndCase(unittest.TestCase):
    
    def test_case_1(self):
        if not CNFutil.equal(propToCNF(["and","P","Q"]), ["and","P","Q"]):
            print "test_case 1 for and failed"
    def test_case_2(self):
        if not CNFutil.equal(propToCNF(["and","P","P"]), "P"):
            print "test_case 2 for and failed"

class testIfAndOnlyIfCase(unittest.TestCase):
    
    def test_case_1(self):
        if not CNFutil.equal(propToCNF(["iff","A","B"]), ["and",["or",["not","A"],"B"],["or",["not","B"],"A"]]):
            print "test_case 1 for iff failed"
    
    def test_case_2(self):
        if not CNFutil.equal(propToCNF(["implies",["and","P","Q"],["iff",["not","P"],"Q"]]), ['and', ['or', 'P', 'Q', ['not', 'P'], ['not', 'Q']], ['or', ['not', 'Q'], ['not', 'P']]]):
            print "test_case 2 for iff failed" 
            print propToCNF(["implies",["and","P","Q"],["iff",["not","P"],"Q"]])
    
    def test_case_3(self):
        if not CNFutil.equal(propToCNF(["iff",["not","P"],"Q"]), ["and",["or","P","Q"],["or",["not","P"],["not","Q"]]]):
            print "test_case 3 for iff failed"
       
class testImpliesCase(unittest.TestCase):
    
    def test_case_2(self):
        if not CNFutil.equal(propToCNF(["implies",["and",["implies","P","Q"],["not","Q"]],["not","P"]]), ["and",["or","P","Q",["not","P"]],["or","Q",["not","Q"],["not","P"]]]):
            print "test_case 2 for implies failed"
    
    def test_case_1(self):
        if not CNFutil.equal(propToCNF(["implies",["implies",["not","Q"],["not","P"]],["implies","P","Q"]]), ["and",["or",["not","Q"],"Q",["not","P"]],["or",["not","P"],"P","Q"]]):
            print "test_case 1 for implies failed"

def test():
#     sys.setrecursionlimit(1500)
    suite = unittest.TestLoader().loadTestsFromTestCase(testDistributyCase)
    unittest.TextTestRunner().run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(testIfAndOnlyIfCase)
    unittest.TextTestRunner().run(suite)    
    suite = unittest.TestLoader().loadTestsFromTestCase(testImpliesCase)
    unittest.TextTestRunner().run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(testAndCase)
    unittest.TextTestRunner().run(suite)
                                                                                                                                                                                                                                                  
def main(argv):
    inputFile = ""
    outputFile = "sentences_CNF.txt"
    try:
        opts,args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print "python CNFconverter.py -i <inputfile>"
        sys.exit(2)
    for opt,arg in opts:
        if opt == "-i":
            inputFile = arg

    fin = open(inputFile,"r")
    fout = open(outputFile,"w")
    count = int(fin.readline())
    for i in range(0,count):
        expr = fin.readline()
        exprList = eval(expr)
        CNFExpr =  propToCNF(exprList)
        fout.write(str(CNFExpr)+"\n")
    fin.close()
    fout.close()
    

if __name__ == "__main__":
#     main(sys.argv[1:])
    test()
