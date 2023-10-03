# Shadowrocket Rules

一个基础版的Shadowrocket规则。

主打懒人配置，简单高效，拒绝冗余，满足日常，外贸用户，非专业人士。


## default-DIRECT

(未命中，则直连) 主要加入国外的域名。规则地址：

|        | 缓存(优先推荐)                                                            | 非缓存                                                                  |
|--------|-------------------------------------------------------------------------|------------------------------------------------------------------------|
| 不去广告 | <img src=".github/qrcode/cdn_default-DIRECT.png?raw=true" width="150">  | <img src=".github/qrcode/gh_default-DIRECT.png?raw=true" width="150"> |
| 去广告   | <img src=".github/qrcode/cdn_advance-DIRECT.png?raw=true" width="150">  | <img src=".github/qrcode/gh_advance-DIRECT.png?raw=true" width="150"> |

- 缓存版
```
https://cdn.jsdelivr.net/gh/harmonsir/Shadowrocket-rules@main/default-DIRECT.conf
```

- 非缓存版
```
https://github.com/harmonsir/Shadowrocket-rules/raw/main/default-DIRECT.conf
```


## default-PROXY

(未命中，则代理) 主要加入中国的域名。规则地址：

|        | 缓存(优先推荐)                                                          | 非缓存                                                                |
|--------|-----------------------------------------------------------------------|----------------------------------------------------------------------|
| 不去广告 | <img src=".github/qrcode/cdn_default-PROXY.png?raw=true" width="150"> | <img src=".github/qrcode/gh_default-PROXY.png?raw=true" width="150"> |
| 去广告   | <img src=".github/qrcode/cdn_advance-PROXY.png?raw=true" width="150"> | <img src=".github/qrcode/gh_advance-PROXY.png?raw=true" width="150"> |

- 缓存版
```
https://cdn.jsdelivr.net/gh/harmonsir/Shadowrocket-rules@main/default-PROXY.conf
```

- 非缓存版
```
https://github.com/harmonsir/Shadowrocket-rules/raw/main/default-PROXY.conf
```


### GeoLite2 - Country

```
https://cdn.jsdelivr.net/gh/Loyalsoldier/geoip@release/Country.mmdb
```

### GeoLite2 - ASN

```
https://cdn.jsdelivr.net/gh/P3TERX/GeoLite.mmdb@download/GeoLite2-ASN.mmdb
```


## 专业人士

自由搭配

```
DOMAIN-SET,ruleset-ocsp.conf,DIRECT
RULE-SET,ruleset-blacklist-ips.conf,REJECT-DROP
RULE-SET,ruleset-umeng.conf,REJECT-DROP
DOMAIN-SET,ruleset-adguard-dns.conf,REJECT
DOMAIN-SET,ruleset-easylist-china.conf,REJECT
RULE-SET,ruleset-v2fly-ads.conf,REJECT
RULE-SET,ruleset-v2fly-proxy.conf,PROXY
RULE-SET,ruleset-v2fly-cn.conf,DIRECT
```


## 注意事项

windows下，的路径转义问题

```
go run ./ -exportlists "category-ads-all,cn,geolocation-\!cn"
```


## 参考资料

- adguard
- easylist-china
- v2fly/domain-list-community
- 
