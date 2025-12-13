
print("**********************************KRUSHKALS***********************************************")

print("def find(graph, node):")
print("    if graph[node] < node:")
print("        return node")
print("    else:")
print("        temp = find(graph, graph[node])")
print("        graph[node] = temp")
print("        return temp")

print("\ndef union(graph, a, b, answer):")
print("    ta = a")
print("    tb = b")
print("    a = find(graph, a)")
print("    b = find(graph, b)")
print("    ")
print("    if a == b:")
print("        pass")
print("    else:")
print("        answer.append([ta, tb])")
print("        if graph[a] < graph[b]:")
print("            graph[a] = graph[0] + graph[b]")
print("            graph[b] = a")
print("        else:")
print("            graph[b] = graph[a] + graph[b]")
print("            graph[a] = b")

print("\nn = 7")
print("ipt = [[1, 2, 1], [1, 3, 3], [2, 6, 4], [3, 6, 2], [3, 4, 1], [4, 5, 5]]")
print("ipt = sorted(ipt, key=lambda ipt: ipt[2])")
print("graph = [-1] * (n + 1)")
print("answer = []")

print("\nfor u, v, d in ipt:")
print("    union(graph, u, v, answer)")

print("\nfor item in answer:")
print("    print(item)")



print("*********************************************************************************")