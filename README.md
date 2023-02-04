[![Checkin](https://github.com/mybdye/A-checkin/actions/workflows/main.yml/badge.svg)](https://github.com/mybdye/A-checkin/actions/workflows/main.yml)
#### ⏱️ TODO
  - None

#### ✏️ NOTE
2023
- 02.04 fix [speech to text]
2022
- 12.21
    - fix 'qsy' checkin button
    - update screenshot func, file path
    - get latest checkin_status after checkin
- 12.20 Multi-account test, add 'xly'
- 12.08 compatible with 'ikuxx' and 'qsy'
- 11.06 rebuild
    - [x] ~~helium/selenium/Playwright~~ >> SeleniumBase
    - [x] ~~MacOS/Windows~~ >> Ubuntu

    * 每次运行时间约 1~3 分钟

#### 🌟️ SUGGESTION
```diff
!自定义schedule
.github/workflows/main.yml

例如：
schedule:
    # UTC (国内 UTC+8)
    - cron: '03 02 */2 * *'   
    # 每2天 10:03am 执行
    
!规则参考
  * * * * *
  | | | | |
  | | | | +----- day of week (0 - 7) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
  | | | +------- month (1 - 12) OR jan,feb,mar,apr ...
  | | +--------- day of month (1 - 31)
  | +----------- hour (0 - 23)
  +------------- minute (0 - 59)
```

#### ㊙️ SECRET

|YOU SECRET NAME|YOU SECRET VALUE|
|-----|--|
|`URL_USER_PASSWD`|逗号`,`分隔<br>单账号`abc.com,username,password`<br>多账号`a1.com,username1,password1,b2.com,username2,password2`<br>不要带有`https://` 和 `/` |
|`BARK_TOKEN`|(可选) api.day.app/`BARK_TOKEN`/ 详见 https://github.com/Finb/Bark|
|`TG_BOT_TOKEN`|(可选) `xxxxxx:xxxxxxxxxxxxx`|
|`TG_USER_ID`|(可选) 给 bot `@userinfobot` 发送 `/start`|

#### 📚 THANKS
- [SeleniumBase](https://github.com/seleniumbase)
- [Python](https://www.python.org/)
- [PyCharm CE](https://www.jetbrains.com/pycharm/)
- [Whisper](https://github.com/openai/whisper)
