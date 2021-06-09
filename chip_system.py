'''
written by Yukuan Yang
2021.05.29
'''

from physical_core import physical_core
from data_task import router_task,data_info
from router import merge_router, split_router
from single_chip import singe_chip
import numpy as np
import logging
import os
from gen_graph import gen_graph_from_path,get_last_node_in_graph,get_pre_node_in_graph
from function import merge_list
from graph_node import Node,AdjacencyList

if os.path.exists('test_example.log'):
  os.remove('test_example.log')
logging.basicConfig(filename='test_example.log', level=logging.INFO)
logging.info('start test process!')



class chip_system(object):
    def __init__(self,chip_numx,chip_numy):
        '''
        :param chip_numx: ??x?????
        :param chip_numy: ??y?????
        '''
        self.chip_numx = chip_numx
        self.chip_numy = chip_numy
        self.chip_array = []
        for i in range(chip_numx):
            chip_array_y = []
            for j in range(chip_numy):
                phy_chip = singe_chip(chip_idx=i,chip_idy=j,core_numx=16,core_numy=10)
                chip_array_y.append(phy_chip)
            self.chip_array.append(chip_array_y)

        self.dynamic_graphs = []
        self.merge_tasks = []
        self.all_used_cores =[]

    def get_chip_from_id(self,chip_idx,chip_idy):
        '''
        :param chip_id: (chip_idx,chip_idy)
        :return: chip
        '''
        return self.chip_array[chip_idx][chip_idy]

    def get_core_from_id(self,core_id):
        '''
        :param core_id: (chip_idx,chip_idy,core_idx,core_idy)
        :return: core
        '''
        cur_chip = self.get_chip_from_id(core_id[0],core_id[1])
        return cur_chip.get_core_from_id(core_id[2],core_id[3])

    def get_router_tasks_path(self, router_tasks, X_Y = 'True'):
        '''
        :param router_tasks: ???????list
        :param X_Y: ?X?Y????
        :return: ???????????
        '''
        router_tasks_paths = []
        for router_task in router_tasks:
            src_chip_id = router_task.src_chip_id
            dst_chip_id = router_task.dst_chip_id
            src_chip_idx = src_chip_id[0]
            src_chip_idy = src_chip_id[1]
            dst_chip_idx = dst_chip_id[0]
            dst_chip_idy = dst_chip_id[1]
            src_id = router_task.src_id
            dst_id = router_task.dst_id
            src_idx = src_id[0]
            src_idy = src_id[1]
            dst_idx = dst_id[0]
            dst_idy = dst_id[1]
            router_task_path = []

            src_chip = self.get_chip_from_id(src_chip_idx,src_chip_idy)
            router_task_path.append((src_chip_idx,src_chip_idy,src_idx,src_idy))

            chip_pathx = dst_chip_idx - src_chip_idx
            chip_pathy = dst_chip_idy - src_chip_idy

            #same chip src_core to dst_core
            if chip_pathx == 0 and chip_pathy == 0:

                pathx = dst_idx - src_idx
                pathy = dst_idy - src_idy

                #First X then Y
                #intra chip
                if pathx < 0:
                    for x in range(np.abs(pathx)):
                        router_task_path.append((src_chip_idx,src_chip_idy,src_idx - 1 - x, src_idy))
                elif pathx > 0:
                    for x in range(np.abs(pathx)):
                        router_task_path.append((src_chip_idx,src_chip_idy,src_idx + 1 + x, src_idy))
                else:
                    pass

                if pathy < 0:
                    for y in range(np.abs(pathy)):
                        router_task_path.append((src_chip_idx,src_chip_idy,dst_idx, src_idy - 1 - y))
                elif pathy > 0:
                    for y in range(np.abs(pathy)):
                        router_task_path.append((src_chip_idx,src_chip_idy,dst_idx, src_idy + 1 + y))
                else:
                    pass

            else:
                # different chip
                # intra chip
                cross_chip_x = False
                if chip_pathx < 0:
                    pathx = 0 - src_idx
                    # First X then Y
                    cross_chip_x = True

                    # src_core to x edge core
                    if pathx < 0:
                        for x in range(np.abs(pathx)):
                            router_task_path.append((src_chip_idx, src_chip_idy, src_idx - 1 - x, src_idy))

                    elif pathx > 0:
                        for x in range(np.abs(pathx)):
                            router_task_path.append((src_chip_idx, src_chip_idy, src_idx + 1 + x, src_idy))
                    else:
                        pass
                    # <----
                    # x edge core to src chip left merge router
                    router_task_path.append((src_chip_idx, src_chip_idy, -1, 0))

                elif chip_pathx > 0:
                    pathx = src_chip.core_numx - 1 - src_idx
                    cross_chip_x = True
                    # First X then Y

                    if pathx < 0:
                        for x in range(np.abs(pathx)):
                            router_task_path.append((src_chip_idx, src_chip_idy, src_idx - 1 - x, src_idy))
                    elif pathx > 0:
                        for x in range(np.abs(pathx)):
                            router_task_path.append((src_chip_idx, src_chip_idy, src_idx + 1 + x, src_idy))
                    else:
                        pass
                    # ---->
                    # x edge core to src chip right merge router
                    router_task_path.append((src_chip_idx, src_chip_idy, -3, 0))

                if cross_chip_x is not True:
                    # only cross Y chips

                    if chip_pathy < 0:
                        pathy = 0 - src_idy
                        # First X then Y

                        if pathy < 0:
                            for y in range(np.abs(pathy)):
                                router_task_path.append((dst_chip_idx, dst_chip_idy, dst_idx, src_idy - 1 - y))
                        elif pathy > 0:
                            for y in range(np.abs(pathy)):
                                router_task_path.append((dst_chip_idx, dst_chip_idy, dst_idx, src_idy + 1 + y))
                        else:
                            pass
                        # __^__
                        # Y edge core to chip top merge router
                        router_task_path.append((src_chip_idx, src_chip_idy, -4, 0))

                    elif chip_pathy > 0:

                        pathy = src_chip.core_numy - src_idy
                        # First X then Y

                        if pathy < 0:
                            for y in range(np.abs(pathy)):
                                router_task_path.append((src_chip_idx, src_chip_idy, dst_idx, src_idy - 1 - y))
                        elif pathy > 0:
                            for y in range(np.abs(pathy)):
                                router_task_path.append((src_chip_idx, src_chip_idy, dst_idx, src_idy + 1 + y))
                        else:
                            pass

                            # --V--
                        # Y edge core to chip bottom merge router
                        router_task_path.append((src_chip_idx, src_chip_idy, -2, 0))

                # inter chip
                # right->left
                if chip_pathx < 0:
                    for x in range(np.abs(chip_pathx)):
                        if x == np.abs(chip_pathx) - 1:
                            # get to the end of X chip split router
                            router_task_path.append((src_chip_idx - 1 - x, src_chip_idy, -3, -1))
                        else:
                            # last chip merge router to next chip split router
                            router_task_path.append((src_chip_idx - 1 - x, src_chip_idy, -3, -1))
                            # same chip split to merge
                            router_task_path.append((src_chip_idx - 1 - x, src_chip_idy, -1, 0))
                # left->right
                elif chip_pathx > 0:
                    for x in range(np.abs(chip_pathx)):
                        if x == np.abs(chip_pathx) - 1:
                            # get to the end of X chip split router
                            router_task_path.append((src_chip_idx + 1 + x, src_chip_idy, -1, -1))
                        else:
                            # last chip merge router to next chip split router
                            router_task_path.append((src_chip_idx + 1 + x, src_chip_idy, -1, -1))
                            # same chip split to merge
                            router_task_path.append((src_chip_idx + 1 + x, src_chip_idy, -3, 0))

                # bottom->top
                if chip_pathy < 0:
                    if cross_chip_x:
                        # get to the end of X chip merge router
                        router_task_path.append((dst_chip_idx, src_chip_idy, -4, 0))
                    for x in range(np.abs(chip_pathy)):
                        if x == np.abs(chip_pathy) - 1:
                            # get to the end of Y chip split router
                            router_task_path.append((dst_chip_idx, src_chip_idy - 1 - x, -2, -1))
                        else:
                            # last chip merge router to next chip split router
                            router_task_path.append((dst_chip_idx, src_chip_idy - 1 - x, -2, -1))
                            # same chip split to merge
                            router_task_path.append((dst_chip_idx, src_chip_idy - 1 - x, -4, 0))
                # top->bottom
                elif chip_pathy > 0:
                    if cross_chip_x:
                        # get to the end of X chip merge router
                        router_task_path.append((dst_chip_idx, src_chip_idy, -2, 0))
                    for x in range(np.abs(chip_pathy)):
                        if x == np.abs(chip_pathy) - 1:
                            # get to the end of Y chip split router
                            router_task_path.append((dst_chip_idx, src_chip_idy + 1 + x, -4, -1))
                        else:
                            # last chip merge router to next chip split router
                            router_task_path.append((dst_chip_idx, src_chip_idy + 1 + x, -4, -1))
                            router_task_path.append((dst_chip_idx, src_chip_idy + 1 + x, -2, 0))

                # intra chip
                chip_in_dir = router_task_path[-1][-2]

                # right in
                if chip_in_dir == -3:

                    pathx = dst_idx - (src_chip.core_numx - 1)
                    # First X then Y
                    if pathx < 0:
                        for x in range(np.abs(pathx)):
                            router_task_path.append((dst_chip_idx, dst_chip_idy, src_chip.core_numx - x - 1, dst_idy))
                    else:
                        pass

                # left in
                elif chip_in_dir == -1:
                    pathx = dst_idx
                    if pathx > 0:
                        for x in range(np.abs(pathx)):
                            router_task_path.append((dst_chip_idx, dst_chip_idy, x, dst_idy))
                    else:
                        pass

                # bottom in
                elif chip_in_dir == -2:

                    pathy = dst_idy - (src_chip.core_numy - 1)
                    # First X then Y

                    if pathy < 0:
                        for y in range(np.abs(pathy)):
                            router_task_path.append((dst_chip_idx, dst_chip_idy, dst_idx, src_chip.core_numy - y - 1))
                    else:
                        pass
                # top in
                elif chip_in_dir == -4:

                    pathy = dst_idy
                    # First X then Y

                    if pathy > 0:
                        for y in range(np.abs(pathy)):
                            router_task_path.append((dst_chip_idx, dst_chip_idy, dst_idx, y))
                    else:
                        pass

                router_task_path.append((dst_chip_idx, dst_chip_idy, dst_idx, dst_idy))



            assert self.path_validate(router_task_path)

            # First X then Y

            router_tasks_paths.append(router_task_path)


        #for path in router_tasks_paths:
        #    for core in path:
        #        print(core)


        self.router_tasks_paths = router_tasks_paths
        logging.info(self.router_tasks_paths)

        router_tasks_paths_with_dir = []
        for router_task in self.router_tasks_paths:
            router_task_path_with_dir = []
            router_task_path_with_dir.append((router_task[0][0],router_task[0][1],router_task[0][2],router_task[0][3],0))
            for i in range(len(router_task)-1):
                cur_core_id = router_task[i]
                next_core_id = router_task[i + 1]

                cur_core_idx = cur_core_id[2]
                cur_core_idy = cur_core_id[3]
                next_core_idx = next_core_id[2]
                next_core_idy = next_core_id[3]

                if  cur_core_idy == next_core_idy and next_core_idx - cur_core_idx == 1:
                    next_core_out_dir = -3
                elif cur_core_idy == next_core_idy and next_core_idx - cur_core_idx  == -1:
                    next_core_out_dir = -1
                elif cur_core_idx == next_core_idx and next_core_idy - cur_core_idy == 1:
                    next_core_out_dir = -2
                elif next_core_idx == next_core_idx and next_core_idy - cur_core_idy == -1:
                    next_core_out_dir = -4
                else:
                    print('output channel wrong')
                router_task_path_with_dir.append(
                    (cur_core_id[0], cur_core_id[1], cur_core_id[2], cur_core_id[3], next_core_out_dir))

            cur_core_id = router_task[-1]
            router_task_path_with_dir.append((cur_core_id[0], cur_core_id[1], cur_core_id[2], cur_core_id[3], -5))
            router_tasks_paths_with_dir.append(router_task_path_with_dir)

        print(router_tasks_paths_with_dir)
        for idx,router_task_path_with_dir in enumerate(router_tasks_paths_with_dir):
            logging.info(router_task_path_with_dir)

        self.router_tasks_paths_with_dir = router_tasks_paths_with_dir



        plot_fig = True
        if plot_fig:
            import matplotlib.pyplot as plt
            from matplotlib.pyplot import MultipleLocator

            plt.figure(figsize=(12,8))
            #fig,ax = plt.subplots(1,1)  # 获取到当前坐标轴信息
            ax=plt.gca()
            ax.xaxis.set_ticks_position('top')  # 将X坐标轴移到上面
            ax.invert_yaxis()
            plt.xlim(-1,16)
            plt.ylim(-1,10)
            plt.xticks(range(-1,16,1))
            plt.yticks(range(-1,10,1))
            plt.grid()
            from itertools import cycle
            cycol = cycle('bgrcmky')

            for tast_id, router_path in enumerate(self.router_tasks_paths):
                color = next(cycol)
                for index,core_id in enumerate(router_path):
                    core_x = core_id[2]
                    core_y = core_id[3]
                    plt.scatter(core_x,core_y,c=color)
                    if index < (len(router_path) - 1):
                       plt.plot([router_path[index][2], router_path[index+1][2]],
                             [router_path[index][3], router_path[index+1][3]],c=color)
                       # print([router_path[index][2], router_path[index+1][2]],
                       #       [router_path[index][3], router_path[index+1][3]])
                    if index==0:
                        #plt.text(core_x-0.8,core_y+0.2,'S'+str(tast_id+1),c=color)
                        plt.text(core_x - 0.5, core_y + 0.2, 'S' + str(tast_id + 1), c=color)
                    elif index==len(router_path)-1:
                        #plt.text(core_x-0.8,core_y+0.2,'D'+str(tast_id+1),c=color)
                        plt.text(core_x - 0.5, core_y + 0.2, 'D' + str(tast_id + 1), c=color)

            plt.savefig('./router_path.pdf')
        #return router_tasks_paths
        return router_tasks_paths_with_dir


    def init_src_cores(self, router_tasks):
        for task_id, router_task in enumerate(router_tasks):
            chip_idx = router_task.src_chip_id[0]
            chip_idy = router_task.src_chip_id[1]

            src_idx = router_task.src_id[0]
            src_idy = router_task.src_id[1]

            src_chip = self.get_chip_from_id(chip_idx, chip_idy)
            src_chip.is_used = 1
            src_core = src_chip.get_core_from_id(src_idx, src_idy)
            src_core.is_final_src = task_id + 1
            src_core.is_used = 1


            for i in range(router_task.data_volume):
                src_core.data_sent_memory.put(data_info(src_chip_id=router_task.src_chip_id,
                                                         dst_chip_id=router_task.dst_chip_id,
                                                         final_src_core_id=router_task.src_id, \
                                                         final_dst_core_id=router_task.dst_id, current_data_volume=i+1,
                                                         final_data_volume=router_task.data_volume,
                                                         data_task_id=task_id + 1, \
                                                         core_path=self.router_tasks_paths_with_dir[task_id]))

            src_core.src_local_data_info = data_info(src_chip_id=router_task.src_chip_id,
                                                         dst_chip_id=router_task.dst_chip_id,
                                                         final_src_core_id=router_task.src_id, \
                                                         final_dst_core_id=router_task.dst_id, current_data_volume=1,
                                                         final_data_volume=router_task.data_volume,
                                                         data_task_id=task_id + 1, \
                                                         core_path=self.router_tasks_paths_with_dir[task_id])



    def init_dst_cores(self, router_tasks):
        for task_id, router_task in enumerate(router_tasks):
            chip_idx = router_task.dst_chip_id[0]
            chip_idy = router_task.dst_chip_id[1]

            dst_idx = router_task.dst_id[0]
            dst_idy = router_task.dst_id[1]

            dst_chip = self.get_chip_from_id(chip_idx, chip_idy)
            dst_chip.is_used = 1

            dst_core = dst_chip.get_core_from_id(dst_idx, dst_idy)
            dst_core.is_final_dst = task_id + 1
            dst_core.is_used = 1

            dst_core.dst_local_data_info = data_info(src_chip_id=router_task.src_chip_id,
                                                     dst_chip_id=router_task.dst_chip_id,
                                                     final_src_core_id=router_task.src_id, \
                                                     final_dst_core_id=router_task.dst_id, current_data_volume=0,
                                                     final_data_volume=router_task.data_volume,
                                                     data_task_id=task_id + 1, \
                                                     core_path=self.router_tasks_paths_with_dir[task_id])

    def init_task_state(self, router_tasks):
        task_num = len(router_tasks)
        self.finished_tasks = np.zeros(task_num, dtype=np.int8)

    def path_validate(self,router_path):
        for id1 in range(len(router_path)):
            for id2 in range(len(router_path)):
                if id1!=id2 and router_path[id1] == router_path[id2]:
                    return False
        return True

    def core_send_request_with_dir(self,cur_core_id_with_dir,next_core,next_core_dir,task_id):

        if next_core_dir == -1:
            next_core.left_channel_get_request = 1
            next_core.left_request_task.append(task_id + 1)
            next_core.left_get_request_core_id.append(cur_core_id_with_dir)
        elif next_core_dir == -3:
            next_core.right_channel_get_request = 1
            next_core.right_request_task.append(task_id + 1)
            next_core.right_get_request_core_id.append(cur_core_id_with_dir)
        elif next_core_dir == -2:
            next_core.bottom_channel_get_request = 1
            next_core.bottom_request_task.append(task_id + 1)
            next_core.bottom_get_request_core_id.append(cur_core_id_with_dir)
        elif next_core_dir == -4:
            next_core.top_channel_get_request = 1
            next_core.top_request_task.append(task_id + 1)
            next_core.top_get_request_core_id.append(cur_core_id_with_dir)
        elif next_core_dir == -5:
            next_core.local_channel_get_request = 1
            next_core.local_request_task.append(task_id + 1)
            next_core.local_get_request_core_id.append(cur_core_id_with_dir)
        else:
            raise ValueError('core direction went wrong!')

    def core_send_request(self):

        core_to_core_edge = []
        assert self.router_tasks_paths_with_dir is not None
        for task_id, router_task_path in enumerate(self.router_tasks_paths_with_dir):
            for idx in range(len(router_task_path)-1):

                cur_chip_idx = router_task_path[idx][0]
                cur_chip_idy = router_task_path[idx][1]
                cur_core_idx = router_task_path[idx][2]
                cur_core_idy = router_task_path[idx][3]
                cur_core_dir = router_task_path[idx][4]

                # final src core
                cur_chip = self.get_chip_from_id(cur_chip_idx,cur_chip_idy)
                cur_core = cur_chip.get_core_from_id(cur_core_idx,cur_core_idy)

                #left_pack_data_info
                #src_core
                if cur_core_dir == 0:
                   if not cur_core.data_sent_memory.empty():
                       task_core_path = cur_core.src_local_data_info.core_path

                       cur_core_path_index = task_core_path.index((cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy, cur_core_dir))

                       next_chip_idx = task_core_path[cur_core_path_index + 1][0]
                       next_chip_idy = task_core_path[cur_core_path_index + 1][1]
                       next_core_idx = task_core_path[cur_core_path_index + 1][2]
                       next_core_idy = task_core_path[cur_core_path_index + 1][3]
                       next_core_dir = task_core_path[cur_core_path_index + 1][4]

                       next_chip = self.get_chip_from_id(next_chip_idx, next_chip_idy)
                       next_core = next_chip.get_core_from_id(next_core_idx, next_core_idy)
                       self.core_send_request_with_dir(router_task_path[idx], next_core, next_core_dir, task_id)
                       core_to_core_edge.append([(cur_chip_idx,cur_chip_idy,cur_core_idx,cur_core_idy,cur_core_dir),\
                                                 (next_chip_idx,next_chip_idy,next_core_idx,next_core_idy,next_core_dir)])

                elif cur_core_dir == -1:
                    if cur_core.left_for_sent_pack_data_info.current_data_volume is not None:
                        if (task_id + 1 != cur_core.left_for_sent_pack_data_info.data_task_id):
                            pass
                        else:
                            task_core_path = cur_core.left_for_sent_pack_data_info.core_path
                            cur_core_path_index = task_core_path.index((cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy,cur_core_dir))

                            next_chip_idx = task_core_path[cur_core_path_index + 1][0]
                            next_chip_idy = task_core_path[cur_core_path_index + 1][1]
                            next_core_idx = task_core_path[cur_core_path_index + 1][2]
                            next_core_idy = task_core_path[cur_core_path_index + 1][3]
                            next_core_dir = task_core_path[cur_core_path_index + 1][4]

                            next_chip = self.get_chip_from_id(next_chip_idx, next_chip_idy)
                            next_core = next_chip.get_core_from_id(next_core_idx, next_core_idy)

                            self.core_send_request_with_dir(router_task_path[idx], next_core, next_core_dir, task_id)
                            core_to_core_edge.append([(cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy, cur_core_dir), \
                                 (next_chip_idx, next_chip_idy, next_core_idx, next_core_idy, next_core_dir)])

                elif cur_core_dir == -3:
                    if cur_core.right_for_sent_pack_data_info.current_data_volume is not None:
                        if (task_id + 1 != cur_core.right_for_sent_pack_data_info.data_task_id):
                            pass
                        else:
                            task_core_path = cur_core.right_for_sent_pack_data_info.core_path
                            cur_core_path_index = task_core_path.index((cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy,cur_core_dir))

                            next_chip_idx = task_core_path[cur_core_path_index + 1][0]
                            next_chip_idy = task_core_path[cur_core_path_index + 1][1]
                            next_core_idx = task_core_path[cur_core_path_index + 1][2]
                            next_core_idy = task_core_path[cur_core_path_index + 1][3]
                            next_core_dir = task_core_path[cur_core_path_index + 1][4]

                            next_chip = self.get_chip_from_id(next_chip_idx, next_chip_idy)
                            next_core = next_chip.get_core_from_id(next_core_idx, next_core_idy)

                            self.core_send_request_with_dir(router_task_path[idx], next_core, next_core_dir, task_id)
                            core_to_core_edge.append(
                                [(cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy, cur_core_dir), \
                                 (next_chip_idx, next_chip_idy, next_core_idx, next_core_idy, next_core_dir)])

                elif cur_core_dir == -2:
                    if cur_core.bottom_for_sent_pack_data_info.current_data_volume is not None:
                        if (task_id + 1 != cur_core.bottom_for_sent_pack_data_info.data_task_id):
                            pass
                        else:
                            task_core_path = cur_core.bottom_for_sent_pack_data_info.core_path
                            cur_core_path_index = task_core_path.index((cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy,cur_core_dir))

                            next_chip_idx = task_core_path[cur_core_path_index + 1][0]
                            next_chip_idy = task_core_path[cur_core_path_index + 1][1]
                            next_core_idx = task_core_path[cur_core_path_index + 1][2]
                            next_core_idy = task_core_path[cur_core_path_index + 1][3]
                            next_core_dir = task_core_path[cur_core_path_index + 1][4]

                            next_chip = self.get_chip_from_id(next_chip_idx, next_chip_idy)
                            next_core = next_chip.get_core_from_id(next_core_idx, next_core_idy)

                            self.core_send_request_with_dir(router_task_path[idx], next_core, next_core_dir, task_id)
                            core_to_core_edge.append(
                                [(cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy, cur_core_dir), \
                                 (next_chip_idx, next_chip_idy, next_core_idx, next_core_idy, next_core_dir)])

                elif cur_core_dir == -4:
                    if cur_core.top_for_sent_pack_data_info.current_data_volume is not None:
                        if (task_id + 1 != cur_core.top_for_sent_pack_data_info.data_task_id):
                            pass
                        else:
                            task_core_path = cur_core.top_for_sent_pack_data_info.core_path
                            cur_core_path_index = task_core_path.index((cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy,cur_core_dir))

                            next_chip_idx = task_core_path[cur_core_path_index + 1][0]
                            next_chip_idy = task_core_path[cur_core_path_index + 1][1]
                            next_core_idx = task_core_path[cur_core_path_index + 1][2]
                            next_core_idy = task_core_path[cur_core_path_index + 1][3]
                            next_core_dir = task_core_path[cur_core_path_index + 1][4]

                            next_chip = self.get_chip_from_id(next_chip_idx, next_chip_idy)
                            next_core = next_chip.get_core_from_id(next_core_idx, next_core_idy)

                            self.core_send_request_with_dir(router_task_path[idx], next_core, next_core_dir, task_id)
                            core_to_core_edge.append(
                                [(cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy, cur_core_dir), \
                                 (next_chip_idx, next_chip_idy, next_core_idx, next_core_idy, next_core_dir)])

        #logging.info(core_to_core_edge)
        self.merge_tasks, self.dynamic_graphs = gen_graph_from_path(core_to_core_edge)

    def core_process_request(self):

        self.all_used_cores =[]
        for graph in self.dynamic_graphs:
            path_used_nodes = []
            last_node_in_graph = get_last_node_in_graph(graph)
            cur_node = last_node_in_graph[0]
            path_used_nodes.append(cur_node)
            get_final_src = 1
            while(get_final_src and cur_node!=[]):
                cur_chip_idx = cur_node[0]
                cur_chip_idy = cur_node[1]
                cur_core_idx = cur_node[2]
                cur_core_idy = cur_node[3]
                cur_core_dir = cur_node[4]

                cur_chip = self.get_chip_from_id(cur_chip_idx, cur_chip_idy)
                cur_core = cur_chip.get_core_from_id(cur_core_idx, cur_core_idy)

                if cur_core_dir == -1:
                    process_request_signal = cur_core.left_channel_get_request
                    process_request_task_id = cur_core.left_request_task
                    process_request_core_id = cur_core.left_get_request_core_id
                elif cur_core_dir == -3:
                    process_request_signal = cur_core.right_channel_get_request
                    process_request_task_id = cur_core.right_request_task
                    process_request_core_id = cur_core.right_get_request_core_id
                elif cur_core_dir == -2:
                    process_request_signal = cur_core.bottom_channel_get_request
                    process_request_task_id = cur_core.bottom_request_task
                    process_request_core_id = cur_core.bottom_get_request_core_id
                elif cur_core_dir == -4:
                    process_request_signal = cur_core.top_channel_get_request
                    process_request_task_id = cur_core.top_request_task
                    process_request_core_id = cur_core.top_get_request_core_id
                elif cur_core_dir == -5:
                    process_request_signal = cur_core.local_channel_get_request
                    process_request_task_id = cur_core.local_request_task
                    process_request_core_id = cur_core.local_get_request_core_id
                else:
                    get_final_src = 0
                    #raise ValueError('processing request went wrong')

                if get_final_src:
                    if cur_core_idx == 0:
                        west_core_id = (cur_chip_idx, cur_chip_idy, -1, -1)
                    else:
                        west_core_id = (cur_chip_idx, cur_chip_idy, cur_core_idx - 1, cur_core_idy, -3)

                    # right
                    if cur_core_idx == cur_chip.core_numx - 1:
                        east_core_id = (cur_chip_idx, cur_chip_idy, -3, -1)
                    else:
                        east_core_id = (cur_chip_idx, cur_chip_idy, cur_core_idx + 1, cur_core_idy, -1)

                    # top
                    if cur_core_idy == 0:
                        north_core_id = (cur_chip_idx, cur_chip_idy, -4, -1)
                    else:
                        north_core_id = (cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy - 1, -2)

                    # bottom
                    if cur_core_idy == cur_chip.core_numy - 1:
                        south_core_id = (cur_chip_idx, cur_chip_idy, -2, -1)
                    else:
                        south_core_id = (cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy + 1, -4)

                    local_core_id = (cur_chip_idx, cur_chip_idy, cur_core_idx, cur_core_idy, 0)

                    if west_core_id in process_request_core_id:
                        final_request_core_id = west_core_id
                    elif east_core_id in process_request_core_id:
                        final_request_core_id = east_core_id
                    elif north_core_id in process_request_core_id:
                        final_request_core_id = north_core_id
                    elif south_core_id in process_request_core_id:
                        final_request_core_id = south_core_id
                    elif local_core_id in process_request_core_id:
                        final_request_core_id = local_core_id
                    else:
                        break
                        #print('request_core:', process_request_core_id)
                        #raise ValueError("request core ileagal")



                    pre_node = get_pre_node_in_graph(graph, cur_node)
                    assert final_request_core_id in pre_node
                    cur_node = final_request_core_id
                    path_used_nodes.append(cur_node)
            self.all_used_cores.append(path_used_nodes)


    def core_to_core_send_data(self,cur_core,next_core,cur_core_id,next_core_id):
        cur_core_dir = cur_core_id[4]
        next_core_dir = next_core_id[4]
        if cur_core_dir == 0:
            pack_data_info = cur_core.data_sent_memory.get()
        elif cur_core_dir==-1:
            pack_data_info = cur_core.left_for_sent_pack_data_info.copy()
        elif cur_core_dir==-3:
            pack_data_info = cur_core.right_for_sent_pack_data_info.copy()
        elif cur_core_dir==-2:
            pack_data_info = cur_core.bottom_for_sent_pack_data_info.copy()
        elif cur_core_dir==-4:
            pack_data_info = cur_core.top_for_sent_pack_data_info.copy()
        else:
            raise ValueError('data sending went wrong')

        if next_core_dir==-1:
            next_core.left_have_rev_pack_data_info = pack_data_info
        elif next_core_dir==-3:
            next_core.right_have_rev_pack_data_info = pack_data_info
        elif next_core_dir==-2:
            next_core.bottom_have_rev_pack_data_info = pack_data_info
        elif next_core_dir==-4:
            next_core.top_have_rev_pack_data_info = pack_data_info
        elif next_core_dir==-5:
            next_core.data_rev_memory.put(pack_data_info)
        else:
            raise ValueError('data receiving went wrong')

        logging.info('core(%d,%d,%d,%d,%d) ---> core(%d,%d,%d,%d,%d) task %d cur_vol %d '%(cur_core_id[0],cur_core_id[1],cur_core_id[2],cur_core_id[3],cur_core_id[4],\
                                                                       next_core_id[0],next_core_id[1],next_core_id[2],next_core_id[3],next_core_id[4], \
                                                                                           pack_data_info.data_task_id,\
                                                                          pack_data_info.current_data_volume))

        print('core(%d,%d,%d,%d,%d) ---> core(%d,%d,%d,%d,%d) task %d cur_vol %d' % (cur_core_id[0], cur_core_id[1], cur_core_id[2], cur_core_id[3], cur_core_id[4], \
                                                               next_core_id[0], next_core_id[1], next_core_id[2], next_core_id[3], next_core_id[4], \
                                                                                     pack_data_info.data_task_id, \
                                                                                     pack_data_info.current_data_volume))



    def core_send_data(self):

        for graph_id,path_used_cores in enumerate(self.all_used_cores):
            print('<<<<<<<<<<<<<<<<<<<<<<%d>>>>>>>>>>>>>>>>>>>'%(graph_id+1))
            logging.info('<<<<<<<<<<<<<<<<<<<<<<%d>>>>>>>>>>>>>>>>>>>' % (graph_id + 1))
            for idx in range(len(path_used_cores) - 1, -1, -1):
                cur_core_id = path_used_cores[idx]
                cur_chip_idx = cur_core_id[0]
                cur_chip_idy = cur_core_id[1]
                cur_core_idx = cur_core_id[2]
                cur_core_idy = cur_core_id[3]
                cur_core_dir = cur_core_id[4]

                cur_chip = self.get_chip_from_id(cur_chip_idx, cur_chip_idy)
                cur_core = cur_chip.get_core_from_id(cur_core_idx, cur_core_idy)

                if cur_core_dir == -1:
                    if cur_core.left_for_sent_pack_data_info.current_data_volume is not None:
                        cur_core_index = cur_core.left_for_sent_pack_data_info.core_path.index(cur_core_id)
                        next_core_id = cur_core.left_for_sent_pack_data_info.core_path[cur_core_index + 1]

                        next_chip_idx = next_core_id[0]
                        next_chip_idy = next_core_id[1]
                        next_core_idx = next_core_id[2]
                        next_core_idy = next_core_id[3]
                        next_core_dir = next_core_id[4]

                        next_chip = self.get_chip_from_id(next_chip_idx, next_chip_idy)
                        next_core = next_chip.get_core_from_id(next_core_idx, next_core_idy)
                        self.core_to_core_send_data(cur_core, next_core, cur_core_id, next_core_id)

                elif cur_core_dir == -3:
                    if cur_core.right_for_sent_pack_data_info.current_data_volume is not None:
                        cur_core_index = cur_core.right_for_sent_pack_data_info.core_path.index(cur_core_id)
                        next_core_id = cur_core.right_for_sent_pack_data_info.core_path[cur_core_index + 1]

                        next_chip_idx = next_core_id[0]
                        next_chip_idy = next_core_id[1]
                        next_core_idx = next_core_id[2]
                        next_core_idy = next_core_id[3]
                        next_core_dir = next_core_id[4]

                        next_chip = self.get_chip_from_id(next_chip_idx, next_chip_idy)
                        next_core = next_chip.get_core_from_id(next_core_idx, next_core_idy)
                        self.core_to_core_send_data(cur_core, next_core, cur_core_id, next_core_id)

                elif cur_core_dir == -2:
                    if cur_core.bottom_for_sent_pack_data_info.current_data_volume is not None:
                        cur_core_index = cur_core.bottom_for_sent_pack_data_info.core_path.index(cur_core_id)
                        next_core_id = cur_core.bottom_for_sent_pack_data_info.core_path[cur_core_index + 1]

                        next_chip_idx = next_core_id[0]
                        next_chip_idy = next_core_id[1]
                        next_core_idx = next_core_id[2]
                        next_core_idy = next_core_id[3]
                        next_core_dir = next_core_id[4]

                        next_chip = self.get_chip_from_id(next_chip_idx, next_chip_idy)
                        next_core = next_chip.get_core_from_id(next_core_idx, next_core_idy)
                        self.core_to_core_send_data(cur_core, next_core, cur_core_id, next_core_id)

                elif cur_core_dir == -4:
                    if cur_core.top_for_sent_pack_data_info.current_data_volume is not None:
                        cur_core_index = cur_core.top_for_sent_pack_data_info.core_path.index(cur_core_id)
                        next_core_id = cur_core.top_for_sent_pack_data_info.core_path[cur_core_index + 1]

                        next_chip_idx = next_core_id[0]
                        next_chip_idy = next_core_id[1]
                        next_core_idx = next_core_id[2]
                        next_core_idy = next_core_id[3]
                        next_core_dir = next_core_id[4]

                        next_chip = self.get_chip_from_id(next_chip_idx, next_chip_idy)
                        next_core = next_chip.get_core_from_id(next_core_idx, next_core_idy)
                        self.core_to_core_send_data(cur_core, next_core, cur_core_id, next_core_id)

                elif cur_core_dir == 0:
                    if cur_core.src_local_data_info.current_data_volume is not None:
                        cur_core_index = cur_core.src_local_data_info.core_path.index(cur_core_id)
                        next_core_id = cur_core.src_local_data_info.core_path[cur_core_index + 1]

                        next_chip_idx = next_core_id[0]
                        next_chip_idy = next_core_id[1]
                        next_core_idx = next_core_id[2]
                        next_core_idy = next_core_id[3]
                        next_core_dir = next_core_id[4]

                        next_chip = self.get_chip_from_id(next_chip_idx, next_chip_idy)
                        next_core = next_chip.get_core_from_id(next_core_idx, next_core_idy)
                        self.core_to_core_send_data(cur_core, next_core, cur_core_id, next_core_id)



    def update_core_state(self):

        for task_id, router_task_path in enumerate(self.router_tasks_paths_with_dir):
            final_dst_core_id = router_task_path[-1]
            final_dst_chip = self.get_chip_from_id(final_dst_core_id[0], final_dst_core_id[1])
            final_dst_core = final_dst_chip.get_core_from_id(final_dst_core_id[2], final_dst_core_id[3])
            if not self.finished_tasks[task_id]:
                if final_dst_core.dst_local_data_info.final_data_volume == final_dst_core.data_rev_memory.qsize():
                   print('************core (%d,%d,%d,%d,%d) is final dst!!!*************' % (final_dst_core_id[0],final_dst_core_id[1],\
                                                                                             final_dst_core_id[2],final_dst_core_id[3],\
                                                                                             final_dst_core_id[4]))
                   logging.info('************core (%d,%d,%d,%d,%d) is clear!!!*************' %(final_dst_core_id[0],final_dst_core_id[1],\
                                                                                             final_dst_core_id[2],final_dst_core_id[3], \
                                                                                             final_dst_core_id[4]))
                   print('task %d is finished!!!'%(task_id+1))
                   logging.info('task %d is finished!!!'%(task_id+1))
                   self.finished_tasks[task_id] = 1

        for path_used_cores in self.all_used_cores:
            for core_id in path_used_cores:
                cur_chip_idx = core_id[0]
                cur_chip_idy = core_id[1]
                cur_core_idx = core_id[2]
                cur_core_idy = core_id[3]
                cur_core_dir = core_id[4]

                cur_chip = self.get_chip_from_id(cur_chip_idx, cur_chip_idy)
                cur_core = cur_chip.get_core_from_id(cur_core_idx, cur_core_idy)

                cur_core.clear_requset_state()
                cur_core.clear_response_state()

                if cur_core_dir == -1:
                    cur_core.left_exchange_sent_rev()
                elif cur_core_dir == -3:
                    cur_core.right_exchange_sent_rev()
                elif cur_core_dir == -2:
                    cur_core.bottom_exchange_sent_rev()
                elif cur_core_dir == -4:
                    cur_core.top_exchange_sent_rev()


