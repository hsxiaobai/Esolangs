
class BrainfuckAnalysisedError(ValueError):
    pass

class BrainfuckCompiledError(ValueError):
    pass

class Brainfuck:
    def __init__(self, code, memorySize=1024):
        self.code = code
        self.memorySize = memorySize
        self.memory = [0 for i in range(self.memorySize)]
        self.ptr = 0
        self.state = 0

    def grammarAnalysis(self):
        if self.state != 0:
            if self.state == 1:
                raise BrainfuckAnalysisedError("Your Brainfuck module has already been analyzed.")
            elif self.state == 2:
                raise BrainfuckCompiledError("Your Brainfuck module has already been compiled.")
        codeList = list(self.code)
        result = []
        charTypeDict = {
            ",": "io",
            ".": "io",
            "+": "op",
            "-": "op",
            "<": "ptr",
            ">": "ptr",
        }
        depth = 0
        block_start = {}
        for ind, char in enumerate(codeList):
            if char in charTypeDict:
                result.append({"type": charTypeDict[char], "command": char})
            elif char == "[":
                depth += 1
                block_start[depth] = ind  # 记录每个深度的起始位置
            elif char == "]":
                if depth == 0:
                    raise ValueError("Unmatched ']' found.")
                start_ind = block_start[depth]
                block_code = "".join(codeList[start_ind+1:ind])
                newBrainfuck = Brainfuck(block_code)
                newBrainfuck.grammarAnalysis()
                nested_analysis = newBrainfuck.code
                result.append({"type": "block", "command": nested_analysis})
                depth -= 1
        self.code = result
        self.state = 1
