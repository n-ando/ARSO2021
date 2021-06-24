#!/usr/bin/env python3

# https://qiita.com/sampo-cure/items/6b57d8503e37a0d2d1f6
##
# 1. Slack workspace を開設（要管理者権限）
#
# 2. Appを作成 (OAuth Tokens 取得)
# - https://api.slack.com/ にて Create App を行う。
# - workspace 名を指定する。
# - 左側メニュー "OAuth & Permissions" をクリック
# - Scopes にて、Bot Token Scopes の Add and OAuth Scope でを追加
# - channel作成に必要なScopeを追加
# https://api.slack.com/methods/conversations.create
# Bot tokenの場合は：
#   - channels:manage
#   - groups:write
#   - im:write
#   - mpim:write
# 上方の　OAuth Tokens for Your Workspace
# において、 Install to Workspace をクリック。許可を求めてくるので許可をクリック。
# Bot User OAuth Token に Tokenが表示されるので Copy ボタンを押す。
# クリップボードにコピーして、.slack_cmd/token にコピー
#

import os
import sys
import configparser

VERSION="1.0"
CONF_FILE = os.environ["HOME"] + "/.slackcmd/slackcmd.conf"
WS_NAME = ""
CHANNEL_NAME = ""
CH_PURPOSE = ""
CH_TOPIC = ""
CONFIG = None
TOKEN_STR = ""

def configure():
    global CONFIG
    global CONF_FILE
    global TOKEN_STR

    CONFIG = configparser.ConfigParser()
    fname = CONFIG.read(CONF_FILE)
    if len(fname) == 0:
        print("Configuration file not found:", CONF_FILE)
        sys.exit(1)

    section = "ieeerasarso2021"

    TOKEN_STR = CONFIG["ieeerasarso2021"]["token"]
    print(TOKEN_STR)

def create_channel():
    global TOKEN_STR
    global CHANNEL_NAME
    global CH_PURPOSE
    global CH_TOPIC
    token_str = TOKEN_STR
    channel_name = CHANNEL_NAME
    channel_purpose = CH_PURPOSE
    channel_topic = CH_TOPIC

    from slack_sdk import WebClient
    client = WebClient(token = token_str)
    response = client.conversations_create(name=channel_name, is_private=False)
    channel_id = response["channel"]["id"]
    print("Channel ID:", response["channel"]["id"])
    # set purpose
    if channel_purpose != None or channel_purpose.empty():
        response = client.conversations_setPurpose(channel=channel_id,\
                                                   purpose=channel_purpose)
        print(channel_purpose)
        print(response)
    if channel_topic != None or channel_purpose.empty():
        response = client.conversations_setTopic(channel=channel_id,\
                                                 topic=channel_topic)
        print(response)


topic_str="Development of a Simultaneous Tracking and Charging Function of the Wireless Power Supply Robot"
topic_str2="Asaka, Shogo (Hosei University), Kondo, Maiku (Hosei University), Toga, Syuhei (Daihen Corpration), Tsuruda, Yoshinori (Daihen Corpration), Nakamura, Sousuke (Hosei University)"


def help():
    help_msg="""
{_cmdname} {_version}, Slack チャネル作成コマンド
使い方: {_cmdname} [WS名] [オプション]...
長いオプションで不可欠な引数は短いオプションでも不可欠です。
スタートアップ:
  -v,  --version                   バージョン情報を表示して終了する
  -h,  --help                      このヘルプを表示する
チャネル生成内容指定:
  [WS名]                           ワークスペース名: <WS名>.slack.com の <WS名>
  -c,  --channel=channel_name      作成するチャネル名を指定する
  -p,  --purpose=purpose_text      チャネルに設定する説明を指定する
  -t,  --topic=topic_text          出力csvファイル名
    """.format(_cmdname=sys.argv[0],
               _version=VERSION).strip()
    print(help_msg)
    print("")

def parse_opt():
    import getopt
    global WS_NAME
    global CHANNEL_NAME
    global CH_PURPOSE
    global CH_TOPIC

    # check WS name
    if not len(sys.argv) > 3:
        print("At least WS name and an option required.")
        help()
        sys.exit(1)
    WS_NAME = sys.argv[1]
    if WS_NAME[0] == "-":
        print("Workspace name required.")
        help()
        sys.exit(1)

    try:
        opts, args = getopt.getopt(
            sys.argv[2:],
            'vhc:p:t:',
            ['version', 'help', 'channel=', 'purpose=', 'topic=']
        )
    except getopt.GetoptError as err:
        print("オプション指定が間違っています。")
        print(str(err))
        help()
        sys.exit(-1)

    exclude_list = []
    for o, a in opts:
        if o in ("-v", "--version"):
            version()
            sys.exit(0)
        if o in ("-h", "--help"):
            help()
            sys.exit(0)
        if o in ("-c", "--channel"):
            CHANNEL_NAME = a
        if o in ("-p", "--purpose"):
            CH_PURPOSE = a
        if o in ("-t", "--topic"):
            CH_TOPIC = a

    print("CHANNEL_NAME:", CHANNEL_NAME)

def main():
    parse_opt()
    configure()
    create_channel()

if __name__ == "__main__":
    main()