import pickle
import os
from digital_life.core.user import UserInfo

def test_1():
    # os.system('pwd')
    # print(os.system('pwd'))

    pickle_file = 'auser_overview_ValueError.pkl'
    
    # 'rb' 表示以二进制读取模式打开文件
    with open(pickle_file, 'rb') as f:
        # pickle.load() 从文件反序列化对象
        # 注意：这里我们只调用一次 load，因为我们之前只 dump 了一个 my_dict
        loaded_data = pickle.load(f)
        # 如果之前 dump 了多个，这里也需要 load 多个
        # loaded_obj1 = pickle.load(f)
        # loaded_obj2 = pickle.load(f)
        # loaded_list = pickle.load(f)

    print("Objects successfully unpickled.")

    print(loaded_data['function_name'],'loaded_data')
    print(loaded_data['frames'][-1],'loaded_data')
    aa =loaded_data['frames'][-1]["locals"]
    
    x = UserInfo()

    print()
