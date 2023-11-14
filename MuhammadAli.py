import random
import ssl
import time
from threading import Thread

import capmonster_python
import requests
import cloudscraper
from capmonster_python import RecaptchaV2Task, RecaptchaV3Task

from bs4 import BeautifulSoup
from eth_account.messages import encode_defunct
from tqdm import tqdm
from web3.auto import w3
import imaplib
import email
from email.header import decode_header
import re

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def random_user_agent():
    browser_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{2}_{3}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{1}.{2}) Gecko/20100101 Firefox/{1}.{2}',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Edge/{3}.{4}.{5}'
    ]

    chrome_version = random.randint(70, 108)
    firefox_version = random.randint(70, 108)
    safari_version = random.randint(605, 610)
    edge_version = random.randint(15, 99)

    chrome_build = random.randint(1000, 9999)
    firefox_build = random.randint(1, 100)
    safari_build = random.randint(1, 50)
    edge_build = random.randint(1000, 9999)

    browser_choice = random.choice(browser_list)
    user_agent = browser_choice.format(chrome_version, firefox_version, safari_version, edge_version, chrome_build, firefox_build, safari_build, edge_build)

    return user_agent

class Twitter:

    def __init__(self, auth_token, csrf, proxy):

        self.session = self._make_scraper()
        self.session.proxies = proxy
        self.session.user_agent = random_user_agent()

        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        authorization_token = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

        self.csrf = csrf
        self.auth_token = auth_token
        self.cookie = f'auth_token={self.auth_token}; ct0={self.csrf}'

        liketweet_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {authorization_token}',
            'x-csrf-token': self.csrf,
            'cookie': self.cookie
        }

        self.session.headers.update(liketweet_headers)

        # print('Аккаунт готов')


    # Основные функции твиттер аккаунта

    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )

    def MyNickname(self):

        with self.session.get("https://api.twitter.com/1.1/account/settings.json", timeout=10) as response:
            return response.json()['screen_name']

    def Tweet(self, text="Just applied for the @MuhammadAliNFT allowlist!\n\nOn-chain generative art by @Ze_blocks "):

        payload = {"variables": {
            "tweet_text": text,
            "dark_request": False,
            "media": {
                "media_entities": [],
                "possibly_sensitive": False
            },
            "withDownvotePerspective": False,
            "withReactionsMetadata": False,
            "withReactionsPerspective": False,
            "withSuperFollowsTweetFields": True,
            "withSuperFollowsUserFields": True,
            "semantic_annotation_ids": []
        }, "features": {
            "tweetypie_unmention_optimization_enabled": True,
            "vibe_api_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "interactive_text_enabled": True,
            "responsive_web_text_conversations_enabled": False,
            "responsive_web_twitter_blue_verified_badge_is_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": False,
            "verified_phone_label_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": False,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_enhance_cards_enabled": False
        },
            "queryId": "Tz_cZL9zkkY2806vRiQP0Q"
        }

        with self.session.post("https://api.twitter.com/graphql/Tz_cZL9zkkY2806vRiQP0Q/CreateTweet", json=payload,
                               timeout=30) as response:
            if response.ok:
                # print(response.text)
                return True

    def Follow(self, user_id):
        # Не работает
        self.session.headers.update({'Content-Type': 'application/json'})

        with self.session.post(f"https://api.twitter.com/1.1/friendships/create.json?user_id={user_id}&follow=True", timeout=30) as response:
            # print(response.text)

            if 'suspended' in response.text:
                # print(f'Аккаунт {self.name} забанен')
                return 'ban'
            else:
                return 1


