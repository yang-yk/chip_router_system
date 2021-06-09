def merge_list(L):
    lenth = len(L)
    temp = []
    for l in L:
        temp.append(set(l))
    L = temp
    merge_id = []
    for i in range(1, lenth):
        for j in range(i):
            if L[i] == {0} or L[j] == {0}:
                continue
            x = L[i].union(L[j])
            y = len(L[i]) + len(L[j])
            if len(x) < y:
                L[i] = x
                L[j] = {0}
                merge_id.append([i,j])

    merge_result = [i for i in L if i != {0}]
    print(L)


    return merge_result,merge_id

#alist = [{'a', 'b', 'c', 'f'}, {'e', 'g'}, {1, 2, 3}, {'h', 'g', 'f'}, {5, 6, 7}, {3, 4}]
#print(merge_list(alist))


cur_router_paths=[[1,2,3,4],[6,4,9],[7,8],[11],[9],[8,10],[12]]

merge_result,merge_id = merge_list(cur_router_paths)
print(merge_id)
print(merge_result)


merge_result1,merge_id1 = merge_list(merge_id)
print(merge_result1)