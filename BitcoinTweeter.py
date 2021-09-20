import requests
import time
import tweepy


def get_current_block():
    url = "https://api.blockchair.com/bitcoin/stats"
    r = requests.get(url)
    return (r.json()['data']['blocks']) - 1


def get_block_info(block):
    api = "https://api.blockchair.com/bitcoin/dashboards/block/"  # Website to get block data
    url = api + str(block)  # form url to get block data
    return requests.get(url)


def has_new_block_been_mined(current):
    if current < get_current_block():
        return True
    return False


def twitter_api():
    consumer_key = ''
    consumer_secret = ''
    access_key = ''
    access_secret = ''
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        return auth
    except Exception as e:
        return None


def create_tweet(r, block):
    OAuth = twitter_api()
    api = tweepy.API(OAuth)
    block_time = (r.json()['data'][str(block)]['block']['time'] + " GMT")  # Time found
    block_size = (r.json()['data'][str(block)]['block']['size'])  # Block size
    block_difficulty = (r.json()['data'][str(block)]['block']['difficulty'])  # Block difficulty
    block_transactions = (r.json()['data'][str(block)]['block']['transaction_count'])  # Transaction count
    print("Block: " + str(block) + "\nTime: " + str(block_time) + "\nSize: " + str(block_size) + " Bytes" +
          "\nDifficulty: " + str(block_difficulty) + "\nNumber Of Transactions: " + str(block_transactions))

    api.update_status("Block: " + str(block) + "\nTime: " + str(block_time) + "\nSize: " + str(
        block_size) + " Bytes" + "\nDifficulty: " + str(block_difficulty) + "\nNumber Of Transactions: " + str(
        block_transactions))


def main():
    current_block = get_current_block()
    new_block = True
    while True:
        if new_block:
            current_block = get_current_block()
            r = get_block_info(current_block)
            create_tweet(r, current_block)
            new_block = False
        else:
            new_block = has_new_block_been_mined(current_block)
        time.sleep(60)


if __name__ == "__main__":
    main()
