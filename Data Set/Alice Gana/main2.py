

# Creating my binary tree
def creating_my_tree(r):
    return[r, [], []]

# Inserting a new branch on the left
def insert_left(tree,new_branch):
    temp=tree.pop(1)
    if len(temp)>1:
        tree.insert(1, [new_branch, temp, []])
    else:
        tree.insert(1, [new_branch, [], []])
    return tree

# Inserting a new branch on the right
def insert_right(tree,new_branch):
    temp=tree.pop(2)
    if len(temp)>1:
        tree.insert(2, [new_branch, [], temp])
    else:
        tree.insert(2, [new_branch, [], []])
    return tree

# Functions to return subtree on the left and on the right
def get_left_child(tree):
    return tree[1]
def get_right_child(tree):
    return tree [2]

# Driving Code
x = creating_my_tree('a')
print(x)
insert_left(x,'b')
print(x)
insert_right(x,'c')
print(x)
insert_right(get_right_child(x), 'd')
print(x)
insert_left(get_right_child(get_right_child(x)), 'e')
print(x)

#OUTPUT:
#['a', [], []]
#['a', ['b', [], []], []]
#['a', ['b', [], []], ['c', [], []]]
#['a', ['b', [], []], ['c', [], ['d', [], []]]]
#['a', ['b', [], []], ['c', [], ['d', ['e', [], []], []]]]
