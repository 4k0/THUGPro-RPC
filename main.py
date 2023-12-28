import time
from utils.utils import get_user_ip, find_hostname, search_hostname, update_discord_presence
from pypresence import Presence
from config import DISCORD_APP_ID, STATS_FILE_URL, API_URL, IP_RETRY_INTERVAL, SEARCH_RETRY_INTERVAL, UPDATE_INTERVAL, HEARTBEAT_INTERVAL

def main():
    rpc = Presence(DISCORD_APP_ID)
    rpc.connect()

    while True:
        #tries to get ip
        user_ip = None
        while user_ip is None:
            print("IP not found, trying again...")
            time.sleep(IP_RETRY_INTERVAL)
            user_ip = get_user_ip()

        # finds
        target_hostname = find_hostname(user_ip, STATS_FILE_URL)

        while target_hostname is None:
            # retry if hostname not found
            print("Hostname not found, retrying...")
            time.sleep(SEARCH_RETRY_INTERVAL)
            target_hostname = find_hostname(user_ip, STATS_FILE_URL)

        # additional info
        server_info = search_hostname(API_URL, target_hostname)

        while True:
            update_discord_presence(rpc, server_info)
            time.sleep(UPDATE_INTERVAL)

            # i tried to make it update
            new_server_info = search_hostname(API_URL, target_hostname)
            if new_server_info != server_info:
                server_info = new_server_info
                break

        # delay thing
        time.sleep(HEARTBEAT_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script terminated by user.")
