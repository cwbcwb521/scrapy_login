# -*- coding: utf-8 -*-
import scrapy
import urllib.request
from scrapy.http import Request,FormRequest
import ssl

context = ssl._create_unverified_context()
class LoginspdSpider(scrapy.Spider):
    name = "loginspd"
    allowed_domains = ["douban.com"]
    header = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    def start_requests(self):
        return [Request("https://accounts.douban.com/login",callback=self.parse,headers=self.header,meta={"cookiejar":1})]

    def parse(self, response):
        # 获取验证码图片地址，获取后赋给captcha变量，此时captcha为一个列表
        captcha = response.xpath('//img[@id="captcha_image"]/@src').extract()
        # 判断是否需要输入验证码
        if len(captcha) > 0:
            print('此时有验证码')
            print(captcha)
            # 设置将验证码存储到本地的地址
            localPath = "/Users/slothgreed/scrapy_study/scrapy_workplace/loginpjt/captchaImage/captcha.png"
            # 将验证码存储到本地供我们查看
            u = urllib.request.urlopen(captcha[0],context=context)
            data = u.read()
            f = open(localPath,'wb')
            f.write(data)
            f.close()

            print("请查看本地图片captcha.png并输入验证码：")

            captcha_value = input()
            # 设置最终要传递的post信息
            data = {
                "form_email":"cwbcwb521@hotmail.com",
                "form_password":"521521cwb",
                "captcha-solution":captcha_value,
                "redir":"https://www.douban.com/people/176254604/",
            }
        else:
            print('此时没有验证码')
            # 设置要传递的post信息
            data = {
                "form_email":"cwbcwb521@hotmail.com",
                "form_password":"521521cwb",
                "redir":"https://www.douban.com/people/176254604/",
            }
        print("登录中...")
        return [FormRequest.from_response(response,formdata=data,meta={"cookiejar":response.meta["cookiejar"]}, headers=self.header, callback=self.next,)]
    def next(self, response):
        print("此时已经登录并完成了爬取个人中心的数据")
        title = response.xpath('//title/text()').extract()
        print(title)











