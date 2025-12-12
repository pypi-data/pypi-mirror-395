import datetime
import re
import requests
import json
from jsonpath import jsonpath
import time
import random
import hmac
from hashlib import sha1
import random
import json, hashlib, hmac


def delete_post(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s" % (env, sales_id)
    res = requests.delete(url, headers=headers).json()
    return res


def delete_relate_post(data):
    """删除串接的facebook或fb group 避免影响串接"""
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales" % env
    sales_type = data.get("sales_type", "LIVE")
    param = {"page_num": 1, "page_size": 100, "sales_type": sales_type}
    platform = "facebook"
    post_id = data["post_id"]
    if "platform" in data:
        platform = data["platform"].upper()
        param["platforms"] = platform
    if "search" in data:
        search_word = data["search"]
        param["search_word"] = search_word
    response = requests.get(url, headers=headers, params=param).json()
    # print("url",url)
    # print("param", param)
    # print("response",response)
    sales_data = response["data"]["list"]
    # print("sales_data",sales_data)
    status = [1, 2, 4]
    if sales_type.lower() == "post":
        status = [0, 1, 2]
    if "status" in data:
        status = data["status"]
    for i in sales_data:
        platforms = i["platforms"]
        post_sale_status = i["post_sale_status"]
        live_sdk = i["live_sdk"]
        related_post = i["related_post"]
        if (platforms == [
            platform.upper()] or live_sdk == platform.upper()) and related_post == True and post_sale_status in status:
            sales_id = i["id"]
            data["sales_id"] = sales_id
            # print(sales_id)
            response = get_live_info(data)
            # print("查询详情返回,",response)
            global relatedPostList
            if sales_type.lower() == "live":
                relatedPostList = response["data"]["relatedPostList"]
            elif sales_type.lower() == "post":
                relatedPostList = response["data"]["related_post_list"]
            if platform.lower() == "facebook":
                count = 0
                for i in relatedPostList:
                    fb_post_id = i["post_id"]
                    # print("fb_post_id",fb_post_id)
                    # print("post_id", post_id)
                    if fb_post_id.strip() in post_id:
                        print("找到串接的帖文:%s" % sales_id)
                        count += 1
                        res = delete_post(data)
                        if count >= len(post_id):
                            return res
            elif platform.lower() == "fb_group":
                count = 0
                id_list = []
                for id in post_id:
                    idData = id.split("posts/")[-1]
                    id_list.append(idData)
                for i in relatedPostList:
                    permalink_url = i["permalink_url"]
                    permalink_url = permalink_url.split("permalink/")[-1]

                    # print("permalink_url",permalink_url)
                    # print("post_id", post_id)
                    if permalink_url.strip() in id_list:
                        print("找到串接的帖文:%s" % sales_id)
                        res = delete_post(data)
                        count += 1
                        if count >= len(id_list):
                            return res


def get_sales_id(data):
    """"查询返回指定直播间的salse_id
    status:准备中 0，直播中 1 已结束 2 断线中 4
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales" % env
    param = {"page_num": 1, "page_size": 100, "sales_type": "LIVE"}
    platform = "LINE"
    if "platform" in data:
        platform = data["platform"].upper()
        param["platforms"] = platform
    if "search" in data:
        search_word = data["search"]
        param["search_word"] = search_word
    response = requests.get(url, headers=headers, params=param).json()
    sales_data = response["data"]["list"]
    if "status" in data:
        status = data["status"]
        for i in sales_data:
            platforms = i["platforms"]
            post_sale_status = i["post_sale_status"]
            if platforms == [platform.upper()] and post_sale_status == status:
                sales_id = i["id"]
                data["sales_id"] = sales_id
                if "type" in data:
                    type = data["type"]
                    response = get_live_info(data)
                    platform_sub_type = response["data"]["sales"]["platform_sub_type"]
                    if platform_sub_type == type.upper():
                        return sales_id, response
                else:
                    return sales_id, response
    else:
        for i in sales_data:
            platforms = i["platforms"]
            if platforms == [platform.upper()]:
                sales_id = i["id"]
                data["sales_id"] = sales_id
                if "type" in data:
                    type = data["type"]
                    response = get_live_info(data)
                    platform_sub_type = response["data"]["sales"]["platform_sub_type"]
                    if platform_sub_type == type.upper():
                        return sales_id, response
                else:
                    return sales_id, response


def create_activity(data):
    env = data["env"]
    headers = data["headers"]
    body = data["body"]
    sales_id = data["sales_id"]
    url = "%s/admin/api/bff-web/live/activity/%s" % (env, sales_id)
    # platform = "FACEBOOK"
    # if "platform" in data:
    #     platform = data["platform"].upper()
    response = requests.post(url, headers=headers, json=body)
    # print(response.json())
    if response.status_code == 200:
        activity_id = response.json()["data"]
        return activity_id
    else:
        print("创建活动失败", response)
        return response


def delate_activity(data):
    #写错名,但很多方法用了，懒得改了
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    url = "%s/admin/api/bff-web/live/activity/%s" % (env, activity_id)
    body = {}
    time.sleep(1)
    response = requests.delete(url, headers=headers,json=body).json()
    return response

def delete_activity(data):
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    url = "%s/admin/api/bff-web/live/activity/%s" % (env, activity_id)
    body = {}
    time.sleep(1)
    response = requests.delete(url, headers=headers,json=body).json()
    return response

def start_activity(data):
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    url = "%s/admin/api/bff-web/live/activity/%s/start" % (env, activity_id)
    body = {}
    response = requests.post(url, headers=headers,json=body).json()
    return response


def end_activity(data):
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    url = "%s/admin/api/bff-web/live/activity/%s/end" % (env, activity_id)
    body = {}
    response = requests.post(url, headers=headers,json=body).json()
    return response


def get_page_info(data):
    info = get_live_info(data)
    platform = data.get("platform", "FACEBOOK")
    sales_type = data.get("sales_type", "live")
    global platform_list
    page_info = {}
    if sales_type.lower() == "live":
        platform_list = jsonpath(info, "$..relatedPostList..platform")
        i = platform_list.index(platform.upper())
        page_id = info["data"]["relatedPostList"][i]["page_id"]
        platform = info["data"]["relatedPostList"][i]["platform"]
        post_id = info["data"]["relatedPostList"][i]["post_id"]
        group_id = info["data"]["relatedPostList"][i]["group_id"]
        permalink_url = info["data"]["relatedPostList"][i]["permalink_url"]
        page_info["page_id"] = page_id
        page_info["platform"] = platform
        page_info["post_id"] = post_id
        page_info["group_id"] = group_id
        page_info["permalink_url"] = permalink_url

    elif sales_type.lower() == "post":
        platform_list = jsonpath(info, "$..related_post_list..platform")
        i = platform_list.index(platform.upper())
        page_id = info["data"]["related_post_list"][i]["page_id"]
        platform = info["data"]["related_post_list"][i]["platform"]
        post_id = info["data"]["related_post_list"][i]["post_id"]
        group_id = info["data"]["related_post_list"][i]["group_id"]
        permalink_url = info["data"]["related_post_list"][i]["permalink_url"]
        page_info["page_id"] = page_id
        page_info["platform"] = platform
        page_info["post_id"] = post_id
        page_info["group_id"] = group_id
        page_info["permalink_url"] = permalink_url
    return page_info


def send__live_comment(data):
    env = data["env"]
    key = data["key"]
    page_id = data.get("page_id", "")
    platform = data.get("platform", "FACEBOOK")
    post_id = data.get("post_id", "")
    group_id = data.get("group_id", "")
    stamp = int(time.time())
    num = random.randint(100000, 999999)
    user_id = "488864%d" % int(time.time())
    name = "test live%d" % int(time.time())
    keyword = "接口测试普通留言"
    user_id = data.get("user_id", user_id)
    name = data.get("name", name)
    keyword = data.get("keyword", keyword)
    # sales_type = data.get("sales_type", "live")
    relationUrl = data.get("relationUrl", "")
    comment_type = data.get("comment_type", "comment")
    if page_id == "" or post_id == "key":
        page_info = get_page_info(data)
        page_id = page_info["page_id"]
        platform = page_info["platform"]
        post_id = page_info["post_id"]
        group_id = page_info["group_id"]
        relationUrl = page_info["permalink_url"]
    # 放到后面，需要等设置完page_id 后再设置
    comment_id = "%s_%d%d" % (page_id, stamp, num)
    comment_id = data.get("comment_id", comment_id)
    body = {}
    if platform.upper() == "INSTAGRAM":
        body = {"entry": [{"id": page_id, "time": stamp, "changes": [{"value": {"from": {"id": user_id,
                                                                                         "username": name},
                                                                                "media": {"id": post_id,
                                                                                          "media_product_type": "FEED"},
                                                                                "id": comment_id, "text": keyword},
                                                                      "field": "comments"}]}], "object": "instagram"}
    elif platform.upper() == "FB_GROUP":
        t_time = stamp * 1000
        if "_" in post_id:
            post_id = post_id.split("_")[-1]
        elif relationUrl != "":
            match = re.search(r'groups/(\d+)/permalink/(\d+)/', relationUrl)
            group_id = match.group(1)
            post_id = match.group(2)
        comment_id = "%d%d" % (stamp, num)
        body = {"object": "page", "entry": [
            {"id": page_id, "time": t_time, "messaging": [{"recipient": {"id": page_id}, "message": keyword,
                                                           "from": {"id": user_id, "name": name}, "group_id": group_id,
                                                           "post_id": post_id, "comment_id": comment_id,
                                                           "created_time": stamp, "item": "comment",
                                                           "verb": "add", "parent_id": post_id,
                                                           "field": "group_feed"}]}]}
    elif platform.upper() == "FACEBOOK":
        if comment_type == "comment":
            body = {"object": "page", "entry": [{"id": page_id, "time": stamp, "changes": [{"field": "feed", "value": {
                "from": {"id": user_id, "name": name},
                "post": {"status_type": "added_video", "is_published": True, "updated_time": "2022-11-18T09:57:26+0000",
                         "permalink_url": "https://www.facebook.com/permalink.php?story_fbid=pfbid02jLK3e6YdFSXp2DmD7j7vtStLXoBzTi8rxKrp6jFhVMUTTEgz6qvZA8soR9Uwydd8l&id=107977035056574",
                         "promotion_status": "inactive", "id": post_id}, "message": keyword, "item": "comment",
                "verb": "add", "post_id": post_id, "comment_id": comment_id,
                "created_time": stamp, "parent_id": post_id}}]}]}
        elif comment_type == "like":
            body = {"entry": [{"id": page_id, "time": stamp, "changes": [{"value": {
                "from": {"id": user_id, "name": name}, "post_id": post_id, "created_time": stamp, "item": "reaction",
                "parent_id": post_id, "reaction_type": "like", "verb": "add"}, "field": "feed"}]}], "object": "page"}
        elif comment_type == "unlike":
            body = {"entry": [{"id": page_id, "time": stamp, "changes": [{"value": {
                "from": {"id": user_id, "name": name}, "post_id": post_id, "created_time": stamp, "item": "reaction",
                "parent_id": post_id, "reaction_type": "like", "verb": "remove"}, "field": "feed"}]}], "object": "page"}

    # print(body)
    url = "%s/facebook/webhook" % env
    sign_text = hmac.new(key.encode("utf-8"), json.dumps(body).encode("utf-8"), sha1)
    signData = sign_text.hexdigest()
    # print("body", json.dumps(body))
    header = {"Content-Type": "application/json", "x-hub-signature": "sha1=%s" % signData}
    response = requests.post(url, headers=header, data=json.dumps(body))
    # print(response.text)
    return user_id, name, comment_id


def send_mc_message(data):
    env = data["env"]
    key = data["key"]
    stamp = int(time.time() * 1000)
    user_id = "488864%d" % int(time.time())
    name = "test live%d" % int(time.time())
    message = "接口测试普通留言"
    payload = data.get("payload", "{}")
    type = data.get("type", "commment")
    user_id = data.get("user_id", user_id)
    name = data.get("name", name)
    message = data.get("message", message)
    page_id = data.get("page_id", "")
    platform = data.get("platform", "FACEBOOK")
    if page_id == "":
        page_info = get_page_info(data)
        page_id = page_info["page_id"]
        platform = page_info["platform"]
        post_id = page_info["post_id"]
        group_id = page_info["group_id"]
    mid = "m_hhAqPhSlMTY4En2oWjSB59T3BFjeU97DdDV4WHr3DLWnPrO0iCsjQlG3hBN%d-sBlT26-6oNg" % stamp
    body = {"entry": [{"id": "%s" % page_id, "messaging": [{"message":
        {
            "mid": mid,
            "text": "%s" % message},
        "recipient": {"id": "%s" % page_id},
        "sender": {"id": "%s" % user_id}, "timestamp": stamp}],
                       "time": stamp}], "object": "page"}
    # if platform.upper()=="FACEBOOK":
    #     body = {"entry":[{"id":"%s"%page_id,"messaging":[{"message":
    #     {"mid":"m_hhAqPhSlMTY4En2oWjSB59T3BFjeU97DdDV4WHr3DLWnPrO0iCsjQlG3hBN%d-sBlT26-6oNg"%stamp,"text":"%s"%message},
    #     "recipient":{"id":"%s"%page_id},"sender":{"id":"%s"%user_id},"timestamp":stamp}],"time":stamp}],"object":"page"}
    if type == "commment" and platform.upper() == "INSTAGRAM":
        body = {"object": "instagram", "entry": [{"time": stamp, "id": "%s" % page_id, "messaging": [
            {"sender": {"id": "%s" % user_id}, "recipient": {"id": "%s" % page_id},
             "timestamp": stamp, "message": {
                "mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDUwMzgwODgwNTMzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI3NjAyNDExMzcwMDc2NTA5MDozMTgzODU0Mzg3NTY4MDYwMTE3ODUxOTE2MD%d" % stamp,
                "text": "%s" % message}}]}]}
    elif type == "postback" and platform.upper() in ("FB_GROUP", "FACEBOOK"):
        # t_time = stamp * 1000
        body = {"object": "page", "entry": [{"time": stamp, "id": "%s" % page_id, "messaging": [
            {"sender": {"id": "%s" % user_id}, "recipient": {"id": "%s" % page_id}, "timestamp": stamp,
             "postback": {"title": "继续 ➡️", "payload": payload,
                          "mid": "m_w6KNGd0PMndK0LvCw7Hzy1zsVSWT0fpN3ievQ9LtB0NxnnTQGDMyKI5DFeVbaJIRni1cqqJYXIJ-wq98aw%d" % stamp}}]}]}
    elif type == "postback" and platform.lower() == "instagram":
        body = {"object": "instagram", "entry": [{"time": stamp, "id": "%s" % page_id, "messaging": [
            {"sender": {"id": "%s" % user_id}, "recipient": {"id": "%s" % page_id}, "timestamp": stamp,
             "postback": {"title": "继续 ➡️", "payload": payload,
                          "mid": "m_w6KNGd0PMndK0LvCw7Hzy1zsVSWT0fpN3ievQ9LtB0NxnnTQGDMyKI5DFeVbaJIRni1cqqJYXIJ-wq98aw%d" % stamp}}]}]}

    url = "%s/facebook/webhook" % env
    sign_text = hmac.new(key.encode("utf-8"), json.dumps(body).encode("utf-8"), sha1)
    signData = sign_text.hexdigest()
    header = {"Content-Type": "application/json", "x-hub-signature": "sha1=%s" % signData}
    response = requests.post(url, headers=header, data=json.dumps(body))
    # print(response.text)
    # print(body)
    return user_id, name


def send_sl_comment(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/viewer/%s/send/comments" % (env, sales_id)
    login_url = "%s/api/posts/live/viewer/unauthorized/post/sales/%s/user/info?appId=SL101-web" % (env, sales_id)
    content = data.get("content", "sl留言")
    headers["content-type"] = "application/json"
    body = {
        "content": content
    }
    #先进入直播间再留言
    login_response = requests.get(login_url,headers=headers).json()
    print("login_response:",login_response)
    response = requests.post(url, headers=headers, json=body).json()
    if response["code"] == "SUCCESS":
        comment_id = response["data"]["comment_id"]
        return comment_id
    return response


def get_live_info(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    sales_type = "live"
    if "sales_type" in data:
        sales_type = data["sales_type"]
    url = "%s/api/posts/%s/sales/%s" % (env, sales_type.lower(), sales_id)
    count = 0
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            time.sleep(1)
            count = count + 1
            if count > 10:
                print("查询报错：", response)
                return response.json()


def get_activity_detail(data):
    """
    type:
    luckyDraw,抽奖活动
    voucher--留言抢优惠
    answerFirst--抢答
    bidding--竞标
    vote:投票
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    type = data["type"]
    url = ""
    if type in "luckyDraw":
        url = "%s/api/activity/luckyDraw/%s" % (env, activity_id)
    elif type in "voucher":
        url = "%s/api/activity/voucher/%s" % (env, activity_id)
    elif type in "answerFirst":
        url = "%s/api/activity/answerFirst/%s" % (env, activity_id)
    elif type in "bidding":
        url = "%s/api/activity/bidding/%s" % (env, activity_id)
    elif type in "vote":
        url = "%s/api/activity/vote/%s" % (env, activity_id)
    response = requests.get(url, headers=headers).json()
    return response


def live_search_oa_gift(data):
    """
    查询oa赠品，命名转为驼峰和返回第一个赠品的信息
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/gifts" % env
    params = {"page": 1}
    response = requests.get(url, headers=headers, params=params).json()
    items = response["data"]["items"]

    if items == []:
        # 新增赠品
        body = {"unlimited_quantity": True, "title_translations": {"zh-cn": "接口自动化新增的赠品%s" % int(time.time())},
                "media_ids": "610d2865ca92cf00264c563c"}
        requests.post(url, headers=headers, json=body).json()
        time.sleep(5)
        # 新增后去查询
        response = requests.get(url, headers=headers, params=params).json()
        items = response["data"]["items"]

    # 返回数量不是0的赠品和spu_id
    # print(json.dumps(items))
    quantityList = jsonpath(items, "$..quantity")
    gift_info = items[0]
    for a, b in enumerate(quantityList):
        if b != 0:
            gift_info = items[a]
    spu_id = gift_info["id"]
    return spu_id, gift_info, response


def live_search_oa_product(data):
    """
    查询OA的商品，并返回响应,返回第一个有库存的商品
    spu:返回无规格
    sku:返回多规格
    quantity:0 返回无库存商品
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/products?page=1&per_page=50" % env
    type = "spu"
    quantity = 100
    type = data.get("type", type)
    quantity = data.get("quantity", quantity)
    if "query" in data:
        query = data["query"]
        url = "%s/openApi/proxy/v1/products?page=1&per_page=4&query=%s" % (env, query)
    response = requests.get(url, headers=headers).json()
    global items
    try:
        items = response["data"]["items"]
    except Exception:
        print("response：", response)
    variant_options_list = jsonpath(items, "$..variations")
    product_info = ""
    spu_id = ""
    sku_id = ""
    sku_id_quantity = []
    for a, b in enumerate(variant_options_list):
        if type == "spu" and b == [] and quantity != 0:
            quantitys = items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                break
        elif type == "sku" and b != [] and quantity != 0:
            quantitys = items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                sku_id = jsonpath(items[a]["variations"], "$.._id")
                sku_id_quantity = jsonpath(items[a]["variations"], "$..total_orderable_quantity")
                break
        elif type == "spu" and b == [] and quantity == 0:
            quantitys = items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                break
        elif type == "sku" and b != [] and quantity == 0:
            quantitys = items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                sku_id = jsonpath(items[a]["variations"], "$..id")
                sku_id_quantity = jsonpath(items[a]["variations"], "$..total_orderable_quantity")
                break
    return spu_id, sku_id, sku_id_quantity, product_info


def get_merchant_info(data):
    env = data["env"]
    headers = data["headers"]
    merchant_id = data["merchant_id"]
    url = "%s/openApi/proxy/v1/merchants/%s" % (env, merchant_id)
    response = requests.get(url, headers=headers).json()
    base_country_code = response["data"]["base_country_code"]
    default_language_code = response["data"]["default_language_code"]
    currency = ""
    if base_country_code == "TW":
        currency = "NT$"
    elif base_country_code == "TH":
        currency = "฿"
    elif base_country_code == "VN":
        # 放金额后面
        currency = "₫"
    return base_country_code, currency, response


def delete_broadcast(data):
    env = data["env"]
    headers = data["headers"]
    broadcast_id = data["broadcast_id"]
    url = "%s/admin/api/bff-web/live/broadcast/%s" % (env, broadcast_id)
    response = requests.delete(url, headers=headers).json()
    return response


def get_broadcast_list(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    name = ""
    platform = data["platform"]
    broadcast_id = ""
    pageNum = 1
    pageSize = 12
    pageNum = data.get("pageNum", pageNum)
    pageSize = data.get("pageSize", pageSize)
    name = data.get("name", name)
    if "name" in data:
        name = data["name"]
    url = "%s/admin/api/bff-web/live/broadcast/query" % env
    body = {
        "businessId": "%s" % sales_id,
        "businessType": "LIVE",
        "businessSubType": "LIVE_STREAM",
        "platform": "%s" % platform,
        "pageNum": pageNum,
        "pageSize": pageSize
    }
    # print(body)
    reponse = requests.post(url, headers=headers, json=body).json()
    if name != "":
        name_list = jsonpath(reponse, "$..name")
        broadcast_id_list = jsonpath(reponse, "$..id")
        for i, value in enumerate(name_list):
            if value == name:
                broadcast_id = broadcast_id_list[i]
    return broadcast_id, reponse


def get_broadcast_detail(data):
    env = data["env"]
    headers = data["headers"]
    broadcast_id = data["broadcast_id"]
    platform = data["platform"]
    url = "%s/admin/api/bff-web/live/broadcast/detail" % env
    body = {
        "id": "%s" % broadcast_id,
        "platform": "%s" % platform
    }
    response = requests.post(url, headers=headers, json=body).json()
    return response


def end_live(data):
    """结束帖文"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s/end" % (env, sales_id)
    response = requests.put(url, headers=headers).json()
    return response


def get_channel(data):
    "查询粉丝页信息，用于创建帖文"
    env = data["env"]
    headers = data["headers"]
    platform = data["platform"]
    valid = data.get("valid",True)
    url = "%s/api/posts/post/sales/multiPlatformChannelList?platformList=%s" % (env, platform.upper())
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json()["code"] == "SUCCESS":
        response = response.json()
        data_list = response["data"]
        for i in data_list:
            validToken = i["validToken"]
            if validToken==valid:
                response = i
                break
    # print(response)
    return response


def create_live(data):
    """创建直播，不套用通用配置"""
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/live/sales" % (env)
    stamp = int(time.time())
    title = "接口创建的直播活动名称%d" % stamp
    salesDescription = "接口创建的直播活动介绍%d" % stamp
    salesOwner = "接口创建的直播主%d" % stamp
    platform = "FB_GROUP"
    patternModel = "INCLUDE_MATCH"
    keywordValidInLive = True
    keywordValidAfterLive = False
    autoNotifyPayEnable = False
    autoNotifyPayMessage = ""
    autoNotifyPayButton = ""
    autoNotifyPayTime = None
    stockEnable = False
    stockIime = None
    lowOfQuantityEnable = False
    lowOfQuantitySound = False
    lowOfQuantityQuantity = "1"
    has_interaction_message = ""
    has_interaction_message_button = ""
    no_interaction_message_first = ""
    second_message = ""
    first_message_button = ""
    second_message_button = " ️"
    need_send_message = True
    has_link = True
    startTime = None
    endTime = None
    stamp = int(time.time())

    title = data.get("title", title)
    salesDescription = data.get("salesDescription", salesDescription)
    salesOwner = data.get("salesOwner", salesOwner)
    platform = data.get("platform", platform)
    patternModel = data.get("patternModel", patternModel)
    keywordValidInLive = data.get("keywordValidInLive", keywordValidInLive)
    keywordValidAfterLive = data.get("keywordValidAfterLive", keywordValidAfterLive)

    autoNotifyPayEnable = data.get("autoNotifyPayEnable", autoNotifyPayEnable)
    autoNotifyPayMessage = data.get("autoNotifyPayMessage", autoNotifyPayMessage)
    autoNotifyPayButton = data.get("autoNotifyPayButton", autoNotifyPayButton)
    autoNotifyPayTime = data.get("autoNotifyPayTime", autoNotifyPayTime)

    stockEnable = data.get("stockEnable", stockEnable)
    stockExpireTime = data.get("stockExpireTime")

    lowOfQuantityEnable = data.get("lowOfQuantityEnable", lowOfQuantityEnable)
    lowOfQuantitySound = data.get("lowOfQuantitySound", lowOfQuantitySound)
    lowOfQuantityQuantity = data.get("lowOfQuantityQuantity", lowOfQuantityQuantity)

    has_interaction_message = data.get("has_interaction_message", has_interaction_message)
    has_interaction_message_button = data.get("has_interaction_message_button", has_interaction_message_button)
    no_interaction_message_first = data.get("no_interaction_message_first", no_interaction_message_first)
    first_message_button = data.get("first_message_button", first_message_button)
    second_message = data.get("second_message", second_message)
    second_message_button = data.get("second_message_button", second_message_button)
    need_send_message = data.get("need_send_message", need_send_message)
    has_link = data.get("has_link", has_link)

    body = {}
    if platform.lower() in ("fb_group", "facebook", "instagram"):
        body = {
            "sales": {
                "title": title,
                "salesOwner": salesOwner,
                "salesDescription": salesDescription,
                "platforms": [
                    platform.upper()
                ],
                "platformChannels": [],
                "startTime": startTime,
                "endTime": endTime
            },
            "salesConfig": {
                "patternModel": {
                    "patternModel": patternModel,
                    "keywordValidInLive": keywordValidInLive,
                    "keywordValidAfterLive": keywordValidAfterLive
                },
                "autoNotifyPay": {
                    "enable": autoNotifyPayEnable,
                    "message": autoNotifyPayMessage,
                    "button": autoNotifyPayButton
                },
                "stock": {
                    "lockStock": stockEnable,
                    "salesStockLockExpireTime": stockIime
                },
                "lowOfQuantity": {
                    "enable": lowOfQuantityEnable,
                    "sound": lowOfQuantitySound,
                    "quantity": lowOfQuantityQuantity
                }
            },
            "postConfigMap": {
                platform: {
                    "message": {
                        "needSendMessage": need_send_message,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": has_interaction_message
                            },
                            "messageButton": has_interaction_message_button
                        },
                        "hasLink": has_link,
                        "noInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": no_interaction_message_first
                            },
                            "firstMessageButton": first_message_button,
                            "secondMessageTemplate": {
                                "topMessage": second_message
                            },
                            "secondMessageButton": second_message_button
                        },
                        "messageType": "MESSAGE"
                    }
                }
            }
        }
    elif platform in ("pl&fb", "obc&fb"):
        platformSubType = platform.split("&")[0].upper()
        data["platform"] = "FACEBOOK"
        res = get_channel(data)
        body = {
            "sales": {
                "title": title,
                "salesOwner": salesOwner,
                "salesDescription": salesDescription,
                "platforms": [
                    "SHOPLINE",
                    "FACEBOOK"
                ],
                "platformSubType": platformSubType,
                "platformChannels": [
                    res
                ],
                "startTime": startTime,
                "endTime": endTime
            },
            "salesConfig": {
                "patternModel": {
                    "patternModel": patternModel,
                    "keywordValidInLive": keywordValidInLive,
                    "keywordValidAfterLive": keywordValidAfterLive
                },
                "autoNotifyPay": {
                    "enable": autoNotifyPayEnable,
                    "message": autoNotifyPayMessage,
                    "button": autoNotifyPayButton,
                    "notifyTime": autoNotifyPayTime
                },
                "stock": {
                    "lockStock": stockEnable,
                    "salesStockLockExpireTime": stockIime
                },
                "lowOfQuantity": {
                    "enable": lowOfQuantityEnable,
                    "sound": lowOfQuantitySound,
                    "quantity": lowOfQuantityQuantity
                }
            },
            "postConfigMap": {
                "FACEBOOK": {
                    "message": {
                        "needSendMessage": need_send_message,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": has_interaction_message
                            },
                            "messageButton": has_interaction_message_button
                        },
                        "hasLink": has_link,
                        "noInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": no_interaction_message_first
                            },
                            "firstMessageButton": first_message_button,
                            "secondMessageButton": second_message_button,
                            "secondMessageTemplate": {
                                "topMessage": second_message
                            }
                        },
                        "messageType": "MESSAGE"
                    }
                },
                "SHOPLINE": {
                    "message": {
                        "needSendMessage": need_send_message,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": has_interaction_message
                            },
                            "messageButton": has_interaction_message_button
                        },
                        "hasLink": has_link,
                        "noInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": no_interaction_message_first
                            },
                            "firstMessageButton": first_message_button,
                            "secondMessageButton": second_message_button,
                            "secondMessageTemplate": {
                                "topMessage": second_message
                            }
                        },
                        "messageType": "MESSAGE"
                    }
                }
            }
        }
    elif platform in ("pl", "obc"):
        platformSubType = platform.upper()
        platform = "SHOPLINE"
        body = {
            "sales": {
                "title": title,
                "salesOwner": salesOwner,
                "salesDescription": salesDescription,
                "platforms": [
                    platform
                ],
                "platformChannels": [],
                "startTime": startTime,
                "endTime": endTime,
                "platformSubType": platformSubType
            },
            "salesConfig": {
                "patternModel": {
                    "patternModel": patternModel,
                    "keywordValidInLive": keywordValidInLive,
                    "keywordValidAfterLive": keywordValidAfterLive
                },
                "autoNotifyPay": {
                    "enable": autoNotifyPayEnable,
                    "message": autoNotifyPayMessage,
                    "button": autoNotifyPayButton
                },
                "stock": {
                    "lockStock": stockEnable,
                    "salesStockLockExpireTime": stockIime
                },
                "lowOfQuantity": {
                    "enable": lowOfQuantityEnable,
                    "sound": lowOfQuantitySound,
                    "quantity": lowOfQuantityQuantity
                }
            },
            "postConfigMap": {}
        }
    elif platform.lower in ("line&pl", "line&obc", "pl&line", "obc&line"):
        shopId, platformChannelId, platformChannelName, response = get_line_info(data)
        if platform.lower in ("line&pl", "pl&line"):
            type = "PL"
        else:
            type = "OBC"
        needArchive = data.get("needArchive", True)
        visibleTime = data.get("visibleTime", get_stamp_time(**{"days": 60}))
        startTime = data.get("startTime", get_stamp_time(**{"minutes": 1}))
        endTime = data.get("startTime", get_stamp_time(**{"minutes": 2}))
        body = {
            "sales": {
                "title": title,
                "salesOwner": salesOwner,
                "salesDescription": salesDescription,
                "platforms": [
                    "LINE"
                ],
                "platformSubType": type,
                "platformChannels": [
                    {
                        "platform": "LINE",
                        "platformChannelName": shopId,
                        "platformChannelId": shopId
                    }
                ],
                "coverImage": "https://img.shoplineapp.com/media/image_clips/67a5678419ad34003b97243c/original.jpeg?1738893188",
                "startTime": startTime,
                "endTime": endTime,
                "archivedStreamVisibleTime": visibleTime,
                "needArchive": needArchive
            },
            "salesConfig": {
                "patternModel": {
                    "patternModel": patternModel,
                    "keywordValidInLive": keywordValidInLive,
                    "keywordValidAfterLive": keywordValidAfterLive
                },
                "autoNotifyPay": {
                    "enable": False
                },
                "stock": {
                    "lockStock": stockEnable,
                    "salesStockLockExpireTime": stockExpireTime
                },
                "lowOfQuantity": {
                    "enable": False,
                    "sound": False
                }
            },
            "postConfigMap": {
                "LINE": {
                    "message": {
                        "needSendMessage": False,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": ""
                            },
                            "messageButton": ""
                        },
                        "hasLink": True,
                        "noInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": ""
                            },
                            "firstMessageButton": "",
                            "secondMessageTemplate": {
                                "topMessage": ""
                            },
                            "secondMessageButton": ""
                        },
                        "messageType": "MESSAGE"
                    }
                }
            }
        }

    count = 0
    # print(body)
    while True:
        response = requests.post(url, headers=headers, json=body)
        # print(response.json())
        if response.status_code == 200 and response.json()["code"] == "SUCCESS":
            sales_id = response.json()["data"]["sales"]["id"]
            return sales_id
        else:
            time.sleep(1)
            count = count + 1
        if count > 10:
            platform = "facebook"
            status = 0
            if "platform" in data:
                platform = data["platform"]
            if "status" in data:
                status = data["status"]
            data["platform"] = platform
            data["status"] = status
            sales_id, __ = get_sales_id(data)
            return sales_id

    # print(json.dumps(body))


def get_stamp_time(data):
    # 拿到指定时间的时间戳
    num = data.get("num", 2)
    time_type = data.get("time_type", "add")
    unit = data.get("unit", "minutes")
    # 获取当前 UTC 时间
    now = datetime.datetime.now()
    if time_type not in {"add", "sub"}:
        raise ValueError("Invalid time_type. Use 'add' or 'sub'.")
    stamp_time = now + datetime.timedelta(**{unit: num if time_type == "add" else -num})
    return int(stamp_time.timestamp() * 1000)


def get_line_info(data):
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales/lineConnectInfo" % env
    response = requests.get(url, headers=headers).json()
    shopId = response["data"]["shopInfo"]["shopId"]
    platformChannelId = response["data"]["channel"]["platformChannelId"]
    platformChannelName = response["data"]["channel"]["platformChannelName"]
    return shopId, platformChannelId, platformChannelName, response


def add_live(data):
    """fb——group 链接帖文"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s/addLive" % (env, sales_id)
    platform = data.get("platform", "FB_GROUP")
    body = {}
    if platform.upper() == "FB_GROUP":
        pageId = data["page_id"]
        relationUrl = data["relationUrl"]
        body = {
            "pageId": pageId,
            "platform": "FB_GROUP",
            "relationUrl": relationUrl
        }
    elif platform.upper() == "FACEBOOK":
        postId = data["post_id"]
        liveVideoId = data["liveVideoId"]
        pageId = data["page_id"]
        pageName = data["page_name"]
        permalinkUrl = data["permalinkUrl"]
        body = {
            "postId": postId,
            "liveVideoId": liveVideoId,
            "pageId": pageId,
            "pageName": pageName,
            "permalinkUrl": permalinkUrl,
            "status": "LIVE",
            "platform": platform.upper()
        }
    response = requests.post(url, headers=headers, json=body).json()
    return response


def edit_live_info(data):
    """
    直播前编辑直播间信息:prepare
    直播中编辑直播间信息:progress
    """
    stamp = int(time.time())
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s" % (env, sales_id)
    title = "接口编辑的直播活动名称%d" % stamp
    salesDescription = "接口编辑的直播活动介绍%d" % stamp
    salesOwner = "接口编辑的直播主%d" % stamp
    patternModel = "INCLUDE_MATCH"
    keywordValidInLive = True
    keywordValidAfterLive = False
    autoNotifyPayEnable = False
    autoNotifyPayMessage = ""
    autoNotifyPayButton = ""
    autoNotifyPayTime = None
    stockEnable = False
    stockPreTime = None
    stockExpireTime = None
    lowOfQuantityEnable = False
    lowOfQuantitySound = False
    lowOfQuantityQuantity = "1"
    has_interaction_message = ""
    has_interaction_message_button = ""
    no_interaction_message_first = ""
    second_message = ""
    first_message_button = ""
    second_message_button = "️"
    need_send_message = True
    has_link = True
    commentIntent = True
    # 无库存讯息
    allOutOfStockMessage = ""
    allOutOfStockEnable = True
    # 欢迎讯息
    welcomeMessage = ""
    welcomeMessageEnable = True
    # 欢迎comment
    welcomeComment = ""
    welcomeCommentEnable = True
    productRecommendMessage = ""
    productRecommendMessageEnable = True
    platform = "FB_GROUP"
    type = "prepare"
    type = data.get("type", type)
    title = data.get("title", title)
    salesDescription = data.get("salesDescription", salesDescription)
    salesOwner = data.get("salesOwner", salesOwner)
    platform = data.get("platform", platform)
    patternModel = data.get("patternModel", patternModel)
    keywordValidAfterLive = data.get("keywordValidAfterLive", keywordValidAfterLive)
    keywordValidInLive = data.get("keywordValidInLive", keywordValidInLive)

    autoNotifyPayEnable = data.get("autoNotifyPayEnable", autoNotifyPayEnable)
    autoNotifyPayMessage = data.get("autoNotifyPayMessage", autoNotifyPayMessage)
    autoNotifyPayButton = data.get("autoNotifyPayButton", autoNotifyPayButton)
    autoNotifyPayTime = data.get("autoNotifyPayTime", autoNotifyPayTime)

    stockEnable = data.get("stockEnable", stockEnable)
    stockExpireTime = data.get("stockExpireTime", stockExpireTime)

    lowOfQuantityEnable = data.get("lowOfQuantityEnable", lowOfQuantityEnable)
    lowOfQuantitySound = data.get("lowOfQuantitySound", lowOfQuantitySound)
    lowOfQuantityQuantity = data.get("lowOfQuantityQuantity", lowOfQuantityQuantity)

    has_interaction_message = data.get("has_interaction_message", has_interaction_message)
    has_interaction_message_button = data.get("has_interaction_message_button", has_interaction_message_button)
    no_interaction_message_first = data.get("no_interaction_message_first", no_interaction_message_first)
    first_message_button = data.get("first_message_button", first_message_button)
    second_message = data.get("second_message", second_message)
    second_message_button = data.get("second_message_button", second_message_button)
    need_send_message = data.get("need_send_message", need_send_message)
    has_link = data.get("has_link", has_link)
    commentIntent = data.get("commentIntent", commentIntent)

    allOutOfStockMessage = data.get("allOutOfStockMessage", allOutOfStockMessage)
    allOutOfStockEnable = data.get("allOutOfStockEnable", allOutOfStockEnable)
    welcomeMessage = data.get("welcomeMessage", welcomeMessage)
    welcomeMessageEnable = data.get("welcomeMessageEnable", welcomeMessageEnable)
    welcomeComment = data.get("welcomeComment", welcomeComment)
    welcomeCommentEnable = data.get("welcomeCommentEnable", welcomeCommentEnable)
    productRecommendMessage = data.get("productRecommendMessage", productRecommendMessage)
    productRecommendMessageEnable = data.get("productRecommendMessageEnable", productRecommendMessageEnable)

    platformChannels = []
    startTime = None
    endTime = None
    body = {}
    if type == "progress":
        # 进行中不允许修改基础设置、关键子下单设置、保留库存、
        res = get_live_info(data)
        title = res["data"]["sales"]["post_sales_title"]
        salesOwner = res["data"]["sales"]["post_sales_owner"]
        salesDescription = res["data"]["sales"]["post_sales_title"]
        patternModel = res["data"]["salesConfig"]["patternModel"]["patternModel"]
        keywordValidInLive = res["data"]["salesConfig"]["patternModel"]["keywordValidInLive"]
        keywordValidAfterLive = res["data"]["salesConfig"]["patternModel"]["keywordValidAfterLive"]
        if "start_time_timestamp" in res["data"]["sales"]:
            startTime = res["data"]["sales"]["start_time_timestamp"]
        if "end_time_timestamp" in res["data"]["sales"]:
            endTime = res["data"]["sales"]["end_time_timestamp"]
        relatedPostList = res["data"]["relatedPostList"]
        for relatedPost in relatedPostList:
            platformChannelName = relatedPost["page_name"]
            platformChannelId = relatedPost["page_id"]
            platformChannel = {
                "platformChannelName": platformChannelName,
                "platformChannelId": platformChannelId,
                "platform": platform.upper()
            }
            platformChannels.append(platformChannel)
    if platform.upper() == "FB_GROUP":
        body = {
            "sales": {
                "title": title,
                "salesOwner": salesOwner,
                "salesDescription": salesDescription,
                "platforms": [
                    platform
                ],
                "platformSubType": "",
                "platformChannels": [],
                "archivedStreamVisibleTime": None
            },
            "salesConfig": {
                "patternModel": {
                    "patternModel": patternModel,
                    "keywordValidInLive": keywordValidInLive,
                    "keywordValidAfterLive": keywordValidAfterLive
                },
                "autoNotifyPay": {
                    "enable": autoNotifyPayEnable,
                    "notifyTime": autoNotifyPayTime,
                    "message": autoNotifyPayMessage,
                    "button": autoNotifyPayButton
                },
                "stock": {
                    "lockStock": stockEnable,
                    "salesStockLockExpireTime": stockExpireTime,
                    "salesStockLockPreTime": stockPreTime
                },
                "commentIntent": {
                    "enabled": commentIntent
                },
                "variationToggleOn": {
                    "enable": True
                },
                "productSort": {
                    "productSort": "NEW_TO_OLD"
                },
                "lowOfQuantity": {
                    "enable": lowOfQuantityEnable,
                    "sound": lowOfQuantitySound,
                    "quantity": lowOfQuantityQuantity
                },
                "notice": None,
                "frontLive": None,
                "liveViewSdk": None,
                "runningLightsConfig": None,
                "fbGroupSettingConfig": {
                    "scGroupPmCommentId": True,
                    "scGroupWebhook": True
                },
                "productPinningStyle": None
            },
            "postConfigMap": {
                platform: {
                    "message": {
                        "needSendMessage": need_send_message,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": has_interaction_message
                            },
                            "messageButton": has_interaction_message_button
                        },
                        "hasLink": has_link,
                        "noInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": no_interaction_message_first
                            },
                            "firstMessageButton": first_message_button,
                            "secondMessageTemplate": {
                                "topMessage": second_message
                            },
                            "secondMessageButton": second_message_button
                        },
                        "messageType": "MESSAGE"
                    },
                    "allOutOfStockMessage": {
                        "needSendMessage": allOutOfStockEnable,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": allOutOfStockMessage
                            }
                        },
                        "messageType": "ALL_OUT_OF_STOCK"
                    },
                    "welcomeMessage": {
                        "needSendMessage": welcomeMessageEnable,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": welcomeMessage
                            }
                        },
                        "messageType": "WELCOME_MESSAGE"
                    },
                    "productRecommendMessage": {
                        "needSendMessage": productRecommendMessageEnable,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "message": productRecommendMessage
                            }
                        },
                        "messageType": "PRODUCT_RECOMMEND_FB_MESSAGE"
                    },
                    "welcomeMessageComment": {
                        "needSendMessage": welcomeCommentEnable,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": welcomeComment
                            }
                        },
                        "messageType": "WELCOME_MESSAGE_COMMENT"
                    },
                    "showNumberOfViewers": None,
                    "showShareButton": None
                }
            }
        }
    elif platform.lower() in ("facebook", "instagram"):
        body = {
            "sales": {
                "title": title,
                "salesOwner": salesOwner,
                "salesDescription": salesDescription,
                "platforms": [
                    platform.upper()
                ],
                "platformSubType": "",
                "platformChannels": platformChannels,
                "archivedStreamVisibleTime": None,
                "startTime": startTime,
                "endtTime": endTime
            },
            "salesConfig": {
                "patternModel": {
                    "patternModel": patternModel,
                    "keywordValidInLive": keywordValidInLive,
                    "keywordValidAfterLive": keywordValidAfterLive
                },
                "autoNotifyPay": {
                    "enable": autoNotifyPayEnable,
                    "notifyTime": autoNotifyPayTime,
                    "message": autoNotifyPayMessage,
                    "button": autoNotifyPayButton
                },
                "stock": {
                    "lockStock": stockEnable,
                    "salesStockLockExpireTime": stockExpireTime,
                    "salesStockLockPreTime": stockPreTime
                },
                "commentIntent": {
                    "enabled": commentIntent
                },
                "variationToggleOn": {
                    "enable": True
                },
                "productSort": {
                    "productSort": "NEW_TO_OLD"
                },
                "lowOfQuantity": {
                    "enable": lowOfQuantityEnable,
                    "sound": lowOfQuantitySound,
                    "quantity": lowOfQuantityQuantity
                },
                "notice": None,
                "frontLive": None,
                "liveViewSdk": None,
                "runningLightsConfig": None,
                "fbGroupSettingConfig": None,
                "productPinningStyle": None
            },
            "postConfigMap": {
                platform.upper(): {
                    "message": {
                        "needSendMessage": need_send_message,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": has_interaction_message
                            },
                            "messageButton": has_interaction_message_button
                        },
                        "hasLink": has_link,
                        "noInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": no_interaction_message_first
                            },
                            "firstMessageButton": first_message_button,
                            "secondMessageTemplate": {
                                "topMessage": second_message
                            },
                            "secondMessageButton": second_message_button
                        },
                        "messageType": "MESSAGE"
                    },
                    "allOutOfStockMessage": {
                        "needSendMessage": allOutOfStockEnable,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": allOutOfStockMessage
                            }
                        },
                        "messageType": "ALL_OUT_OF_STOCK"
                    },
                    "welcomeMessage": {
                        "needSendMessage": welcomeMessageEnable,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": welcomeMessage
                            }
                        },
                        "messageType": "WELCOME_MESSAGE"
                    },
                    "productRecommendMessage": {
                        "needSendMessage": productRecommendMessageEnable,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "message": productRecommendMessage
                            }
                        },
                        "messageType": "PRODUCT_RECOMMEND_FB_MESSAGE"
                    },
                    "welcomeMessageComment": {
                        "needSendMessage": welcomeCommentEnable,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": welcomeComment
                            }
                        },
                        "messageType": "WELCOME_MESSAGE_COMMENT"
                    },
                    "showNumberOfViewers": None,
                    "showShareButton": None
                }
            }
        }
    print(body)
    response = requests.put(url, headers=headers, json=body).json()
    return response


