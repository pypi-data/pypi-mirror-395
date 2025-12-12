import datetime
import requests
import json
from jsonpath import jsonpath
import time
import random
import hmac
from hashlib import sha1
import random
# from Platform import Platform
import itertools



platform = "FACEBOOK"
count = 0
num = 100
def create_general_post(data):
    """创建普通贴文销售，返回响应和贴文销售ID
    sc_common_interface
    platform："FACEBOOK"、"INSTAGRAM"、"FB_GROUP"
    patternModel:
    INCLUDE_MATCH：模式1-留言包含 关键字 或 关键字+数量
    WITH_QTY_MATCH：模式2-留言包含 关键字+数量
    EXACT_MATCH：模式3-留言只有 关键字 或 关键字+数量
    WITH_SPU_MATCH:模式4-留言包含 商品编号+规
    title 不是必填
    """
    global response
    env = data["env"]
    headers = data["headers"]
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    patternModel = "INCLUDE_MATCH"
    if "patternModel" in data:
        patternModel = data["patternModel"]
    title = "接口自动化创建的普通贴文%d"%int(time.time())
    if "title" in data:
        title = data["title"]
    url = "%s/api/posts/post/sales/create"%env
    body = {
      "platform": platform,
      "type": 1,
      "platforms": [
          platform
      ],
      "title": title,
      "patternModel": patternModel
         }
    count = 0
    while True:
        try:
            response = requests.post(url,headers=headers,json=body)
            # print("响应码",response.status_code)
            if response.status_code==200:
                break
        except Exception as e:
            print(e)
            time.sleep(1)
        finally:
            count += 1
        if count > num:
            break
    response = response.json()
    # print("创建贴文返回",response)
    sales_id = response["data"]["id"]
    return response,sales_id

def create_commerce_post(data):
    """创建留言串销售贴文，返回响应和贴文销售ID
    platform："FACEBOOK"、"INSTAGRAM"、"FB_GROUP"
    patternModel:
    INCLUDE_MATCH：模式1-留言包含 关键字 或 关键字+数量
    WITH_QTY_MATCH：模式2-留言包含 关键字+数量
    EXACT_MATCH：模式3-留言只有 关键字 或 关键字+数量
    WITH_SPU_MATCH:模式4-留言包含 商品编号+规
    title 不是必填
    """

    global response
    env = data["env"]
    headers = data["headers"]
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    # platform = data["platform"]
    patternModel = "INCLUDE_MATCH"
    if "patternModel" in data:
        patternModel = data["patternModel"]
    title = "接口自动化创建的留言串销售贴文%d" % int(time.time())
    if "title" in data:
        title = data["title"]
    url = "%s/api/posts/post/sales/create"%env
    body = {
      "platform": platform,
      "type": 1,
      "platforms": [
          platform
      ],
      "title": title,
      "patternModel": patternModel,
      "postSubType": "COMMERCE_STACK"
         }
    count = 0
    while True:
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(1)
        finally:
            count +=1
        if count>num:
            break
    response = response.json()
    # print(response)
    sales_id = response["data"]["id"]
    return response,sales_id


def change_dict_into_hump(json_data):
    if isinstance(json_data, dict):
        new_data = {}
        for key, value in json_data.items():
            components = key.split('_')
            new_key = components[0] + ''.join(x.title() for x in components[1:])
            # new_key = key.replace('_', ' ')
            # new_key = new_key.title().replace(' ', '')
            new_data[change_dict_into_hump(new_key)] = change_dict_into_hump(value)
        return new_data
    elif isinstance(json_data, list):
        return [change_dict_into_hump(item) for item in json_data]
    else:
        return json_data



def search_oa_gift(data):
    """
    查询oa赠品，命名转为驼峰和返回第一个赠品的信息
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/gifts"%env
    params = {"page":1}
    response = requests.get(url,headers=headers,params=params).json()
    items = response["data"]["items"]

    if items == []:
        # 新增赠品
        body = {"unlimited_quantity": True, "title_translations": {"zh-cn": "接口自动化新增的赠品%s" % int(time.time())},
                "media_ids": "610d2865ca92cf00264c563c"}
        requests.post(url, headers=headers, json=body).json()
        time.sleep(5)
        #新增后去查询
        response = requests.get(url, headers=headers, params=params).json()
        items = response["data"]["items"]

    # 返回赠品数量不是0
    # print(json.dumps(items))
    quantityList = jsonpath(items,"$..quantity")
    gift_info = items[0]
    for a,b in enumerate(quantityList):
        if b!=0:
            gift_info = items[a]
    # 下划线命名转变为驼峰命名
    change_dict_into_hump(gift_info)

    return gift_info,response


def search_oa_product(data):
    """
    查询OA的商品，并返回响应，和第一个商品信息，并转为驼峰命名
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/products?page=1&per_page=4" %env
    if "query" in data:
        query = data["query"]
        url = "%s/openApi/proxy/v1/products?page=1&per_page=4&query=%s" % (env,query)
    response = requests.get(url, headers=headers).json()
    return response

def get_has_stock_product(data):
    """返回有库存商品的spu_id和sku_id"""
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/products?page=1&per_page=20" % env
    if "query" in data:
        query = data["query"]
        url = "%s/openApi/proxy/v1/products/search?page=1&per_page=20&%s" % (env,query)
    response = requests.get(url, headers=headers).json()
    product_item = response["data"]["items"]
    sku_id = ""
    for product in product_item:
        variations = product["variations"]
        status = product["status"]
        if variations == [] and status != "draft":
            total_orderable_quantity = product["total_orderable_quantity"]
            if total_orderable_quantity > 0 or total_orderable_quantity == -1:
                spu_id = product["id"]
                return spu_id,sku_id
        elif status != "draft":
            for variation in variations:
                total_orderable_quantity = variation["total_orderable_quantity"]
                if total_orderable_quantity > 0 or total_orderable_quantity == -1:
                    spu_id = product["id"]
                    sku_id = variation["id"]
                return spu_id,sku_id


def create_post_lucky_draw(data):
    """
    创建抽奖活动
    :param data:
    :return:
    """
    global response
    env = data["env"]
    headers = data["headers"]
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    title = "接口自动化创建的抽奖活动%d"%int(time.time())
    if "title" in data:
        title = data["title"]
    body = {"title":title,"activityType":"LUCKY_DRAW","platforms":
        [platform],"timeZone":"Asia/Shanghai"}
    url = "%s/api/posts/post/activity/sales/create"%env
    count = 0
    while True:
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            time.sleep(1)
        finally:
            count += 1
        if count > 20:
            break
    response = response.json()
    sales_id = response["data"]["id"]
    return sales_id,response

