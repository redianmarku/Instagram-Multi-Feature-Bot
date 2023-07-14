#!/usr/bin/env python3

import argparse
import json
import customtkinter
from InstagramBot import InstagramBot

def load_accounts():
    try:
        with open("accounts.json", "r") as file:
            accounts = json.load(file)
    except FileNotFoundError:
        accounts = []
    return accounts

def save_accounts(accounts):
    with open("accounts.json", "w") as file:
        json.dump(accounts, file)

def create_bot(account):
    bot = InstagramBot()
    bot.login(email=account["username"], password=account["password"])
    return bot

def main():
    parser = argparse.ArgumentParser(description="Instagram Bot")

    parser.add_argument("-c", "--comment", action="store_true", help="Comment on posts")
    parser.add_argument("-d", "--dm", action="store_true", help="Send direct messages")
    parser.add_argument("-ht", "--hashtag", help="Hashtag to scrape posts from")
    parser.add_argument("-cm", "--message", help="Comment or message to post")
    parser.add_argument("-del", "--delay", type=int, default=5, help="Delay in seconds between actions")

    args = parser.parse_args()

    app = customtkinter.CTk()
    app.title("Instagram Bot")
    app.geometry("800x600")

    frame = customtkinter.CTkFrame(app, width=800, height=600)
    frame.pack(fill=customtkinter.BOTH, expand=True)

    entry_username = customtkinter.CTkEntry(frame, placeholder_text="Username",
                                            height=40,
                                            width=400,
                                            corner_radius=15,
                                            placeholder_text_color="gray",
                                            fg_color="#192e2d",
                                            font=("Arial", 20, "bold"))

    entry_password = customtkinter.CTkEntry(frame, placeholder_text="Password",
                                            height=40,
                                            width=400,
                                            corner_radius=15,
                                            placeholder_text_color="gray",
                                            fg_color="#192e2d",
                                            font=("Arial", 20, "bold"))

    textbox = customtkinter.CTkTextbox(frame, width=400, corner_radius=5, height=100)

    check_var_1 = customtkinter.StringVar(value="on")
    checkbox_1 = customtkinter.CTkCheckBox(frame, text="Comment/Message",
                                           variable=check_var_1,
                                           onvalue="on",
                                           offvalue="off",
                                           font=("Arial", 16, "bold"))

    check_var_2 = customtkinter.StringVar(value="on")
    checkbox_2 = customtkinter.CTkCheckBox(frame, text="Send Direct Messages",
                                           variable=check_var_2,
                                           onvalue="on",
                                           offvalue="off",
                                           font=("Arial", 16, "bold"))

    entry_hash = customtkinter.CTkEntry(frame, placeholder_text="Hashtag",
                                        height=33,
                                        width=300,
                                        corner_radius=15,
                                        placeholder_text_color="gray",
                                        fg_color="#474131",
                                        font=("Arial", 15, "bold"))

    entry_comment = customtkinter.CTkEntry(frame, placeholder_text="Comment/Message",
                                           height=33,
                                           width=300,
                                           corner_radius=15,
                                           placeholder_text_color="gray",
                                           fg_color="#474131",
                                           font=("Arial", 15, "bold"))

    entry_delay = customtkinter.CTkEntry(frame, placeholder_text="Delay (in seconds)",
                                         height=33,
                                         width=300,
                                         corner_radius=15,
                                         placeholder_text_color="gray",
                                         fg_color="#474131",
                                         font=("Arial", 15, "bold"))

    def add_account():
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password:
            textbox.insert("end", "Please enter a username and password.\n")
            return

        account = {
            "username": username,
            "password": password
        }

        bot = create_bot(account)
        accounts = load_accounts()
        accounts.append(account)
        save_accounts(accounts)

        textbox.insert("end", f"Account added: {username}\n")

    def start_bot():
        accounts = load_accounts()

        if len(accounts) == 0:
            textbox.insert("end", "No accounts found. Please add accounts first.\n")
            return

        if checkbox_1.get() == "on" and checkbox_2.get() == "on":
            textbox.insert("end", "Please choose either commenting or sending direct messages.\n")
            return

        if checkbox_1.get() == "on":
            if not entry_hash.get() or not entry_comment.get():
                textbox.insert("end", "Please provide a hashtag and a comment/message.\n")
                return

            hashtag = entry_hash.get()
            comment = entry_comment.get()

            bot = create_bot(accounts[0])
            post_links = bot.scrape_hashtag_posts(hashtag=hashtag)
            bot.comment_on_posts(links=post_links, comment=comment, delay_time=args.delay)

            textbox.insert("end", "Commenting started.\n")

        if checkbox_2.get() == "on":
            if not entry_comment.get():
                textbox.insert("end", "Please provide a comment/message.\n")
                return

            comment = entry_comment.get()

            bot = create_bot(accounts[0])
            post_links = bot.scrape_hashtag_posts(hashtag=hashtag)
            usernames = bot.scrape_usernames(post_links)
            bot.send_dm(usernames=usernames, message=comment, delay_time=args.delay)

            textbox.insert("end", "Sending direct messages started.\n")

    entry_username.pack(pady=10)
    entry_password.pack(pady=10)
    button = customtkinter.CTkButton(frame, text="Add account", command=add_account,
                                     font=("Arial", 15, "bold"))
    button.pack(pady=10)
    textbox.pack(pady=15)
    checkbox_1.pack(pady=10)
    checkbox_2.pack(pady=10)
    entry_hash.pack(pady=5)
    entry_comment.pack(pady=5)
    entry_delay.pack(pady=5)
    button_start = customtkinter.CTkButton(frame, text="Start", command=start_bot,
                                           font=("Arial", 15, "bold"),
                                           corner_radius=10)
    button_start.pack(pady=25)

    app.mainloop()

if __name__ == "__main__":
    main()