def router_task_not_done(multi_chip_system, router_tasks):
    if multi_chip_system.finished_tasks.sum() > 0 and (multi_chip_system.finished_tasks.sum() == len(router_tasks)):
       return False
    else:
       return True

def multi_chip_test(multi_chip_system, router_tasks):
    multi_chip_system.get_router_tasks_path(router_tasks)
    multi_chip_system.init_src_cores(router_tasks)
    multi_chip_system.init_dst_cores(router_tasks)
    multi_chip_system.init_task_state(router_tasks)
    group_clock_sum = 0
    while (router_task_not_done(multi_chip_system, router_tasks)):
        if group_clock_sum == 4:
            print('pause')
        print('<<<<<<<<<<<<<<<<<<<<<clock %d>>>>>>>>>>>>>>>>>>>>>>>>>'%(group_clock_sum))
        logging.info('<<<<<<<<<<<<<<<<<<<<<clock %d>>>>>>>>>>>>>>>>>>>>>>>>>'%(group_clock_sum))
        multi_chip_system.core_send_request()
        multi_chip_system.core_process_request()
        multi_chip_system.core_send_data()
        multi_chip_system.update_core_state()
        group_clock_sum = group_clock_sum + 1

    print('data sent over!!!')
    logging.info('data sent over!!!')
    return group_clock_sum

