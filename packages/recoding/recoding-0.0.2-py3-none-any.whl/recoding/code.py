class Code(str):
    def __new__(cls, code):
        return super().__new__(cls, code)
    
    def replace(self, old: str, new: str, exceptIn: dict={}):
        if exceptIn is None:
            exceptIn = {}
        
        if not exceptIn or not old:
            return Code(super().replace(old, new))
        
        result = []
        i = 0
        length = len(self)
        oldLength = len(old)
        
        exception = None
        stack = []
        
        while i < length:
            matchKey = None
            for key in exceptIn:
                if self[i:].startswith(key):
                    matchKey = key
                    break
                    
            if matchKey and (not stack or exceptIn.get(stack[-1]) != matchKey):
                stack.append(matchKey)
                result.append(matchKey)
                i += len(matchKey)
                continue
            
            if stack and self[i:].startswith(exceptIn[stack[-1]]):
                end_char = exceptIn[stack.pop()]
                result.append(end_char)
                i += len(end_char)
                continue
            
            if self[i:].startswith(old) and not stack:
                result.append(new)
                i += oldLength
            else:
                result.append(self[i])
                i += 1
                
        return Code("".join(result))
