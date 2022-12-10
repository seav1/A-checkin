# https://github.com/mybdye 🌟


import os, requests, urllib, pydub, base64, ssl
from seleniumbase import SB


def recaptcha():
    global body
    print('- recaptcha')
    try:
        sb.open(urlLogin)
        sb.assert_element('#email', timeout=20)
        print('- access')
    except Exception as e:
        print('👀 ', e, '\n try again!')
        sb.open(urlLogin)
        sb.assert_element('#email', timeout=20)
        print('- access')
    #   reCAPTCHA
    sb.switch_to_frame('[src*="recaptcha.net/recaptcha/api2/anchor?"]')
    print('- switch to frame checkbox')
    checkbox = 'span#recaptcha-anchor'
    print('- click checkbox')
    sb.click(checkbox)
    sb.sleep(4)
    #   预防弹了广告
    #sb.switch_to_window(0)
    #sb.switch_to_frame('[src*="recaptcha.net/recaptcha/api2/anchor?"]')
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
            mp3_to_wav()
            text = speech_to_text()
            sb.switch_to_window(0)
            sb.assert_element('#email', timeout=20)
            sb.switch_to_default_content()  # Exit all iframes
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
            print('- 💣 Exception:', e)
            body = e
            sb.switch_to_default_content()  # Exit all iframes
            sb.sleep(1)
            sb.switch_to_frame('[src*="recaptcha.net/recaptcha/api2/bframe?"]')
            msgBlock = '[class*="rc-doscaptcha-body-text"]'
            if sb.assert_element(msgBlock):
                body = sb.get_text(msgBlock)
                print('- 💣 maybe block by google', body)
                break
            elif tryReCAPTCHA > 3:
                break
            else:
                tryReCAPTCHA += 1
    if status == 'true':
        print('- reCAPTCHA solved!')
        return True


def login():
    print('- login')
    sb.switch_to_default_content()  # Exit all iframes
    sb.sleep(1)
    sb.type('#email', username)
    sb.type('input[type="password"]', password)
    sb.click('button[type="submit"]')
    sb.sleep(6)
    #sb.assert_exact_text('用户中心', '[class*="badge badge-success"]')
    #sb.assert_text('用户中心', 'h1', timeout=20)
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


def mp3_to_wav():
    print('- mp3_to_wav')
    pydub.AudioSegment.from_mp3(
        os.getcwd() + audioMP3).export(
        os.getcwd() + audioWAV, format="wav")
    print('- mp3_to_wav done')


def speech_to_text():
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
        text = response.split('-' * 80)[1].split('\n')[1].replace('. ', '.')
        print('- text:', text)
        if ' ' in text:
            break
        trySpeech += 1
    return text

def checkinstatus():
    global body
    print('- checkinstatus')
    try:
        status = sb.get_text('[class*="card-action"]')
    except Exception as e:
        print('- 👀 checkin status:', e)
        status = sb.get_text('#checkin-div')
    print('- status:', status)
    if '已' in status or '再' in status or '明' in status:
        body = status
        return True
    else:
        body = '执行签到'
        return False
    
def dialogRead():
    print('- dialog read')
    try:
        sb.click('Read')
    except Exception as e:
        print('- 👀 dialog read:', e)
        
def checkin():
    global body
    print('- checkin')
    try:
        sb.click('#checkin')
    except Exception as e:
        print('- 👀 checkin button:', e)
        sb.click('a[onclick="checkin()"]')
    print('- checkin clicked')
        
def trafficInfo():
    print('- get traffic')
    sb.open(urlUser)
    assert '/user' in sb.get_current_url()
    dialogRead()
    sb.sleep(2)
    try:
        #traffic = sb.get_text('div.col-lg-3:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)', by='css selector')
        traffic = sb.get_text('div.col-lg-3:nth-child(2) > div:nth-child(1) > div:nth-child(2)', by='css selector')
    except Exception as e:
        print('- 👀 trafficInfo:', e)
        traffic = sb.get_text('#remain')
    print('- trafficInfo:', traffic)
    return traffic


def screenshot():
    global body
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
        sb.sleep(2)
        imgUrl = sb.get_current_url()
        i += 1
    print('- 📷 img url:', imgUrl)
    body = imgUrl
    print('- screenshot upload done')

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
        title = urlBase
        rq_bark = requests.get(url=f'{barkurl}/{title}/{body}?isArchive=1')
        if rq_bark.status_code == 200:
            print('- bark push Done!')
        else:
            print('*** bark push fail! ***', rq_bark.content.decode('utf-8'))
    # tg push
    if tgBotToken == '' or tgUserID == '':
        print('*** No TG_BOT_TOKEN or TG_USER_ID ***')
    else:
        body = urlBase + '\n\n' + body
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
    urlBase = os.environ['URL_BASE']
except:
    # 本地调试用， please type here the website address without any 'https://' or '/'
    urlBase = ''
try:
    username = os.environ['USERNAME']
except:
    # 本地调试用
    username = ''
try:
    password = os.environ['PASSWORD']
except:
    # 本地调试用
    password = ''
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
body = ''
statuRenew = False
audioMP3 = '/' + urlBase + '.mp3'
audioWAV = '/' + urlBase + '.wav'
imgFile = urlBase + '.png'
##
urlLogin = 'https://' + urlBase + '/auth/login'
urlUser = 'https://' + urlBase + '/user'
urlSpeech = url_decode(
    'aHR0cHM6Ly9henVyZS5taWNyb3NvZnQuY29tL2VuLXVzL3Byb2R1Y3RzL2NvZ25pdGl2ZS1zZXJ2aWNlcy9zcGVlY2gtdG8tdGV4dC8jZmVhdHVyZXM==')
# 关闭证书验证
ssl._create_default_https_context = ssl._create_unverified_context

with SB(uc=True) as sb:  # By default, browser="chrome" if not set.
    print('- 🚀 loading...')
    if urlBase != '' and username != '' and password != '':
        try:
            if recaptcha():
                if login():
                    if not checkinstatus():
                        checkin()
                    sb.sleep(2)
                    body = body + '，' + trafficInfo()
        except Exception as e:
            print('💥', e)
            try:
                screenshot()
            finally:
                push(e)
        push(body)
    else:
        print('- please check urlBase/username/password')

# END
