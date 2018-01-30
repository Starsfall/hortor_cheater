# hortor_cheater

> 王者头脑（lajiwaigua）辅助工具

基于 [mitmproxy](https://github.com/mitmproxy/mitmproxy) 实现, 具体方式是抓包获取数据问题和选项, 通过搜索引擎查询问题, 
并在返回页面中匹配问题选项出现的次数, 一般来说出现次数最多的选型可能是正确答案的概率较大 (或者出现次数最少的选项).

添加了MySQL数据库，抓到的问题先搜索数据库，数据库里没有对应答案再通过搜索引擎查询问题，回答后再次抓包正确答案并和问题一起存入数据库
![](screenshot3.png)
windows系统下
在.py文件所在目录打开命令提示行，运行程序：
  mitmdump -p 8888  -s xxx.py
现在手机端 wifi的http代理处设置相应地址及端口(eg. 39.108.66.50:8888)
打开 `http://mitm.it` 下载并安装证书（IOS需要在关于本机处信任证书）

![](screenshot3.png)

选项在搜索结果中出现的次数, 会显示在选项最后

![](screenshot4.jpg)

或者, 输入 "e" 查看日志可以提前看到答案

![](screenshot2.png)

然后, 就可以轻松王者啦

![](screenshot1.jpg)
