'''
written by Yukuan Yang
2021.05.29
'''

class router_task(object):

    def __init__(self, src_chip_id=None, dst_chip_id=None, src_id=None, dst_id=None, data_volume=None, cur_volume=0):
        '''
        ???????
        :param src_chip_id: ??????
        :param dst_chip_id: ??????
        :param src_id: ?????
        :param dst_id: ?????
        :param data_volume: ?????? ???None
        :param cur_volume: ?????? ???0 ????
        '''
        self.src_chip_id = src_chip_id
        self.dst_chip_id = dst_chip_id

        self.src_id = src_id
        self.dst_id = dst_id
        self.data_volume = data_volume
        self.cur_volume = cur_volume


    def clear(self):
        self.src_chip_id = None
        self.dst_chip_id = None
        self.src_id = None
        self.dst_id = None
        self.data_volume = 0
        self.cur_volume = 0

    def copy(self):
        return router_task(src_chip_id=self.src_chip_id, dst_chip_id=self.dst_chip_id, src_id=self.src_id, dst_id=self.dst_id, data_volume=self.data_volume, cur_volume=self.cur_volume)

    def print(self):
        print(self.src_chip_id, self.dst_chip_id, self.src_id, self.dst_id, self.data_volume)


class data_info(object):

    def __init__(self,src_chip_id=None, dst_chip_id=None, final_src_core_id = None, \
                 final_dst_core_id = None, current_data_volume = None, final_data_volume = None,data_task_id = 0,\
                 core_path=None):
        '''
        :param src_chip_id: ??????
        :param dst_chip_id: ??????
        :param final_src_core_id: ?????
        :param final_dst_core_id: ?????
        :param current_data_volume: ??????? ???None
        :param final_data_volume: ???????
        :param data_task_id: ????id ???0 ?1????
        :param core_path: ??????????? ???None
        '''

        self.src_chip_id = src_chip_id
        self.dst_chip_id = dst_chip_id
        self.final_src_core_id = final_src_core_id
        self.final_dst_core_id = final_dst_core_id
        self.current_data_volume = current_data_volume
        self.final_data_volume = final_data_volume
        self.data_task_id = data_task_id
        self.core_path = core_path


    def clear(self):

        self.src_chip_id = None
        self.dst_chip_id = None
        self.final_src_core_id = None
        self.final_dst_core_id = None
        self.current_data_volume = None
        self.final_data_volume = 0
        self.data_task_id = 0
        self.core_path = None

    def print(self):
        print(self.src_chip_id,self.dst_chip_id,self.final_src_core_id,self.final_dst_core_id,self.current_data_volume,self.final_data_volume)


    def copy(self):
        return data_info(src_chip_id=self.src_chip_id,dst_chip_id=self.dst_chip_id,\
                         final_src_core_id=self.final_src_core_id,final_dst_core_id=self.final_dst_core_id,\
                         current_data_volume=self.current_data_volume,final_data_volume=self.final_data_volume,\
                         data_task_id=self.data_task_id,core_path=self.core_path)









