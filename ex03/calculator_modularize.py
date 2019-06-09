def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1


def readMult(line, index):
  token = {'type': 'MULT'}
  return token, index + 1


def readDiv(line, index):
  token = {'type': 'DIV'}
  return token, index + 1


def readLPar(line, index):
  token = {'type': 'LPAR'}
  return token, index + 1


def readRPar(line, index):
  token = {'type': 'RPAR'}
  return token, index + 1


def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '*':
      (token, index) = readMult(line, index)
    elif line[index] == '/':
      (token, index) = readDiv(line, index)
    elif line[index] == '(':
      (token, index) = readLPar(line, index)
    elif line[index] == ')':
      (token, index) = readRPar(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


# handle parentheses (returns updated tokens)
def evaluate_Par(tokens):
  index = 0
  rpar_index = len(tokens)
  have_lpar = []
  have_rpar = []
  # indexes of '(' and ')' in tokens
  for i in range(len(tokens)):
    if tokens[i]['type'] == 'LPAR':
      have_lpar.append(i)
    elif tokens[i]['type'] == 'RPAR':
      have_rpar.append(i)
  if len(have_lpar) != len(have_rpar): # if the number of '(' and ')' are unequal
    print('Invalid syntax 1')
    exit(1)
  popcount = 0 # to renew indexes after updating tokens
  while have_lpar and have_rpar:
      lpar_index = have_lpar.pop()
      rpar_index = [x for x in have_rpar if x > lpar_index]
      rpar_index = rpar_index[0]
      have_rpar.remove(rpar_index)
      rpar_index -=  popcount # renew index
      popcount = 0
      # evaluate tokens inside parentheses and update tokens
      inpar_tokens = tokens[lpar_index+1:rpar_index]
      tokens[lpar_index] = {'type': 'NUMBER', 'number': evaluate_normal(inpar_tokens)}
      del tokens[lpar_index+1:rpar_index+1]
      # check if index should be updated
      if have_lpar:
          next_lpar = have_lpar[len(have_lpar)-1]
          next_rpar = [x for x in have_rpar if x > next_lpar]
          if rpar_index < next_rpar[0]:
              popcount = rpar_index - lpar_index
  return tokens


# multiplication and division (returns updated tokens)
def evaluate_MD(tokens):
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'MULT':
        tokens[index - 2]['number'] = tokens[index - 2]['number'] * tokens[index]['number']
        tokens.pop(index)
        tokens.pop(index - 1)
        index -= 1
      elif tokens[index - 1]['type'] == 'DIV':
        if tokens[index]['number'] != 0:
          tokens[index - 2]['number'] = tokens[index - 2]['number'] / tokens[index]['number']
          tokens.pop(index)
          tokens.pop(index - 1)
          index -= 1
        else:
          print('Cannot divide by ZERO')
          exit(1)
      elif tokens[index - 1]['type'] == 'PLUS' or tokens[index - 1]['type'] == 'MINUS':
        index += 1
      else:
        print('Invalid syntax 3')
        exit(1)
    index += 1
  return tokens


# plus and minus
def evaluate_PM(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax 4')
        exit(1)
    index += 1
  return answer


# normal + - * / calculator
def evaluate_normal(tokens):
  return evaluate_PM(evaluate_MD(tokens))


def test(line):
  tokens = tokenize(line)
  tokens = evaluate_Par(tokens)
  actualAnswer = evaluate_normal(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("1")
  test("0*77")
  test("1*5.3")
  test("1.5*4")
  test("1.5*10/3")
  test("5-1.5*10/3")
  test("2-1.5*10-6/30")
  test("1.4/0.7")
  test("(1+5)")
  test("3*(1+5)")
  test("3*(1+5/4)")
  test("100*((7-5*4-3/92)/6)+7/5")
  test("(5+4*2)/3-2*(4+5)")
  test("(1+5)/3-4*(6*(12/7+8))+15")
  test("((1+2)*3)/4-7*2+(4+3)*30")
  test("1+5/675/34*(2+(3/4)+(5-7*34)-2)")
  # test("3-9/0")
  # test("2/0")
  # test("4^5")
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input().replace(" ", "")
  tokens = tokenize(line)
  tokens = evaluate_Par(tokens)
  answer = evaluate_normal(tokens)
  print("answer = %f\n" % answer)
