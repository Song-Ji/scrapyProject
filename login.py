import requests

# python2 和 python3的兼容代码
try:
    # python2 中
    import cookielib
    print(f"user cookielib in python2.")
except:
    # python3 中
    import http.cookiejar as cookielib
    print(f"user cookielib in python3.")

# session 代表某一次连接
# tangrenSession = requests.session()
# tangrenSession.cookies = cookielib.LWPCookieJar(filename="tangrenCookies.txt")

User_Agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36"
header = {
    # "origin": "https://passport.mafengwo.cn",
    "Referer": "http://tangren.co.nz/",
    'User-Agent': User_Agent,
}


def tangrenLogin(username, password):
    # 马蜂窝模仿 登录
    print("Start analog user login")

    postUrl = "http://tangren.co.nz/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=Lu4E4&mobile=2"
    postData = {
        "username": username,
        "password": password,
    }
    # 使用session直接post请求
    responseRes = requests.post(postUrl, data=postData, headers=header)
    # 无论是否登录成功，状态码一般都是 statusCode = 200
    print(f"statusCode = {responseRes.status_code}")
    print(f"text = {responseRes.text}")
    # tangrenSession.cookies.save()


if __name__ == "__main__":
    # 从返回结果来看，有登录成功
    tangrenLogin("tangren", "jian1980_")