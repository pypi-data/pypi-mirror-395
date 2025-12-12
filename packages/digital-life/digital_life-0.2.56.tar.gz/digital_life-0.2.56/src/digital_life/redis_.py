
import redis
import json # 导入 json 库用于序列化和反序列化
from digital_life import logger
from digital_life.log import struct_log

def get_redis_client(username, password, host, port,db,decode_responses = True):
    """
    创建一个 Redis 客户端连接，包含阿里云 Redis 的认证信息。
    """
    try:
        r = redis.StrictRedis(
            host=host,
            port=port,                                          
            db=db,                        
            username=username,                                    
            password=password,                                
            decode_responses=decode_responses,                              
            socket_connect_timeout=10                           
        )
        # 尝试进行一次ping操作，验证连接是否成功
        r.ping()
        struct_log(logger.info,"成功连接到阿里云 Redis！","")
        return r
    except redis.exceptions.ConnectionError as e:
        struct_log(logger.info,f"无法连接到阿里云 Redis 服务器: {e}","")

        return None
    except redis.exceptions.AuthenticationError as e:
        struct_log(logger.info,f"Redis 认证失败，请检查用户名和密码: {e}","")

        return None
    except Exception as e:
        struct_log(logger.info,f"连接阿里云 Redis 时发生未知错误: {e}","")

        return None


def store_with_expiration(r_client, key, value, expiration_seconds=7200):
    """
    将 key-value 对存储到 Redis，并设置过期时间。
    如果 value 是列表或字典等复杂类型，会先将其序列化为 JSON 字符串。

    Args:
        key (str): 要存储的键。
        value (any): 要存储的值。可以是字符串、数字、列表、字典等。
        expiration_seconds (int): 过期时间（秒）。默认值 7200 秒（2小时）。
    """
    try:
        r = r_client
        # 检查 value 的类型，如果是列表或字典，则序列化为 JSON 字符串
        if isinstance(value, (list, dict)):
            # json.dumps() 将 Python 对象序列化为 JSON 字符串
            # ensure_ascii=False 允许存储非 ASCII 字符（如中文）
            # separators=(',', ':') 紧凑输出，不添加空格
            serialized_value = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
        else:
            # 对于字符串、数字等简单类型，直接使用
            serialized_value = value

        # 使用 set 方法存储 key-value 对，并设置过期时间 (EX参数)
        r.set(key, serialized_value, ex=expiration_seconds)

    except redis.exceptions.ConnectionError as e:
        print(f"无法连接到 Redis 服务器: {e}")
    except Exception as e:
        print(f"发生了一个错误: {e}")

def get_value(r_client,key):
    """
    从 Redis 获取指定 key 的值。
    如果存储的是 JSON 字符串，会尝试反序列化为 Python 对象。

    Args:
        key (str): 要获取的键。

    Returns:
        any or None: 如果键存在，则返回其值（可能已反序列化）；否则返回 None。
    """
    try:
        r = r_client
        retrieved_data = r.get(key) # 获取到的会是字符串 (因为 decode_responses=True)

        if retrieved_data:
            try:
                # 尝试将获取到的字符串反序列化为 Python 对象
                # 如果存储的是普通字符串，json.loads 会抛出异常，此时捕获并返回原始字符串
                deserialized_data = json.loads(retrieved_data)
                return deserialized_data
            except json.JSONDecodeError:
                # 如果不是有效的 JSON 字符串，则返回原始字符串
                return retrieved_data
        else:
            return None
    except redis.exceptions.ConnectionError as e:
        print(f"无法连接到 Redis 服务器: {e}")
        return None
    except Exception as e:
        print(f"发生了一个错误: {e}")
        return None