def modify_lucky_draw(data):
    """
    编辑post投票活动
    :param data:
    activityInfo:
    留言指定文字:keyword 写指定文字，若不选择则为空字符串""
    留言任意文字内容并按赞贴文：taskTypes: ["LIKED_POST", "COMMENT"]
    留言任意文字内容并建立过订单：taskTypes: ["HAD_ORDER", "COMMENT"]
    标记好友：标记好友就必须留言指定文字，tagFriendsNum：1，好友个数
    message:
    若开关关闭则传：
    winComment：""
    winMessage：""
    winReplyComment：""
    days:
    从当前日前算起，要间隔的天数
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    prize_type = ""
    reward = {"reward": None, "rewardType": None}
    if "prize_type" in data:
        prize_type = data["prize_type"]
    if prize_type=="gift":
        gift_info,__ = search_oa_gift(data)
        spuId = gift_info["id"]
        reward = {"reward": {"productDetail":gift_info,"spuId":spuId}, "rewardType": "GIFT"}
    elif prize_type=="product":
        product = search_oa_product(data)["data"]["items"][0]
        product_info = change_dict_into_hump(product)
        spuId = product["id"]
        product_info["productId"] = spuId
        variations= product_info["variations"]
        skuId = ""
        if variations!=[]:
            skuId = variations[0]["id"]
            product_info["variationInfo"] = variations[0]
        product_info["variations"] = []
        reward = {"reward": {"productDetail": product_info, "spuId": spuId,"skuId":skuId}, "rewardType": "PRODUCT"}
    elif prize_type=="discount":
        amount = 1
        if "amount" in data:
            amount = data["amount"]
        reward = {"reward":  {"amount": amount}, "rewardType": "COUPON"}
    keyword = ""
    if "keyword" in data:
        keyword= data["keyword"]
    autoAward = True
    if "autoAward" in data:
        autoAward = data["autoAward"]
    tagFriendsNum = 0
    if "tagFriendsNum" in data:
        tagFriendsNum = data["tagFriendsNum"]
    taskTypes = data.get("taskTypes",["COMMENT"])
    # if "taskTypes" in data:
    #     if "taskTypes" =="order":
    #         taskTypes = ["HAD_ORDER", "COMMENT"]
    #     elif "taskTypes" == "like":
    #         taskTypes = ["LIKED_POST", "COMMENT"]
    activityInfo = {"keyword": keyword, "autoAward": autoAward, "tagFriendsNum": tagFriendsNum, "taskTypes": taskTypes}
    winReplyComment = "🎁 恭喜您中奖！请与小编联系确认领奖细节！"
    if "winReplyComment" in data:
        winReplyComment = data["winReplyComment"]
    winComment = "恭喜 {@winner} 中奖 👏，请与小编联系确认领奖细节！"
    if "winComment" in data:
        winComment = data["winComment"]
    winMessage = "🎁 恭喜您中奖！请与小编联系确认领奖细节！"
    if "winMessage" in data:
        winMessage = data["winMessage"]
    message = {
        "winReplyComment":winReplyComment,
        "winComment":winComment,
        "winMessage":winMessage
    }
    totalWinner = 2
    if "winner" in data:
        totalWinner = data["winner"]
    days = 5
    if "days" in data:
        days = data["days"]
    today = datetime.datetime.now()
    start_time = int(time.mktime(time.strptime(today.strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S')) * 1000)
    end_time = int(time.mktime(
        time.strptime((today + datetime.timedelta(days=days)).strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S')) * 1000)
    if "start_time" in data:
        start_time = data["start_time"]
    if "end_time" in data:
        end_time = data["end_time"]
    body = {"activityType":"LUCKY_DRAW","startTime":start_time,"endTime":end_time,
            "totalWinner":totalWinner,"activityInfo":activityInfo,"message":message,"reward":reward}
    if "sales_id" in data:
        sales_id = data["sales_id"]
    else:
        sales_id,__ = create_post_lucky_draw(data)
    url = "%s/api/posts/activity/post/%s"%(env, sales_id)
    response = requests.put(url,headers=headers,json=body).json()
    return sales_id,response

def get_channel_info(data):
    """
    获取串接的渠道信息
    :param data:   platform："FACEBOOK"、"INSTAGRAM"、"FB_GROUP"
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    # platform = data["platform"]
    url = "%s/api/posts/post/sales/channels?platform=%s"%(env,platform)
    res = requests.get(url, headers=headers).json()
    page_id = res["data"][0]["platformChannelId"]
    page_name = res["data"][0]["platformChannelName"]
    group_id = res["data"][0]["groupId"]
    return page_id,page_name,group_id

def get_page_post(data):
    """
    查询串接的贴文
    :param data:
    since：
    最近7天传：1699027200
    最近30天传：1697040000
    最近90天传：1691856000
    最近180天传：1684080000
    fb group:
    今天：1699545600
    最近3天：1699372800
    type:
    faceboook和ig:POST
    fb group:GROUP_POST
    :return:响应
    """
    #时间戳转换
    env = data["env"]
    headers = data["headers"]
    platform = "FACEBOOK"
    type = "POST"
    days = 180
    current_time = datetime.datetime.now()
    since = int((current_time - datetime.timedelta(days=days)).timestamp())
    if "type" in data:
        type = data["type"]
    if "platform" in data:
        platform = data["platform"].upper()
    if "page_id" in data:
        page_id = data["page_id"]
    else:
        page_id, page_name, group_id = get_channel_info(data)
        if platform=="FB_GROUP":
            page_id = group_id
            type = "GROUP_POST"
            since = int((current_time - datetime.timedelta(days=7)).timestamp())
    if "days" in data:
        days = data["days"]
        since = int((current_time - datetime.timedelta(days=int(days))).timestamp())

    # since = 1699027200
    # if "since" in data:
    #     since = data["since"]
    page_size = 50
    if "page_size" in data:
        page_size = data
    params = {"page_size":page_size,"type":type,"since":since,"party_channel_id":page_id,"platform":platform}
    url = "%s/api/posts/post"%env
    print("params",params)
    response =requests.get(url,headers=headers,params=params).json()
    return response


def relate_post(data):
    """
    链接贴文，只链接返回的第一个可链接的贴文
    :param data:
    :return:
    """
    global platform
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    if "platform" in data:
        platform = data["platform"].upper()
    url = "%s/api/posts/post/sales/%s/addPost"%(env,sales_id)
    body = {}
    if platform=="FB_GROUP":
        page_id = data["page_id"]
        relationUrl = data["relationUrl"]
        body = {
            "pageId": page_id,
            "platform": "FB_GROUP",
            "relationUrl": relationUrl
            }
    else:
        response = get_page_post(data)
        available_post_list = []
        related_sales = jsonpath(response,"$..related_sales")
        # print("查询到的贴文信息",related_sales)
        for index,value in enumerate(related_sales):
            if value==False:
                available_post_list.append(response["data"]["data"][index])

    # platform = "FACEBOOK"
    # print(available_post_list[0])
        page_id = jsonpath(available_post_list[0],"$..from.id")[0]
        page_name = jsonpath(available_post_list[0],"$..from.name")[0]
        post_id = jsonpath(available_post_list[0],"$.id")[0]
        message = jsonpath(available_post_list[0],"$.message")[0]
        permalink_url = jsonpath(available_post_list[0],"$.permalink_url")[0]
        status_type = jsonpath(available_post_list[0],"$.status_type")[0]
        picture = jsonpath(available_post_list[0],"$.picture")[0]
        body = {"pageId": page_id, "pageName": page_name, "platform": platform,
            "postList": [{"postId": post_id, "postTitle": page_name,
                          "postDescription": message, "postImageUrl": picture,
                          "permalinkUrl": permalink_url,
                          "statusType": status_type}]}

    response = requests.post(url,headers=headers,json=body).json()
    return response


