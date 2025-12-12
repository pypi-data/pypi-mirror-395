import redis
import time,random
import csv


class OperaRedis():
    def __init__(self,redis_host,redis_port,redis_password = None):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.connect = redis.Redis(host=redis_host, db=1, port=redis_port, password=redis_password)


    def set_key(self,set_key,set_value):
        try:
            self.connect.set(set_key, set_value)  # 设置键值对
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.connect.close()

    def get_key(self,key):
        try:
            keys = self.connect.keys(key)  # 设置键值对
            data_list = []
            for key in keys:
                data = str(key.decode()).replace("_", "=").replace(":", "_")
                data_list.append(data)
            write_to_csv(data_list)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.connect.close()


def write_to_csv(data,file_name = "../test_data/view_cookie.csv"):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入多行数据
        writer.writerows(data)

if __name__=="__main__":
    pass
