from slackclient import SlackClient

API_TOKEN="xoxb-172636780100-fn9GHw9mVOoOjsAqH49lv8ql"
sc = SlackClient(API_TOKEN)

def send_msg(msg):
    sc.api_call(
        "chat.postMessage",
        channel="#lectures",
        text=msg
    )

def main():
    send_msg("test")

if __name__ == "__main__":
    main()
