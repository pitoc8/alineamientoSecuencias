from score import Score

# -------------------------------------------------------------------------------
# Prints any matrix
# Receives the matrix, rows qty, cols qty

def printMatrix(matrix, rows, cols):
    for i in range(rows):
        for j in range(cols):
            print(" %d " %matrix[i][j].value, end='')
        print()

# -------------------------------------------------------------------------------
# Initialize any score matrix size
#Receives rows qty, cols qty

def initializeMatrix(rows, cols):
    newMatrix = []
    for i in range(rows):
        newLine = []
        for j in range(cols):
            if (i == 0) & (j > 0):
                newLine.append(Score(0, 'left'))
            elif (i > 0) & (j == 0):
                newLine.append(Score(0, 'up'))
            else:
                newLine.append(Score(0, {}))
        newMatrix.append(newLine)
    return newMatrix

# -------------------------------------------------------------------------------
#Calculates matrix values
#Receives strings to be aligned

def generateScoreMatrix( string1, string2):
    rows = len(string1)+1
    cols = len(string2)+1
    print(string1)
    print(string2)
    aMatrix = initializeMatrix(rows, cols)
    sI = 0
    for i in range(1, rows):
        sJ = 0
        for j in range(1, cols):
            aMatrix[i][j] = calculateScore(string1[sI],
                                           string2[sJ],
                                           aMatrix[i][j-1].value,
                                           aMatrix[i-1][j-1].value,
                                           aMatrix[i-1][j].value)
            sJ += 1
        sI += 1

    printMatrix(aMatrix, rows, cols)
    return aMatrix

# -------------------------------------------------------------------------------
# Checks if score is < 0
# Receives score
def checkFor0(score):
    if (score.value <= 0):
        return Score(0,'')
    else:
        return score


# -------------------------------------------------------------------------------
# Gets max value from 3 calculated scores
# Receives left, diag, and up values

def max(a, b, c):
    if (a.value > b.value) & (a.value > c.value):
        return checkFor0(a)
    elif (c.value > b.value):
        return checkFor0(c)
    else:
        return checkFor0(b)

# -------------------------------------------------------------------------------
# Calculates score for each field in the matrix
# Receives char1, char2, leftScore, diagScore, upScore
def calculateScore(bN1, bN2, left, diag, up):

    leftRes = Score(left - 2, 'left')
    upRes = Score(up - 2, 'up')
    if bN1 == bN2:
        diagRes = Score(diag + 1, 'diag')
        # result = max(leftRes, diagRes, upRes)
    else:
        diagRes = Score(diag - 1, 'diag')
        # result = max(leftRes, diagRes, upRes)

    result = max(leftRes, diagRes, upRes)
    return result

# -------------------------------------------------------------------------------
# Print Alignments
# Receives alignments
def printAlignmnents(alignments):
    for i in range(len(alignments)):
        print("Sequence#{}".format(i))
        for j in range(len(alignments[i])):
            print("{} ".format(alignments[i][j]))


def getHighestScore(alignments):
    hIndex = 0
    for i in range(1, len(alignments)):
        if(alignments[i][2] > alignments[hIndex][2]):
            hIndex = i
    return hIndex

def hasOverlap(align, index, newAlign):
    result = False
    for i in range(len(align)):
        for j in range(len(newAlign)):
            if (index != i) & (newAlign[j][0].find(align[i][0]) == -1) & (newAlign[j][1].find(align[i][1]) == -1):
                result = True
    return result

    # if (alignment[hIndex][0].find(alignment[i][0]) == -1) & (alignment[hIndex][1].find(alignment[i][1]) == -1):
    #     return False
    # else:
    #     return True

def getValidAlignments(alignments):
    hIndex = getHighestScore(alignments)
    newAlignments = [alignments[hIndex]]
    for i in range(len(alignments)):
        if (i != hIndex) & (hasOverlap(alignments, i, newAlignments) == False):
            newAlignments.append(alignments[i])
    printAlignmnents(newAlignments)
    return newAlignments


# -------------------------------------------------------------------------------
# Analyze matrix to get alignments
# Receives string1, string2, matrix, rows, cols
def analyzeMatrix(string1, string2, matrix, rows, cols):
    alignments = []
    for i in range(rows-1, 0, -1):
        for j in range(cols-1, 0, -1):
            if (matrix[i][j].value > 0) & (string1[i-1] == string2[j-1]) & (matrix[i][j].dir == 'diag') & \
                    (matrix[i-1][j-1].dir == 'diag'):
                print("[{}][{}] = {} - {}".format(i, j, matrix[i][j].value, matrix[i][j].dir))
                alignments.append(checkAlignmnent(matrix, i, j, string1, string2))
    printAlignmnents(alignments)
    getValidAlignments(alignments)
    return alignments


def checkAlignmnent (matrix, iStart, jStart, string1, string2):
    arrayString1 = []
    arrayString2 = []
    i = iStart
    j = jStart
    scoring = 0
    while(matrix[i][j].dir == 'diag') & (matrix[i][j].value != 0):
        arrayString1.append(string1[i-1])
        arrayString2.append(string2[j-1])
        if (string1[i-1] == string2[j-1]):
            scoring += 1
        else:
            scoring -= 1
        i -= 1
        j -= 1
    newString1 = ''.join(arrayString1)
    newString2 = ''.join(arrayString2)
    return [newString1[::-1], newString2[::-1], scoring]


# def analyzeMatrix(string1, string2, matrix, rows, cols):
#     arrayString1 = []
#     arrayString2 = []
#     i = rows - 1
#     j = cols - 1
#     sI = rows - 2
#     sJ = cols - 2
#     # print("i: {} - j: {} - sI: {} - sJ: {}".format(i, j, sI, sJ))
#     # print("matrix[{}][{}] = {}".format(i,j, matrix[i][j].dir))
#
#     while ( i > 0 ) | (j > 0):
#             if (matrix[i][j].dir == 'diag'):
#                 arrayString1.append(string1[sI])
#                 arrayString2.append(string2[sJ])
#                 i -= 1
#                 j -= 1
#                 sI -= 1
#                 sJ -= 1
#             elif (matrix[i][j].dir == 'left'):
#                 arrayString1.append('_')
#                 arrayString2.append(string2[sJ])
#                 j -= 1
#                 sJ -= 1
#             else:
#                 arrayString1.append(string1[sI])
#                 arrayString2.append('_')
#                 i -= 1
#                 sI -= 1
#     newString1 = ''.join(arrayString1)
#     newString2 = ''.join(arrayString2)
#     return [newString1[::-1], newString2[::-1]]



def generateLocalAlignment(string1, string2):
    matrix = generateScoreMatrix(string1, string2)
    alignment = analyzeMatrix(string1, string2, matrix, len(string1)+1, len(string2)+1)
    # alignment = analyzeMatrix(string1, string2, matrix, len(string1)+1, len(string2)+1)
    # print("{}".format(alignment[0]))
    # print("{}".format(alignment[1]))




generateLocalAlignment("gtacattcta","attgtgatcc")