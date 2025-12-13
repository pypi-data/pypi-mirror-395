"""
union
intersection
complement
difference
"""

def contains(A, x):
    """
    A = [[a, b], [c, d]]
    """
    output = False
    for I in A:
        if (I[0] <= x) and (x <= I[1]):
            output = True
    return output

# Check if intersecting
def is_intersecting(A, B):
    """
    A = [a, b]
    B = [c, d]
    """
    output = False
    master = [A, B]
    master.sort(key=lambda sublist: sublist[0])
    if master[1][0] <= master[0][1]:
        output = True
    return output

def is_intersectingco(A, B):
    """
    A = [a, b]
    B = [c, d]
    """
    output = False
    master = [A, B]
    master.sort(key=lambda sublist: sublist[0])
    if master[1][0] < master[0][1]:
        output = True
    return output

def is_containing(A, B):
    """
    A = [a, b]
    B = [c, d]
    Does A contain B?
    """
    output = False
    if (A[0] <= B[0]) and (B[1] <= A[1]):
        output = True
    return output

def union_two2one(A, B):
    """
    A = [a, b]
    B = [c, d]
    """
    if not is_intersecting(A, B):
        raise ValueError("Input intervals are not overlapping.")
    values = [A[0], A[1], B[0], B[1]]
    output = [min(values), max(values)]
    return output

# Union Intervals
def union(A, B):
    """
    A = [[a, b], [c, d]]
    B = [[e, f], [g, h]]
    """
    master = A + B
    master.sort(key=lambda sublist: sublist[0])
    output = [[0, 0]]
    candidate = []
    for i in master:
        if not candidate:
            candidate = i
        else:
            if is_intersecting(candidate, i):
                if is_containing(candidate, i):
                    pass
                else:
                    candidate = union_two2one(candidate, i)
            else:
                output.append(candidate)
                candidate = i
    #print(f"union master: {master}")
    #print(f"union pre-output: {output}")
    try:
        if output[-1] != master[-1]:
            output.append(candidate)
        output.pop(0)
    except Exception as e:
        print(f"Exception (union): {e}")
        print(f"master: {master}")
        print(f"output: {output}")
    return output

def overlapping(A, B):
    """
    A = [[a, b], [c, d]]
    B = [[e, f], [g, h]]
    """
    output = []
    #print(f"overlapping, B: {B}")
    for I in A:
        add = False
        for J in B:
            if is_intersecting(I, J):
                add = True
                break
        if add:
            output.append(I)
    return output

def excluding(A, B):
    """
    A = [[a, b], [c, d]]
    B = [[e, f], [g, h]]
    """
    output = []
    for I in A:
        remove = False
        for J in B:
            if is_intersecting(I, J):
                remove = True
        if not remove:
            output.append(I)
    return output

def excludingco(A, B):
    """
    A = [[a, b], [c, d]]
    B = [[e, f], [g, h]]
    """
    output = []
    for I in A:
        remove = False
        for J in B:
            if is_intersectingco(I, J):
                remove = True
        if not remove:
            output.append(I)
    return output

def remove_overlapping_intervals(A):
    """
    A = [[a, b], [c, d]]
    """
    if len(A) == 1:
        output = A
        return output
    A.sort(key=lambda sublist : sublist[0])
    output = [[0, 0]]
    for I in A:
        J = output[-1]
        if not is_intersecting(I, J):
            output.append(I)
    output.pop(0)
    return output 

def complement(I, U):
    """
    I = [a, b]
    U = [c, d]
    """
    J = [U[0], I[0]-1]
    K = [I[1]+1, U[1]]
    # This is a set-theoretic complement of closed intervals
    if J[1]-J[0] <= 0:
        J = None
    if K[1]-K[0] <= 0:
        K = None
    output = [J, K]
    return output

def complements(A, U):
    """
    A = [[a, b], [c, d]]
    U = [e, f]

    xxxooxxoxx
    oooxxooxoo
    0123456789
    """
    output = []
    for I in A:
        J, K = complement(I, U)
        if J is not None:
            output.append(J)
        U = K
    if U is not None:
        output.append(U)
    return output
