
print("**********************************TOPOLOGICAL SORT***********************************************")

print("import collections")

print("adjacency_list = [")
print("    [],        ")
print("    [1, 3],    ")
print("    [0, 1],    ")
print("    [0, 2]     ")
print("]")

print("\ndef dfs(node, visited, adj):")
print("    visited[node] = 1")
print("    for neighbor in adj[node]:")
print("        if visited[neighbor] == 0:")
print("            dfs(neighbor, visited, adj)")
print("    if node not in stack:")
print("        stack.append(node)")

print("visited = [0] * len(adjacency_list)")
print("stack = []\n")

print("for i in range(len(adjacency_list)):")
print("    if visited[i] == 0:")
print("        dfs(i, visited, adjacency_list)")

print("print(stack[::-1])")


print("*********************************************************************************")