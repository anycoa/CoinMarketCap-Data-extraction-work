from selenium import webdriver
from time import sleep
import re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"

try:
    import xie_xlsx
except:
    from  我的工具 import xie_xlsx



with open('爬取列表.csv', 'r', encoding='gbk') as f:
    pa01 = f.read()

tihuan01 = re.findall('(".*?")',pa01, flags=re.DOTALL)
for i01 in range(0, len(tihuan01)):
    tihuan02 = tihuan01[i01]
    pa01=pa01.replace(tihuan02,tihuan02.replace('\n','').replace('\r','').replace('\t',''))

pa01=pa01.split('\n')
print(len(pa01))

zhuan01 = pa01[0].split(',')[-7:]
print(zhuan01)

r01 = {}
for y01 in range(1, len(pa01)):
    pa001 = pa01[y01].split(',')
    pa02 = [x if x else '' for x in pa001[:7]]
    # print(y01, pa02)
    if len(pa02) > 2 and (pa02[0] or pa02[1]):
        cha01 = r01.get(pa02[0], [])
        r02 = pa02
        if cha01:
            r02 = ['-'.join(set([cha01[x], pa02[x]])).strip('-') for x in range(0, len(pa02))]

        r01[pa02[0]] = r02

pa_zong = []
for k, v in r01.items():
    pa_zong.append(v)

print(pa_zong)
print(len(pa_zong))


yue01=xie_xlsx.xie_xlsx('结果01.xlsx')
yue01.chuangbiao(pa01[0].split(','))


driver = webdriver.Chrome()
driver.set_window_size(1000, 800)


for y01 in range(0, len(pa_zong)):
    pa02 = pa_zong[y01]

    print('*' * 120)
    print(f'第{y01}/{len(pa_zong)}个。。。。。')
    print(pa02)

    gjc01 = 'Ribbon'
    if pa02[1]:
        gjc01 = pa02[1]
    else:
        gjc01 = pa02[0]

    a01=-1
    while 1:
        try:
            a01=a01+1

            url01 = 'https://coinmarketcap.com'
            driver.get(url01)
            sleep(3+a01)

            v01 = driver.find_elements_by_css_selector('div[class="sc-1xvlii-0 dQjfsE"]>svg')
            print('搜索个数：', len(v01))
            v01[0].click()
            sleep(1.6+a01)

            v02 = driver.find_elements_by_css_selector('input[placeholder="What are you looking for?"]')
            v02[0].send_keys(gjc01)
            sleep(1.2)

            v03 = driver.find_elements_by_css_selector('div[class="sc-5kpu8c-4 JYOCB"]>a[class="cmc-link"]')

            if v03:
                v03[0].click()
                sleep(1.2+a01)
            else:
                print('无数据结果*****')
                yue01.xiubiao02(pa02)
                break

            for i01 in range(12, 16):
                # print(i01, 300 * i01)
                # 拖动页面向下移动， 1000代表移动的距离 注意 要等待页面加载完成
                js = "var q=document.documentElement.scrollTop={}".format(300 * i01)
                driver.execute_script(js)
                sleep(0.3)

            # driver.find_elements_by_css_selector('h2[class="sc-1q9q90x-0 jCInrl"]')[0].click()
            # sleep(1.2)

            n01 = driver.find_elements_by_css_selector('small[class="nameSymbol"]')
            n001 = [x.text for x in n01]

            n01 = driver.find_elements_by_css_selector('div[class="namePill namePillPrimary"]')
            n002 = [x.text for x in n01]

            n03 = driver.find_elements_by_css_selector('div[class="statsItemRight"]>div[class="statsValue"]')

            if len(n03)>=4:
                n003 = [n03[0].text, n03[2].text]
            else:
                n003=['-','-']

            n01 = driver.find_elements_by_css_selector('p[font-weight="semibold"]')
            n004 = [x.text for x in n01]

            print(1, n001)
            print(2, n002)
            print(3, n003)
            print(4, n004)

            zhuan02=[]
            for i01 in zhuan01:
                biao01=0
                for i02 in n004:
                    if re.findall(i02,i01,flags=re.I):
                        biao01=1
                        break

                    if i01=='MEXC':
                        if re.findall(i02,'MXC', flags=re.I):
                            biao01 = 1
                            break

                if biao01==1:
                    zhuan02.append('√')
                else:
                    zhuan02.append('x')

            pa02[1]=n001[0]
            nr01=pa02+[n002[0].replace('Rank #','')]+n003+zhuan02

            print('内容：',nr01)
            yue01.xiubiao02(nr01)

            sleep(1.5)
            break
        except:
            s = sys.exc_info()
            print("错误第{}行,详情：【'{}' 】".format(s[2].tb_lineno, s[1]).replace('\n', ''))
            sleep(1)



print('程序运行完成**********')
while 1:
    input('>>>')

