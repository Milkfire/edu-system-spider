# edu-system-spider

#### 主要内容

1. **第一个**:爬取的自然是天津城建大学，但是假期之余无法连接到内网，导致爬虫处于未完成状态

   然后在闲暇之余手痒，找自己的小伙伴借到账号，开始迈上另一个爬虫的艰难旅途

2. **第二个**: 开始爬取江汉大学的教务处网站
    >**每个版本出现的问题**
    >
    >**version 0.1**: 卡在登陆报错的界面，不停报出“正在加载权限数据中...”，一时不知如何解决
    >
    >**version 0.2**:“正在加载权限数据中...”原来是正在载入的界面，说明我们已经登陆成功了，*BUT*
    那个课表的img文件无法下载、不能在新标签页里面打开，尝试浏览器自带的另存为功能**第一次**可以保存该HTML文件，
    但是**第二次**是一个跳转报错的HTML文件，我看这教务系统就是故意为难我
    >
    >等哪天找到解决办法🧐🧐🧐再接着完善......
#### 混子经验😂😂😂
1.江汉大学的教务系统界面是以asp写的，与其他的html不一样:
整个网页主要是js脚本，大部分内容动态加载，反正是恶心到我了，也知道爬取数据不是一件容易的事

2.关于登陆界面的加密机制:第一次接触到加密方面的知识，一开始我看见页面加载了MD5.js文件就以为是MD5的加密方式，一打开这个js文件🤢🤮，等会我找个部分代码展现一下
```javascript
  H = md5_ii(H, G, J, I, K[C + 6], 15, -1560198380);
    I = md5_ii(I, H, G, J, K[C + 13], 21, 1309151649);
    J = md5_ii(J, I, H, G, K[C + 4], 6, -145523070);
    G = md5_ii(G, J, I, H, K[C + 11], 10, -1120210379);
    H = md5_ii(H, G, J, I, K[C + 2], 15, 718787259);
    I = md5_ii(I, H, G, J, K[C + 9], 21, -343485551);
    J = safe_add(J, E);
    I = safe_add(I, D);
    H = safe_add(H, B);
    G = safe_add(G, A)
}
if (mode == 16) {
    return Array(I, H)
} else {
    return Array(J, I, H, G)
}
}
function md5_cmn(F, C, B, A, E, D) {
return safe_add(bit_rol(safe_add(safe_add(C, F), safe_add(A, D)), E), B)
}
function md5_ff(C, B, G, F, A, E, D) {
return md5_cmn((B & G) | ((~B) & F), C, B, A, E, D)
}
function md5_gg(C, B, G, F, A, E, D) {
return md5_cmn((B & F) | (G & (~F)), C, B, A, E, D)
}
function md5_hh(C, B, G, F, A, E, D) {
return md5_cmn(B ^ G ^ F, C, B, A, E, D)
}
function md5_ii(C, B, G, F, A, E, D) {
return md5_cmn(G ^ (B | (~F)), C, B, A, E, D)
}
function core_hmac_md5(C, F) {
var E = str2binl(C);
if (E.length > 16) {
    E = core_md5(E, C.length * chrsz)
}
```
由于总共有200行代码就不全展示，有兴趣的可以自行[百度](http://buhuibaidu.me/)，主要是教务系统不仅仅MD5加密还^TM^加'盐'，但是知道js运行方式就可以模拟出加密结果，具体方法见[江汉大学教务处.py](https://github.com/Milkfire/edu-system-spider/blob/master/江汉大学教务处.py)

3.还是佩服江汉大学教务系统的系统防御力，如果你还没有看我写的东西~~(那根本不能叫代码)~~，建议自己亲手操作一波😜😜😜，当然前提是你已经能够爬取一些静态网页以及了解HTTP的GET、POST请求

4.如果我还继续完善这些爬虫，再写一点自己的混子经验

#### 小结
反正就这样，有能力或者时间应该会更新完成

我开心就好了，顺着网线来打我啊

#### 接头暗号
如果你有什么好的想法或者独到的见解，我非常希望你能与我交流一下，开导一下我这个爬虫小白🤓🤓🤓

邮箱：2656423861@qq.com


