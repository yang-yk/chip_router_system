'''
written by Yukuan Yang
2021.05.29
'''

from data_task import data_info
from queue import Queue
class physical_core(object):
    def __init__(self,chip_id, core_coordinate, is_used = 0):
        '''
        :param chip_id: ????????
        :param core_coordinate: ???
        :param is_used: ????? ????0
        :param is_final_src = 0 ?????? ????????????????id
        :param is_final_dst = 0 ?????? ????????????????id
        '''

        self.chip_id = chip_id
        self.core_coordinate = core_coordinate
        self.chip_idx = chip_id[0]
        self.chip_idy = chip_id[1]
        self.core_idx = core_coordinate[0]
        self.core_idy = core_coordinate[1]

        self.is_used = is_used

        self.data_sent_memory = Queue()
        self.data_rev_memory = Queue()

        self.left_for_sent_pack_data_info = data_info()
        self.left_have_rev_pack_data_info = data_info()

        self.right_for_sent_pack_data_info = data_info()
        self.right_have_rev_pack_data_info = data_info()

        self.top_for_sent_pack_data_info = data_info()
        self.top_have_rev_pack_data_info = data_info()

        self.bottom_for_sent_pack_data_info = data_info()
        self.bottom_have_rev_pack_data_info = data_info()

        self.local_for_sent_pack_data_info = data_info()
        self.local_have_rev_pack_data_info = data_info()

        self.left_channel_get_request = 0
        self.left_request_task = []
        self.left_get_request_core_id = []

        self.right_channel_get_request = 0
        self.right_request_task = []
        self.right_get_request_core_id = []

        self.top_channel_get_request = 0
        self.top_request_task = []
        self.top_get_request_core_id = []

        self.bottom_channel_get_request = 0
        self.bottom_request_task = []
        self.bottom_get_request_core_id = []

        self.local_channel_get_request = 0
        self.local_request_task = []
        self.local_get_request_core_id = []

        self.is_final_src = 0
        self.is_final_dst = 0

        self.final_src_dir = 0

        self.left_rev_response = 0
        self.right_rev_response = 0
        self.bottom_rev_response = 0
        self.top_rev_response = 0
        self.local_rev_response = 0

        self.type = 'core'

    def get_core_id(self):
        return self.core_coordinate[0],self.core_coordinate[1]

    def get_chip_id(self):
        return self.chip_id[0],self.chip_id[1]


    def clear(self):

        self.is_used = 0

        self.data_sent_memory = Queue()
        self.date_rev_memory = Queue()

        self.left_for_sent_pack_data_info = data_info()
        self.left_have_rev_pack_data_info = data_info()

        self.right_for_sent_pack_data_info = data_info()
        self.right_have_rev_pack_data_info = data_info()

        self.top_for_sent_pack_data_info = data_info()
        self.top_have_rev_pack_data_info = data_info()

        self.bottom_for_sent_pack_data_info = data_info()
        self.bottom_have_rev_pack_data_info = data_info()

        self.local_for_sent_pack_data_info = data_info()
        self.local_have_rev_pack_data_info = data_info()



        self.is_final_src = 0
        self.is_final_dst = 0
        self.final_src_dir = 0

        self.left_channel_get_request = 0
        self.left_request_task = []
        self.left_get_request_core_id = []

        self.right_channel_get_request = 0
        self.right_request_task = []
        self.right_get_request_core_id = []

        self.top_channel_get_request = 0
        self.top_request_task = []
        self.top_get_request_core_id = []

        self.bottom_channel_get_request = 0
        self.bottom_request_task = []
        self.bottom_get_request_core_id = []

        self.local_channel_get_request = 0
        self.local_request_task = []
        self.local_get_request_core_id = []

        self.left_rev_response = 0
        self.right_rev_response = 0
        self.bottom_rev_response = 0
        self.top_rev_response = 0
        self.local_rev_response = 0


    def clear_requset_state(self):
        self.left_channel_get_request = 0
        self.left_request_task = []
        self.left_get_request_core_id = []

        self.right_channel_get_request = 0
        self.right_request_task = []
        self.right_get_request_core_id = []

        self.top_channel_get_request = 0
        self.top_request_task = []
        self.top_get_request_core_id = []

        self.bottom_channel_get_request = 0
        self.bottom_request_task = []
        self.bottom_get_request_core_id = []

        self.local_channel_get_request = 0
        self.local_request_task = []
        self.local_get_request_core_id = []

    def clear_response_state(self):
        self.left_rev_response = 0
        self.right_rev_response = 0
        self.bottom_rev_response = 0
        self.top_rev_response = 0
        self.local_rev_response = 0

    def left_exchange_sent_rev(self):
        self.left_for_sent_pack_data_info = self.left_have_rev_pack_data_info.copy()
        self.left_have_rev_pack_data_info = data_info()

    def right_exchange_sent_rev(self):
        self.right_for_sent_pack_data_info = self.right_have_rev_pack_data_info.copy()
        self.right_have_rev_pack_data_info = data_info()

    def top_exchange_sent_rev(self):
        self.top_for_sent_pack_data_info = self.top_have_rev_pack_data_info.copy()
        self.top_have_rev_pack_data_info = data_info()

    def bottom_exchange_sent_rev(self):
        self.bottom_for_sent_pack_data_info = self.bottom_have_rev_pack_data_info.copy()
        self.bottom_have_rev_pack_data_info = data_info()

    def local_exchange_sent_rev(self):
        self.local_for_sent_pack_data_info = self.local_have_rev_pack_data_info.copy()
        self.local_have_rev_pack_data_info = data_info()


    #def exchange_src_sent_rev(self):
        #self.for_sent_pack_data_info = self.have_rev_pack_data_info.copy()


    def clear_task_used(self):
        self.task_used = 0

    def clear_src(self):
        self.is_final_src = 0

    def clear_dst(self):
        self.is_final_dst = 0





