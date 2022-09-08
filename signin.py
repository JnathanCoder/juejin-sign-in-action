import os

import requests

# 添加 server 酱通知
server_key = os.environ["SERVER_KEY"]
# 添加 息知通知
# https://xz.qqoq.net/#/index
xz_key = os.environ["XZ_KEY"]

# 获取掘金 cookie
jj_cookie = os.environ["JJ_COOKIE"]

# 掘金 api_url
baseUrl = 'https://api.juejin.cn/'
checkInUrl = baseUrl + 'growth_api/v1/check_in'
lotteryUrl = baseUrl + 'growth_api/v1/lottery/draw'
# 沾手气列表
dipLuckyListUrl = baseUrl + 'growth_api/v1/lottery_history/global_big'
dipLuckyUrl = baseUrl + 'growth_api/v1/lottery_history/dip_lucky'

# user-agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}

# server 酱消息推送
# def send_server(title, content):
#     url = "https://sctapi.ftqq.com/%s.send" % server_key
#     params = {'text': title, 'desp': content}
#     resp = requests.post(url, params=params)
#     print('server 酱推送状态码: %s' % resp.status_code)

# server 息知消息推送
def xz_server(title, content):
    url = "https://xizhi.qqoq.net/%s.send" % xz_key
    params = {'title': title, 'content': content}
    resp = requests.post(url, params=params)
    print('息知 推送状态码: %s' % resp.status_code)

# 入口
if __name__ == '__main__':
    # checkInResp = requests.post(checkInUrl, headers=headers, cookies={'Cookie': jj_cookie})
    # lotteryResp = requests.post(lotteryUrl, headers=headers, cookies={'Cookie': jj_cookie})
    dipLuckyListResp = requests.post(dipLuckyListUrl, headers=headers, cookies={'Cookie': jj_cookie}, data={page_no: 1, page_size: 5})
    # resultMsg = "签到结果\n" + checkInResp.text + "\n 抽奖结果\n" + lotteryResp.text
    if xz_server:
        # xz_server('掘金签到+每日抽奖', resultMsg)
        xz_server('------', dipLuckyListResp.json())
    else:
        print('未启用 息知通知')
    # print('本次签到与抽奖结果信息:\n %s' % resultMsg)
