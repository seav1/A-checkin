# https://github.com/mybdye 🌟

import base64
import os
import ssl
import time
import urllib
import pydub
import requests
from seleniumbase import SB


def url_open(urlLogin):
    try:
        sb.open(urlLogin)
        sb.assert_element('#email', timeout=20)
        print('- page access')
        return True
    except Exception as e:
        print('- 👀 sb.open(urlLogin)', e)
        return False


def recaptcha_checkbox():
    try:
        sb.switch_to_frame('[src*="recaptcha.net/recaptcha/api2/anchor?"]')
        print('- switch to frame checkbox')
        checkboxElement = 'span#recaptcha-anchor'
        print('- click checkboxElement')
        sb.click(checkboxElement)
        sb.sleep(4)
        return True
    except Exception as e:
        print('- 👀 def recaptcha_checkbox():', e)
        return False


def recaptcha(audioMP3, audioWAV):
    print('- recaptcha')

    #   预防弹了广告
    # sb.switch_to_window(0)
    # sb.switch_to_frame('[src*="recaptcha.net/recaptcha/api2/anchor?"]')
    status = checkbox_status()
    tryReCAPTCHA = 1
    while status != 'true':
        sb.switch_to_default_content()  # Exit all iframes
        sb.sleep(1)
        sb.switch_to_frame('[src*="recaptcha.net/recaptcha/api2/bframe?"]')
        print('- switch to frame image/audio')
        sb.click("button#recaptcha-audio-button")
        try:
            sb.assert_element('[href*="recaptcha.net/recaptcha/api2/payload/audio.mp3?"]')
            print('- normal')
            src = sb.find_elements('[href*="recaptcha.net/recaptcha/api2/payload/audio.mp3?"]'
                                   )[0].get_attribute("href")
            print('- audio src:', src)
            # download audio file
            urllib.request.urlretrieve(src, os.getcwd() + audioMP3)
            mp3_to_wav(audioMP3, audioWAV)
            text = speech_to_text(audioWAV)
            sb.switch_to_window(0)
            sb.switch_to_default_content()  # Exit all iframes
            sb.assert_element('#email', timeout=20)
            sb.sleep(1)
            sb.switch_to_frame('[src*="recaptcha.net/recaptcha/api2/bframe?"]')
            sb.type('#audio-response', text)
            sb.click('button#recaptcha-verify-button')
            sb.sleep(4)
            sb.switch_to_default_content()  # Exit all iframes
            sb.switch_to_frame('[src*="recaptcha.net/recaptcha/api2/anchor?"]')
            sb.sleep(1)
            status = checkbox_status()

        except Exception as e:
            print('- 💣 recaptcha Exception:', e)
            sb.switch_to_default_content()  # Exit all iframes
            sb.sleep(1)
            sb.switch_to_frame('[src*="recaptcha.net/recaptcha/api2/bframe?"]')
            msgBlock = '[class*="rc-doscaptcha-body-text"]'
            if sb.assert_element(msgBlock):
                print('- 💣 maybe block by google', sb.get_text(msgBlock))
                break
            elif tryReCAPTCHA > 3:
                break
            else:
                tryReCAPTCHA += 1
    if status == 'true':
        print('- reCAPTCHA solved!')
        return True


def login(username, password, loginButton):
    print('- login')
    sb.switch_to_default_content()  # Exit all iframes
    sb.sleep(1)
    sb.type('#email', username)
    sb.type('input[type="password"]', password)
    sb.click(loginButton)
    sb.sleep(6)
    assert '/user' in sb.get_current_url()
    print('- login success')
    dialogRead()
    return True


def checkbox_status():
    print('- checkbox_status')
    statuslist = sb.find_elements('#recaptcha-anchor')
    # print('- statuslist:', statuslist)
    status = statuslist[0].get_attribute('aria-checked')
    print('- status:', status)
    return status


