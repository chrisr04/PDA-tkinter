
class BinaryNode:

    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None
        self.i = 0
        self.anul = None
        self.fpos = []
        self.lpos = []
        self.npos = []

    def __str__(self):
        return "{0}({1})({2})".format(self.value,self.left,self.right)
 
class ExpressionTree:

    precedence = {
        '('  : 4,
        ')'  : 4,
        '*'  : 3,
        '?'  : 3,
        '.'  : 2,
        '|'  : 1
    }
    
    def __init__(self,language,expression):
        self.language = language
        self.regex =  self.formatExpression(expression)
        self._root = self._createExpressionTree(self.regex)

    def getParenthesisExp(self,expression):
        stack = [expression[-1]]
        result = [expression[-1]]
        i = len(expression)-1
        while stack:
            i-=1
            result.insert(0,expression[i])
            if expression[i] == ")":
                stack.append(expression[i])
            elif expression[i] == "(":
                stack.pop()
        result.insert(0,".")
        result.extend(["*","."])
        return result
            
    def formatExpression(self,expression):
        exFormat = []
        for i,l in enumerate(expression):
            if l!="#":
                if l == "+":
                    if expression[i-1] == ")":
                        exFormat.extend(self.getParenthesisExp(exFormat.copy())) 
                    elif expression[i-1] not in "|*+?()":
                        exFormat.extend([expression[i-1],"*","."])
                elif (l in "*?" or l not in "|()") and expression[i+1] not in "|*?)":
                    if l== "l":
                        exFormat.extend(["λ","."])
                    else:
                        exFormat.extend([l,"."])
                elif l==")" and expression[i+1] not in "|*?)#":
                    exFormat.extend([l,"."])
                else:
                    exFormat.append(l)
            else:
                if expression[i-1] == ")":
                    exFormat.extend([".","#"])
                else:
                    exFormat.append("#")
        return exFormat

    def _postfixConvert(self,infix):

        stack = []
        postfix = [] 

        for char in infix:
            if char not in self.precedence:
                postfix.append(char)
            else:
                if len(stack) == 0:
                    stack.append(char)
                else:
                    if char == "(":
                        stack.append(char)
                    elif char == ")":
                        while stack[len(stack) - 1] != "(":
                            postfix.append(stack.pop())
                        stack.pop()
                    elif self.precedence[char] > self.precedence[stack[len(stack) - 1]]:
                        stack.append(char)
                    elif self.precedence[char] == self.precedence[stack[len(stack) - 1]]:
                        postfix.append(stack.pop())
                        stack.append(char)
                    else:
                        while len(stack) != 0:
                            if stack[len(stack) - 1] == '(':
                                break
                            postfix.append(stack.pop())
                        stack.append(char)
        
        while len(stack) != 0:
            postfix.append(stack.pop())

        return postfix

    def inorder(self):
        expression = []
        self._inorderHelper(self._root,expression)
        return expression
         
    def _inorderHelper(self, node, expression):
        if node:
            self._inorderHelper(node.left,expression)
            expression.append(node.value)
            self._inorderHelper(node.right,expression)
 
    def preorder(self):
        expression = []
        self._preorderHelper(self._root,expression)
        return expression
         
    def _preorderHelper(self, node, expression):
        if node:
            expression.append(node.value)
            self._inorderHelper(node.left,expression)
            self._inorderHelper(node.right,expression)
 
    def postorder(self):
        expression = []
        self._postorderHelper(self._root,expression)
        return expression
         
    def _postorderHelper(self, node, expression):
        if node:
            self._postorderHelper(node.left,expression)
            self._postorderHelper(node.right,expression)
            print("value:",node.value,", fpos:",node.fpos,", lpos:",node.lpos,", anulable:",node.anul)
            expression.append(node.value)

    def searchNode(self,i):
        node = []
        self.searchHelper(self._root,i,node)
        return node[0]

    def searchHelper(self,root,i,node):
        if root:
            self.searchHelper(root.left,i,node)
            self.searchHelper(root.right,i,node)
            if root.i == i:
                node.append(root) 
 
    def _createExpressionTree(self,infix):
        postfix = self._postfixConvert(infix)
        stack = []
        i = 0
        for char in postfix:
            if char not in self.precedence:
                node = BinaryNode(char)
                i+=1
                node.i=i
                stack.append(node)
            else:
                node = BinaryNode(char)
                if node.value in "?*":
                    node.right = stack.pop()
                else:
                    node.right = stack.pop()
                    node.left = stack.pop()
                stack.append(node)
      
        return stack.pop()

    def getExpressionTree(self):
        return self._root

    def anulable(self,node):
        if node.right is None and node.left is None:
            if node.value == "λ":
                return True
            else:
                return False
        elif node.value == "|":
            return node.left.anul or node.right.anul
        elif node.value == ".":
            return node.left.anul and node.right.anul
        elif node.value == "*" or node.value == "?":
            return True

    def firstPos(self, node):
        if node.right is None and node.left is None:
            if node.value == "λ":
                node.fpos = []
            else:
                node.fpos.append(node.i)
        elif node.value == "|":
            node.fpos = node.left.fpos.copy()
            node.fpos.extend(node.right.fpos.copy())
        elif node.value == ".":
            if self.anulable(node.left):
                node.fpos = node.left.fpos.copy()
                node.fpos.extend(node.right.fpos.copy())
            else:
                node.fpos = node.left.fpos.copy()
        elif node.value in "*?":
            node.fpos = node.right.fpos.copy()

    def lastPos(self, node):
        if node.right is None and node.left is None:
            if node.value == "λ":
                node.lpos = []
            else:
                node.lpos.append(node.i)
        elif node.value == "|":
            node.lpos = node.left.lpos.copy()
            node.lpos.extend(node.right.lpos.copy())
        elif node.value == ".":
            if self.anulable(node.right):
                node.lpos = node.left.lpos.copy()
                node.lpos.extend(node.right.lpos.copy())
            else:
                node.lpos = node.right.lpos.copy()
        elif node.value in "*?":
            node.lpos = node.right.lpos.copy()
    
    def evaluateExpression(self,root):

        if root:
            self.evaluateExpression(root.left)
            self.evaluateExpression(root.right)
            root.anul = self.anulable(root)
            self.firstPos(root)
            self.lastPos(root)
            # print("value:",root.value,", fpos:",root.fpos,", lpos:",root.lpos,", anulable:",root.anul)
            if root.value == ".":
                for n in root.left.lpos:
                    node = self.searchNode(n)
                    node.npos.extend(root.right.fpos.copy())
                    node.npos = sorted(list(set(node.npos)))
                    # print("i:",n,", nextpos: ",node.npos)
            elif root.value == "*":
                for n in root.lpos:
                    node = self.searchNode(n)
                    node.npos.extend(root.fpos.copy())
                    node.npos = sorted(list(set(node.npos)))
                    # print("i:",n,", nextpos: ",node.npos)

    def searchState(self,state, matrix):
        for f in matrix:
            if state == f['state']:
                return True, f['id']
        return False, 0

    def createMatrix(self, root, language):

        iAccepted = root.right.i
        if iAccepted in root.fpos:
            matrix = [{'id':0,'state':sorted(list(set(root.fpos.copy()))),'accepted':True}]
        else:
            matrix = [{'id':0,'state':sorted(list(set(root.fpos.copy()))),'accepted':False}]
        nS=0
        trasitions = []
        for f in matrix:
            newState = []
            for l in language:
                sw2=False
                for s in f['state']:
                    node = self.searchNode(s)
                    if l == node.value:
                        sw2=True
                        newState.extend(node.npos.copy())
                        newState = sorted(list(set(newState)))
                if sw2:
                    result, id = self.searchState(newState,matrix)
                    if not result:
                        nS+=1
                        if iAccepted in newState:
                            matrix.append({'id':nS,'state':newState.copy(),'accepted':True})
                        else:
                            matrix.append({'id':nS,'state':newState.copy(),'accepted':False})
                        trasitions.append({'from':f['id'],'to':nS,'with':l})
                        # print({'from':f['id'],'to':nS,'with':l})
                    else:
                        trasitions.append({'from':f['id'],'to':id,'with':l})
                        # print({'from':f['id'],'to':id,'with':l})
                    newState = []
                elif f['state']!=[0]:
                    if l != "λ":
                        nS+=1
                        matrix.append({'id':nS,'state':[0],'accepted':False})
                        trasitions.append({'from':f['id'],'to':nS,'with':l})
                        for l2 in language:
                            if l2!="λ":
                                trasitions.append({'from':nS,'to':nS,'with':l2})
                        # print({'from':f['id'],'to':nS,'with':l})
        return matrix, trasitions

    def getAutomata(self):     
        # self.nextPos(self._root)
        self.evaluateExpression(self._root)
        # self.postorder()
        return self.createMatrix(self._root,self.language)
        
# ex = "b(aa|b)*|b(ba)*#"
# print(exFormat)
# expresionTree = ExpressionTree(['λ','a','b'],ex)
# print(expresionTree.regex)
# print(expresionTree.getExpressionTree())
# expresionTree.getAutomata()
# print("In Order:")
# for i in expresionTree.inorder():
#     print(i)