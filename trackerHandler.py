import discord
import websocket
import json

try:
    import thread
except ImportError:
    import _thread as thread
import time

async def on_message(ws, message: str):
    try:
        import mops
        print("data recieved: {0}".format(message))
        #data = message.split("Event number:")[1].split(sep="\n", maxsplit=1)
        #eventMessage = json.loads(data[1])
        #channel = mops.client.get_channel(eventMessage["ChannelId"])
        #embed = discord.Embed.from_dict(eventMessage["Embed"])
        #await channel.send(eventMessage["Notification"], embed=embed)
    except:
        pass

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print('ws open')

def startTrackerHandler():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:11000",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    