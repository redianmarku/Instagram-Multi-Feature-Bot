import argparse
import json
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

    parser.add_argument("-a", "--accounts", action="store_true", help="Use multiple accounts")
    parser.add_argument("-c", "--comment", action="store_true", help="Comment on posts")
    parser.add_argument("-d", "--dm", action="store_true", help="Send direct messages")
    parser.add_argument("-ht", "--hashtag", help="Hashtag to scrape posts from")
    parser.add_argument("-cm", "--message", help="Comment or message to post")
    parser.add_argument("-del", "--delay", type=int, default=5, help="Delay in seconds between actions")

    args = parser.parse_args()

    if args.accounts:
        accounts = load_accounts()

        if len(accounts) == 0:
            print("No accounts found. Please add accounts first.")
            return

        for i, account in enumerate(accounts):
            print(f"Account {i+1}: {account['username']}")

        account_choice = input("Select an account number: ")

        try:
            account_choice = int(account_choice)
            if account_choice < 1 or account_choice > len(accounts):
                print("Invalid account number.")
                return
        except ValueError:
            print("Invalid input.")
            return

        account = accounts[account_choice - 1]
        bot = create_bot(account)
    else:
        username = input("Enter your Instagram username: ")
        password = input("Enter your Instagram password: ")

        account = {
            "username": username,
            "password": password
        }
        bot = create_bot(account)

        save_accounts([account])

    if args.comment:
        if not args.hashtag or not args.message:
            print("Please provide a hashtag and a message to comment.")
            return

        post_links = bot.scrape_hashtag_posts(hashtag=args.hashtag)
        bot.comment_on_posts(links=post_links, comment=args.message, delay_time=args.delay)
    elif args.dm:
        if not args.message:
            print("Please provide a message to send.")
            return

        post_links2 = bot.scrape_hashtag_posts(hashtag=args.hashtag)
        usernames = bot.scrape_usernames(post_links2)
        bot.send_dm(usernames=usernames, message=args.message, delay_time=args.delay)
    else:
        print("Please choose whether to comment (-c) or send direct messages (-d).")

if __name__ == "__main__":
    main()
