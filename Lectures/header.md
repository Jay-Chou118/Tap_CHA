# HTTP header 常用属性
(1) Host：

请求报头域主要用于指定被请求资源的Internet主机和端口号，它通常从HTTP URL中提取出来的，例如我们在浏览器中输入：https://www.baidu.com，浏览器发送的请求消息中，就会包含Host请求报头域，如下：

Host：www.baidu.com(此处使用缺省端口号443，若指定了端口号，则变成：Host：指定端口号

(2)Referer

当浏览器向web服务器发送请求的时候，一般会带上Referer，告诉服务器该请求是从哪个页面链接过来的，服务器借此可以获得一些信息用于处理。比如从我主页上链接到一个朋友那里，他的服务器就能够从HTTP Referer中统计出每天有多少用户点击我主页上的链接访问他的网站。

### (3)User-Agent

这个对于爬虫比较重要 因为一班都需要添加该属性，否则稍微处理过的网站，都无法爬取。
告诉HTTP服务器， 客户端使用的操作系统和浏览器的名称和版本。
我们上网登陆论坛的时候，往往会看到一些欢迎信息，其中列出了你的操作系统的名称和版本，这往往让很多人感到很神奇，实际上，服务器应用程序就是从User-Agent这个请求报头域中获取到这些信息。User-Agent请求报头域允许客户端将它的操作系统、浏览器和其它属性告诉服务器。
例如： User-Agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; CIBA; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; InfoPath.2; .NET4.0E)

应用程序版本“Mozilla/4.0”表bai示：你使用Maxthon 2.0 浏览du器使用 IE8 内核；
版本标识“zhiMSIE 8.0”
平台自身的dao识别信息“Windows NT 5.1”表示“操作系统为zhuan Windows XP”

4）Content-type

表示后面的文档属于什么MIME类型。Servlet默认为text/plain，但通常需要显式地指定为text/html。由于经常要设置Content-Type，因此HttpServletResponse提供了一个专用的方法setContentType。

（5）Accept-Language

Accept-Langeuage：指出浏览器可以接受的语言种类，如en或en-us指英语，zh或者zh-cn指中文，当服务器能够提供一种以上的语言版本时要用到。

（6）Cookie

Cookie：浏览器用这个属性向服务器发送Cookie。Cookie是在浏览器中寄存的小型数据体，它可以记载和服务器相关的用户信息，也可以用来实现会话功能。


