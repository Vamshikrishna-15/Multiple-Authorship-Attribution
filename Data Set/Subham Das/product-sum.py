def productSum(array):
    return specialArrays(array, 1)

def specialArrays(array, currentLevel):
    if not array:
        return 0
    
    sum = 0
    for elem in array:
        if type(elem) == list:
            sum += specialArrays(elem, currentLevel + 1)
        else:
            sum += elem
            
    return sum * currentLevel
