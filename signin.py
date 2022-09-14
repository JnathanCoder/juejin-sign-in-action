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
dipLuckyUrl = baseUrl + 'growth_api/v1/lottery_lucky/dip_lucky'

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
    # 签到
    checkInResp = requests.post(checkInUrl, headers=headers, cookies={'Cookie': jj_cookie})
    checkInJson = checkInResp.json()
    if checkInJson['err_msg'] == 'success':
        checkInMsg = "签到结果： 成功！获得" + str(checkInJson['data']['incr_point']) + '钻石💎，当前：' + str(checkInJson['data']['sum_point'])
    else:
        checkInMsg = '签到结果：失败！原因：' + checkInJson["err_msg"]

    # 免费抽奖 可优化下根据get_today_status接口判断今日是否抽过奖
    lotteryResp = requests.post(lotteryUrl, headers=headers, cookies={'Cookie': jj_cookie})
    lotteryJson = lotteryResp.json()
    if lotteryJson['err_msg'] == 'success':
        lotteryMsg = '免费抽奖结果：成功！抽到' + lotteryJson['data']['lottery_name'] + '。幸运值提升' + str(lotteryJson["data"]["draw_lucky_value"]) + "点，当前：" + str(lotteryJson["data"]["total_lucky_value"]) + " / 6000"
    else:
        lotteryMsg = '免费抽奖结果：失败！原因' + lotteryJson["err_msg"]

    # 沾手气
    dipLuckyListResp = requests.post(dipLuckyListUrl, headers=headers, cookies={'Cookie': jj_cookie}, data={'page_no': 1, 'page_size': 5})
    listRespToJson = dipLuckyListResp.json()
    lottery_history_id = listRespToJson["data"]["lotteries"][0]["history_id"]
    dipLuckyResp = requests.post(dipLuckyUrl, headers=headers, cookies={'Cookie': jj_cookie}, data={'lottery_history_id': lottery_history_id})
    respToJson = dipLuckyResp.json()
    if respToJson["err_msg"] == 'success':
        if respToJson["data"]["has_dip"] == true:
            dipLuckyMsg = "沾手气结果：失败！原因：今日已沾过" + str(respToJson["data"]["dip_value"]) + "点喜气！"
        else:
            dipLuckyMsg = "沾手气结果: 成功！幸运值提升" + str(respToJson["data"]["dip_value"]) + "点，当前：" + str(respToJson["data"]["total_value"]) + " / 6000"
    else:
        dipLuckyMsg = "沾手气结果：失败！原因：" + respToJson["err_msg"]


    # resultMsg = "签到结果\n" + checkInResp.text + "\n 抽奖结果\n" + lotteryResp.text
    resultMsg = checkInMsg + "\n\n" + lotteryMsg + "\n\n" + dipLuckyMsg
    if xz_server:
        xz_server('掘金签到 && 免费抽奖 && 沾手气', resultMsg)
    else:
        print('未启用 息知通知')
