# appium和mitmproxy在爬虫中的使用

## appium和mitmproxy的介绍
appium 是一个自动化测试开源工具，支持 iOS 平台和 Android 平台上的原生应用，web应用和混合应用。类似Selenium。 
mitmproxy是一款抓包工具，类似charles等，不过它的一大优势就是可以通过python脚本来自动化抓包，自动获取url,response等信息，虽然可视化界面不如其他的抓包工具，但这一功能无可比拟。 

## appium的安装
appium有两种版本，一种是有界面的appium-desktop，另一种是命令行的，推荐都安装。 
前一种可以直接搜索后在github上下载，但是由于墙的原因，我虽然翻了墙，但下了很多次还是失败了，最后通过网友的百度云下载，有需要的可以搜搜看，有很多热心网友。 
命令行的安装会复杂一些，并且会有许多坑，先贴上命令：
```bash
# 安装java
brew cask install java
# 安装nodejs 
brew install nodejs
# 安装淘宝cnpm(非必须，只要你能够翻墙)
npm install -g cnpm --registry=https://registry.npm.taobao.org
# 安装appium
sudo cnpm install -g appium
sudo cnpm install -g appium-doctor
sudo cnpm install -g wd
# 安装android-sdk
brew install android-sdk
```
其中android-sdk的安装可能会出现问题，推荐安装Android Studio来配置，我之前因为有安卓的课所以事先有安装，其中的坑可以通过百度谷歌解决。 
npm需要安装node.js才能使用，然后自己配置环境路径，很简单。但我在使用的时候出现了以下的错误：
```bash
npm WARN checkPermissions Missing write access to /../node_modules/is
npm ERR! path /.../node_modules/is
npm ERR! code ELOOP
npm ERR! errno -62
npm ERR! syscall access
```
用npm -v查看版本，没有问题，但一旦使用npm install等命令就会出现这种错误，经过将近一天的查询，最后找到了一种可行的解决办法，即更改npm的默认目录，下面的命令取自官方文档，有相同错误的可以尝试一下。
```bash
# 在命令行的主目录中，为全局安装创建一个目录：
mkdir ~/.npm-global
# 配置npm以使用新的目录路径：
npm config set prefix '~/.npm-global'
# 在首选的文本编辑器中，打开或创建一个~/.profile文件并添加以下行：
export PATH=~/.npm-global/bin:$PATH
# 在命令行上，更新系统变量：
source ~/.profile
# 要测试新配置，请在不使用sudo以下情况下全局安装软件包：
npm install -g jshint
```
如果最后的测试可以正常安装的话，说明没问题了，终于解决这个错误了。 
一路安装完毕后，可以通过以下命令进行校验：
```bash
appium-doctor # 确保 各个校验项目正常
appium # 确保 0.0.0.0:4723 正常启动
adb connect 127.0.0.1:62001 # 确保adb连接成功 (夜神模拟器的端口，其他模拟器端口自行查询)
```
一切非常顺利。。。当然是不可能的。appium-desktop的安装使用没有问题，但是同出一门的appium却有很大的问题：
```
Fatal TypeError: Class constructor BaseDriver cannot be invoked without ‘new‘
```
再次百度谷歌后，找到一种解决办法。我安装的最新版的1.9.1会有这种错误，卸载后安装1.8.1就行了：
```
npm uninstall -g appium
npm install -g appium@1.8.1
```
一切终于完毕，可以连接手机进行测试了，下面是参数，需要在脚本中声明：
```
PLATFORM='Android'  #系统
deviceName='127.0.0.1:62001'  #模拟器端口号/手机型号，可通过adb devices -l查看
app_package='com.android.browser'  #包名
app_activity='.BrowserActivity'    #启动时的activity  可通过adb logcat|grep START查看包名和activity
driver_server='http://localhost:4723/wd/hub'  #appium端口，不需要更改
```

下一步就是如何进行元素定位了，appium-desktop可以获取xpath并且生成不同语言的代码，非常方便，同时可以清楚看到id等定位信息。对于appium来说，则需要用到android sdk中的uiautomatorviewer了，在android-sdk/tools目录下。然而，我又碰上了问题，简单来说错误提醒我mac无法打开java虚拟机,百度后，需要将java版本降到8.0，一通忙活后，所有环境的配置完成。 


## mitmproxy安装及环境配置
```
brew install mitmproxy
pip install mitmproxy
```
安装非常简单，环境路径添加后，下面是启动命令：
```
mitmproxy -p 8080
```
8080是端口号，可以自己设置，手机端的设置的话和charles等抓包工具一样，设置一下代理就行。完成后就能抓到http请求了，之后为了抓取https请求，需要安装证书，手机浏览器访问mitm.it就可以下载了，但是我下载失败（原因不知）。只能手动添加了。
初次运行mitmproxy或mitmdump时，会生成.mitmproxy文件夹，cd ~/.mitmproxy后可以看到有4个文件，将mitmproxy-ca-cert.cer传给手机，我用的小米手机，在wifi设置里安装，不同手机安装方法不同，自行百度。到此，大功告成。















