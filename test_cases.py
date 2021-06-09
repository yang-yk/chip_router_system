'''
written by Yukuan Yang
2021.05.29
single chip test
'''
import os
import logging
from chip_system import chip_system,multi_chip_test
import random
from data_task import router_task
import time

#if os.path.exists('test_example.log'):
#   os.remove('test_example.log')
#logging.basicConfig(filename='test_example.log', level=logging.DEBUG)
#logging.info('start test process!')


def gen_router_tasks(task_num):
    all_cores = []
    for i in range(16):
        for j in range(10):
            all_cores.append((i,j))

    used_cores = random.sample(all_cores,2*task_num)
    task_data_volume = []
    for i in range(task_num):
        task_data_volume.append(random.randint(50,100))

    router_tasks = []
    for i in range(task_num):
        test_router_task = router_task((0,0),(0,0),used_cores[2*i],used_cores[2*i+1],task_data_volume[i])
        logging.info('task  %d:(0,0,%d,%d)---->(0,0,%d,%d)  data volume: %d'%(i+1,used_cores[2*i][0],used_cores[2*i][1],used_cores[2*i+1][0],used_cores[2*i+1][1],task_data_volume[i]))
        print('task  %d:(0,0,%d,%d)---->(0,0,%d,%d)  data volume: %d'%(i+1,used_cores[2*i][0],used_cores[2*i][1],used_cores[2*i+1][0],used_cores[2*i+1][1],task_data_volume[i]))
        router_tasks.append(test_router_task)

    #print(router_tasks)



    return router_tasks


#test_router_tasks = gen_router_tasks(5)
#print('over')




def test_cases(sim_times):
    start_time = time.time()
    for sim_time in range(sim_times):
        test_chip_system = chip_system(5, 5)
        task_num = random.randint(20,30)
        logging.basicConfig(filename='.test_example_'+str(time)+'task_num'+str(task_num)+'.log', level=logging.DEBUG)
        logging.info('start test process!')
        test_router_tasks = gen_router_tasks(task_num)
        multi_chip_test(test_chip_system, test_router_tasks)
    end_time = time.time()
    print('Simulation uses %d seconds!'%(end_time-start_time))
    logging.info('Simulation uses %d seconds!'%(end_time-start_time))

test_cases(1)




