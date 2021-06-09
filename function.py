'''
basic functions for chip system
written by Yukuan
2021.05.29
'''
def merge_list(L):

    print(L)
    lenth = len(L)
    temp = []
    for l in L:
        temp.append(set(l))
    L = temp

    merge_id = []
    for i in range(lenth):
        merge_id.append([])

    for i in range(1, lenth):
        merge_id[i].append(i)
        for j in range(i):
            if L[i] == {0} or L[j] == {0}:
                continue
            x = L[i].union(L[j])
            y = len(L[i]) + len(L[j])
            if len(x) < y:
                L[i] = x
                L[j] = {0}
                merge_id[i].append(i)
                merge_id[i].append(j)
                merge_id[i] = merge_id[j] + merge_id[i]
                merge_id[j] = []


    #print(merge_id)

    merge_id_without_repetition = []
    for id in merge_id:
        id = set(id)
        #print(id)
        merge_id_without_repetition.append(list(id))

    #print(merge_id_without_repetition)

    merge_result = [i for i in L if i != {0}]
    merge_id = [i for i in merge_id_without_repetition if i != []]
    print(merge_id)
    print(merge_result)


    return merge_result,merge_id


#cur_router_paths=[[(0,0,0,0),(0,0,1,0),(0,0,2,0),(0,0,3,0)],[(0,0,3,0),(0,0,3,1),(0,0,3,2),(0,0,3,3)],[(0,0,5,0),(0,0,6,0)]]
#merged_router_paths, merged_router_id = merge_list(cur_router_paths)
#print(merged_router_paths)
#print(merged_router_id)

#test
#cur_router_paths=[[1,2,3,4],[6,4,9],[7,8],[11],[9],[8,10],[12]]
#merge_result,merge_id = merge_list(cur_router_paths)
#print(merge_id)