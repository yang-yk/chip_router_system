
def gen_graph_from_path(L):
    exist = dict()
    for id, path in enumerate(L):
        for node in path:
            if node in exist:
                exist[node].append(id)
            else:
                exist[node] = [id]

    N = len(L)
    
    parent = [-1,] * N
    def root(i):
        if parent[i] < 0:
            return i
        parent[i] = root(parent[i])
        return parent[i]
    def union(i, j):
        ri, rj = root(i), root(j)
        if ri < rj:
            parent[rj] = ri
        if ri > rj:
            parent[ri] = rj
    
    for lst in exist.values():
        for i in lst:
            union(lst[0], i)
    
    contain = []
    graphs = []
    to_graph = [-1] * N
    for i in range(N):
        if root(i) == i:
            contain.append({i})
            graphs.append(dict())
            to_graph[i] = len(graphs) - 1
        else:
            contain[to_graph[root(i)]].add(i)
        graph = graphs[to_graph[root(i)]]
        for j in range(len(L[i])):
            if not L[i][j] in graph:
                graph[L[i][j]] = set()
            if j < len(L[i])-1:
                graph[L[i][j]].add(L[i][j+1])
            
    return contain, graphs # contain 表示每个图包含输入中的哪些路径


def get_last_node_in_graph(graph):
    last_node_list =[]
    for key, val in graph.items():
        if val == set():
            last_node_list.append(key)
    return last_node_list

def get_pre_node_in_graph(graph,node):
    pre_node_list = []
    for key, val in graph.items():
        if val == {node}:
            pre_node_list.append(key)
    return pre_node_list

def get_one_path(graph,node):
    path = []
    path.append(node)


if __name__ == "__main__":
    #cur_router_paths=[[1,2,3,4],[6,4,9],[7,8],[11],[9],[8,10],[12]]
    #cur_router_paths = [[0,1],[1,2],[1,3],[4,5],[5,6],[7,3]]
    cur_router_paths = [[0,1], [1,2], [3,2],[4,2], [2,5], [7, 3]]
    contain, graphs = gen_graph_from_path(cur_router_paths)
    print(contain)
    print(graphs)