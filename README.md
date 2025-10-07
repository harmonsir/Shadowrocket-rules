# Shadowrocket Rules

一个基础版的Shadowrocket规则。

主打懒人配置，简单高效，拒绝冗余，满足日常，外贸用户，非技术背景人士。


## 🛡️ 企业安全与 DLP 定制服务

本项目隶属于网络安全与数据防护方向的应用研究范畴。  
我为企业及开发者提供以下 **定制化安全解决方案**：

- 🌐 **DNS / 域名智能分析**：基于大数据的威胁识别与行为建模  
- 🧠 **数据防泄漏（DLP）策略引擎**：支持敏感信息检测与规则定制  
- 📊 **安全可视化与合规报表**：帮助企业满足合规与内部审计需求  
- 🔗 **API 与私有化部署支持**：便于集成至现有安全体系

如需了解企业安全或 DLP 定制开发合作，请邮件联系。

> 合规、安全、隐私保护为核心，拒绝一切非法用途。


#### 🧼 自动提交清理机制说明（必读 **[🚨 开发者须知](#-开发者须知)**）

本项目启用了自动化提交清理机制：

- 每 14 天自动运行一次 Git 清理脚本
- 会 **重写主分支历史（`main`）**
- 自动删除 **3 个月前的 `ci: auto-build` 自动提交**

---

## 配置文件介绍

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
RULE-SET,ruleset-asn-cn.conf,DIRECT
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
- https://bgp.he.net/country/CN
- 

---

### 🚨 开发者须知

请务必注意以下几点，以免产生冲突或数据丢失：

#### ✅ 如果你是协作者：

- **不要长时间在本地保留未同步的 `main` 分支**
- 每次开发前，**先同步远程主分支**：

  ```bash
  git fetch origin
  git checkout main
  git reset --hard origin/main
  ```

* 如果你基于旧的 `main` 分支开发，请使用 **`rebase` 而非 `merge`** 来更新：

  ```bash
  git fetch origin
  git rebase origin/main
  ```


### ⚠️ 如果你遇到这些问题：

* Push 报错：`non-fast-forward`
* Pull 显示大量冲突
* 本地提交“消失”

请使用以下方法恢复你的工作：

```bash
# 保存当前工作为备份分支
git checkout -b backup-before-rebase

# 强制重置 main 分支为远程最新
git fetch origin
git checkout main
git reset --hard origin/main

# 如果需要，把旧提交 cherry-pick 回来
git checkout backup-before-rebase
git log  # 找到你需要的提交
git checkout main
git cherry-pick <commit-hash>
```


### ✅ 推荐协作方式

1. 永远不要直接在 `main` 上开发，请使用功能分支：

   ```bash
   git checkout -b feature/my-task
   ```

2. 使用 Pull Request 合并到 `main`

3. 避免在 `main` 上手动提交或强推


### 🤔 为什么要清理历史？

* 自动提交频繁，长期堆积会污染 Git 历史
* 保留重要手动提交的可读性
* 减少仓库体积，加快 clone 和 CI 执行速度


> 经验提醒：用 git filter-repo 的 commit-callback 时 **不要** 用 commit.skip() 来删除历史提交——它可能会连带跳过后续提交。更安全的做法是把目标提交的改动清空（commit.file_changes = []），让空提交被工具自动剔除。我花了 ~2 小时定位并修复了这个坑。

---

📌 如果你对这个机制有疑问，欢迎通过 Issue 反馈。