def mp3_to_wav(audioMP3, audioWAV):
    print('- mp3_to_wav')

    pydub.AudioSegment.from_mp3(
        os.getcwd() + audioMP3).export(
        os.getcwd() + audioWAV, format="wav")
    print('- mp3_to_wav done')


def speech_to_text(audioWAV):
    print('- speech_to_text')
    sb.open_new_window()
    text = ''
    trySpeech = 1
    while trySpeech <= 3:
        print('- trySpeech *', trySpeech)
        sb.open(urlSpeech)
        sb.assert_text('Speech to text', 'h1')
        sb.choose_file('input[type="file"]', os.getcwd() + audioWAV)
        sb.sleep(5)
        response = sb.get_text('[id*="speechout"]')
        print('- response:', response)
        try:
            text = response.split('-' * 80)[1].split('\n')[1].replace('. ', '.')
        except Exception as e:
            print('- 👀 response.split:', e)
        print('- text:', text)
        if ' ' in text:
            break
        trySpeech += 1
    return text


def checkin_status(checkinStatus):
    print('- checkin_status')
    status = sb.get_text(checkinStatus)
    print('- status:', status)
    if '已' in status or '再' in status or '明' in status:
        return True, status
    else:
        return False, status
    
def dialogRead():
    print('- dialog read')
    try:
        sb.click('Read')
    except Exception as e:
        print('- 👀 dialog read:', e)


def checkin(checkinButton):
    print('- checkin')
    sb.click(checkinButton)
    print('- checkin clicked')


def traffic_info(urlUser, trafficInfo):
    print('- get traffic')
    sb.open(urlUser)
    assert '/user' in sb.get_current_url()
    dialogRead()
    sb.sleep(2)
    traffic = sb.get_text(trafficInfo)
    print('- traffic:', traffic)
    return traffic


def screenshot(imgFile):
    print('- screenshot')
    sb.save_screenshot(imgFile, folder=os.getcwd())
    print('- screenshot done')
    sb.open_new_window()
    print('- screenshot upload')
    sb.open('http://imgur.com/upload')
    sb.choose_file('input[type="file"]', os.getcwd() + '/' + imgFile)
    sb.sleep(6)
    imgUrl = sb.get_current_url()
    i = 1
    while not '/a/' in imgUrl:
        if i > 3:
            break
        print('- waiting for url... *', i)
        sb.sleep(5)
        imgUrl = sb.get_current_url()
        i += 1
    print('- 📷 img url: %s\n- screenshot upload done' % imgUrl)
 

    return imgUrl


def url_decode(s):
    return str(base64.b64decode(s + '=' * (4 - len(s) % 4))).split('\'')[1]


def push(body):
    print('- body: %s \n- waiting for push result' % body)
    # bark push
    if barkToken == '':
        print('*** No BARK_KEY ***')
    else:
        barkurl = 'https://api.day.app/' + barkToken
        title = 'A-checkin'
        rq_bark = requests.get(url=f'{barkurl}/{title}/{body}?isArchive=1')
        if rq_bark.status_code == 200:
            print('- bark push Done!')
        else:
            print('*** bark push fail! ***', rq_bark.content.decode('utf-8'))
    # tg push
    if tgBotToken == '' or tgUserID == '':
        print('*** No TG_BOT_TOKEN or TG_USER_ID ***')
    else:
        body = 'A-checkin' + '\n\n' + body
        server = 'https://api.telegram.org'
        tgurl = server + '/bot' + tgBotToken + '/sendMessage'
        rq_tg = requests.post(tgurl, data={'chat_id': tgUserID, 'text': body}, headers={
            'Content-Type': 'application/x-www-form-urlencoded'})
        if rq_tg.status_code == 200:
            print('- tg push Done!')
        else:
            print('*** tg push fail! ***', rq_tg.content.decode('utf-8'))
    print('- finish!')


##
try:
    urlUserPasswd = os.environ['URL_USER_PASSWD']
except:
    # 本地调试用， without any 'https://' or '/'
    urlUserPasswd = ''
try:
    barkToken = os.environ['BARK_TOKEN']
except:
    # 本地调试用
    barkToken = ''
