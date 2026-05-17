# 青择校开发环境记录

更新时间：2026-05-17

## 本地项目

- 项目文件夹：`/Users/daxiang/Desktop/青择校`
- 小程序名称：`青择校`
- 小程序 AppID：`wx32d955e2fe9c7e6e`
- Git 仓库：已初始化，本地分支 `main`
- 包管理器：pnpm

## 已确认工具

| 工具 | 状态 | 说明 |
| --- | --- | --- |
| Cursor | 已安装 | 用户已登录免费版账号 |
| 微信开发者工具 | 已安装并登录 | CLI 路径：`/Applications/wechatwebdevtools.app/Contents/MacOS/cli` |
| 微信开发者工具服务端口 | 已开启 | 端口：`28240` |
| Node.js | 已安装 | v24.15.0 |
| npm | 已安装 | v11.12.1 |
| pnpm | 已安装 | v11.1.2 |
| Git | 已安装 | Apple Git 2.50.1 |
| Taro CLI | 已安装为项目本地依赖 | v4.2.0，运行方式：`pnpm taro` |
| Figma 插件 | 已连接 | 用于后续设计稿和组件协作 |
| GitHub CLI | 已安装并登录 | v2.73.0，账号：`844177590-afk`，Git 协议：HTTPS |
| GitHub 权限 | 已授权 | scopes：`repo`、`read:org`、`gist` |
| Git 提交身份 | 已配置 | 当前仓库用户名：`844177590-afk`，邮箱：GitHub noreply |
| Shadowrocket | 已配置 | 当前节点：`ISP/US`；全局路由：`配置`；国内规则直连，海外走代理 |

## 网络配置记录

- Shadowrocket 全局路由：`Config/配置`
- 当前代理节点：`ISP/US`
- Wi-Fi DNS：`223.5.5.5`、`119.29.29.29`
- Shadowrocket 默认配置已包含中国大陆直连规则：`GEOIP,CN,DIRECT`
- 默认路由由 Shadowrocket 虚拟网卡接管，按规则分流。
- 重启电脑和 Shadowrocket 后已复查：配置模式仍生效。

## 待用户提供或确认

- Figma 设计文件位置，或允许我新建设计文件
- 小程序隐私协议和手机号授权合规文案

## 下一步

1. 创建 GitHub 远程仓库并推送首版工程。
2. 建立 Figma 设计文件或把现有设计文件接入项目。
3. 开始正式开发首页、列表页、详情页组件系统。
4. 准备小程序隐私协议和手机号授权合规文案。

## 当前验证结果

- `pnpm build:weapp` 已通过。
- `dist/` 微信小程序产物已生成。
- 微信开发者工具已打开项目：`/Users/daxiang/Desktop/青择校`。
- 模拟器已加载启动页：`pages/splash/index`。
- 微信相关域名验证通过：`mp.weixin.qq.com`、`servicewechat.com`、`api.weixin.qq.com`、`weixin.qq.com`。
- 海外开发域名验证通过：`github.com`、`api.openai.com`。
- 国内依赖镜像验证通过：`registry.npmmirror.com`。
- 当前海外出口 IP：`72.1.131.166`。