# test_chip_system = chip_system(5, 5)
# router_tasks = [router_task((0,0),(0,0),(0,0),(3,3),4)]
# multi_chip_test(test_chip_system,router_tasks)

# test_chip_system = chip_system(5, 5)
# router_tasks = [router_task((0,0),(0,0),(12,5),(5,3),10),router_task((0,0),(0,0),(3,2),(5,8),6)]
# multi_chip_test(test_chip_system,router_tasks)


# INFO:root:task  1:(0,0,11,5)---->(0,0,4,4)  data volume: 1
# INFO:root:task  2:(0,0,3,7)---->(0,0,11,0)  data volume: 13
# INFO:root:task  3:(0,0,11,8)---->(0,0,11,4)  data volume: 3

#bug exchange one core two times
# test_chip_system = chip_system(5, 5)
# #router_tasks = [router_task((0,0),(0,0),(11,5),(4,4),1),router_task((0,0),(0,0),(3,7),(11,0),13),router_task((0,0),(0,0),(11,8),(11,4),3)]
# router_tasks = [router_task((0,0),(0,0),(3,7),(11,0),13),router_task((0,0),(0,0),(11,8),(11,4),10)]
# #router_tasks = [router_task((0,0),(0,0),(11,8),(11,4),3)]
# multi_chip_test(test_chip_system,router_tasks)



