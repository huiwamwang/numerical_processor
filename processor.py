# static and repeating methods turned into functions
def finish():
    exit()


# using comprehensions to read input from the user
def inp_matrix():
    a = input("Enter size of matrix: ").split()
    print("Enter matrix:")
    matrix_a = [input().split() for _ in range(int(a[0]))]
    return matrix_a


def inp_matrices():
    a = input("Enter size of first matrix: ").split()
    print("Enter first matrix:")
    matrix_a = [input().split() for _ in range(int(a[0]))]
    b = input("Enter size of second matrix: ").split()
    print("Enter second matrix:")
    matrix_b = [input().split() for _ in range(int(b[0]))]
    return a, b, matrix_a, matrix_b


def print_result(result):
    print("The result is:")
    for r in result:
        print(*r, sep=' ')


def determinant_recursive(matrix_a, total=0):
    # Section 1: store indices in list for row referencing
    indices = list(range(len(matrix_a)))
    if len(matrix_a) == 1 and len(matrix_a[0]) == 1:
        return matrix_a[0][0]
    # Section 2: when at 2x2 sub matrices recursive calls end
    elif len(matrix_a) == 2 and len(matrix_a[0]) == 2:
        val = float(matrix_a[0][0]) * float(matrix_a[1][1]) - float(matrix_a[1][0]) * float(matrix_a[0][1])
        return val

    # Section 3: define sub matrix for focus column and
    #      call this function
    for fc in indices:  # A) for each focus column, ...
        # find the sub matrix ...
        m_a = matrix_a  # B) make a copy, and ...
        m_a = m_a[1:]  # ... C) remove the first row
        height = len(m_a)  # D)

        for i in range(height):
            # E) for each remaining row of sub matrix ...
            #     remove the focus column elements
            m_a[i] = m_a[i][0:fc] + m_a[i][fc + 1:]

        sign = (-1) ** (fc % 2)  # F)
        # G) pass sub matrix recursively
        sub_det = determinant_recursive(m_a)
        # H) total all returns from recursion
        total += sign * float(matrix_a[0][fc]) * sub_det

    return total


def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]


def transposeMatrix(matrix_a):
    return [[matrix_a[j][i] for j in range(len(matrix_a))] for i in range(len(matrix_a[0]))]


class Processor:

    def __init__(self):
        self.choice = None

    # first we process user's choice and redirecting to corresponding method
    def welcome(self):
        print("""\n1. Add matrices\n2. Multiply matrix by a constant\n3. Multiply matrices \
                \r4. Transpose matrix\n5. Calculate a determinant\n6. Inverse matrix\n0. Exit""")
        self.choice = int(input("Your choice: "))
        if self.choice == 1:
            self.summation()
        elif self.choice == 2:
            self.constant_multiplication()
        elif self.choice == 3:
            self.multiplication()
        elif self.choice == 4:
            self.transposition()
        elif self.choice == 5:
            self.determinant()
        elif self.choice == 6:
            self.inverse()
        elif self.choice == 0:
            finish()

    def summation(self):
        a, b, matrix_a, matrix_b = inp_matrices()
        # Checking if the matrices are of the same size
        if (a[0] != b[0]) or (a[1] != b[1]):
            print("ERROR")

        # If yes, we are doing summation by adding corresponding elements for two matrices
        elif (a[0] == b[0]) and (a[1] == b[1]):
            result = [[float(matrix_a[i][j]) + float(matrix_b[i][j]) for j in range(len(matrix_a[0]))] for i in
                      range(len(matrix_a))]
            print_result(result)

        self.welcome()

    def constant_multiplication(self):
        matrix_a = inp_matrix()
        x = int(input("Enter constant: "))

        result = [[int(matrix_a[i][j]) * x for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]
        print_result(result)
        self.welcome()

    def multiplication(self):
        a, b, matrix_a, matrix_b = inp_matrices()

        result = [[sum(float(a) * float(b) for a, b in zip(matrix_a_row, matrix_b_col))
                   for matrix_b_col in zip(*matrix_b)] for matrix_a_row in matrix_a]
        print_result(result)
        self.welcome()

    def transposition(self):
        print("""1. Main diagonal\n2. Side diagonal\n3. Vertical line\n4. Horizontal line""")
        choice = int(input("Your choice: "))
        matrix_a = inp_matrix()
        if choice == 1:
            result = transposeMatrix(matrix_a)
            print_result(result)    # changing [i][j] of initial matrix with [j][i]
        elif choice == 2:
            result = [[matrix_a[j][i] for j in reversed(range(len(matrix_a)))]
                      for i in reversed(range(len(matrix_a[0])))]   # same, but we reverse original matrix twice
            print_result(result)
        elif choice == 3:
            result = [i[::-1] for i in matrix_a]    # reversing elements of each 'row' in the matrix
            print_result(result)
        elif choice == 4:
            result = reversed(matrix_a)    # 'reversing' rows of the matrix
            print_result(result)
        self.welcome()

    def determinant(self):
        matrix_a = inp_matrix()
        det = determinant_recursive(matrix_a)
        print(f"The result is:\n{det}")
        self.welcome()

    def inverse(self):
        m = inp_matrix()
        determinant = determinant_recursive(m)
        if not determinant:
            print("This matrix doesn't have an inverse.")
            self.welcome()

        # special case for 2x2 matrix:
        if len(m) == 2:
            return [[float(m[1][1]) / determinant, -1 * float(m[0][1]) / determinant],
                    [-1 * float(m[1][0]) / determinant, float([0][0]) / determinant]]

        # find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = getMatrixMinor(m, r, c)
                cofactorRow.append(((-1) ** (float(r) + float(c))) * determinant_recursive(minor))
            cofactors.append(cofactorRow)
        cofactors = transposeMatrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c] / determinant
        print_result(cofactors)
        self.welcome()


start = Processor()
start.welcome()
