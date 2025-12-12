import random
import time
import random
import secrets
import string
from datetime import datetime

import pymysql



class OperaMysql():
    def __init__(self,host,username,password,db,port):
        self.host= host
        self.username = username
        self.password = password
        self.db = db
        self.port = port
        self.con = pymysql.connect(host=self.host,user=self.username,password=self.password,database=self.db,port=self.port)
    #whatsapp 广播
    def whatsapp_broadcast_update(self,num,merchantId,waba,phone,country_code="86",interaction_time=None):
        """
        :param num: 要插入的数据条数
        :param merchantId:店铺ID
        :param phone:插入的号码，插入的号码不能一样，所以会从这个递增
        :param waba:店铺的wabaid
        :return:
        """
        cur = self.con.cursor()
        phone = phone
        name = "jmeter压测%d"%int(time.time())
        select_sql = """
        select max(id) from sl_uc_test.whatsapp_contact;
        """
        cur.execute(select_sql)
        id = cur.fetchone()[0]
        # 准备批量插入的数据
        insert_data = []
        formatted_time =get_strf_time()
        if interaction_time==None:
            interaction_time = get_strf_time()
        # print(id)
        for i in range(num):
            phone+=1
            id+=1
            phone_str = str(phone)
            insert_data.append((
                id,
                merchantId,
                waba,
                name,
                country_code,
                phone_str,
                phone_str,
                phone_str,
                2,
                interaction_time,
                None,
                None,
                phone_str,
                1,
                formatted_time,
                formatted_time
            ))

            # 批量插入或更新
        insert_sql = """
                INSERT INTO sl_uc_test.whatsapp_contact 
                (id, merchant_id, merchant_waba_id, name, country_code, phone_number, display_phone_number, head_img, optin_status, interaction_time, customer_name, customer_id, waba_id, is_wabaaccount, update_time, create_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                phone_number = VALUES(phone_number),
                display_phone_number = VALUES(display_phone_number);
                """
        try:
            # 开始事务
            self.con.begin()
            cur.executemany(insert_sql, insert_data)
            # 提交事务
            self.con.commit()
        except Exception as e:
            print(f"Error: {e}")
            self.con.rollback()  # 回滚事务
        finally:
            cur.close()
            self.con.close()
    #line、faceboook 、instagram 平台广播
    def other_broadcast_update(self,num,page_id,platform,interaction_time=None):
        """
        page_id、platform 需要替换成自己店铺的数据,
        num 为 插入的条数
        """
        if interaction_time==None:
            interaction_time = get_strf_time()
        cur = self.con.cursor()
        select_sql = """
            select max(id) from sl_uc_test.uc_user_interaction ;
            """
        cur.execute(select_sql)
        id = cur.fetchone()[0]
        # 准备批量插入的数据
        formatted_time = get_strf_time()
        insert_data = []
        for i in range(num):
            id+=1
            user_id = '{}c4af{}k74{}9'.format(random.randint(100, 999), int(time.time()), generate_random_string(4))
            insert_data.append((
                id,
                user_id,
                page_id,
                platform,
                interaction_time,
                formatted_time,
                formatted_time
            ))
        # 批量插入或更新
        insert_sql ="""
         INSERT INTO sl_uc_test.uc_user_interaction
        (id, platform_user_id, platform_channel_id, platform, interaction_time, create_time, update_time)
        VALUES(%s, %s, %s, %s, %s, %s, %s);
         """
        try:
            # 开始事务
            self.con.begin()
            cur.executemany(insert_sql, insert_data)
            # 提交事务
            self.con.commit()
        except Exception as e:
            print(f"Error: {e}")
            self.con.rollback()  # 回滚事务
        finally:
            cur.close()
            self.con.close()

    def select(self,select_sql):
        # con = con_mysql()
        cur = self.con.cursor()
        cur.execute(select_sql)
        data = cur.fetchall()
        return data


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_strf_time():
    # 获取当前时间
    now = datetime.now()
    # 格式化为字符串，确保微秒部分有 9 位数
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S.%f')
    # 将微秒部分填充到 9 位
    formatted_time = formatted_time[:-3] + formatted_time[-3:].ljust(9, '0')
    return formatted_time






if __name__=="__main__":
    # host = "10.98.32.7"
    # port = 6303
    # db = "sl_sc_medium_test"
    # username = "sl_sc2_backend"
    # password = "XVPt6eS7r9nHZF8qlfoivy9u"

    # host = "10.98.216.252"
    # port = 3306
    # db = "sl_uc_test"
    # username = "admin"
    # password = "p2qJrad0rr5AxfGGe3gN69fF"

    host = "10.98.32.38"
    port = 6304
    db = "sl_uc_test"
    username = "sl_sc_1_dev_test"
    password = "VJ6H54iSPjStkFZqWiTYHJNe"
    operaMysql = OperaMysql(host,username,password,db,port)
    phone = 1827679999
    num = 10
    merchant_id = "613581c9820e260046693ef5"
    waba = "102324679313339"
    # operaMysql.whatsapp_broadcast_update(num,merchant_id,waba,phone)
    # page_id = "110234798670383"
    # platform = "FACEBOOK"
    # ig
    page_id = "17841453464121067"
    platform = "INSTAGRAM"
    operaMysql.other_broadcast_update(10,page_id,platform)






