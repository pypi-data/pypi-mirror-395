from typing import Dict, Any
import os
import httpx
from .embedding_pool import EmbeddingPool
from digital_life.redis_ import get_redis_client, store_with_expiration, get_value

recommended_biographies_cache_max_leng = int(os.getenv("recommended_biographies_cache_max_leng",2))
recommended_cache_max_leng = int(os.getenv("recommended_cache_max_leng",2))
# recommended_top_k = 10
user_callback_url = os.getenv("user_callback_url")
two_hours_in_seconds = os.getenv("two_hours_in_seconds")

async def aget_(url = ""):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # 如果状态码是 4xx 或 5xx，会抛出 HTTPStatusError 异常
            
            assert response.status_code == 200
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    return None

'''
class Recommend_old():
    def __init__(self):
        self.ep = EmbeddingPool()
        self.recommended_biographies_cache: Dict[str, Dict[str, Any]] = {}
        self.recommended_figure_cache: Dict[str, Dict[str, Any]] = {}

    def update(self,text, id, type):
        self.ep.update(text=text, id=id, type=type)

    def delete(self,id):
        self.ep.delete(id)

    async def recommended_biographies_and_cards(self,user_id):
        user_profile_id_to_fetch = user_id
        memory_info = await aget_(url = user_callback_url + f"/api/inner/getMemoryCards?userProfileId={user_profile_id_to_fetch}")

        user_brief = '\n'.join([i.get('content') for i in memory_info['data']["memoryCards"][:4]])
        user_brief = user_brief or "这是一个简单的记忆卡片"

        result = self.ep.search_bac(query=user_brief) # 假如top_k = 1000

        # 是否记录了该用户, 如果没记录, 创建空列表
        if self.recommended_biographies_cache.get(user_id):
            clear_result = [i for i in result if i.get("id") not in self.recommended_biographies_cache.get(user_id)]
        else:
            self.recommended_biographies_cache[user_id] = []
            clear_result = result
        clear_result = clear_result[:recommended_top_k]
        # 加入缓存 去重
        self.recommended_biographies_cache[user_id] += [i.get("id") for i in clear_result]
        self.recommended_biographies_cache[user_id] = list(
            set(self.recommended_biographies_cache[user_id])
        )

        reset_length = recommended_biographies_cache_max_leng if recommended_biographies_cache_max_leng < len(result) else len(result) -1

        if len(self.recommended_biographies_cache[user_id]) > reset_length:
            self.recommended_biographies_cache[user_id] = []
        return clear_result


    async def recommended_figure_person(self,user_id):
        user_profile_id_to_fetch = user_id
        avatar_info = await aget_(url = user_callback_url + f"/api/inner/getAvatarDesc?userProfileId={user_profile_id_to_fetch}")
        if avatar_info["code"] == 200:
            user_brief = avatar_info["data"].get("avatarDesc")
        else:
            user_brief = "这是一个简单的人"

        result = self.ep.search_figure_person(query=user_brief)  # 100+

        if self.recommended_figure_cache.get(user_id):
            clear_result = [i for i in result if i.get("id") not in self.recommended_figure_cache.get(user_id)]
        else:
            self.recommended_figure_cache[user_id] = []
            clear_result = result

        clear_result = clear_result[:recommended_top_k]
        self.recommended_figure_cache[user_id] += [i.get("id") for i in result]
        self.recommended_figure_cache[user_id] = list(
            set(self.recommended_figure_cache[user_id])
        )

        reset_length = recommended_cache_max_leng if recommended_cache_max_leng < len(result) else len(result) -1

        if len(self.recommended_figure_cache[user_id]) > reset_length:
            self.recommended_figure_cache[user_id] = []
        return clear_result

'''

class Recommend():
    def __init__(self):
        self.ep = EmbeddingPool()
        self.biographies_redis_client = get_redis_client(username = os.getenv("redis_username"), 
                                             password = os.getenv("redis_password"), 
                                             host = os.getenv("redis_host"), 
                                             port = os.getenv("redis_port"),
                                             db = 20)
        self.figure_redis_client = get_redis_client(username = os.getenv("redis_username"), 
                                        password = os.getenv("redis_password"), 
                                        host = os.getenv("redis_host"), 
                                        port = os.getenv("redis_port"),
                                        db = 21)

        # self.recommended_biographies_cache: Dict[str, Dict[str, Any]] = {}
        # self.recommended_figure_cache: Dict[str, Dict[str, Any]] = {}

    def update(self,text, id, type):
        self.ep.update(text=text, id=id, type=type)

    def delete(self,id):
        self.ep.delete(id)

    async def recommended_biographies_and_cards(self,user_id,timestamp,current:int,size = 10):
        # TODO
        user_profile_id_to_fetch = user_id
        user_id_timestamp = f"{user_id}_{timestamp}"
        memory_info = await aget_(url = user_callback_url + f"/api/inner/getMemoryCards?userProfileId={user_profile_id_to_fetch}")

        user_brief = '\n'.join([i.get('content') for i in memory_info['data']["memoryCards"][:4]])
        user_brief = user_brief or "这是一个简单的记忆卡片"

        result = self.ep.search_bac(query=user_brief) # 假如top_k = 1000
        # result  300个推荐结果
        # 是否记录了该用户, 如果没记录, 创建空列表
        if current == 1:
            store_with_expiration(self.biographies_redis_client, user_id_timestamp, [], two_hours_in_seconds) 

        now_values = get_value(self.biographies_redis_client,user_id_timestamp)

        if now_values:
            clear_result = [i for i in result if i.get("id") not in now_values] # 将300个id 过滤一遍
        else:
            store_with_expiration(self.biographies_redis_client, user_id_timestamp, [], two_hours_in_seconds) # 新建不用过滤
            clear_result = result

        clear_result = clear_result[:size]

        now_user_id_list = get_value(self.biographies_redis_client,user_id_timestamp)
        now_user_id_list += [i.get("id") for i in clear_result]
        now_user_id_list = list(set(now_user_id_list))
        store_with_expiration(self.biographies_redis_client, user_id_timestamp, now_user_id_list, two_hours_in_seconds)

        return clear_result


    async def recommended_figure_person(self,user_id,timestamp,current:int,size:int = 10):
        # TODO
        user_profile_id_to_fetch = user_id
        user_id_timestamp = f"{user_id}_{timestamp}"
        avatar_info = await aget_(url = user_callback_url + f"/api/inner/getAvatarDesc?userProfileId={user_profile_id_to_fetch}")
        if avatar_info["code"] == 200:
            user_brief = avatar_info["data"].get("avatarDesc")
        else:
            user_brief = "这是一个简单的人"

        result = self.ep.search_figure_person(query=user_brief)  # 100+

        if current == 1:
            store_with_expiration(self.figure_redis_client, user_id_timestamp, [], two_hours_in_seconds) 

        now_values = get_value(self.figure_redis_client,user_id_timestamp)

        if now_values:
            clear_result = [i for i in result if i.get("id") not in now_values]
        else:
            store_with_expiration(self.figure_redis_client, user_id_timestamp, [], two_hours_in_seconds)
            clear_result = result

        clear_result = clear_result[:size]

        now_user_id_list = get_value(self.figure_redis_client,user_id_timestamp)
        now_user_id_list += [i.get("id") for i in result]
        now_user_id_list = list(set(now_user_id_list))
        store_with_expiration(self.figure_redis_client, user_id_timestamp, now_user_id_list, two_hours_in_seconds)

        return clear_result


