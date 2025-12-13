

print("*************************************BFS*****************************************")

print("import collections")

print("graph = {")
print("    0: [1, 2, 3],")
print("    1: [0, 2],")
print("    2: [0, 1, 4],")
print("    3: [0],")
print("    4: [2]")
print("}")

print("\ndef bfs(graph, root):")
print("    visited = set()")
print("    queue = collections.deque([root])")
print("    while queue:")
print("        vertex = queue.popleft()")
print("        visited.add(vertex)")
print("        for neighbor in graph[vertex]:")
print("            if neighbor not in visited:")
print("                queue.append(neighbor)")
print("    print('Visited nodes:', visited)")

print("\nif __name__ == '__main__':")
print("    graph = {")
print("        0: [1, 2, 3],")
print("        1: [0, 2],")
print("        2: [0, 1, 4],")
print("        3: [0],")
print("        4: [2]")
print("    }")
print("    bfs(graph, 0)")


print("*********************************************************************************")