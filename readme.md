# project
全自动化智能化的图片下载器

目前只是支持 windows 11 64bit，后续会考虑更多 macos 等等

#  dev log
- [x] 9/17，开发出版本 v1 的图片下载器
  - [x] 目前只支持 windows 桌面版本 app
  - [x] 目前只是百度图片爬虫
  - [x] 目前只是在关掉代理的情况下可以   
  - [x] yu 反应我生成的软件是硬加载支付宝图片，支付宝图片没打包进去，回退。。。 

- [x] 9/18，开发出版本 v2 的图片下载器
  - [x] 设置 proxy 在 http 和 https 都是''，这样有代理情况我也不鸟
  - [x] 更新后的图片下载器无视代理，更加鲁棒。  
  - [x] 在 yu 这里找到打开方式，提示词：**2024 校招海报** 

- [x] 9/19，更新 feature
  - [x] 下载完图片之后，自动打开文件夹，更方便用户（salty 建议） 
  - [x] 增加项目的 【依赖管理文件】使用 venv (感谢 fizz 腾讯视频 建议)
  - [x] 重构代码文件组织，这样更清晰，**2024/09/19 是第一次开始做独立开源工具项目的起点**  
  - [x] 后续会考虑更多的图像源，跨平台支持的 

- [x] 9/20，测试 cursor 的时候发现周五中午下载器失败
  - [ ] 此时其他的 app 网络都差的很，改天再用
  - [ ] 昨晚获得思路，可以用 ai 生成图片