def save_global_config(data):
    "保存直播间通用配置"
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales/global/LIVE" % env
    patternModel = "INCLUDE_MATCH"
    keywordValidInLive = True
    keywordValidAfterLive = False
    autoNotifyPayEnable = False
    autoNotifyPayMessage = ""
    autoNotifyPayButton = ""
    autoNotifyPayTime = None
    stockEnable = False
    stockPreTime = None
    stockExpireTime = None
    lowOfQuantityEnable = False
    lowOfQuantitySound = False
    lowOfQuantityQuantity = "1"
    has_interaction_message = ""
    has_interaction_message_button = ""
    no_interaction_message_first = ""
    second_message = ""
    first_message_button = ""
    second_message_button = " ️"
    need_send_message = True
    has_link = True
    commentIntent = True
    # 无库存讯息
    allOutOfStockMessage = ""
    allOutOfStockEnable = True
    # 欢迎讯息
    welcomeMessage = ""
    welcomeMessageEnable = True
    # 欢迎comment
    welcomeComment = ""
    welcomeCommentEnable = True
    # 推荐讯息
    fbProductRecommendMessage = ""
    igProductRecommendMessage = ""
    slProductRecommendMessage = ""
    # productRecommendMessageEnable = True
    # 视频观看人数
    show_number = True
    show_share = True
    stamp = int(time.time())
    title = "直播间标题%d" % stamp
    salesDescription = "直播间描述%d" % stamp
    salesOwner = "直播间主%d" % stamp
    platform = "FACEBOOK"
    title = data.get("title", title)
    salesDescription = data.get("salesDescription", salesDescription)
    salesOwner = data.get("salesOwner", salesOwner)
    platform = data.get("platform", platform)
    patternModel = data.get("patternModel", patternModel)
    keywordValidInLive = data.get("keywordValidInLive", keywordValidInLive)
    keywordValidAfterLive = data.get("keywordValidAfterLive", keywordValidAfterLive)

    autoNotifyPayEnable = data.get("autoNotifyPayEnable", autoNotifyPayEnable)
    autoNotifyPayMessage = data.get("autoNotifyPayMessage", autoNotifyPayMessage)
    autoNotifyPayButton = data.get("autoNotifyPayButton", autoNotifyPayButton)
    autoNotifyPayTime = data.get("autoNotifyPayTime", autoNotifyPayTime)

    stockEnable = data.get("stockEnable", stockEnable)
    stockExpireTime = data.get("stockExpireTime", stockExpireTime)

    lowOfQuantityEnable = data.get("lowOfQuantityEnable", lowOfQuantityEnable)
    lowOfQuantitySound = data.get("lowOfQuantitySound", lowOfQuantitySound)
    lowOfQuantityQuantity = data.get("lowOfQuantityQuantity", lowOfQuantityQuantity)

    has_interaction_message = data.get("has_interaction_message", has_interaction_message)
    has_interaction_message_button = data.get("has_interaction_message_button", has_interaction_message_button)
    no_interaction_message_first = data.get("no_interaction_message_first", no_interaction_message_first)
    first_message_button = data.get("first_message_button", first_message_button)
    second_message = data.get("second_message", second_message)
    second_message_button = data.get("second_message_button", second_message_button)
    need_send_message = data.get("need_send_message", need_send_message)
    has_link = data.get("has_link", has_link)
    commentIntent = data.get("commentIntent", commentIntent)

    allOutOfStockMessage = data.get("allOutOfStockMessage", allOutOfStockMessage)
    allOutOfStockEnable = data.get("allOutOfStockEnable", allOutOfStockEnable)

    welcomeMessage = data.get("welcomeMessage", welcomeMessage)
    welcomeMessageEnable = data.get("welcomeMessageEnable", welcomeMessageEnable)

    welcomeComment = data.get("welcomeComment", welcomeComment)
    welcomeCommentEnable = data.get("welcomeCommentEnable", welcomeCommentEnable)

    show_number = data.get("show_number", show_number)
    show_share = data.get("show_share", show_share)

    fbProductRecommendMessage = data.get("fbProductRecommendMessage", fbProductRecommendMessage)
    igProductRecommendMessage = data.get("igProductRecommendMessage", igProductRecommendMessage)
    slProductRecommendMessage = data.get("slProductRecommendMessage", slProductRecommendMessage)

    body = {
        "saveList": [
            {
                "configKey": "PATTERN_MODEL",
                "configValue": {
                    "patternModel": patternModel,
                    "keywordValidInLive": keywordValidInLive,
                    "keywordValidAfterLive": keywordValidAfterLive
                }
            },
            {
                "configKey": "STOCK",
                "configValue": {
                    "lockStock": stockEnable,
                    "salesStockLockExpireTime": stockExpireTime
                }
            },
            {
                "configKey": "LOW_OF_QUANTITY",
                "configValue": {
                    "enable": lowOfQuantityEnable,
                    "sound": lowOfQuantitySound,
                    "quantity": lowOfQuantityQuantity
                }
            },
            {
                "configKey": "MESSAGE",
                "configValue": {
                    "needSendMessage": need_send_message,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": has_interaction_message
                        },
                        "messageButton": has_interaction_message_button
                    },
                    "hasLink": has_link,
                    "noInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": no_interaction_message_first
                        },
                        "firstMessageButton": first_message_button,
                        "secondMessageTemplate": {
                            "topMessage": second_message
                        },
                        "secondMessageButton": second_message_button
                    },
                    "messageType": "MESSAGE"
                }
            },
            {
                "configKey": "WELCOME_MESSAGE",
                "configValue": {
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": welcomeMessage
                        }
                    },
                    "needSendMessage": welcomeMessageEnable,
                    "messageType": "WELCOME_MESSAGE"
                }
            },
            {
                "configKey": "WELCOME_MESSAGE_COMMENT",
                "configValue": {
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": welcomeComment
                        }
                    },
                    "needSendMessage": welcomeCommentEnable,
                    "messageType": "WELCOME_MESSAGE_COMMENT"
                }
            },
            {
                "configKey": "PRODUCT_RECOMMEND_FB_MESSAGE",
                "configValue": {
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "message": fbProductRecommendMessage
                        }
                    },
                    "messageType": "PRODUCT_RECOMMEND_FB_MESSAGE"
                }
            },
            {
                "configKey": "PRODUCT_RECOMMEND_IG_MESSAGE",
                "configValue": {
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "message": igProductRecommendMessage
                        }
                    },
                    "messageType": "PRODUCT_RECOMMEND_IG_MESSAGE"
                }
            },
            {
                "configKey": "PRODUCT_RECOMMEND_SHOP_LINE_MESSAGE",
                "configValue": {
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "message": slProductRecommendMessage
                        }
                    },
                    "messageType": "PRODUCT_RECOMMEND_SHOP_LINE_MESSAGE"
                }
            },
            {
                "configKey": "ALL_OUT_OF_STOCK",
                "configValue": {
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": allOutOfStockMessage
                        }
                    },
                    "needSendMessage": allOutOfStockEnable,
                    "messageType": "ALL_OUT_OF_STOCK"
                }
            },
            {
                "configKey": "AUTO_NOTIFY_PAY",
                "configValue": {
                    "enable": autoNotifyPayEnable,
                    "message": autoNotifyPayMessage,
                    "button": autoNotifyPayButton
                }
            },
            {
                "configKey": "COMMENT_INTENT",
                "configValue": {
                    "enabled": commentIntent
                }
            },
            {
                "configKey": "SHOW_NUMBER_OF_VIEWERS",
                "configValue": {
                    "enabled": show_number
                }
            },
            {
                "configKey": "SHOW_SHARE_BUTTON",
                "configValue": {
                    "enabled": show_share
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=body).json()
    return response


def get_global_config(data):
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales/global/LIVE" % env
    response = requests.get(url, headers=headers).json()
    # print(response)
    return response


def remove_live_product(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    url = "%s/api/posts/post/sales/%s/product/%s" % (env, sales_id, product_id)
    response = requests.delete(url, headers=headers).json()
    return response


def change_keyword_status(data):
    """生效普通商品状态"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    status = "true"
    if "status" in data:
        status = data["status"]
    url = "%s/api/posts/post/sales/%s/product/keyword/status/%s" % (env, sales_id, status)
    body = {
        "spuIdList": [
            product_id
        ]
    }
    response = requests.put(url, headers=headers, json=body).json()
    return response


def delete_product_set(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set" % (env, sales_id)
    body = {
        "ids": [
            product_id
        ]
    }
    res = requests.delete(url, headers=headers, json=body).json()
    return res


# 查询普通商品列表
def get_live_product(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    query = ""
    if "query" in data:
        query = data["query"]
    url = "%s/api/posts/post/sales/%s/product/v2" % (env, sales_id)
    params = {"salesId": sales_id, "pageIndex": 1, "pageSize": 25, }
    if query != "":
        params["queryType"] = "PRODUCT_NAME"
        params["query"] = query
    response = requests.get(url, headers=headers, params=params).json()
    return response


def search_product_set(data):
    """查询直播间组合商品列表"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    query = ""
    pageNum = 1
    pageNum = data.get("pageNum", pageNum)
    query = data.get("query", query)
    url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set" % (env, sales_id)
    param = {"pageNum": pageNum, "pageSize": 10, "query": query, "queryType": "PRODUCT_NAME"}
    # print(param)
    res = requests.get(url, headers=headers, params=param).json()
    return res


def get_product_set(data):
    """查询来添加组合商品"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    query = ""
    pageNum = 1
    pageNum = data.get("pageNum", pageNum)
    query = data.get("query", query)
    url = "%s/admin/api/bff-web/live/sale/%s/product/product_set/list" % (env, sales_id)
    param = {"pageNum": pageNum, "pageSize": 10, "query": query}
    # print(param)
    count = 0
    while True:
        res = requests.get(url, headers=headers, params=param)
        if res.status_code == 200:
            return res.json()
        else:
            count += 1
            if count > 10:
                print("查询get_product_set 异常")
                return res


def get_sales_keyword(data):
    """查询直播间关键字"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/admin/api/bff-web/live/sale/%s/keyword/list" % (env, sales_id)
    res = requests.get(url, headers=headers).json()
    return res


def get_stock_product_set(res, type="stock"):
    """直播间查询OA组合商品信息
    stock:查询有库存
    out:查询无库存
    """
    list_data = res["data"]["list"]
    if type == "stock":
        for i in list_data:
            combinationList = i["combinationList"]
            for combination in combinationList:
                products = combination["products"]
                for product in products:
                    count = product["count"]
                    quantity = product["quantity"]
                    if quantity == -1:
                        # print("库存无限数量")
                        pass
                    elif quantity < count:
                        break
                    keyword = combination["keywords"][0]
                    product_id = i["id"]
                    combination_id = combination["id"]
                    return keyword, product_id, combination_id, i
    elif type == "out":
        for i in list_data:
            combinationList = i["combinationList"]
            for combination in combinationList:
                products = combination["products"]
                for product in products:
                    count = product["count"]
                    quantity = product["quantity"]
                    if quantity != -1 and quantity < count:
                        keyword = combination["keywords"][0]
                        product_id = i["id"]
                        combination_id = combination["id"]
                        return keyword, product_id, combination_id, i


def change_product_set_keyword_status(data):
    "修改组合商品关键字生效状态"
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    status = True
    if "status" in data:
        status = data["status"]
    url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set/keyword/status" % (env, sales_id)
    body = {
        "ids": [
            product_id
        ],
        "status": status
    }
    response = requests.put(url, headers=headers, json=body).json()
    return response


def get_produnct_set_detail(data):
    """直播间查询OA组合商品详情"""
    # print(data)
    env = data["env"]
    headers = data["headers"]
    product_id = data["product_id"]
    sales_id = data["sales_id"]
    url = "%s/admin/api/bff-web/live/sale/%s/product/product_set/%s" % (env, sales_id, product_id)
    # print(url)
    count = 0
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            count += 1
            if count > 10:
                print("查询get_produnct_set_detail 异常")
                return response


def add_product_set_to_live(data):
    "添加组合商品到直播间"
    global title
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    keyword = data.get("keyword", "python添加商品关键子%d" % int(time.time()))
    product_id = data.get("product_id", "")
    if product_id == "":
        set_list_res = get_product_set(data)
        data_list = set_list_res["data"]["list"]
        arr = 0
        if "arr" in data:
            arr = data["arr"]
            if arr > len(data_list) - 1:
                arr = 0
        product_info = data_list[arr]
        product_id = product_info["id"]
        childrenInfo = product_info["childrenInfo"]
        title = product_info["title"]
        spu_ids = list(childrenInfo.keys())
        # necessaryQuantitys  = jsonpath(data_list, "$..necessaryQuantity")
        data["product_id"] = product_id
    # 查询组合商品详情信息
    response = get_produnct_set_detail(data)
    # print(response)
    products = []
    zi_list = response["data"]
    # print(zi_list)
    childrenInfo = zi_list["childrenInfo"]
    childrenProducts = zi_list["childrenProducts"]
    for children in childrenProducts:
        # print(children)
        product = {}
        spu_id = children["id"]
        product["count"] = childrenInfo[spu_id]["necessaryQuantity"]
        product["spuId"] = spu_id
        variations = children["variations"]
        if variations == []:
            product["skuId"] = spu_id
        else:
            sku_id = variations[0]["id"]
            product["skuId"] = sku_id
        products.append(product)

    url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set" % (env, sales_id)
    # keyword = "python添加商品关键子%d" % int(time.time())
    if isinstance(keyword, str):
        add_body = {
            "spuList": [
                {
                    "id": "%s" % product_id,
                    "defaultKey": "",
                    "combinationList": [
                        {
                            "products": products,
                            "keywords": [
                                "%s" % keyword
                            ],
                            "skuId": ""
                        }
                    ]
                }
            ]
        }
    else:
        add_body = {
            "spuList": [
                {
                    "id": "%s" % product_id,
                    "defaultKey": "",
                    "combinationList": [
                        {
                            "products": products,
                            "keywords": keyword,
                            "skuId": ""
                        }
                    ]
                }
            ]
        }
    print(add_body)
    try:
        # 先删除再添加
        data["product_id"] = product_id
        delete_product_set(data)
        time.sleep(2)
        data_res = requests.post(url, headers=headers, json=add_body).json()
        # print(data_res)
        return product_id, products, keyword, title, data_res
    except Exception:
        print("出现异常")


def add_all_product_set_to_live(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    while True:
        print(data)
        set_list_res = get_product_set(data)
        print(set_list_res)
        data_list = set_list_res["data"]["list"]
        for product_info in data_list:
            product_id = product_info["id"]
            childrenInfo = product_info["childrenInfo"]
            spu_ids = list(childrenInfo.keys())
            # necessaryQuantitys  = jsonpath(data_list, "$..necessaryQuantity")
            data["spu_ids"] = spu_ids
            # 查询子商品信息
            response = get_produnct_set_detail(data)
            products = []
            zi_list = response["data"]["list"]
            # print(vars["childrenInfo"])
            for i in zi_list:
                product = {}
                spu_id = i["id"]
                product["count"] = childrenInfo[spu_id]["necessaryQuantity"]
                product["spuId"] = spu_id
                variations = i["variations"]
                if variations == []:
                    product["skuId"] = spu_id
                else:
                    sku_id = variations[0]["id"]
                    product["skuId"] = sku_id
                products.append(product)
            url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set" % (env, sales_id)
            keyword = "python添加商品关键子%d" % int(time.time())
            add_body = {
                "spuList": [
                    {
                        "id": "%s" % product_id,
                        "defaultKey": "",
                        "combinationList": [
                            {
                                "products": products,
                                "keywords": [
                                    "%s" % keyword
                                ],
                                "skuId": ""
                            }
                        ]
                    }
                ]
            }
            try:
                data_res = requests.post(url, headers=headers, json=add_body).json()
                print(data_res)
            except Exception:
                print("出现异常")
        lastPage = set_list_res["data"]["pageInfo"]["lastPage"]
        pageNum = set_list_res["data"]["pageInfo"]["pageNum"]
        # print("加前的pagenum",pageNum)
        # print(lastPage)
        if lastPage == False:
            pageNum = pageNum + 1
            data["pageNum"] = pageNum
            print("pageNum=", pageNum)
        else:
            break


def add_all_product_set_to_keyword(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    while True:
        print(data)
        set_list_res = get_product_set(data)
        print(set_list_res)
        data_list = set_list_res["data"]["list"]
        for product_info in data_list:
            product_id = product_info["id"]
            childrenInfo = product_info["childrenInfo"]
            spu_ids = list(childrenInfo.keys())
            # necessaryQuantitys  = jsonpath(data_list, "$..necessaryQuantity")
            data["spu_ids"] = spu_ids
            # 查询子商品信息
            response = get_produnct_set_detail(data)
            products = []
            zi_list = response["data"]["list"]
            # print(vars["childrenInfo"])
            for i in zi_list:
                product = {}
                spu_id = i["id"]
                product["count"] = childrenInfo[spu_id]["necessaryQuantity"]
                product["spuId"] = spu_id
                variations = i["variations"]
                if variations == []:
                    product["skuId"] = spu_id
                else:
                    sku_id = variations[0]["id"]
                    product["skuId"] = sku_id
                products.append(product)
            url = "%s/admin/api/bff-web/keyword/product_set" % (env)
            keyword = "python添加商品关键子%d" % int(time.time())
            add_body = {
                "productKeywordList": [
                    {
                        "id": "%s" % product_id,
                        "defaultKey": "",
                        "combinationList": [
                            {
                                "products": products,
                                "keywords": [
                                    "%s" % keyword
                                ],
                                "skuId": ""
                            }
                        ]
                    }
                ]
            }
            try:
                data_res = requests.post(url, headers=headers, json=add_body).json()
                print(data_res)
            except Exception:
                print("出现异常")
        lastPage = set_list_res["data"]["pageInfo"]["lastPage"]
        pageNum = set_list_res["data"]["pageInfo"]["pageNum"]
        # print("加前的pagenum",pageNum)
        # print(lastPage)
        if lastPage == False:
            pageNum = pageNum + 1
            data["pageNum"] = pageNum
            print("pageNum=", pageNum)
        else:
            break


def add_auto_reply(data):
    global response
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/auto_reply" % (env, sales_id)
    stamp = int(time.time())
    name = "自动回复工具名称%d" % stamp
    keyword_type = "ANY"
    mode = "BASIC"
    keywords = ["自动回复关键字%d" % stamp]
    commentStatus = True
    messageStatus = True
    commentContent = "留言回复内容%d" % stamp
    messageContent = "私讯回复内容%d" % stamp
    name = data.get("name", name)
    keyword_type = data.get("keyword_type", keyword_type)
    mode = data.get("mode", mode)
    keywords = data.get("keywords", keywords)
    commentStatus = data.get("commentStatus", commentStatus)
    messageStatus = data.get("messageStatus", messageStatus)
    commentContent = data.get("commentContent", commentContent)
    messageContent = data.get("messageContent", messageContent)
    body = {
        "id": "",
        "name": name,
        "keywordMatchType": keyword_type,
        "mode": mode,
        "status": False,
        "keywords": [keywords],
        "answer": {
            "commentStatus": commentStatus,
            "messageStatus": messageStatus,
            "commentContent": commentContent,
            "messageContent": messageContent
        }
    }
    try:
        response = requests.post(url, headers=headers, json=body).json()
        auto_reply_id = response["data"]["id"]
        return auto_reply_id
    except Exception:
        print("创建自动回复失败:", response)


def enable_auto_reply(data):
    global response
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    auto_reply_id = data["auto_reply_id"]
    status = True
    status = data.get("status", status)
    url = "%s/api/posts/post/sales/%s/auto_reply/%s/switch" % (env, sales_id, auto_reply_id)
    body = {
        "status": status
    }
    try:
        response = requests.put(url, headers=headers, json=body).json()
        return response
    except Exception:
        print("更改自动回复状态失败:", response)


def edit_auto_reply(data):
    global response
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    auto_reply_id = data["auto_reply_id"]
    url = "%s/api/posts/post/sales/%s/auto_reply" % (env, sales_id)
    stamp = int(time.time())
    name = "自动回复工具名称%d" % stamp
    keyword_type = "ANY"
    mode = "BASIC"
    keywords = ["自动回复关键字%d" % stamp]
    commentStatus = True
    messageStatus = True
    commentContent = "留言回复内容%d" % stamp
    messageContent = "私讯回复内容%d" % stamp
    name = data.get("name", name)
    keyword_type = data.get("keyword_type", keyword_type)
    mode = data.get("mode", mode)
    keywords = data.get("keywords", keywords)
    commentStatus = data.get("commentStatus", commentStatus)
    messageStatus = data.get("messageStatus", messageStatus)
    commentContent = data.get("commentContent", commentContent)
    messageContent = data.get("messageContent", messageContent)
    body = {
        "id": auto_reply_id,
        "name": name,
        "keywordMatchType": keyword_type,
        "mode": mode,
        "status": False,
        "keywords": [keywords],
        "answer": {
            "commentStatus": commentStatus,
            "messageStatus": messageStatus,
            "commentContent": commentContent,
            "messageContent": messageContent
        }
    }
    try:
        response = requests.put(url, headers=headers, json=body).json()
        return response
    except Exception:
        print("编辑自动回复失败:", response)


def delete_auto_reply(data):
    global response
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    auto_reply_id = data["auto_reply_id"]
    url = "%s/api/posts/post/sales/%s/auto_reply" % (env, sales_id)
    body = {
        "id": auto_reply_id
    }
    try:
        response = requests.delete(url, headers=headers, json=body).json()
        return response
    except Exception:
        print("删除自动回复状态失败:", response)


def handler_auto_reply(data):
    """处理自动回复，避免超过10个，超过10个无法新增"""
    live_info = get_live_info(data)
    autoReplyCommentConfig = live_info["data"]["autoReplyCommentConfig"]["rules"]
    num = data.get("num", 8)
    if len(autoReplyCommentConfig) > num:
        for info in autoReplyCommentConfig:
            auto_reply_id = info["id"]
            data["auto_reply_id"] = auto_reply_id
            delete_auto_reply(data)


def handler_bidding(data):
    "删除在开启中的竞标活动"
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/admin/api/bff-web/live/activity/list/POST/%s" % (env, sales_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        for i in response.json()["data"]:
            status = i["status"]
            activity_type = i["type"]
            if status == "PROGRESS" and activity_type == "BIDDING":
                activity_id = i["id"]
                data["activity_id"] = activity_id
                end_activity(data)
                time.sleep(1)
                delate_activity(data)


def check_14_day(data):
    flag = False
    try:
        response = get_live_info(data)
        code = response["code"]
        if code != "SUCCESS":
            flag = True
            return flag
        else:
            start_time_timestamp = response["data"]["sales"]["start_time_timestamp"]
            # 将毫秒转换为秒
            start_time_timestamp = start_time_timestamp / 1000
            # 计算 14 天的秒数
            fourteen_days_seconds = 13 * 24 * 60 * 60
            # 获取当前时间戳（秒）
            current_time_seconds = time.time()

            if (current_time_seconds - start_time_timestamp) >= fourteen_days_seconds:
                flag = True
            return flag
    except Exception:
        flag = True
        return flag


def get_fb_sales_id(data):
    """"查询返回指定直播间的salse_id
    status:准备中 0，直播中 1 已结束 2 断线中 4
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales" % env
    param = {"page_num": 1, "page_size": 100, "sales_type": "LIVE"}
    platform = data.get("platform", "FACEBOOK")
    param["platforms"] = platform.upper()
    if "search" in data:
        search_word = data["search"]
        param["search_word"] = search_word
    response = requests.get(url, headers=headers, params=param).json()
    sales_data = response["data"]["list"]
    if "status" in data:
        status = data["status"]
        for i in sales_data:
            real_platform = i["platform"]
            platforms = i["platforms"]
            post_sale_status = i["post_sale_status"]
            if real_platform == "SHOPLINE" and platforms == ["SHOPLINE", "FACEBOOK"] and post_sale_status in status:
                sales_id = i["id"]
                return sales_id
            elif platform.upper() == "FACEBOOK" and platforms == ["FACEBOOK"] and post_sale_status in status:
                sales_id = i["id"]
                return sales_id
    else:
        if len(sales_data) > 0:
            return sales_data[0]["id"]


def get_receipt_sales_id(data):
    sales_id = data["sales_id"]
    flag = check_14_day(data)
    if flag:
        # 先从列表查出一个最新结束的直播间，还是不返回要再创建直播和链接直播
        sales_id = get_fb_sales_id(data)
        data["sales_id"] = sales_id
        flag2 = check_14_day(data)
        if flag2:
            # 超过14天，创建一个直播间，并串接，然后结束直播
            data["platform"] = "FACEBOOK"
            sales_id = create_live(data)
            # 串接
            # 先删除已被串接的
            delete_relate_post(data)
            time.sleep(2)
            data["sales_id"] = sales_id
            add_live(data)
            # 结束直播
            end_live(data)
        return sales_id
    else:
        return sales_id


def delete_keyword_product_set(data):
    "删除关键字组件里的组合商品"
    "product_id为：[]"
    env = data["env"]
    headers = data["headers"]
    product_id = data["product_id"]
    url = "%s/admin/api/bff-web/keyword/product_set" % env
    if isinstance(product_id, str):
        product_id = [product_id]
    body = {
        "ids": product_id
    }
    response = requests.delete(url, headers=headers, json=body).json()
    return response


def delete_keyword_product(data):
    "删除关键字组件里的组合商品"
    "product_id为：[]"
    env = data["env"]
    headers = data["headers"]
    product_id = data["product_id"]
    url = "%s/api/posts/common/product/key/spu" % env
    if isinstance(product_id, str):
        product_id = [product_id]
    body = {
        "ids": product_id
    }
    response = requests.delete(url, headers=headers, json=body).json()
    return response


def get_keyword_product_set(data):
    "查询关键字组件里的组合商品"
    env = data["env"]
    headers = data["headers"]
    url = "%s/admin/api/bff-web/keyword/product_set/list" % env
    pageNum = data.get("pageNum", 1)
    pageSize = data.get("pageSize", 25)
    param = {"pageNum": pageNum, "pageSize": pageSize}
    if "title" in data:
        title = data.get("title")
        param["title"] = title
    response = requests.get(url, headers=headers, params=param).json()
    return response


def get_oa_product_set(data):
    "查询OA组合商品列表"
    env = data["env"]
    headers = data["headers"]
    pageNum = data.get("pageNum", 1)
    pageSize = data.get("pageSize", 10)
    param = {"pageNum": pageNum, "pageSize": pageSize}
    if "query" in data:
        query = data.get("query")
        param["query"] = query
    url = "%s/admin/api/bff-web/keyword/product/product_set/list" % env
    response = requests.get(url, headers=headers, params=param).json()
    return response


def get_product_set_detail(data):
    "查询OA组合商品详情信息"
    env = data["env"]
    headers = data["headers"]
    product_id = data["product_id"]
    url = "%s/admin/api/bff-web/keyword/product/product_set/detail?id=%s" % (env, product_id)
    response = requests.get(url, headers=headers).json()
    return response


def get_not_exist_keyword_set(data):
    pageNum = 1
    while True:
        response = get_oa_product_set(data)
        data_list = response["data"]["list"]
        for set in data_list:
            title = set["title"]
            product_id = set["id"]
            data["title"] = title
            res = get_keyword_product_set(data)
            set_id_list = [item["id"] for item in res["data"]["list"]]
            if product_id not in set_id_list:
                return product_id, title
        pageNum += 1
        data["pageNum"] = pageNum


def search_product_by_keyword(data):
    env = data["env"]
    headers = data["headers"]
    keyword = data["keyword"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/product/v2" % (env, sales_id)
    param = {"salesId": sales_id, "pageIndex": 1, "pageSize": 25, "query": keyword, "queryType": "KEYWORD"}
    response = requests.get(url, headers=headers, params=param).json()
    return response


def search_product_set_by_keyword(data):
    env = data["env"]
    headers = data["headers"]
    keyword = data["keyword"]
    sales_id = data["sales_id"]
    url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set" % (env, sales_id)
    param = {"pageNum": 1, "pageSize": 25, "query": keyword, "queryType": "KEYWORD"}
    response = requests.get(url, headers=headers, params=param).json()
    return response


def delete_product_by_keyword(data):
    """根据关键字查询出商品，删除该普通商品和组合商品"""
    response = search_product_by_keyword(data)
    result = response["data"]["product_page_result"]["list"]
    if len(result) > 0:
        spu_id = result[0]["spu_id"]
        data["product_id"] = spu_id
        remove_live_product(data)
    set_response = search_product_set_by_keyword(data)
    set_result = set_response["data"]["list"]
    if len(set_result) > 0:
        set_spu_id = set_result[0]["id"]
        data["product_id"] = set_spu_id
        delete_product_set(data)


def add_product_to_live(data):
    "添加普通商品到直播间"
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    keyword = ["pythonaddkeyword%d" % int(time.time())]
    keyword = data.get("keyword", keyword)
    url = "%s/api/posts/post/sales/%s/products" % (env, sales_id)
    product_id = data["product_id"]
    missCommonKey = data.get("missCommonKey", True)
    customNumber = data.get("customNumber", [])
    type = data.get("type", "spu")
    if isinstance(keyword, str):
        keyword = [keyword]
    if isinstance(customNumber, str):
        customNumber = [customNumber]
    body = {
        "spuList": [
            {
                "spuId": product_id,
                "missCommonKey": missCommonKey,
                "customNumbers": customNumber,
                "keyList": keyword
            }
        ]
    }
    if type == "sku":
        """
        skuList 格式：
        [
        {
            "skuId": "67b5739c05e4b200102ae7bf",
            "missCommonKey": false,
            "keyList": [
                "fb直播间新增的对规格关键字17399448600"
            ]
        },
        {
            "skuId": "67b5739c05e4b200102ae7c0",
            "missCommonKey": false,
            "keyList": [
                "fb直播间新增的对规格关键字17399448601"
            ]
        } ]   
        """
        skuList = data["skuList"]
        body = {
            "spuList": [
                {
                    "spuId": product_id,
                    "missCommonKey": missCommonKey,
                    "customNumbers": customNumber,
                    "skuList": skuList
                }
            ]
        }
    # 添加前先删除直播间的商品
    remove_live_product(data)
    print(body)
    response = requests.post(url, headers=headers, json=body).json()
    return response


def send_comment():
    timStamp = int(time.time())

    # key = "a2f4cae7b637eb42967ef5ab6a6a3ff7"
    # url = "https://front-service.shoplinestg.com/facebook/webhook"
    # post_id = "119305964434044_1342551670179146"
    # page_id = "119305964434044"

    # message = "fb文3本消息%d"%timStamp
    # message = "%d" % random.randint(3, 999)
    message = "哦哦哦哦订单"

    # 生产
    # key = 'a2f4cae7b637eb42967ef5ab6a6a3ff7'
    # url = 'https://front-admin.shoplineapp.com/facebook/webhook'
    # post_id = "119305964434044_1453999779043575"
    # page_id = "107977035056574"

    #预发
    # key = '5e3bba98882fc0fb22a0607238bc5b8f'
    # url = 'https://front-admin-preview.shoplineapp.com/facebook/webhook'
    # post_id = "106411048594439_1764064707792500"
    # page_id = "106411048594439"

    #test
    key = '4f6b54deff90cdc9966cbe7b82731b3b'
    url = 'https://front-service.shoplinestg.com/facebook/webhook'
    post_id = "119305964434044_1453999779043575"
    page_id = "119305964434044"

    randnum = random.randint(1, 1000)
    user_id = "4724508317%d%d" % (timStamp, randnum)
    # user_id = "47245083171744792310"0
    name = "️%d%dtest" % (randnum, timStamp)
    contentbody = {"entry": [{"id": page_id, "time": timStamp, "changes": [{"value": {
        "from": {"id": user_id,"name":name},
        "post": {"status_type": "added_video", "is_published": True, "updated_time": "2024-10-16T13:28:29+0000",
                 "permalink_url": "https://www.facebook.com/161726309710099/videos/3266941630279674",
                 "promotion_status": "inactive", "id": post_id}, "message": message, "post_id": post_id,
        "comment_id": "%s_350%d%d" % (page_id, int(time.time() * 1000), random.randint(4, 1000)),
        "created_time": timStamp, "item": "comment",
        "parent_id": post_id, "verb": "add"}, "field": "feed"}]}], "object": "page"}
    # print("contentbody", contentbody)
    # contentbody["entry"][0]["time"] = time
    print(contentbody)

    signdata = hmac.new(key.encode('utf-8'), json.dumps(contentbody).encode('utf-8'), hashlib.sha1).hexdigest()
    signdata = signdata
    contentbody = json.dumps(contentbody)
    headers = {"Content-Type": "application/json", "x-hub-signature": "sha1=%s" % signdata}
    res = requests.post(url, headers=headers, data=contentbody)
    # print(res.content)
def create_single_product(data):
    """
        新增无规格商品
        :param data:
        :return: 返回新增的商品的spu_id
        """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    quantity = 1000
    if "quantity" in data:
        quantity = data["quantity"]
    url = "%s/api/posts/post/sales/%s/product/create" % (env, sales_id)
    product_name = "post接口新增商品多规格商品名称%d" % int(time.time())
    if "product_name" in data:
        product_name = data["product_name"]
    keyword = "post接口新增商品多规格商品关键字%d" % int(time.time())
    if "keyword" in data:
        keyword = data["keyword"]
    body = {"customNumber": keyword, "quantity": quantity, "unlimitedQuantity": False, "productName": product_name,
            "imageUrl": "https://s3-ap-southeast-1.amazonaws.com/static.shoplineapp.com/sc-admin/product-default.png",
            "price": 3}
    response = requests.post(url, headers=headers, json=body).json()
    spu_id = response["data"]
    return spu_id



def get_bulk_edit_keyword(data):
    global customNumber, pre_keyword, spu
    keyword_type = data.get("keyword_type","keyList")
    if keyword_type=="customNumber":
        customNumber = "前和后关键字%d"%int(time.time())
        customNumber = data.get("customNumber",customNumber)
    elif keyword_type=="keyList":
        pre_keyword = "前缀关键字%d"%int(time.time())
        pre_keyword = data.get("keyList", pre_keyword)
    #拿到直播间商品信息
    response = get_live_product(data)
    product_page_result = response["data"]["product_page_result"]["list"]
    spuList = []
    bulk_edit_body = {"spuList":spuList}
    if product_page_result!=[]:
        for product in product_page_result:
            spu = {}
            product_info = product["product_info"]
            product_id = product_info["id"]
            spu["spuId"] = product_id
            spu["defaultKey"] = ""
            if keyword_type=="customNumber":
                spu["customNumbers"] = [customNumber]
            else:
                spu["customNumbers"] = []
            sku_product_list = product["sku_product_list"]
            sku_list = []
            num = 1
            for sku in sku_product_list:
                sku_dict = {}
                sku_id = sku["sku_id"]
                sku_dict["skuId"] = sku_id
                if keyword_type=="customNumber":
                    sku_dict["keyList"] = []
                else:
                    keyword = pre_keyword+str(num)
                    sku_dict["keyList"] = [keyword]
                    num+=1
                sku_list.append(sku_dict)
            spu["skuList"] = sku_list
            break
        spuList.append(spu)
    else:
        # 给直播间创建商品
        spu_id = create_single_product(data)
        spu = {}
        spu["spuId"] = spu_id
        spu["defaultKey"] = ""
        if keyword_type == "customNumber":
            spu["customNumbers"] = [customNumber]
        else:
            spu["customNumbers"] = []
        skuList = []
        sku = {}
        sku["skuId"] = spu_id
        if keyword_type == "customNumber":
            sku["keyList"] = []
        else:
            sku["keyList"] = [pre_keyword]
        skuList.append(sku)
        spu["skuList"] = skuList
        spuList.append(spu)
    return bulk_edit_body

def  syn_line_product(data):
    "INTRODUCING,HIDDEN、DISPLAYING"
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    line_status = data.get("line_status","HIDDEN")
    url = "%s/api/posts/post/sales/%s/spu/%s/status?status=%s"%(env,sales_id,product_id,line_status)
    response = requests.post(url,headers=headers).json()
    return response


def get_product_detail(data):
    #headers为sc使用的token
    oa_env = data["oa_env"]
    headers = data["headers"]
    product_id = data["product_id"]
    url = "%s/v1/products/%s?strategy=app_token&includes[]=locked_inventory_count"%(oa_env,product_id)
    res = requests.get(url, headers=headers).json()
    return res


def get_live_comment(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    pageSize = data.get("pageSize","3")
    url = "%s/api/posts/post/comments?pageNo=1&pageSize=%s&salesId=%s"%(env,pageSize,sales_id)
    platform = data.get("platform")
    page_id = data.get("page_id")
    if platform !=None and page_id!=None:
        url = "%s/api/posts/post/comments?pageNo=1&pageSize=%s&salesId=%s&platform=%s&pageId=%s"%(env,pageSize,sales_id,platform,page_id)
    response = requests.get(url,headers=headers).json()
    return response["data"]["list"]

def line_bind_webhook(data):
    env = data["env"]
    url = "%s/dc/webhook/line/user/bind"%env
    line_user_info = data["line_user_info"]
    merchant_id = line_user_info["merchant_id"]
    ecid = line_user_info["ecid"]
    line_user_id = line_user_info["line_user_id"]
    ec_user_id = line_user_info["ec_user_id"]
    sales_id = line_user_info["sales_id"]
    body = {
          "event": "Customer",
          "merchant_id": merchant_id,
          "topic": "customer/bind_line_live_user",
          "trace_id": "a2af56da-6218-4bf2-b825-8fcfd212e0be",
          "ts": "1731232573927498500",
          "resource": {
            "ecid": ecid,
            "line_user_id": line_user_id,
            "ec_user_id": ec_user_id,
            "live_event_id": sales_id,
            "sale_event_id": sales_id
          },
          "retry_count": 0
            }

    response = requests.post(url,json=body,headers={"Content-Type":"application/json"})


def get_live_global(data):
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales/global/LIVE"%env
    res = requests.get(url, headers=headers).json()
    return res








if __name__ == "__main__":
   pass







