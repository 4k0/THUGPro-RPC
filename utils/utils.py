# utils/utils.py

import requests
from pypresence import Presence

def get_user_ip():
    try:
        with requests.get('https://api.ipify.org?format=json') as response:
            user_ip = response.json().get('ip')
            return user_ip
    except requests.RequestException as e:
        print(f"Error fetching user's IP: {e}")
        return None

def find_hostname(user_ip, stats_file_url):
    try:
        with requests.get(stats_file_url) as response:
            stats_content = response.text.split('\n')

        ip_port_line = next((line for line in stats_content if user_ip in line), None)

        if ip_port_line:
            port = ip_port_line.split()[1]
            search_string = f"{user_ip}:{port}"
            hostname_line = next((line for line in stats_content if search_string in line), None)

            if hostname_line:
                hostname = hostname_line.split("\\")[2]
                return hostname
            else:
                print(f"Hostname not found for {user_ip}:{port}")
                return None
        else:
            print(f"IP and port not found for {user_ip}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching stats file: {e}")
        return None

def search_hostname(api_url, target_hostname):
    try:
        with requests.get(api_url) as response:
            data = response.json()

        found_servers = [server for server in data if server.get("hostname") == target_hostname]

        if found_servers:
            return found_servers[0]
        else:
            print(f"No servers found with the hostname '{target_hostname}'.")
            return None

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def update_discord_presence(presence, server_info):
    if server_info:
        presence.update(
            details=f"Playing {server_info['gamemode']}",
            state=f"On {server_info['mapname']}",
            large_image="thugpro",
            large_text="By @4k0 on Github | @lxfd on Discord",
            small_image=None,
            small_text=None,
            buttons=[
                {"label": f"Server: {server_info.get('hostname', 'Unknown')}", "url": "http://beta.openspy.net/en/server-list/thugpro"},
                {"label": "Get THUGPro", "url": "https://thugpro.com"}
            ],
            party_id="PARTY",
            party_size=(server_info.get('numplayers', 0), server_info.get('maxplayers', 0))
        )
    else:
        presence.update(
            details="Online",
            state=None,
            large_image="thugpro",
            large_text="By @4k0 on Github | @lxfd on Discord",
            small_image=None,
            small_text=None,
            buttons=None,
            party_id="PARTY",
            party_size=(0, 0)
        )
