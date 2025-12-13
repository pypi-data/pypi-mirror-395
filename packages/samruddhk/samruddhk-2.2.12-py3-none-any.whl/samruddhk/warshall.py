
print("***********************************WARSHALS**********************************************")

print("def trans_closure(graph):")

print("    nodes = len(graph)")
print("    trans = [list(row) for row in graph]")

print("    for k in range(nodes):")
print("        for i in range(nodes):")
print("            for j in range(nodes):")
print("                trans[i][j] = trans[i][j] or (trans[i][k] and trans[k][j])")            
print("    return trans")

print("def print_transitive_closure(trans):")
print("    for row in trans:")
print("        print(row)")
        
print("graph = [")
print("    [1, 1, 0, 1],")
print("    [0, 1, 1, 0],")
print("    [0, 0, 1, 1],")
print("    [0, 0, 0, 1]")
print("]")
print("trans = trans_closure(graph)")
print("print_transitive_closure(trans)")
print("*********************************************************************************")