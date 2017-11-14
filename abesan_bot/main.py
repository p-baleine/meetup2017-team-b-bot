import os
import re
import time
import pygsheets

from slackclient import SlackClient

import abesan_bot.knowledge as knowledge
import abesan_bot.tutorial as tutorial

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

SHEET_ID = "1AuqnYXBsy8dwij7K--kNLHPo9m-EhicVP2gA6nJIawQ"
BOT_ID = "U7ZGBME1H"
ABE_CHANNEL_ID = "C6GV7G26M"
SAKAI_CHANNEL_ID = "C73273N5B"
CHANNEL_ID = "G80LARY5D" # FIXME これは外出しないと複数で開発する時面倒くさい

def is_invited_event(event):
    return ("type" in event and event["type"] == "member_joined_channel"
            and event["user"] == BOT_ID
            and event["channel"] in [ABE_CHANNEL_ID, SAKAI_CHANNEL_ID, CHANNEL_ID])

def is_message_event(event):
    # 面倒くさいのでハードコーディングしたCHANNEL_IDに一致するかだけチェックする
    # CHANNEL_IDには1人しかユーザーがいない想定
    return ("type" in event and event["type"] == "message"
            and event["channel"] == CHANNEL_ID and "bot_id" not in event
            and re.match(r"^@abe", event["text"]))

def send_message(channel, text):
    text = text if text is list else [text]
    for t in text:
        sc.api_call("chat.postMessage", channel=channel,
                    text=text )
        sleep(0.5)

if __name__ == "__main__":
    gc = pygsheets.authorize(outh_file='client_secret.json')
    sh = gc.open_by_key(SHEET_ID)
    wks_list = sh.worksheets()
    sequence = tutorial.Sequence(wks_list[0].get_as_df())
    knowledge = knowledge.Knowledge(wks_list[1].get_as_df())

    print("Bot ready")

    if sc.rtm_connect():
        while True:
            for event in sc.rtm_read():
                if is_invited_event(event):
                    print("Invitation event:", event)
                    msg = sequence.next(event)
                    send_message(event["channel"], msg)
                elif is_message_event(event):
                    print("Message event:", event)
                    msg = knowledge.query(event)
                    send_message(event["channel"], msg)
                else:
                    print("Unknown event:", event)
            time.sleep(1)
    else:
        print("Connection Failed")