# INFO:root:task  1:(0,0,1,2)---->(0,0,13,8)  data volume: 3
# INFO:root:task  2:(0,0,1,1)---->(0,0,3,5)  data volume: 16
# INFO:root:task  3:(0,0,13,9)---->(0,0,0,9)  data volume: 1
# INFO:root:task  4:(0,0,9,9)---->(0,0,7,3)  data volume: 17
# INFO:root:task  5:(0,0,0,1)---->(0,0,2,5)  data volume: 13
# INFO:root:task  6:(0,0,1,9)---->(0,0,5,5)  data volume: 10


# task 1 2 5
# test_chip_system = chip_system(5, 5)
# #router_tasks = [router_task((0,0),(0,0),(11,5),(4,4),1),router_task((0,0),(0,0),(3,7),(11,0),13),router_task((0,0),(0,0),(11,8),(11,4),3)]
# router_tasks = [router_task((0,0),(0,0),(1,2),(13,8),3),router_task((0,0),(0,0),(1,1),(3,5),16),router_task((0,0),(0,0),(0,1),(2,5),13)]
# #router_tasks = [router_task((0,0),(0,0),(11,8),(11,4),3)]
# multi_chip_test(test_chip_system,router_tasks)


#task 3 4 6
# test_chip_system = chip_system(5, 5)
# #router_tasks = [router_task((0,0),(0,0),(13,9),(0,9),1),router_task((0,0),(0,0),(9,9),(7,3),17),router_task((0,0),(0,0),(1,9),(5,5),10)]
# router_tasks = [router_task((0,0),(0,0),(13,9),(0,9),1),router_task((0,0),(0,0),(9,9),(7,3),17)]
# #router_tasks = [router_task((0,0),(0,0),(13,9),(0,9),1),router_task((0,0),(0,0),(1,9),(5,5),10)]
# multi_chip_test(test_chip_system,router_tasks)


