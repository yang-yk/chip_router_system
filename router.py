'''
written by Yukuan Yang
2021.05.29from queue import Queue
'''
from queue import Queue
class merge_router(object):
    def __init__(self,chip_id, core_coordinate, memory_size = 2, is_used = 0):
        '''
        :param chip_id: merge router??????
        :param core_coordinate: merge router????
        :param memory_size: router fifo??
        :param is_used: ?????
        '''
        self.chip_id = chip_id
        self.core_coordinate = core_coordinate
        self.chip_idx = chip_id[0]
        self.chip_idy = chip_id[1]
        self.core_idx = core_coordinate[0]
        self.core_idy = core_coordinate[1]

        self.memory_size = memory_size

        self.is_used = is_used

        self.type = 'merge_router'

        self.pack_data_info = Queue(maxsize = memory_size)

        self.get_request = 0
        self.rev_multi_request = 0
        self.get_request_task = []
        self.get_request_core_id = []

        self.rev_response = 0

    #same chip
    def request_sort(self):
        '''
        :return: ??????????????????get_request_core_id?????????get_request_task
        '''
        if len(self.get_request_core_id) <=1:
            pass
        else:
            core_id_sum_list = []
            for core_id in self.get_request_core_id:
                core_id_sum = core_id[0]+core_id[1]
                core_id_sum_list.append(core_id_sum)
            import numpy as np
            core_id_sum_array = np.array(core_id_sum_list)
            sort_id = core_id_sum_array.argsort()
            self.get_request_task = list(np.array(self.get_request_task)[sort_id])
            self.get_request_core_id = list(np.array(self.get_request_core_id)[sort_id])


    def get_first_level_request_core(self):
        '''
        :return: ???????????????
        '''
        if len(self.get_request_core_id) <=1:
            return self.get_request_core_id[0]
        else:
            core_id_sum_list=[]
            for core_id in self.get_request_core_id:
                chip_idx = core_id[0]
                chip_idy = core_id[1]
                core_idx = core_id[2]
                core_idy = core_id[3]
                if (chip_idx,chip_idy,-1,-1) in self.get_request_core_id:
                    return (chip_idx,chip_idy,-1,-1)
                elif (chip_idx,chip_idy,-3,-1) in self.get_request_core_id:
                    return (chip_idx, chip_idy, -3, -1)
                elif (chip_idx,chip_idy,-4,-1) in self.get_request_core_id:
                    return (chip_idx, chip_idy, -4, -1)
                elif (chip_idx,chip_idy,-2,-1) in self.get_request_core_id:
                    return (chip_idx, chip_idy, -2, -1)
                else:
                    core_id_sum = core_id[2] + core_id[3]
                    core_id_sum_list.append(core_id_sum)
                import numpy as np
                core_id_sum_array = np.array(core_id_sum_list)
                sort_id = core_id_sum_array.argsort()
                self.get_request_task_sorted = list(np.array(self.get_request_task)[sort_id])
                self.get_request_core_id_sorted = list(np.array(self.get_request_core_id)[sort_id])
                return self.get_request_core_id_sorted[0]

    def clear_requset_state(self):
        self.get_request = 0
        self.rev_multi_request = 0
        self.get_request_task = []
        self.get_request_core_id = []

    def clear_response_state(self):
        self.rev_response = 0


class split_router(object):
    def __init__(self,chip_id, core_coordinate, memory_size = 2, is_used = 0):
        '''
        :param chip_id: merge router??????
        :param core_coordinate: merge router????
        :param memory_size: router fifo??
        :param is_used: ?????
        '''
        self.chip_id = chip_id
        self.core_coordinate = core_coordinate
        self.chip_idx = chip_id[0]
        self.chip_idy = chip_id[1]
        self.core_idx = core_coordinate[0]
        self.core_idy = core_coordinate[1]

        self.memory_size = memory_size

        self.type = 'split_router'

        self.is_used = is_used

        self.pack_data_info = Queue(maxsize = memory_size)

        self.get_request = 0
        self.rev_multi_request = 0
        self.get_request_task = []
        self.get_request_core_id = []

        self.rev_response = 0


    def clear_requset_state(self):

        self.get_request = 0
        self.rev_multi_request = 0
        self.get_request_task = []
        self.get_request_core_id = []


    def clear_response_state(self):
        self.rev_response = 0