class Account:

    def __init__(self, mode, proxy, address, auth_token, csrf, email, answer1, answer2, answer3):

        proxy = f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"

        self.mode = mode
        # self.cap_key = cap_key
        self.email = email
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3

        self.address = address.lower()
        self.tw_auth_token = auth_token
        self.tw_csrf = csrf
        self.proxy = {'http': proxy, 'https': proxy}

        self.session = self._make_scraper()
        self.session.proxies = self.proxy
        self.session.user_agent = random_user_agent()
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)


    def execute_task(self):

        if self.mode == '1':
            try:

                tw_acc = Twitter(proxy=self.proxy,
                        auth_token=self.tw_auth_token,
                        csrf=self.tw_csrf)

                status = tw_acc.Follow(1626447456941535240)
                time.sleep(1)

                if status == 'ban':
                    return 'Твиттер забанен'

                tw_acc.Tweet()
                time.sleep(1.5)

                nickname = tw_acc.MyNickname()

                payload = {'email': self.email,
                           'ethAddress': self.address,
                           'twitter': f'@{nickname}',
                           'userInput': self.answer1,
                           'userInput2': self.answer2,
                           'userInput3': self.answer3
                           }

            except:
                return 'Ошибка с твиттером'
        else:
            nickname = self.tw_auth_token

            payload = {'email': self.email,
                       'ethAddress': self.address,
                       'twitter': f'{nickname}',
                       'userInput': self.answer1,
                       'userInput2': self.answer2,
                       'userInput3': self.answer3
                       }

        try:

            with self.session.post("https://api.muhammadalinft.io/submit", json=payload, timeout=10) as response:

                print(response.text)

                if response.json()['message'] == 'Submission successfully created':
                    return 'Успешно зарегистрирован'
                else:
                    return 'Ошибка при регистрации'
        except:
            return 'Ошибка при регистрации'


    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )



if __name__ == '__main__':



    Addresses = []
    TW_data = []
    Proxys = []
    Emails = []
    Answers1 = []
    Answers2 = []
    Answers3 = []

    while True:
        mode = input('Выберите режим загона акканутов:\n\n'
                     '1 - В файле Twitters.txt находятся куки твиттер аккаунтов и будут выполнены все действия, которые указаны на сайте\n'
                     '2 - В файле Twitters.txt находятся ники, которые будут прописаны в форму\n')
        if mode not in ['1', '2']:
            print('Введите 1 или 2')
        else:
            break

    if mode == '1':
        with open('Files/Twitters.txt', 'r') as file:
            for i in file:
                data = i.strip('\n')
                ready = f"auth_token={data.split('auth_token=')[1].split(';')[0]}; ct0={data.split('ct0=')[1].split(';')[0]}"
                TW_data.append(ready)
    else:
        with open('Files/Twitters.txt', 'r') as file:
            for i in file:
                data = i.strip('\n')
                TW_data.append(data)


    with open('Files/Addresses.txt', 'r') as file:
        for i in file:
            data = i.strip('\n')
            Addresses.append(data)
    with open('Files/Proxys.txt', 'r') as file:
        for i in file:
            data = i.strip('\n')
            Proxys.append(data)
    with open('Files/Emails.txt', 'r') as file:
        for i in file:
            data = i.strip('\n')
            Emails.append(data)
    with open('Files/Answers_1.txt', 'r') as file:
        for i in file:
            data = i.strip('\n')
            Answers1.append(data)
    with open('Files/Answers_2.txt', 'r') as file:
        for i in file:
            data = i.strip('\n')
            Answers2.append(data)
    with open('Files/Answers_3.txt', 'r') as file:
        for i in file:
            data = i.strip('\n')
            Answers3.append(data)

    if len(Addresses) != len(Proxys) != len(TW_data) != len(Emails) != len(Answers1) != len(Answers2) != len(Answers3):
        print('Количество ресурсов в текстовиках разнятся, сделайте так, чтобы ресурсов было одинаковое кол-во')
        input()
        exit(1)


    if mode == '1':
        for i in range(len(Addresses)):
            try:
                rers = Account(proxy=Proxys[i],
                               address=Addresses[i],
                               auth_token=TW_data[i].split('auth_token=')[-1].split(';')[0],
                               csrf=TW_data[i].split('ct0=')[-1].split(';')[0],
                               email=Emails[i].split(':')[0],
                               answer1=Answers1[i],
                               answer2=Answers2[i],
                               answer3=Answers3[i],
                               mode=mode
                               ).execute_task()
            except:
                rers = 'Ошибка'
            print(i, '-', rers)

    else:

        for i in range(len(Addresses)):
            try:
                rers = Account(proxy=Proxys[i],
                               address=Addresses[i],
                               auth_token=TW_data[i],
                               csrf=TW_data[i],
                               email=Emails[i].split(':')[0],
                               answer1=Answers1[i],
                               answer2=Answers2[i],
                               answer3=Answers3[i],
                               mode=mode
                               ).execute_task()
            except:
                rers = 'Ошибка'
            print(i, '-', rers)


    print('\nАбуз окончен')
    input()