# INFO:root:task  1:(0,0,5,7)---->(0,0,14,5)  data volume: 8
# INFO:root:task  2:(0,0,10,7)---->(0,0,15,1)  data volume: 9
# INFO:root:task  3:(0,0,9,4)---->(0,0,3,3)  data volume: 9
# INFO:root:task  4:(0,0,3,8)---->(0,0,10,8)  data volume: 1
# INFO:root:task  5:(0,0,6,5)---->(0,0,15,3)  data volume: 1
# INFO:root:task  6:(0,0,1,1)---->(0,0,2,8)  data volume: 15




# INFO:root:task  1:(0,0,2,5)---->(0,0,9,1)  data volume: 8
# INFO:root:task  2:(0,0,8,9)---->(0,0,9,4)  data volume: 13
# INFO:root:task  3:(0,0,4,2)---->(0,0,14,0)  data volume: 2
# INFO:root:task  4:(0,0,5,9)---->(0,0,10,9)  data volume: 16
# INFO:root:task  5:(0,0,12,3)---->(0,0,3,4)  data volume: 6



# INFO:root:task  3:(0,0,4,0)---->(0,0,13,8)  data volume: 17
# INFO:root:task  5:(0,0,5,1)---->(0,0,12,6)  data volume: 13
# INFO:root:task  6:(0,0,13,7)---->(0,0,12,1)  data volume: 19
# INFO:root:task  7:(0,0,6,0)---->(0,0,15,7)  data volume: 13
# INFO:root:task  8:(0,0,3,0)---->(0,0,10,1)  data volume: 18


