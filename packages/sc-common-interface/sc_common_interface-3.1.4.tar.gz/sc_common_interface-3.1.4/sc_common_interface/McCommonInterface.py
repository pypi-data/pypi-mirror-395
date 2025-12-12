import datetime
import requests
import json
from jsonpath import jsonpath
import time
import random
import hmac
from hashlib import sha1
import random

def send_mc_message(data):
    env = data["env"]
    key = data["key"]
    stamp = int(time.time()*1000)
    user_id = "488864%d" % int(time.time())
    if "user_id" in data:
        user_id = data['user_id']
    name = "test live%d" % int(time.time())
    if "name" in data:
        name = data['name']
    message = "接口测试普通留言"
    if "message" in data:
        message = data['message']
    page_id = ""
    if "page_id" in data:
        page_id = data['page_id']
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data['platform']
    type = "text"
    if "type" in data:
        type = data["type"]
    mid = "m_hhAqPhSlMTY4En2oWjSB59T3BFjeU97DdDV4WHr3DLWnPrO0iCsjQlG3hBN%d-sBlT26-6oNg" % stamp
    if "mid" in data:
        mid = data["mid"]
    body={}
    if "body" in data:
        body = data["body"]
    if platform.upper() == "FACEBOOK":
        if type=="text":
            body = {"entry": [{"id": "%s" % page_id, "messaging": [{"message":
              {
               "mid": mid,
                "text": "%s" % message},
                 "recipient": {"id": "%s" % page_id},
                 "sender": {"id": "%s" % user_id}, "timestamp": stamp}],
                 "time": stamp}], "object": "page"}
        elif type=="gif":
            body = {"entry": [{"id": "%s" % page_id, "messaging": [{"message":{
                "mid": mid,
                "attachments": [{"type": "image", "payload": {
                    "url": "https://cdn.fbsbx.com/v/t59.2708-21/267652425_2742112282760223_8342075864203047385_n.gif?_nc_cat=107\u0026ccb=1-7\u0026_nc_sid=cf94fc\u0026_nc_ohc=aa48LfY75iUQ7kNvgFdUHh0\u0026_nc_ht=cdn.fbsbx.com\u0026oh=03_Q7cD1QE9ftiyK21HTVYBWqW8JAaA-rEYS0ydqSuWlLUW5LwslA\u0026oe=66F73B3C"}}]
            },
            "recipient": {"id": "%s" % page_id},
            "sender": {"id": "%s" % user_id}, "timestamp": stamp}],
                           "time": stamp}], "object": "page"}
        elif type=="picture":
            body = {"entry": [{"id": "%s" % page_id, "messaging": [{"message": {
                "mid": mid,
                "attachments": [{"type": "image", "payload": {
                    "url": "https://cdn.fbsbx.com/v/t59.2708-21/267652425_2742112282760223_8342075864203047385_n.gif?_nc_cat=107\u0026ccb=1-7\u0026_nc_sid=cf94fc\u0026_nc_ohc=aa48LfY75iUQ7kNvgFdUHh0\u0026_nc_ht=cdn.fbsbx.com\u0026oh=03_Q7cD1QE9ftiyK21HTVYBWqW8JAaA-rEYS0ydqSuWlLUW5LwslA\u0026oe=66F73B3C"}}]
            },
                "recipient": {"id": "%s" % page_id},
                "sender": {"id": "%s" % user_id}, "timestamp": stamp}],
                               "time": stamp}], "object": "page"}
        elif type =="template":
            body = {"object":"page","entry":[{"id":"%s" % page_id,"time":stamp,"messaging":[{"sender":{"id":"%s" % user_id},"recipient":{"id":"%s" % page_id},"timestamp":stamp,"message":{"mid":mid,"text":"Hi，name1716183125。感謝您的支持和信任。這是您的訂單，請盡快完成付款。\n\n訂單編號:\n#20240926134206449\n創建時間:\n2024-09-26 20:42:10\n\n待付款金額：฿70.11","is_echo":True,"app_id":197583024153108,"metadata":"MC3.0_61b096beb7bef100245dbd8b","attachments":[{"type":"template","payload":{"template_type":"button","buttons":[{"type":"web_url","url":"https://message-center.shoplineapp.com/admin/user/order-checkout/634553c44e79c6f331c4ba1fe744199b?merchant_id=61b096beb7bef100245dbd8b\u0026locale=zh-hant","title":"去支付"}]}}]}}]}],"Fbe":False}
        elif type == "video":
            body = {"entry": [{"id": "%s" % page_id, "messaging": [{"message": {
                "mid": mid,
                "attachments": [{"type": "video", "payload": {
                    "url": "https://video.xx.fbcdn.net/v/t42.3356-2/432615672_8029825447033772_7739712335639564092_n.mp4?_nc_cat=108\u0026ccb=1-7\u0026_nc_sid=4f86bc\u0026_nc_ohc=b4-Y6xX1rtUQ7kNvgFmSRk_\u0026_nc_ht=video.xx\u0026_nc_gid=A-Pz8fTYZc89Un5kLMoLJMv\u0026oh=03_Q7cD1QG_WI1uD77MmN9xKAxXx3tZOL8muTvMgCFpNENoI9S7lw\u0026oe=66F74642"}}]
            },
                "recipient": {"id": "%s" % page_id},
                "sender": {"id": "%s" % user_id}, "timestamp": stamp}],
                               "time": stamp}], "object": "page"}
        elif type == "audio":
            body = {"entry": [{"id": "%s" % page_id, "messaging": [{"message": {
                "mid": mid,
                "attachments": [{"type": "audio", "payload": {
                    "url": "https://cdn.fbsbx.com/v/t59.3654-21/461150567_1761086874427012_6172811562215217140_n.wav/audio_clip.wav?_nc_cat=101\u0026ccb=1-7\u0026_nc_sid=d61c36\u0026_nc_ohc=L5BQtwl4CAgQ7kNvgGHihOx\u0026_nc_ht=cdn.fbsbx.com\u0026_nc_gid=AP5AR1-XZNRACEs4Q2hlS7w\u0026oh=03_Q7cD1QGwgqbQ-_sc078THHpQqaTSy83Xg9FpPv9DfswxesIBWw\u0026oe=66F754B6"}}]
            },
                "recipient": {"id": "%s" % page_id},
                "sender": {"id": "%s" % user_id}, "timestamp": stamp}],
                               "time": stamp}], "object": "page"}
        elif type == "file":
            body = {"entry": [{"id": "%s" % page_id, "messaging": [{"message": {
                "mid": mid,
                "attachments": [{"type": "file", "payload": {
                    "url": "https://cdn.fbsbx.com/v/t59.2708-21/372887834_1477966239657135_964223859622790441_n.xls/shopline.xls?_nc_cat=104\u0026ccb=1-7\u0026_nc_sid=2b0e22\u0026_nc_ohc=HD1EWsL_GAMQ7kNvgH1XAqH\u0026_nc_ht=cdn.fbsbx.com\u0026_nc_gid=AbQ5mUwXgVRLcTg_SDMsXuQ\u0026oh=03_Q7cD1QGbJ5rcs9fnkSYImAoSTVMEYZzCn0Uop0a1LT06MItUHw\u0026oe=66F743BF"}}]
            },
                "recipient": {"id": "%s" % page_id},
                "sender": {"id": "%s" % user_id}, "timestamp": stamp}],
                               "time": stamp}], "object": "page"}
        elif type == "image":
            body = {"entry": [{"id": "%s" % page_id, "messaging": [{"message": {
                "mid": mid,
                "attachments": [{"type": "image", "payload": {
                    "url": "https://scontent.xx.fbcdn.net/v/t1.15752-9/453334896_849046190144775_2687107896488738244_n.png?_nc_cat=106\u0026ccb=1-7\u0026_nc_sid=fc17b8\u0026_nc_ohc=PHylk2lIl2UQ7kNvgE62hJr\u0026_nc_ad=z-m\u0026_nc_cid=0\u0026_nc_ht=scontent.xx\u0026_nc_gid=A1lL9UZ_Rb3le2HUKS5-i7y\u0026oh=03_Q7cD1QFfWFzhNi_lgujYyTyBM5c5YPONyX7YXKLN4du04YHU7A\u0026oe=671CD669"}}]
            },
                "recipient": {"id": "%s" % page_id},
                "sender": {"id": "%s" % user_id}, "timestamp": stamp}],
                               "time": stamp}], "object": "page"}
        elif type == "product":
            body = {"entry": [{"id": "%s" % page_id, "messaging": [{"message": {
                "mid": mid,
                "text":"Hi！快來看看我們為您挑選的精選商品👇\nhttps://shln.me/HT/gb0sQ"
                     },
                "recipient": {"id": "%s" % page_id},
                "sender": {"id": "%s" % user_id}, "timestamp": stamp}],
                               "time": stamp}], "object": "page"}

    if platform.upper()=="INSTAGRAM":
        body={"object":"instagram","entry":[{"time":stamp,"id":"%s"%page_id,"messaging":[{"sender":{"id":"%s"%user_id},"recipient":{"id":"%s"%page_id},
       "timestamp":stamp,"message":{"mid":mid,"text":"%s"%message}}]}]}
    url = "%s/facebook/webhook" % env
    sign_text = hmac.new(key.encode("utf-8"), json.dumps(body).encode("utf-8"), sha1)
    signData = sign_text.hexdigest()
    header = {"Content-Type": "application/json", "x-hub-signature": "sha1=%s" % signData}
    response = requests.post(url, headers=header, data=json.dumps(body))
    return user_id, name,mid


if __name__=="__main__":
    data = {'env': 'https://front-admin-preview.shoplineapp.com', 'key': '5e3bba98882fc0fb22a0607238bc5b8f', 'page_id': '108513131786753'}
    data["type"] = "product"
    user_id, name,mid = send_mc_message(data)
    # data["mid"] = mid
    # send_mc_message(data)

