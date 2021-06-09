'''
written by Yukuan Yang
2021.05.29
'''

from physical_core import physical_core
from router import merge_router, split_router

class singe_chip(object):
    def __init__(self, chip_idx, chip_idy, core_numx, core_numy):
        '''
        ???????
        :param chip_idx:  ????idx
        :param chip_idy:  ????idy
        :param core_numx:  x??????
        :param core_numy:  y??????
        '''
        self.chip_idx = chip_idx
        self.chip_idy = chip_idy
        self.chip_id = (self.chip_idx,self.chip_idy)
        self.core_numx = core_numx
        self.core_numy = core_numy
        self.core_array = []
        for i in range(core_numx):
            core_array_y = []
            for j in range(core_numy):
                phy_core = physical_core(chip_id=(chip_idx, chip_idy), core_coordinate=(i, j))
                core_array_y.append(phy_core)
            self.core_array.append(core_array_y)

        self.init_chip_router()


    def init_chip_router(self):
        # -1/-2/-3/-4 position 0 merge
        self.left_merge_router = merge_router(chip_id=self.chip_id, core_coordinate=(-1, 0))
        self.bottom_merge_router = merge_router(chip_id=self.chip_id, core_coordinate=(-2, 0))
        self.right_merge_router = merge_router(chip_id=self.chip_id, core_coordinate=(-3, 0))
        self.top_merge_router = merge_router(chip_id=self.chip_id, core_coordinate=(-4, 0))

        # -1/-2/-3/-4 position -1 split
        self.left_split_router = split_router(chip_id=self.chip_id, core_coordinate=(-1, -1))
        self.bottom_split_router = split_router(chip_id=self.chip_id, core_coordinate=(-2, -1))
        self.right_split_router = split_router(chip_id=self.chip_id, core_coordinate=(-3, -1))
        self.top_split_router = split_router(chip_id=self.chip_id, core_coordinate=(-4, -1))

    def get_core_from_id(self, idx, idy):
        if idx == -1 and idy == 0:
            return self.left_merge_router
        elif idx == -2 and idy == 0:
            return self.bottom_merge_router
        elif idx == -3 and idy == 0:
            return self.right_merge_router
        elif idx == -4 and idy == 0:
            return self.top_merge_router
        elif idx == -1 and idy == -1:
            return self.left_split_router
        elif idx == -2 and idy == -1:
            return self.bottom_split_router
        elif idx == -3 and idy == -1:
            return self.right_split_router
        elif idx == -4 and idy == -1:
            return self.top_split_router
        else:
            return self.core_array[idx][idy]