# test_chip_system = chip_system(5, 5)
# router_tasks = [router_task((0,0),(0,0),(4,0),(13,8),7),\
#                 router_task((0,0),(0,0),(6,0),(15,7),3),\
#                 router_task((0,0),(0,0),(3,0),(10,1),8)]
# #router_tasks = [router_task((0,0),(0,0),(3,0),(3,3),8)]
# multi_chip_test(test_chip_system,router_tasks)


#bug case 7
# INFO:root:task  1:(0,0,8,6)---->(0,0,2,8)  data volume: 10
# INFO:root:task  2:(0,0,12,9)---->(0,0,5,6)  data volume: 10
# INFO:root:task  3:(0,0,2,5)---->(0,0,11,8)  data volume: 29
# INFO:root:task  4:(0,0,14,7)---->(0,0,1,2)  data volume: 18
# INFO:root:task  5:(0,0,11,6)---->(0,0,6,2)  data volume: 47
# INFO:root:task  6:(0,0,7,2)---->(0,0,6,6)  data volume: 46
# INFO:root:task  7:(0,0,11,3)---->(0,0,0,9)  data volume: 49
# INFO:root:task  8:(0,0,9,5)---->(0,0,6,3)  data volume: 27
# INFO:root:task  9:(0,0,10,2)---->(0,0,9,3)  data volume: 10
# INFO:root:task  10:(0,0,0,7)---->(0,0,13,1)  data volume: 46
# INFO:root:task  11:(0,0,4,7)---->(0,0,6,4)  data volume: 25
# INFO:root:task  12:(0,0,11,9)---->(0,0,3,0)  data volume: 38
# INFO:root:task  13:(0,0,9,6)---->(0,0,0,5)  data volume: 42
# INFO:root:task  14:(0,0,2,7)---->(0,0,7,7)  data volume: 45
# INFO:root:task  15:(0,0,2,1)---->(0,0,13,8)  data volume: 22
# INFO:root:task  16:(0,0,5,2)---->(0,0,4,9)  data volume: 39
# INFO:root:task  17:(0,0,10,7)---->(0,0,4,5)  data volume: 23
# INFO:root:task  18:(0,0,15,2)---->(0,0,7,6)  data volume: 18
# INFO:root:task  19:(0,0,9,7)---->(0,0,3,5)  data volume: 20
# INFO:root:task  20:(0,0,12,2)---->(0,0,4,6)  data volume: 45


if __name__ == "__main__":
    test_chip_system = chip_system(5, 5)
    router_tasks = [
                router_task((0,0),(0,0),(9,5),(6,3),7),\
                router_task((0,0),(0,0),(0,7),(13,1),6),\
                router_task((0,0),(0,0),(4,7),(6,4),5)
                ]
    #router_tasks = [router_task((0,0),(0,0),(3,0),(3,3),8)]
    multi_chip_test(test_chip_system,router_tasks)



















