def create_fb_text_post(data):
    """
    创建fb、fb group纯文本贴文
    :param data: fb group 创建贴文时，pageId为group_id
    :return:post_pid 为贴文在post数据库的ID，取消和编辑贴文时会使用到
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    #获取page信息
    page_id, page_name, group_id = get_channel_info(data)
    postDescription = "一天天工作这么忙，烦死了%d"%int(time.time())
    if "postDescription" in data:
        postDescription = data["postDescription"]
    if platform == "FB_GROUP":
        page_id = group_id
    url = "%s/api/posts/post/%s/post"%(env,sales_id)
    body = {"postDescription":postDescription,"platform":platform,
            "url":[],"mediaFbid":[],"pageId":page_id}
    response = requests.post(url,headers=headers,json=body).json()
    # print("创建贴文返回",response)
    post_id = response["data"]["post_id"]
    post_pid = response["data"]["id"]
    return post_id,post_pid,response

def search_post_product(data):
    """
    查询可添加的商品，只查询前10个，和查询openApi/proxy/v1/products不一样，这个接口经过post组装关键字返回
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    type = "spu"
    quantity = 100
    if "type" in data:
        type = data["type"]
    if "quantity" in data:
        quantity = data["quantity"]
    url = "%s/api/posts/common/product/key/spu/list?page=1&searchType=ALL&pageSize=10"%(env)
    if "query" in data:
        query = data["query"]
        url = "%s/api/posts/common/product/key/spu/list?page=1&searchType=ALL&pageSize=10&query=%s" % (env, query)
    response = requests.get(url, headers=headers).json()
    items = response["data"]["openApiProductDetails"]
    # productSpuKeyVos = response["data"]["productSpuKeyVos"][0]
    # skuKeys = productSpuKeyVos["skuKeys"]
    # spuId = productSpuKeyVos["spuId"]
    # return skuKeys,spuId,response

    variant_options_list = jsonpath(items, "$..variations")
    product_info = ""
    spu_id = ""
    sku_id = ""
    sku_id_quantity = []

    for a, b in enumerate(variant_options_list):
        if type == "spu" and b == [] and quantity != 0:
            quantitys = items[a]["totalOrderableQuantity"]
            unlimited_quantity = items[a]["unlimitedQuantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                break
        elif type == "sku" and b != [] and quantity != 0:
            quantitys = items[a]["totalOrderableQuantity"]
            unlimited_quantity = items[a]["unlimitedQuantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                sku_id = jsonpath(items[a]["variations"], "$..id")
                sku_id_quantity = jsonpath(items[a]["variations"], "$..totalOrderableQuantity")
                break
        elif type == "spu" and b == [] and quantity == 0:
            quantitys = items[a]["totalOrderableQuantity"]
            unlimited_quantity = items[a]["unlimitedQuantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                break
        elif type == "sku" and b != [] and quantity == 0:
            quantitys = items[a]["totalOrderableQuantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                sku_id = jsonpath(items[a]["variations"], "$..id")
                sku_id_quantity = jsonpath(items[a]["variations"], "$..totalOrderableQuantity")
                break
    return spu_id, sku_id, sku_id_quantity, product_info


def model_one_add_product(data):
    """
    贴文销售模式1-模式3添加商品，只添加第一个有库存商品到贴文
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/products"%(env,sales_id)
    spu_id, sku_id, sku_id_quantity, product_info = search_post_product(data)
    # print("sku_id",sku_id)
    skuList = []
    body = {}
    if len(sku_id) >1:
        for index, sku in enumerate(sku_id):
            # skuId = sku["skuId"]
            # spuId = sku["spuId"]
            sku_data = {}
            sku_data["skuId"] = sku
            sku_data["missCommonKey"] = False
            sku_data["keyList"] = ["模式1关键字%d" % index]
            skuList.append(sku_data)
    # print(skuList)
    if len(sku_id)<=1:
        body = {
            "spuList": [{"spuId": spu_id, "missCommonKey": "false", "customNumbers": [], "keyList": ["无规格商品关键字"]}]}
    else:
        body = {
            "spuList": [{"spuId": spu_id, "missCommonKey": "false", "customNumbers": [], "skuList": skuList}]}
    # print(body)
    response = requests.post(url, headers=headers, json=body).json()
    return response

def model_four_add_product(data):
    """
    贴文销售模式4添加商品，只添加第一个商品到贴文
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/products"%(env,sales_id)
    spu_id, sku_id, sku_id_quantity, product_info = search_post_product(data)
    skuList = []
    if len(sku_id) >1:
        for index, sku in enumerate(sku_id):
            # skuId = sku["skuId"]
            # spuId = sku["spuId"]
            sku_data = {}
            sku_data["skuId"] = sku
            sku_data["missCommonKey"] = False
            skuList.append(sku_data)
    # print(skuList)
    customNumbers = "模式4接口关键字下单"
    body = {}
    if len(sku_id) <= 1:
        body = {"spuList": [
            {"spuId": spu_id, "missCommonKey": "true", "customNumbers": [customNumbers], "customNumber": customNumbers}]}
    else:
        body = {"spuList": [
            {"spuId": spu_id, "missCommonKey": "false", "customNumbers": [customNumbers], "customNumber": customNumbers,
             "skuList": skuList}]}
    response = requests.post(url, headers=headers, json=body).json()
    return response

def modify_post_schedule(data):
    """
    修改贴文排程时间
    :param data: start_time若没有传则默认给当前时间，end_time若没有传则默认是永远有效
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    start_time = int(time.time() * 1000)
    end_time = 32503611599000
    if "start_time" in data:
        start_time = data["start_time"]*1000 if len(str(data["start_time"]))<13 else data["start_time"]
    if "end_time" in data:
        end_time = data["end_time"] * 1000 if len(str(data["end_time"])) < 13 else data["end_time"]
    url = "%s/api/posts/post/sales/schedule/%s"%(env,sales_id)
    body = {"start_time": start_time, "end_time": end_time}
    response = requests.put(url,headers=headers,json=body).json()
    return response

def publish_post(data):
    """启用贴文"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    #启用前先修改排程时间，若没有传时间，则按默认值设置
    modify_post_schedule(data)
    url = "%s/api/posts/post/sales/publish/%s"%(env,sales_id)
    response = requests.put(url, headers=headers).json()
    return response

def end_post_activity(data):
    """
    抽奖活动开奖
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/activity/end/%s"%(env,sales_id)
    response = requests.put(url,headers=headers).json()
    return response

def get_post_activity_winner(data):
    """
    获取获奖者
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/activity/listWinner/%s?limit=1000"%(env,sales_id)
    response = requests.get(url,headers=headers).json()
    return response


def get_post_info(data):
    """
    获取贴文信息
    :param data:
    :return: 贴文全部信息，若需要调用后再过滤
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s?fieldScopes=DETAILS,PRODUCT_NUM," \
          "SALES_CONFIG,LOCK_INVENTORY,PRODUCT_LIST"%(env,sales_id)
    response = requests.get(url, headers=headers).json()
    return response

def get_post_activity_detail(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/activity/detail/%s"%(env,sales_id)
    response = requests.get(url, headers=headers).json()
    return response

def get_post_list(data):
    """
    查询活动列表
    贴文销售列表：POST，活动：ACTIVITY
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_type = "POST"
    if "sales_type" in data:
        sales_type = data["sales_type"]
    params = {"page_num":1,"page_size":10,"sales_type":sales_type}
    url = "%s/api/posts/post/sales"%env
    response = requests.get(url,headers=headers,params=params).json()
    return response


def get_post_product_keyword(data):
    """获取贴文返回第一个商品的关键字"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s?fieldScopes=PRODUCT_LIST" % (env, sales_id)
    response = requests.get(url, headers=headers).json()
    keyword = jsonpath(response,"$..custom_keys_label_str")[0]
    return keyword,response



def send_post_comment(data):
    """
    在贴文下留言
    :param data:
    :return:
    """
    #获取关联的贴文信息-第一则贴文
    type = "post"
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"]
    if "type" in data:
        type = data["type"]
    response = {}
    if type == "post":
        response = get_post_info(data)
    elif type == "activity":
        response = get_post_activity_detail(data)
    related_post_list = response["data"]["related_post_list"][0]
    page_id = related_post_list["page_id"]
    post_id = related_post_list["post_id"]
    platform = related_post_list["platform"]
    group_id = related_post_list["group_id"]
    # print("请求的平台是",platform)
    stamp = int(time.time())
    num = random.randint(100000, 999999)
    env = data["env"]
    user_id = "488864%d" % int(time.time())
    if "user_id" in data:
        user_id = data['user_id']
    name = "test post%d" % int(time.time())
    if "name" in data:
        name = data['name']
    comment_id = "%s_%d%d" % (page_id, stamp, num)
    if "comment_id" in data:
        comment_id = data['comment_id']
    keyword = "接口测试普通留言"
    if "keyword" in data:
        keyword = data['keyword']
    key = data["key"]
    body = {}
    if platform=="FACEBOOK":
        body = {"object": "page", "entry": [{"id": page_id, "time": stamp, "changes": [{"field": "feed", "value": {
        "from": {"id": user_id, "name": name},
        "post": {"status_type": "added_video", "is_published": True, "updated_time": "2022-11-18T09:57:26+0000",
                 "permalink_url": "https://www.facebook.com/permalink.php?story_fbid=pfbid02jLK3e6YdFSXp2DmD7j7vtStLXoBzTi8rxKrp6jFhVMUTTEgz6qvZA8soR9Uwydd8l&id=107977035056574",
                 "promotion_status": "inactive", "id": post_id}, "message": keyword, "item": "comment",
        "verb": "add", "post_id": post_id, "comment_id": comment_id,
        "created_time": stamp, "parent_id": post_id}}]}]}
    elif platform=="INSTAGRAM":
        body = {"entry": [{"id": page_id, "time": stamp, "changes": [{"value": {"from": {"id": user_id,
         "username": name}, "media": {"id": post_id, "media_product_type": "FEED"},
         "id": comment_id, "text": keyword}, "field": "comments"}]}], "object": "instagram"}
    elif platform.upper() == "FB_GROUP":
        t_time = stamp * 1000
        post_id = post_id.split("_")[-1]
        comment_id = "%d%d" % (stamp, num)
        body = {"object": "page", "entry": [
            {"id": page_id, "time": t_time, "messaging": [{"recipient": {"id": page_id}, "message": keyword,
                                                           "from": {"id": user_id, "name": name}, "group_id": group_id,
                                                           "post_id": post_id, "comment_id": comment_id,
                                                           "created_time": stamp, "item": "comment",
                                                           "verb": "add", "parent_id": post_id,
                                                           "field": "group_feed"}]}]}

    url = "%s/facebook/webhook"%env
    sign_text = hmac.new(key.encode("utf-8"), json.dumps(body).encode("utf-8"), sha1)
    signData = sign_text.hexdigest()
    # print("body",json.dumps(body))
    header = {"Content-Type": "application/json", "x-hub-signature": "sha1=%s" % signData}
    response = requests.post(url, headers=header, data=json.dumps(body))
    return user_id,name,comment_id

def get_payment(data):
    """
    获取店铺的付款方式，默认查询10条
    :param data:
    :return:默认返回第一个支付方式
    """
    env = data["env"]
    oc_env = data["oc_env"]
    headers = data["headers"]
    url ="%s/openApi/proxy/v1/payments?page=1&per_page=10&include_fields[]=config_data.tappay"%oc_env
    response = requests.get(url, headers=headers).json()
    payment_types = [item["type"] for item in response["data"]["items"]]
    payment_id = ""
    for payment in payment_types:
        # print(delivery)
        if payment == "bank_transfer":
            index = payment_types.index(payment)
            payment_info = response["data"]["items"][index]
            payment_id = payment_info["id"]
            break
    if payment_id == "":
        payment_id = response["data"]["items"][0]["id"]
    return payment_id,response

def get_delivery(data):
    """
    获取店铺的物流方式，默认查询10条
    :param data:
    :return:默认返回第一个物流方式
    """
    # print("物流data",data)
    env = data["env"]
    oc_env = data["oc_env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/delivery_options?page=1&per_page=998"%oc_env
    response = requests.get(url, headers=headers).json()
    # print(response)
    delivery_types = [item["region_type"] for item in response["data"]["items"]]
    delivery_id = ""
    for delivery in delivery_types:
        # print(delivery)
        if delivery == "custom":
            index = delivery_types.index(delivery)
            delivery_info = response["data"]["items"][index]
            delivery_id = delivery_info["id"]
            break
    if delivery_id=="":
        delivery_id = response["data"]["items"][0]["id"]
    return delivery_id,response

def get_comment_user(data):
    """
    查询留言面板的留言用户，查全部，并返回第一个留言用户
    :return:post_user_id,编辑购物车，发送购物车链接需要用到这个值
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    params = {"pageNo":1,"pageSize":25,"salesId":sales_id}
    if "query" in data:
        query = data["query"]
        params["query"] = query
    url = "%s/api/posts/post/comments"%env
    # print(params)
    response = requests.get(url, headers=headers,params=params).json()
    print(response)
    post_user_id = jsonpath(response, "$..id")[0]
    return post_user_id,response

def post_edit_cart(data):
    """
    编辑购物车，给用户加入查询到的第一个商品：没有排除无库存的情况
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    post_user_id, __ = get_comment_user(data)
    url = "%s/api/posts/post/sales/%s/user/" \
          "%s/cart/item?skip_reapply_promotion=false"%(env,sales_id,post_user_id)
    response = search_oa_product(data)
    variations = response["data"]["items"][0]["variations"]
    spu_id = response["data"]["items"][0]["id"]
    quantity = 1
    if "quantity" in data:
        quantity = data["quantity"]
    body = {"spu_id": spu_id, "owner_type": "Guest", "quantity": quantity, "type": "product"}
    if variations != []:
        sku_id = variations[0]["id"]
        body = {"spu_id": spu_id, "owner_type": "Guest", "sku_id": sku_id, "quantity": quantity,
                "type": "product"}
    response = requests.post(url, headers=headers, json=body).json()
    return response

def search_customer(data):
    env = data["env"]
    headers = data["headers"]
    phone = data["phone"]
    url = "%s/openApi/proxy/v1/customers/search?query=%s&per_page=50&search_fields[]=mobile_phone" \
          "&search_fields[]=phones" % (env, phone)
    response = requests.get(url, headers=headers).json()
    return response

def merge_customer(data):
    env = data["env"]
    headers = data["headers"]
    phone = data["phone"]
    __, response = get_comment_user(data)
    # print("留言面板查询返回",response)
    name = data["name"]
    user_id = data["user_id"]
    page_id = data["page_id"]
    platform = data["platform"]
    customer_id  = jsonpath(response,"$..customer_id")[0]

    if customer_id==None:
        response = search_customer(data)
        items = response["data"]["items"]
        # 创建会员
        url = "%s/uc/customers/merge" % env
        body = {"email": "", "mobile_phone": phone, "mobile_phone_country_calling_code": "86",
                "name": name, "page_scoped_id": user_id, "locale_code": None, "country_code": "cn",
                "id": None, "party_channel_id": page_id, "platform": platform, "is_member": True}
        if items != []:
            id = jsonpath(response, "$..id")[0]
            customer_id = id
            body = {"email": "", "mobile_phone": phone, "mobile_phone_country_calling_code": "86",
                    "name": name, "page_scoped_id": user_id, "locale_code": None, "country_code": "cn",
                    "id": id, "party_channel_id": page_id, "platform": platform, "is_member": True}
        response = requests.put(url, headers=headers, json=body)
        print("合并会员返回",response.json())
        # print("创建会员请求体",body)
        if response.raise_for_status():
            customer_id = response.json()["data"]["id"]
        elif response.json()["code"]=="UC0409":
            email = "%d@qq.com"%int(time.time())
            body = {"email": email, "mobile_phone": "", "mobile_phone_country_calling_code": "86",
                    "name": name, "page_scoped_id": user_id, "locale_code": None, "country_code": "cn",
                    "id": "", "party_channel_id": page_id, "platform": platform, "is_member": False}
            response = requests.put(url, headers=headers, json=body)
        else:
            customer_id = response.json()["data"]["id"]
    return response,customer_id

def manual_order(data):
    """
    创建会员，若存在则合并会员
    创建订单
    :param data:
    :return:
    """
    oc_env_stg = "https://create-order.shoplinestg.com"
    oc_env_pre = "https://create-order-preview.shoplineapp.com"
    oc_env_pro = "https://create-order.shoplineapp.com"
    river_env_tag = data["river_env_tag"]
    if river_env_tag=="test":
        oc_env = oc_env_stg
    elif river_env_tag=="pre":
        oc_env = oc_env_pre
    elif river_env_tag=="pro":
        oc_env = oc_env_pro
    else:
        oc_env = oc_env_pre
    env = data["env"]
    data["oc_env"] = oc_env
    headers = data["headers"]
    phone = "18776343453"
    phone = data.get("phone",phone)
    __, response = get_comment_user(data)
    name = jsonpath(response, "$..name")[0]
    user_id = jsonpath(response, "$..psid")[0]
    page_id = jsonpath(response, "$..page_id")[0]
    data["name"] = name
    data["user_id"] = user_id
    data["page_id"] = page_id
    data["phone"] = phone
    platform = "facebook"
    if "platform" in data:
        platform = data["platform"].upper()
    data["platform"] = platform
    # 先查询号码或邮箱是否被占有
    #创建会员
    response,customer_id = merge_customer(data)
    # print("会员ID",customer_id)
    # print("创建会员返回，",response.text)
    #给会员新增物流地址
    url = "%s/uc/customers/%s" % (env,customer_id)
    postcode = "76653"
    delivery_data = {"delivery_addresses": [
        {"city": "bb", "country": "CN", "postcode": postcode, "recipient_name": name,
         "recipient_phone": phone, "recipient_phone_country_code": "86", "logistic_codes": [],
         "address_1": "aa"}]}
    res = requests.put(url, json=delivery_data, headers=headers).json()
    # print("信息会员物流地址返回",res)

    # 查询会话ID
    # platform = "facebook"
    # if "platform" in data:
    #     platform = data["platform"]
    # url = "%s/mc/conversation/id?type=%s&user_id=%s&party_channel_id=%s" % (env,platform,user_id, page_id)
    # # param = {"type":"facebook","user_id":vars["user_id"],"party_channel_id":vars["platform_channel_id"]}
    # response = requests.get(url, headers=headers).json()
    # conversation_id = jsonpath(response, "$.data.id")[0]
    data["user_id"] = user_id
    data["page_id"] = page_id
    conversation_id,__ = get_user_conversation_id(data)

    # 给cart 设置物流 和设置支付方式
    url = "%s/openApi/proxy/v1/internal/mc/api/carts/%s?owner_type=User&cart_uid=%s&created_by=post&skip_reapply_promotion=false&shop_session_id=%s" % (
    oc_env,customer_id, customer_id, user_id)
    delivery_id,__ = get_delivery(data)
    payment_id,__ = get_payment(data)
    body = {"delivery_option_id": delivery_id, "country": "CN", "countryCode": "CN",
            "payment_id": payment_id}
    res = requests.put(url, headers=headers, json = body).json()
    # print("设置cart",res)
    # 成立订单
    url = "%s/manual_order/checkout"%oc_env
    delivery_address = delivery_data["delivery_addresses"][0]
    delivery_address["district"] = None
    delivery_address["key"] = None
    delivery_address["regioncode"] = None
    delivery_address["province"] = None
    delivery_address["address_2"] = None
    delivery_address["country_code"] = "CN"
    body = {"country": "CN", "customer_email": None, "customer_id": customer_id, "customer_name": name,
            "customer_phone": phone, "whatsapp_phone": phone, "delivery_address": delivery_address,
            "delivery_data": {"recipient_name": name, "recipient_phone": phone},
            "delivery_option_id": delivery_id, "display_payment_info": False, "invoice": {}, "lang": "zh-cn",
            "order_remarks": "", "order_tags": [], "payment_id": payment_id,
            "payment_info": "{\"text\":\"\",\"images\":[]}", "send_notification": False, "created_by": "post",
            "created_from": "admin_post", "platform": "FACEBOOK", "conversation_id": conversation_id,
            "merchant_name": "泰国店", "shop_session_id": user_id, "platform_channel_name": "kkk",
            "source_data": {"type": "fb", "source_id": page_id}, "customer_phone_country_code": "86",
            "postcode": postcode}
    res = requests.post(url,headers=headers,json=body)
    print("创建订单返回",res.text)
    #获取订单ID
    orderNumber = ""
    if res.status_code==200:
        orderNumber = jsonpath(res.json(),"$..orderNumber")[0]
    return orderNumber,customer_id,res

def get_user_conversation_id(data):
    """
    :return: 会员ID
    platform 为小写，有一些是大写，这个要注意区分
    """
    # 查询会话ID
    env = data["env"]
    headers = data["headers"]
    user_id = data["user_id"]
    page_id = data["page_id"]
    platform = "facebook"
    if "platform" in data:
        platform = data["platform"].lower()
    url = "%s/mc/conversation/id?type=%s&user_id=%s&party_channel_id=%s" % (env, platform, user_id, page_id)
    # param = {"type":"facebook","user_id":vars["user_id"],"party_channel_id":vars["platform_channel_id"]}
    print(url)
    response = requests.get(url, headers=headers).json()
    print(response)

    conversation_id = jsonpath(response, "$.data.id")[0]
    return conversation_id,response

def get_user_message(data):
    """
    获取信息
    :param data: 
    :return: 
    """""
    env = data["env"]
    headers = data["headers"]
    # 获取发送的私讯内容
    conversation_id,__ = get_user_conversation_id(data)
    url = "%s/mc/message/%s?create_time="%(env,conversation_id)
    response = requests.get(url,headers=headers).json()
    content = jsonpath(response,"$..content")[0]
    text = ""
    if "message" in json.loads(content):
        text = json.loads(content)["message"]["attachment"]["payload"]["text"]
    return text


def modify_order_status(data):
    """
    :param data:
    status:订单的状态
    confirmed:已确认
    pending：处理中
    completed：已完成
    cancelled ：已取消
    :return:
    """
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    status = data["status"]
    # 查询订单id
    global customer_id
    if "customer_id" in data:
        customer_id = data["customer_id"]
    else:
        __,customer_id,__ = manual_order(data)
    if "order_id" in data:
        order_id = data["order_id"]
    else:
        url = "%s/v1/orders/search?page=1&per_page=5&customer_id=%s" % (oa_env,customer_id)
        res = requests.get(url, headers=oa_headers).json()
        order_id = jsonpath(res, "$..id")[0]
    # print("订单ID", vars["order_id"])
    # 修改订单状态为-已确认
    url = "%s/v1/orders/%s/status" % (oa_env,order_id)
    body = {
        "status": status,
        "mail_notify": False
    }
    res = requests.patch(url, headers=oa_headers, json=body).json()
    return res

def modify_order_payment_status(data):
    """
    :param data:
    status:订单的状态
    pending：未付款
    completed：已付款
    refunding ：退款中
    refunded：已退款
    partially_refunded：部分退款
    :return:
    """
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    status = data["status"]
    # 查询订单id
    global customer_id
    if "customer_id" in data:
        customer_id = data["customer_id"]
    else:
        __,customer_id,__ = manual_order(data)
    if "order_id" in data:
        order_id = data["order_id"]
    else:
        url = "%s/v1/orders/search?page=1&per_page=5&customer_id=%s" % (oa_env, customer_id)
        res = requests.get(url, headers=oa_headers).json()
        order_id = jsonpath(res, "$..id")[0]
    # print("订单ID", vars["order_id"])
    # 修改订单状态为-已确认
    url = "%s/v1/orders/%s/order_payment_status" % (oa_env,order_id)
    body = {
        "status": status,
        "mail_notify": False
    }
    res = requests.patch(url, headers=oa_headers, json=body).json()
    return res

def modify_order_delivery_status(data):
    """
    :param data:
    status:订单的状态
    pending：备货中
    shipping：发货中
    shipped ：已发货
    arrived：已到达
    collected：已取货
    returned：已退货
    returning：退回中
    :return:
    """
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    status = data["status"]
    # 查询订单id
    global customer_id
    if "customer_id" in data:
        customer_id = data["customer_id"]
    else:
        __,customer_id,__ = manual_order(data)
    if "order_id" in data:
        order_id = data["order_id"]
    else:
        url = "%s/v1/orders/search?page=1&per_page=5&customer_id=%s" % (oa_env, customer_id)
        res = requests.get(url, headers=oa_headers).json()
        order_id = jsonpath(res, "$..id")[0]
    # print("订单ID", vars["order_id"])
    # 修改订单状态为-已确认
    url = "%s/v1/orders/%s/order_delivery_status" % (oa_env,order_id)
    body = {
        "status": status,
        "mail_notify": False
    }
    res = requests.patch(url, headers=oa_headers, json=body).json()
    return res

def delete_post(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s"%(env,sales_id)
    res = requests.delete(url, headers=headers).json()
    return res

def modelone_create_single_product(data):
    """
    贴文新增无规格商品
    :param data:
    :return: 返回新增的商品的spu_id
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    quantity = 1000
    price = 3
    if "quantity" in data:
        quantity = data["quantity"]
    url = "%s/api/posts/post/sales/%s/product/create" % (env, sales_id)
    product_name = "post接口新增商品多规格商品名称%d" % int(time.time())
    if "product_name" in data:
        product_name = data["product_name"]
    keyword = "post接口新增商品多规格商品关键字%d" % int(time.time())
    if "keyword" in data:
        keyword = data["keyword"]
    if "price" in data:
        price = data["price"]
    body = {"customKey":keyword,"quantity":quantity,"unlimitedQuantity":False,"productName":product_name,
            "imageUrl":"https://s3-ap-southeast-1.amazonaws.com/static.shoplineapp.com/sc-admin/product-default.png","price":price}
    response = requests.post(url,headers=headers,json=body).json()
    # print(body)
    print(response)
    spu_id = response["data"]
    return spu_id

def modelfour_create_single_product(data):
    """
    贴文新增无规格商品
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
    body = {"customNumber":keyword,"quantity":quantity,"unlimitedQuantity":False,"productName":product_name,
            "imageUrl":"https://s3-ap-southeast-1.amazonaws.com/static.shoplineapp.com/sc-admin/product-default.png","price":3}
    response = requests.post(url,headers=headers,json=body).json()
    spu_id = response["data"]
    return spu_id


def modelone_create_mutil_product(data):
    """
    贴文新增多规格商品，
    :param data: variance需要传入需要新增的规格:格式:{"color":["红","黄"],"size":["X","M"]}
    规格类型，规格具体名称
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/product/create"%(env,sales_id)
    product_name = "post接口新增商品多规格商品名称%d"%int(time.time())
    if "product_name" in data:
        product_name = data["product_name"]
    keyword = "post接口新增商品多规格商品关键字%d"%int(time.time())
    if "keyword" in data:
        keyword = data["keyword"]
    variance = {"color":["红","黄"],"size":["X","M"]}
    if "variance" in data:
        variance = data["variance"]
    price = 10
    if "price" in data:
        price = data["price"]
    quantity = 99
    if "quantity" in data:
        quantity = data["quantity"]
    customVariantTypes = []
    variantOptions = []
    variations = []
    variance_type = variance.keys()
    # print(variance_type)
    custom_keys = []
    for index,value in enumerate(variance_type):
        # print(value)
        customVariantType = {}
        type = "custom_%d"%(index+1)
        customVariantType["type"] = type
        customVariantType["name"] = value
        customVariantTypes.append(customVariantType)
        variance_names = variance[value]
        # print(variance_names)
        custom_key = []
        for index,value in enumerate(variance_names):
            variantOption = {}
            variantOption["type"] = type
            variantOption["name"] = value
            variantOption["key"] = "%s_%s_4218"%(type,value)
            custom_key.append(variantOption["key"])
            variantOptions.append(variantOption)
        custom_keys.append(custom_key)
    # print(customVariantTypes)
    # print(variantOptions)
    # print(custom_keys)
    # 生成所有组合
    combinations = []
    for i in range(len(custom_keys)):
        for j in range(i + 1, len(custom_keys)):
            # 使用 itertools.product 生成每对子数组的组合
            combinations.extend(itertools.product(custom_keys[i], custom_keys[j]))
    for i in range(len(combinations)):
        variantion = {}
        variantion["price"] = price
        variantion["quantity"] = quantity
        variantion["keyList"] = [keyword + "%d" % i]
        variantion["variantOptionKeys"] = list(combinations[i])
        variations.append(variantion)
    # print(variations)

    body = {
        "unlimitedQuantity": False,
        "productName": product_name,
        "imageUrl": "https://s3-ap-southeast-1.amazonaws.com/static.shoplineapp.com/sc-admin/product-default.png",
        "customVariantTypes":customVariantTypes,
        "variantOptions": variantOptions,
        "variations": variations,
        "price": 0
    }
    response = requests.post(url, headers=headers, json=body).json()
    spu_id = response["data"]
    return spu_id

def get_mc_post(data):
    """
    获取mc贴文信息，若配传page_id,则通过sales_id去查贴文关联的粉丝页信息
    :param data:
    :return:只查询前100个贴文
    """
    env = data["env"]
    headers = data["headers"]
    # page_id = ""
    if "page_id" in data:
        page_id = data["page_id"]
    else:
        response = get_post_info(data)
        page_id = jsonpath(response,"$..page_id")[0]
    url = "%s/mc/postcomment/posts"%env
    # print(url)
    params = {"platform_channel_id":page_id,"staff_id":"all","page_num":1,"page_size":100}
    response = requests.get(url, headers=headers,params=params).json()
    id = jsonpath(response,"$..id")
    post_id = jsonpath(response,"$..fb_post_id")
    return id,post_id,response

def get_post_comment(data):
    """
    没有传则查询贴文关联的post_id
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    id_list, post_id_list, __ = get_mc_post(data)
    print("id_list",id_list)
    print("post_id_list", post_id_list)
    post_id = ""
    if "post_id" in data:
        post_id = data["post_id"]
    else:
        response = get_post_info(data)
        post_id = jsonpath(response, "$..post_id")[1]
    print("查询的贴文post_id",post_id)
    mc_post_id = 1
    for index,value in enumerate(post_id_list):
        if value==post_id:
            mc_post_id = id_list[index]
    url = "%s/mc/postcomment/comments"%env
    params = {"post_id":mc_post_id,"page_num":1,"page_size":10}
    response = requests.get(url, headers=headers, params=params).json()
    return response

def get_post_product_comment(data):
    """
    获取盖大楼销售，创建商品评论的信息
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/product/send/msg/info/%s"%(env,sales_id)

def modify_message(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]

    url = "%s/api/posts/post/sales/%s/keyword_message"%(env,sales_id)
    need_send_message = True
    if "need_send_message" in data:
        need_send_message = data["need_send_message"]
    no_interaction_first_message = "您好，以下商品加单成功！{products} 购物车商品总金额: {total}请按以下按钮「继续」！"
    if "no_interaction_first_message" in data:
        no_interaction_first_message = data["no_interaction_first_message"]
    no_interaction_first_button = "继续"
    if "no_interaction_first_button" in data:
        no_interaction_first_button = data["no_interaction_first_button"]
    no_interaction_second_message = "您好，以下商品加单成功！{products} 购物车商品总金额: {total}请前往购物网站！"
    if "no_interaction_second_message" in data:
        no_interaction_second_message = data["no_interaction_first_message"]
    no_interaction_second_button = "结账"
    if "no_interaction_second_button" in data:
        no_interaction_second_button = data["no_interaction_first_button"]
    has_interaction_message = "您好，以下商品加单成功！{products} 购物车商品总金额: {total}请前往购物网站！"
    if "has_interaction_message" in data:
        has_interaction_message = data["has_interaction_message"]
    has_interaction_button = "您好，以下商品加单成功！{products} 购物车商品总金额: {total}请前往购物网站！"
    if "has_interaction_button" in data:
        has_interaction_button = data["has_interaction_button"]
    comment_reply_switch = True
    if "comment_reply_switch" in data:
        comment_reply_switch = data['comment_reply_switch']
    comment_reply_content = "您好，{customerName}，谢谢你在贴文下留言订购商品"
    if "comment_reply_content" in data:
        comment_reply_content = data['comment_reply_content']
    all_out_of_stock_switch = True
    if "all_out_of_stock_switch" in data:
        all_out_of_stock_switch = data['all_out_of_stock_switch']
    all_out_of_stock_content = "您好，{customerName}，以下商品库存不足，请选购其他商品，谢谢！️{products}"
    if "all_out_of_stock_content" in data:
        all_out_of_stock_content = data['all_out_of_stock_content']
    body ={"message_config_req":{"need_send_message":need_send_message,"no_interaction_message":
        {"first_message":no_interaction_first_message,"first_message_button":no_interaction_first_button,
         "second_message":no_interaction_second_message,
         "second_message_button":no_interaction_second_button},"has_interaction_message":
        {"first_message":has_interaction_message,
         "message_button":has_interaction_button},"has_link":True},"comment_reply_req":
        {"need_reply":comment_reply_switch,"content":comment_reply_content},
           "all_out_of_stock_req":{"need_reply":all_out_of_stock_switch,"content":all_out_of_stock_content}}
    response = requests.post(url,headers=headers,json=body).json()
    return response

def modify_post_general_config(data):
    """
 修改通用配置
    :param data:
    patternModel：默认 INCLUDE_MATCH
    INCLUDE_MATCH：模式1-留言包含 关键字 或 关键字+数量
    WITH_QTY_MATCH：模式2-留言包含 关键字+数量
    EXACT_MATCH：模式3-留言只有 关键字 或 关键字+数量
    WITH_SPU_MATCH:模式4-留言包含 商品编号+规
    lockStock：False,True，默认False
    salesStockLockPreTime:lockStock 为True,必传，枚举值："" ，7，14，传""为每场销售活动自动时间
    schedule_time:枚举值：0,7,14,30    0为：用不过期
    :return:返回查询的通用配置
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales/global/POST" % env
    patternModel = "INCLUDE_MATCH"
    #下单模式
    if "patternModel" in data:
        patternModel = data["patternModel"]
    lockStock = False
    #锁库存设置
    if "lockStock" in data:
        patternModel = data["lockStock"]
    salesStockLockPreTime = 7
    if "salesStockLockPreTime" in data:
        patternModel = data["salesStockLockPreTime"]
    #私讯回复
    needSendMessage = True
    if "needSendMessage" in data:
        needSendMessage = data["needSendMessage"]
    hasInteractionTopMessage = "您好，以下商品加单成功！{products}💰购物车商品总金额: {total}请前往购物网站！一定时间内有交互信息%d"%int(time.time())
    if "hasInteractionTopMessage" in data:
        needSendMessage = data["hasInteractionTopMessage"]
    hasInteractionMessageButton = "一定时间内有交互按钮%d"%int(time.time())
    if "hasInteractionMessageButton" in data:
        hasInteractionMessageButton = data["hasInteractionMessageButton"]
    noInteractionFirstTopMessage = "您好，以下商品加单成功！{products}💰 购物车商品总金额: {total}请前往购物网站！一定时间内没有交互%d"%int(time.time())
    if "noInteractionFirstTopMessage" in data:
        noInteractionFirstTopMessage = data["noInteractionFirstTopMessage"]
    noInteractionFirstMessageButton = "继续%d"%int(time.time())
    if "noInteractionFirstMessageButton" in data:
        noInteractionFirstMessageButton = data["noInteractionFirstMessageButton"]
    noInteractionSecondTopMessage = "您好，以下商品加单成功！{products}💰 购物车商品总金额: {total}请前往购物网站！点击继续后发送的消息%d"%int(time.time())
    if "noInteractionSecondTopMessage" in data:
        noInteractionSecondTopMessage = data["noInteractionSecondTopMessage"]
    noInteractionSecondMessageButton = "立即结账%d"%int(time.time())
    if "noInteractionSecondMessageButton" in data:
        noInteractionSecondMessageButton = data["noInteractionSecondMessageButton"]
    #留言回复
    comment_reply_need_reply = True
    if "comment_reply_need_reply" in data:
        comment_reply_need_reply = data["comment_reply_need_reply"]
    comment_reply_content = "您好，{customerName},谢谢你在贴文下留言订购以下商品。%d"%int(time.time())
    if "comment_reply_content" in data:
        comment_reply_content = data["comment_reply_content"]
    all_out_of_stock_need_reply = True
    if "all_out_of_stock_need_reply" in data:
        all_out_of_stock_need_reply = data["all_out_of_stock_need_reply"]
    all_out_of_stock_content = "您好，{customerName}，以下商品库存不足，请选购其他商品，谢谢!%d"%int(time.time())
    if "all_out_of_stock_content" in data:
        all_out_of_stock_content = data["all_out_of_stock_content"]
    schedule_time = 0
    if "schedule_time" in data:
        schedule_time = data["schedule_time"]
    body = {"saveList":[{"configKey":"PATTERN_MODEL","configValue":{"patternModel":patternModel}},
                        {"configKey":"STOCK","configValue":{"lockStock":lockStock,"salesStockLockPreTime":salesStockLockPreTime}},
                        {"configKey":"MESSAGE","configValue":{"needSendMessage":needSendMessage,"noInteractionMessage":
                            {"firstMessageTemplate":{"topMessage":noInteractionFirstTopMessage},"firstMessageButton":noInteractionFirstMessageButton,
                             "secondMessageTemplate":{"topMessage":noInteractionSecondTopMessage},"secondMessageButton":noInteractionSecondMessageButton},
                           "hasInteractionMessage":{"firstMessageTemplate":{"topMessage":hasInteractionTopMessage},"messageButton":hasInteractionMessageButton},"hasLink":True}},
                        {"configKey":"COMMENT_REPLY","configValue":{"need_reply":comment_reply_need_reply,"content":comment_reply_content}},
                        {"configKey":"ALL_OUT_OF_STOCK_POST","configValue":{"need_reply":all_out_of_stock_need_reply,
                        "content":all_out_of_stock_content}},{"configKey":"SCHEDULE_TIME","configValue":{"salesPreEndTime":schedule_time}}]}
    requests.post(url,headers=headers,json=body).json()
    time.sleep(3)
    #修改后获取通用配置
    response = requests.get(url,headers=headers).json()
    return response

def copy_post(data):
    """
    复制单个贴文销售
    :param data:
    :return: 复制生成贴文的sales_id，请求内容
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/copy/%s"%(env,sales_id)
    response = requests.post(url,headers=headers).json()
    sales_id = response["data"]["id"]
    return sales_id,response

def end_post(data):
    """
    手动结束贴文
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/disconnectPost/%s"%(env,sales_id)
    response = requests.put(url,headers=headers).json()
    return response

def get_oa_payment(data):
    env = data["env"]
    headers = data["headers"]
    type_value = data["type"]
    name = ""
    if "name" in data:
        name = data["name"]
    url = "%s/openApi/proxy/v1/payments?page=1&per_page=999&include_fields[]=config_data.tappay"%env
    response = requests.get(url,headers=headers).json()
    type_list = [item["type"] for item in response["data"]["items"]]
    payment_ids = []
    for i in type_list:
        if i==type_value:
            index = type_list.index(i)
            payment_id = response["data"]["items"][index]["id"]
            payment_ids.append(payment_id)
    return payment_ids,response

def get_oa_delivery(data):
    env = data["env"]
    headers = data["headers"]
    type_value = data["type"]
    name = ""
    if "name" in data:
        name = data["name"]
    url = "%s/openApi/proxy/v1/delivery_options?page=1&per_page=999"%env
    response = requests.get(url,headers=headers).json()
    type_list = [item["type"] for item in response["data"]["items"]]
    delivery_ids = []
    for i in type_list:
        if i==type_value:
            index = type_list.index(i)
            delivery_id = response["data"]["items"][index]["id"]
            delivery_ids.append(delivery_id)
    return delivery_ids,response

def set_payment(data):
    env = data["env"]
    headers = data["headers"]
    customer_id = data["customer_id"]
    owner_type = data["owner_type"]
    url = "%s/openApi/proxy/v1/internal/mc/api/carts/%s?owner_type=%s&cart_uid=%s&created_by=sc_manual_order&skip_reapply_promotion=false"%(
        env,customer_id,owner_type,customer_id
    )
    payment_id = ""
    if "payment_id" in data:
        payment_id = data["payment_id"]
    else:
        payment_ids,__ = get_oa_payment(data)
        payment_id = payment_ids[0]
    body = {

      "owner_id": customer_id,
      "payment_id": payment_id
    }
    response = requests.put(url, headers=headers, json = body).json()
    return response


def set_delivery(data):
    env = data["env"]
    headers = data["headers"]
    customer_id = data["customer_id"]
    owner_type = data["owner_type"]
    url = "%s/openApi/proxy/v1/internal/mc/api/carts/%s?owner_type=%s&cart_uid=%s&created_by=sc_manual_order&skip_reapply_promotion=false" % (
        env, customer_id, owner_type, customer_id
    )
    country = "TW"
    if "country" in data:
        country = data["country"]
    delivery_id = ""
    if "delivery_id" in data:
        delivery_id = data["delivery_id"]
    else:
        delivery_ids, __ = get_oa_delivery(data)
        delivery_id = delivery_ids[0]
    body = {
      "delivery_option_id": delivery_id,
      "country": country,
      "owner_id": customer_id,
      "payment_id": ""
    }
    response = requests.put(url, headers=headers, json=body).json()
    return response

def get_mc_order_link(url):
    response = requests.get(url)
    print(response.headers)
    location = response.headers.get("Location")
    # print(location)
    key = location.split("/")[-1].split("?")[0]
    return key

def edit_message(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/keyword_message" % (env,sales_id)
    has_interaction_message = "您好，以下商品加单成功！购物车商品总金额: 请按以下按钮结账%d" % int(time.time())
    no_interaction_message_first = "您好，以下商品加单成功 !购物车商品总金额: 请按以下按钮继续」%d" % int(time.time())
    second_message = "您好，以下商品加单成功！{products} 购物车商品总金额: {total}请前往购物网站！%d" % int(time.time())
    first_message_button = "继续"
    second_message_button = "立即结帐 ️"
    need_send_message = True
    message_button = "立即结帐️"
    has_link = True
    #留言回复comment_reply
    comment_reply = True
    comment_reply_content = "testcopypost您好，谢谢你在贴文下留言订购以下商%d." % int(time.time())
    #无库存信息
    all_out_of_stock =True
    all_out_of_stock_content = "您好，{customerName}，以下商品库存不足，请选购其他商品，谢谢！{products}%d" % int(time.time())
    if "has_interaction_message" in data:
        has_interaction_message = data["has_interaction_message"]
    if "no_interaction_message_first" in data:
        has_interaction_message = data["no_interaction_message_first"]
    if "first_message_button" in data:
        first_message_button = data["first_message_button"]
    if "second_message" in data:
        second_message = data["second_message"]
    if "second_message_button" in data:
        second_message_button = data["second_message_button"]
    if "need_send_message" in data:
        need_send_message = data["need_send_message"]
    if "message_button" in data:
        message_button = data["message_button"]
    if "has_link" in data:
        has_link = data["has_link"]
    if "comment_reply" in data:
        comment_reply = data["comment_reply"]
    if "comment_reply_content" in data:
        comment_reply_content = data["comment_reply_content"]
    if "all_out_of_stock" in data:
        all_out_of_stock = data["all_out_of_stock"]
    if "all_out_of_stock_content" in data:
        all_out_of_stock_content = data["all_out_of_stock_content"]

    message = {"has_interaction_message":has_interaction_message,"no_interaction_message_first":no_interaction_message_first,
               "first_message_button":first_message_button,"second_message_button":second_message_button,"second_message":second_message,
              "comment_reply_content":comment_reply_content,"all_out_of_stock_content" :all_out_of_stock_content

    }
    body = {"message_config_req": {"need_send_message": need_send_message,
                                   "no_interaction_message": {"first_message": no_interaction_message_first,
                                                              "first_message_button": first_message_button,
                                                              "second_message":second_message ,
                                                              "second_message_button": second_message_button},
                                   "has_interaction_message": {"first_message": has_interaction_message,
                                                               "message_button": message_button}, "has_link": has_link},
            "comment_reply_req": {"need_reply": comment_reply, "content": comment_reply_content},
            "all_out_of_stock_req": {"need_reply": all_out_of_stock, "content": all_out_of_stock_content}}
    response = requests.post(url, headers=headers, json = body).json()
    return message,response



if __name__=="__main__":
    pass