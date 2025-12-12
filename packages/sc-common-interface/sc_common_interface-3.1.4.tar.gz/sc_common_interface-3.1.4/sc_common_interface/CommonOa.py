import requests
from datetime import datetime,timedelta,timezone


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
    order_id = data["order_id"]
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
    order_id = data["order_id"]
    # 查询订单id
    url = "%s/v1/orders/%s/order_delivery_status" % (oa_env,order_id)
    body = {
        "status": status,
        "mail_notify": False
    }
    res = requests.patch(url, headers=oa_headers, json=body).json()
    return res

def delete_product(data):
    """可以删除组合商品和普通商品"""
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    product_id = data["product_id"]
    url = "%s/v1/products/%s"%(oa_env,product_id)
    res = requests.delete(url,headers=oa_headers).json()
    return res

def get_product(data):
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    product_id = data["product_id"]
    url = "%s/v1/products/%s" % (oa_env, product_id)
    res = requests.get(url, headers=oa_headers).json()
    return res

def edit_product_spu(data):
    """"
    编辑商品名称、隐藏价格、限购数量、预售时间，spu维度的编辑
    hide_price:false true
    隐藏商品/下架商品[status]: hidden、active、draft
    限购数量【max_order_quantity】：-1【不限购】
    商品名称格式：
    {'vi': '商品名称1734667300--多规格---编辑', 'th': '商品名称1734667300', 'zh-hant': '商品名称1734667300---编辑繁体', 'en': '商品名称1734667300-----编辑英文', 'id': '商品名称1734624132',
             'fr': '商品名称1734624132', 'zh-cn': '商品名称1734667300----多篇规格简体中文'}

    available_start_time 预购开始时间：格式："2024-12-25T15:00:00.000+00:00"
    available_end_time 预购结束时间：用不过期为null
    ------无规格商品编辑商品预购库存、无限库存-------
    unlimited_quantity：现货库存无限库存，True,False
    is_preorder【预购类型】：True,False
    preorder_limit:预购数量,无限数量为-1
    """
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    product_id = data["product_id"]
    url = "%s/v1/products/%s" % (oa_env, product_id)
    body = {}
    if "title" in data:
        title_translations = data["title"]
        body["title_translations"] = title_translations
    else:
        response = get_product(data)
        # print(response)
        title_translations = response["title_translations"]
        body["title_translations"] = title_translations

    if "hide_price" in data:
        hide_price = data["hide_price"]
        body["hide_price"] = hide_price
    if "status" in data:
        status = data["status"]
        body["status"] = status
    if "max_order_quantity" in data:
        max_order_quantity = data["max_order_quantity"]
        body["max_order_quantity"] = max_order_quantity
    if "available_start_time" in data:
        available_start_time = data["available_start_time"]
        available_end_time = data["available_end_time"]
        body["available_end_time"] = available_end_time
        body["available_start_time"] = available_start_time
    # if "quantity" in data:
    #     quantity = data["quantity"]
    #     body["quantity"] = quantity
    if "unlimited_quantity" in data:
        unlimited_quantity = data["unlimited_quantity"]
        body["unlimited_quantity"] = unlimited_quantity
    if "is_preorder" in data:
        is_preorder = data["is_preorder"]
        body["is_preorder"] = is_preorder
        if is_preorder==True:
            preorder_limit = data["preorder_limit"]
            body["preorder_limit"] = preorder_limit
    if "with_product_set" in data:
        with_product_set = data["with_product_set"]
        body["with_product_set"] = with_product_set
    # print(body)
    res = requests.put(url, headers=oa_headers, json=body).json()
    return res

def edit_spu_quantity(data):
    """更新无库存商品的现货库存数量"""
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    product_id = data["product_id"]
    url = "%s/v1/products/%s/update_quantity" % (oa_env, product_id)
    # print(url)
    quantity = 100
    if "quantity" in data:
        quantity = data["quantity"]
    body = {
      "quantity": quantity,
      "replace": True
        }
    # print(body)
    res = requests.put(url, headers=oa_headers, json=body).json()
    return res

def edit_sku_quantity(data):
    """更新指定规格的库存数量"""
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    product_id = data["product_id"]
    sku_id = data["sku_id"]
    url = "%s/v1/products/%s/variations/%s/update_quantity" % (oa_env, product_id,sku_id)
    quantity = 100
    if "quantity" in data:
        quantity = data["quantity"]
    body = {
      "quantity": quantity,
      "replace": True
        }
    res = requests.put(url, headers=oa_headers, json=body).json()
    return res

def edit_spu_price(data):
    """更新无库存商品的价格"""
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    product_id = data["product_id"]
    url = "%s/v1/products/%s/update_price" % (oa_env, product_id)
    body = {}
    if "price" in data:
        """原价"""
        price = data["price"]
        body["price"] = price
    if "price_sale" in data:
        """特价"""
        price_sale = data["price_sale"]
        body["price_sale"] = price_sale
    if "cost" in data:
        """成本价"""
        cost = data["cost"]
        body["cost"] = cost
    if "member_price" in data:
        """会员价"""
        member_price = data["member_price"]
        body["member_price"] = member_price
    if "retail_price" in data:
        """实体店价格"""
        retail_price = data["retail_price"]
        body["retail_price"] = retail_price

    res = requests.put(url, headers=oa_headers, json=body).json()
    return res

def edit_sku_price(data):
    """更新指定规格的价格"""
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    product_id = data["product_id"]
    sku_id = data["sku_id"]
    url = "%s/v1/products/%s/variations/%s/update_price" % (oa_env, product_id, sku_id)
    body = {}
    if "price" in data:
        """原价"""
        price = data["price"]
        body["price"] = price
    if "price_sale" in data:
        """特价"""
        price_sale = data["price_sale"]
        body["price_sale"] = price_sale
    if "cost" in data:
        """成本价"""
        cost = data["cost"]
        body["cost"] = cost
    if "member_price" in data:
        """会员价"""
        member_price = data["member_price"]
        body["member_price"] = member_price
    if "retail_price" in data:
        """实体店价格"""
        retail_price = data["retail_price"]
        body["retail_price"] = retail_price
    res = requests.put(url, headers=oa_headers, json=body).json()
    return res

def get_str_time(time_type="add",unit="days",num=1,format='%Y-%m-%dT%H:%M:%S.%f'):
    now = datetime.now()
    expect_time = now+timedelta(**{unit:num if time_type=="add" else -num})
    format_time = expect_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00'
    return format_time







if __name__=="__main__":
   pass






