__author__ = 'Adam'

# Prints the contents of the adjacency list in format
# <NODE> -> <OUT1> <OUT2>
def debug_adjacency_list(adjacency_list):
    test = ''
    for element in adjacency_list.keys():
        test += element+' -> '
        for i in adjacency_list[element]:
            test += i['edge'] + ' '
        test += '\n'
    test += '\n'
    return test

# Prints the degrees of the adjacency list in format
# <NODE>: <DEGREE>
def debug_degree_list(degree_list):
    test = ''
    for tag in degree_list.keys():
        test += tag + ': ' + str(degree_list[tag]) + '\n'

    return test

# Prints the degrees equation to calculate average
def debug_degrees(degree_list):
    if not degree_list:
        return 'No hashtags found'
    else:
        test = '('
        for tag in degree_list.keys():
            test += str(degree_list[tag]) + ' + '
        position = len(test)-3
        test = test[:position]
        test += ')/'+ str(len(degree_list))
        return test