class BrainfuckAnalysisedError(ValueError):
	pass

class BrainfuckCompiledError(ValueError):
	pass

class BrainfuckNotAnalysised(ValueError):
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
			">": "ptr"
		}
		depth = 0
		blockStart = {}
		for ind, char in enumerate(codeList):
			if char in charTypeDict:
				result.append({"type": charTypeDict[char], "command": char})
			elif char == "[":
				depth += 1
				blockStart[depth] = ind
			elif char == "]":
				if depth == 0:
					raise ValueError("Unmatched ']' found.")
				startInd = blockStart[depth]
				blockCode = "".join(codeList[startInd+1:ind])
				newBrainfuck = Brainfuck(blockCode)
				newBrainfuck.grammarAnalysis()
				nestedAnalysis = newBrainfuck.code
				result.append({"type": "block", "command": nestedAnalysis})
				depth -= 1
		self.code = result
		self.state = 1
	def compileToPython(self):
		if state != 1:
			if state == 0:
				raise BrainfuckNotAnalysisedError("Your Brainfuck module hasn't been analysised yet.")
			elif state == 2:
				raise BrainfuckCompiledError("Your Brainfuck module has already been compiled.")
		result = ""
		charDict = {
			",":"self.memory[self.ptr] = ord(input()[1])",
			".":"print(chr(self.memory[self.ptr])",
			"+":"self.memory[self.ptr] += 1",
			"-":"self.memory[self.ptr] -= 1",
			"<":"""if self.ptr == 0:
				self.ptr = self.memorySize - 1
			else:
   				self.ptr -= 1""",
			">":"""if self.ptr == self.memorySize - 1:
   				self.ptr = 0
	   		else:
	  			self.ptr += 1"""
		}
		for command in code:
			if command["type"] in ("io","op","ptr"):
				result += charDict[command["command"]] + "\n"
			elif command["type"] == "block":
				newAST = Brainfuck(command["command"])
				newAST.state = 1
				newAST.compileToPython()
				result += "".join(map(lambda s:"\t" + s,"\n".split(newAST.code)))