try:
    tgBotToken = os.environ['TG_BOT_TOKEN']
except:
    # 本地调试用
    tgBotToken = ''
try:
    tgUserID = os.environ['TG_USER_ID']
except:
    # 本地调试用
    tgUserID = ''
##
body = []
# Speech2text
urlSpeech = url_decode(
    'aHR0cHM6Ly9henVyZS5taWNyb3NvZnQuY29tL2VuLXVzL3Byb2R1Y3RzL2NvZ25pdGl2ZS1zZXJ2aWNlcy9zcGVlY2gtdG8tdGV4dC8jZmVhdHVyZXM==')
# 关闭证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# ikuxx, qsy, xly
loginButtonList = ('button[type="submit"]', 'button[type="button"]')
checkinStatusList = ('[id*="checkin"]', '[class*="card-action"]',
                     '[class="btn btn-transparent-white font-weight-bold py-3 px-6 mr-2 disabled"]')
checkinButtonList = ('#checkin', 'a[onclick*="checkin()"]')
trafficInfoList = (
    'div.col-lg-3:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)', '#remain',
    '.bg-diagonal-light-success > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
with SB(uc=True, pls="none", sjw=True) as sb:  # By default, browser="chrome" if not set
    if urlUserPasswd != '':
        account = urlUserPasswd.split(',')
        accountNumber = int(len(account) / 3)
        print('- Number of accounts：', accountNumber)
        for i in range(accountNumber):
            print('- Start account %s' % (i + 1))
            urlBase = account[i * 3]
            username = account[i * 3 + 1]
            password = account[i * 3 + 2]
            urlLogin = 'https://' + urlBase + '/auth/login'
            urlUser = 'https://' + urlBase + '/user'
            audioMP3 = '/' + urlBase + '.mp3'
            audioWAV = '/' + urlBase + '.wav'
            imgFile = urlBase + '.png'
            time.sleep(1)
            if 'ikuuu' in urlBase:
                loginButton = loginButtonList[0]
                checkinStatus = checkinStatusList[0]
                checkinButton = checkinButtonList[1]
                trafficInfo = trafficInfoList[0]
            elif 'qiushiyun' in urlBase:
                loginButton = loginButtonList[0]
                checkinStatus = checkinStatusList[1]
                checkinButton = checkinButtonList[1]
                trafficInfo = trafficInfoList[1]
            elif 'xiaolongyun' in urlBase:
                loginButton = loginButtonList[1]
                checkinStatus = checkinStatusList[0]
                checkinButton = checkinButtonList[0]
                trafficInfo = trafficInfoList[2]
            try:
                if url_open(urlLogin):
                    if recaptcha_checkbox():
                        recaptcha(audioMP3, audioWAV)
                    if login(username, password, loginButton):
                        status = checkin_status(checkinStatus)
                        if not status[0]:
                            checkin(checkinButton)
                        sb.sleep(2)
                        traffic = traffic_info(urlUser, trafficInfo)
                        sb.sleep(4)
                        body.append('账号(%s/%s):[%s|%s***]\n签到状态：%s\n剩余流量：%s' % (
                            i + 1, accountNumber, urlBase.split('.')[-2], username[:3], status[1], traffic))
                        # print('- body:', body)
            except Exception as e:
                print('- 💥', e)
                try:
                    imgUrl = screenshot(imgFile)
                    body.append('账号(%s/%s):[%s|%s***]\n%s\n%s' % (i + 1, accountNumber, urlBase.split('.')[-2], username[:3], e, imgUrl))
                except:
                    # push(e)
                    body.append('账号(%s/%s):[%s|%s***]\n%s' % (i + 1, accountNumber, urlBase.split('.')[-2], username[:3], e))
        pushbody = ''
        for i in range(len(body)):
            if i + 1 != len(body):
                pushbody += body[i] +'\n---\n'
            else:
                pushbody += body[i]
        push(pushbody)
    else:
        print('*** Please Check URL_USER_PASSWD ***')

# END
