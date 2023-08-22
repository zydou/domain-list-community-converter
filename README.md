# 简介

本项目用于将 v2ray 官方社区维护的各域名列表[@v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)转换成以下规则集 (RULE-SET), 使用 GitHub Actions 每日自动构建，保证规则最新。

- [Clash](https://github.com/Dreamacro/clash): RULE-SET ([behavior: domain](https://lancellc.gitbook.io/clash/clash-config-file/rule-provider#behavior))
- [Surge](https://manual.nssurge.com/rule/domain-based.html): DOMAIN-SET
- [Surge](https://manual.nssurge.com/rule/ruleset.html): RULE-SET
- [Shadowrocket](https://apps.apple.com/us/app/shadowrocket/id932747118): DOMAIN-SET
- [Shadowrocket](https://apps.apple.com/us/app/shadowrocket/id932747118): RULE-SET

此外，对于具有属性的域名（如@cn, @ads），还会额外生成对应的域名列表，以便于用户自行使用。例如对于`apple`服务，在生成`apple.yml`的同时，还会额外生成`apple@ads.yml`和`apple@cn.yml`。

## 使用说明

### **Clash**

只适用于 Clash **Premium** 版本。Clash Premium 相对于普通版，增加了 **TUN 增强模式**，能接管设备所有 TCP 和 UDP 流量，类似 [Surge for Mac](https://nssurge.com) 的增强模式。更多高级特性请看[官方 wiki](https://github.com/Dreamacro/clash/wiki/premium-core-features)。

#### **Clash Premium 各版本下载地址**

- Clash Premium **命令行**版（适用于 Windows、macOS、Linux、OpenWRT 等多种平台）：[https://github.com/Dreamacro/clash/releases/tag/premium](https://github.com/Dreamacro/clash/releases/tag/premium)
- Clash Premium **图形用户界面**版：
  - [ClashX Pro](https://install.appcenter.ms/users/clashx/apps/clashx-pro/distribution_groups/public)（适用于 macOS）
  - [Clash for Windows](https://github.com/Fndroid/clash_for_windows_pkg/releases)（适用于 Windows、macOS）
  - [Clash for Android](https://github.com/Kr328/ClashForAndroid/releases)（适用于 Android）

#### **使用方式**

在 Clash 配置文件中添加 `rule-providers` 和 `rules`字段：

```yml
rule-providers:
  ads:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/zydou/domain-list-community-converter/clash/category-ads-all.yml"
    path: ./ruleset/category-ads-all.yml
    interval: 86400
  google:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/zydou/domain-list-community-converter/clash/google.yml"
    path: ./ruleset/google.yml
    interval: 86400
  microsoft:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/zydou/domain-list-community-converter/clash/microsoft.yml"
    path: ./ruleset/microsoft.yml
    interval: 86400
  cn:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/zydou/domain-list-community-converter/clash/cn.yml"
    path: ./ruleset/cn.yml
    interval: 86400
rules:
  - RULE-SET,ads,REJECT
  - RULE-SET,google,PROXY
  - RULE-SET,microsoft,DIRECT
  - RULE-SET,cn,DIRECT
```

- 以上配置中，除了 `DIRECT` 和 `REJECT` 是默认存在于 Clash 中的 policy（路由策略/流量处理策略），其余均为自定义 policy，对应配置文件中 proxies 或 proxy-groups 中的 name。如你直接使用上面的 rules 规则，则需要在 proxies 或 proxy-groups 中手动配置一个 name 为 PROXY 的 policy。
- 如你希望添加更多域名列表，可以[点击此处](https://github.com/zydou/domain-list-community-converter/blob/clash/README.md)查询所有列表并添加到`rule-providers`字段中，然后在`rules`字段中添加规则，格式为 `RULE-SET,name,policy`，其中 `name` 和 `policy` 可以自定义。

更多关于 Clash Premium 使用方式，请查看[官方文档](https://github.com/Dreamacro/clash/wiki/premium-core-features) 或 [Lancellc's GitBook](https://lancellc.gitbook.io/clash/)。

### **Surge** 和 **Shadowrocket**

Shadowrocket 兼容 Surge 配置文件格式，以下只介绍 Surge 的使用方法，Shadowrocket 可以使用和 Surge 相同的配置。

#### ⚠️ 注意：

- **DOMAIN-SET** 同时适用于 Surge for Mac **v3.5.1** 及更新的版本、Surge for iOS **v4.2.2** 及更新的版本，拥有比 RULE-SET 更优秀的匹配效率。
- **RULE-SET** 同时适用于 Surge for Mac **v3.0** 及更新的版本、Surge for iOS **v3.4** 及更新的版本。
- **DOMAIN-SET**相比于**RULE-SET**的缺点是不支持 eTLD 后缀（如 `.github.io` 无法匹配 `example.github.io` ). 详见[官方文档](https://manual.nssurge.com/rule/domain-based.html)

#### **使用方式**

在 Surge 配置文件中添加如下规则：

**DOMAIN-SET：**

```ini
[Rule]
DOMAIN-SET,https://raw.githubusercontent.com/zydou/domain-list-community-converter/surge-domain-set/category-ads-all.txt,REJECT
DOMAIN-SET,https://raw.githubusercontent.com/zydou/domain-list-community-converter/surge-domain-set/google.txt,PROXY
DOMAIN-SET,https://raw.githubusercontent.com/zydou/domain-list-community-converter/surge-domain-set/microsoft.txt,DIRECT
DOMAIN-SET,https://raw.githubusercontent.com/zydou/domain-list-community-converter/surge-domain-set/cn.txt,DIRECT
```

**RULE-SET：**

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/zydou/domain-list-community-converter/surge-rule-set/category-ads-all.txt,REJECT
RULE-SET,https://raw.githubusercontent.com/zydou/domain-list-community-converter/surge-rule-set/google.txt,PROXY
RULE-SET,https://raw.githubusercontent.com/zydou/domain-list-community-converter/surge-rule-set/microsoft.txt,DIRECT
RULE-SET,https://raw.githubusercontent.com/zydou/domain-list-community-converter/surge-rule-set/cn.txt,DIRECT
```

- 以上配置中，除了 `DIRECT` 和 `REJECT` 是默认存在于 Surge 中的 policy（路由策略/流量处理策略），其余均为自定义 policy，对应配置文件中 `[Proxy]` 或 `[Proxy Group]` 中的代理名称。如你直接使用上面的 `[Rule]` 规则，则需要在 `[Proxy]` 或 `[Proxy Group]` 中手动配置一个名为 `PROXY` 的 policy。
- 如你希望添加更多**DOMAIN-SET**域名列表，可以[点击此处](https://github.com/zydou/domain-list-community-converter/blob/surge-domain-set/README.md)查询所有列表，并在`[Rule]`字段中添加规则，格式为 `DOMAIN-SET,https://raw.githubusercontent.com/zydou/domain-list-community-converter/surge-domain-set/name.txt,policy`，其中 `name` 和 `policy` 可以自定义。
- 如你希望添加更多**RULE-SET**域名列表，可以[点击此处](https://github.com/zydou/domain-list-community-converter/blob/surge-rule-set/README.md)查询所有列表，并在`[Rule]`字段中添加规则，格式为 `RULE-SET,https://raw.githubusercontent.com/zydou/domain-list-community-converter/surge-rule-set/name.txt,policy`，其中 `name` 和 `policy` 可以自定义。

更多关于 Surge 使用方式，请查看[官方文档](https://manual.nssurge.com/)。

## 致谢

- [@v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)，数据来源
- [@Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)，README 参考
- [@Loyalsoldier/surge-rules](https://github.com/Loyalsoldier/surge-rules)，README 参考
