import re

class Language:
    
    def __init__(self, expression):
        self.rule = re.compile(r"[^\s{},][\w]*")
        self.expression = expression
        self.words = self.rule.findall(expression)

    def __str__(self):
        return "L = {0}".format(self.expression)

    def verifyComposition(self,word):
        i = e = 0
        while i<len(word):
            sw = False
            for w in range(0,len(self.words)):
                e = len(self.words[w])
                if i+e <= len(word):
                    if self.words[w] == word[i:i+e]:
                        i = i+e
                        sw = True
                        break
            if not sw:
                return False
        else:
            return True