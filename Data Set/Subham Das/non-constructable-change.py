# O(NlogN) time, O(1) space
def nonConstructibleChange(coins):
    if not coins:
        return 1

    coins.sort()
    maxChangeGenerated = 0
    i = 0
    while i < len(coins):
        if coins[i] <= maxChangeGenerated + 1:
            maxChangeGenerated += coins[i]
        else:
            return maxChangeGenerated + 1
        i += 1

    return maxChangeGenerated + 1
