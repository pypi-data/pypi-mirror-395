import json
import ssl
import time

import websockets
import asyncio
import requests
import websocket

# 定义回调函数
class WebSocketClient():
    def __init__(self, url,admin_url, sales_id):
        self.url = url
        self.admin_url = admin_url
        self.sales_id = sales_id
        self.ws = websocket.WebSocketApp(self.url, on_open=self.on_open,on_message=self.on_message,
                                         on_error=self.on_error,on_close=self.on_close)

    def on_open(self, ws):
        print("连接已打开")
        subscribeToken, userToken = get_imtoken(self.admin_url,self.sales_id)
        stamp = int(time.time()*1000)
        reqid = "53%d"%stamp
        device = {
            "version": 1,
            "reqid": reqid,
            "payload": {
                "appid": "SL101-web",
                "devid": "7ecce8fc-44af-4c65-b75b-aa84b%d"%stamp,
                "sdkver": "1.1.0"
            },
            "type": "REQUEST",
            "url": "ap://auth/device",
            "sign": "TDbwNFgmAPEPG5VGn5ozdSShpPPHK8PVsir9VXQ1ygx/RaeKjJ8lRnWf+gZ9wUH72EkgjSFGHaisv77wE8sgBBxxUud81V19t/mJY03MUwPQLSxJEY0hPPPr4mGhDK4IxYx154OJieyiDKNR5zO3jiGrEFWSn1Ft/0uMugkHQe8="
        }
        # 将消息转换为 JSON 格式并发送
        ws.send(json.dumps(device))
        subscribe = {
            "version": 1,
            "reqid": reqid,
            "payload": {
                "groups": [
                    "POST_%d"%self.sales_id,
                    "VIEW_ONLINE_%d"%self.sales_id
                ],
                "token": subscribeToken
            },
            "type": "REQUEST",
            "url": "http://broadcast/broadcast/subscribe",
            "sign": "gaoLzQ6q1+Fn5uq0UqHAamaKJieEvMXRqo+rwR0u9WZnBhJ27StRlWohqCsO89/QyJvxupaGPuCwLpPji/xfMpeHacmodUrWO3J/EffRX0lGeIo+Zz35XjqleFruaXmu1GGkCQ82SZmNdaAo6YrGN//twyiIPNH3KZ7xNRO/+dI="
        }
        ws.send(json.dumps(subscribe))

    def on_message(self,ws,message):
        print("收到消息:", message)

    def on_error(self,ws,error):
        print("发生错误:", error)

    def on_close(self,ws, res1, res2):
        print("连接已关闭", res1, res2)
        self.ws.close()

    def run(self):
        self.ws.run_forever()

    def close(self):
        print("主动关闭")
        self.ws.close()



def get_imtoken(admin_url,sales_id):
    url = "%s/api/posts/live/viewer/unauthorized/post/sales/%d/user/info?appId=SL101-web"%(admin_url,sales_id)
    headers = {"content-type":"application/json"}
    response = requests.get(url,headers=headers).json()
    subscribeToken = response["data"]["subscribeToken"]
    userToken = response["data"]["userToken"]
    # print(subscribeToken)
    return subscribeToken,userToken


async def client(url,message):
    async with websockets.connect(url) as websocket:
        for msg in message:
            await websocket.send(json.dumps(msg))
            response = await websocket.recv()
            print(response)

async def live_view_client(socket_url,admin_url,sales_id):
    subscribeToken, userToken = get_imtoken(admin_url, sales_id)
    message = []
    stamp = int(time.time() * 1000)
    reqid = "53%d" % stamp
    #绑定设备
    device = {
        "version": 1,
        "reqid": reqid,
        "payload": {
            "appid": "SL101-web",
            "devid": "7ecce8fc-44af-4c65-b75b-aa84b%d" % stamp,
            "sdkver": "1.1.0"
        },
        "type": "REQUEST",
        "url": "ap://auth/device",
        "sign": "TDbwNFgmAPEPG5VGn5ozdSShpPPHK8PVsir9VXQ1ygx/RaeKjJ8lRnWf+gZ9wUH72EkgjSFGHaisv77wE8sgBBxxUud81V19t/mJY03MUwPQLSxJEY0hPPPr4mGhDK4IxYx154OJieyiDKNR5zO3jiGrEFWSn1Ft/0uMugkHQe8="
    }
    # 订阅 将消息转换为 JSON 格式并发送

    subscribe = {
        "version": 1,
        "reqid": reqid,
        "payload": {
            "groups": [
                "POST_%d" % sales_id,
                "VIEW_ONLINE_%d" % sales_id
            ],
            "token": subscribeToken
        },
        "type": "REQUEST",
        "url": "http://broadcast/broadcast/subscribe",
        "sign": "gaoLzQ6q1+Fn5uq0UqHAamaKJieEvMXRqo+rwR0u9WZnBhJ27StRlWohqCsO89/QyJvxupaGPuCwLpPji/xfMpeHacmodUrWO3J/EffRX0lGeIo+Zz35XjqleFruaXmu1GGkCQ82SZmNdaAo6YrGN//twyiIPNH3KZ7xNRO/+dI="
    }
    message.append(device)
    message.append(subscribe)
    await client(socket_url,message)




if __name__=="__main__":
    pass
    # admin_url = "https://front-service.shoplinestg.com"
    # url = "ws://service-websocket.myshoplinestg.com/"
    # url = "ws://api-webservice-preview.myshopline.com"
    # url = "ws://api-webservice.myshopline.com"
    # admin_url = "https://front-admin.shoplineapp.com"
    # webSocketClient = WebSocketClient(url,admin_url,561242)
    # webSocketClient.run()
    # webSocketClient.close()
    # asyncio.run(live_view_client(url,admin_url,561242))
    #启用多个客户端


