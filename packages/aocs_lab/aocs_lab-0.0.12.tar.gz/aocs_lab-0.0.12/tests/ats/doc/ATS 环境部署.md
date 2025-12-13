# 自动化测试开发

## 环境安装

1. 安装docker

2. 执行下面命令

```shell
wget http://172.16.8.187:9900/OTHER/ubuntu_zc.tar
docker load<ubuntu_zc.tar
docker run --privileged -itd --name ubuntu_zc1 --net=host --restart=always -v /yinhe/docker/yinhe/:/yinhe ubuntu_zc /usr/sbin/init
```

3. `ssh root@ubuntu_ip -p 222` 用户名密码都是 root, 进入容器

先输 pm2 resurrect 恢复 ams 进程

4. 测试环境相关的配置文件在 `/yinhe/application/conf` 目录下

5. 启动遥控遥测服务：

```shell
cd /yinhe/application/ats_server
pm2 start dotnet --name XW_01-ats_server -- ATS.Server.dll conf="http://127.0.0.1:9000" sate="XW_01"
cd /yinhe/application/tmprocess
pm2 start dotnet --name XW_01-tmprocess -- TMProcessCore.dll http://127.0.0.1:9000/ XW_01


cd /yinhe/application/ats-server
sh pm2_start_with_auth.sh PIESAT02_C01-ats_server http://127.0.0.1:9000 PIESAT02_C01
cd /yinhe/application/tmprocess
pm2 start dotnet --name PIESAT02_C01-tmprocess -- TMProcessCore.dll http://127.0.0.1:9000/ PIESAT02_C01
```

1. Tmdisplay 和 ats 输入配置中心，选择卫星登陆：

配置中心 `ubuntu_ip:9000`

## 综测环境说明

application 文件夹下的目录

```
application
|-- ams
|-- ats-server
|-- conf
`-- tmprocess
```
conf 下目录

```
conf
|-- FramesStruct.json
|-- PIESAT02_C
|   |-- commands.json
|   |-- commandsGround.json
|   |-- epdusConfig.json
|   `-- tctmAlias.json
|-- allsates.json
`-- env-PIE02_1.json
```

- `FramesStruct.json`: 各型号 cadu_vcdu 包格式设置
- `allsates.json`: 卫星名称，ID，遥控遥测文件地址，环境配置文件地址，FramesStruct，amsSystem
- `env-PIE02_1.json`：influxdb 地址，内外can地址，ats后端地址，动力学ip
- `PIESAT02_C`
    - `commands.json`: 星上遥控指令配置
    - `commandsGround.json`: 地面设备遥控指令
    - `epdusConfig.json`: 遥测包配置
    - `tctmAlias.json`: 遥控遥测别名

### ats api 说明

http://172.16.61.212:10400/swagger/index.html


## 调试

### 远程登录

```shell
ssh wz -p 222
password: root
```

查看程序运行状态

```shell
pm2 l
```

### 网络调试

udp 发令测试

```
scoop install nmap # windows 安装 nmap（包含 ncat）
```

```
echo 1234567 | ncat -u 127.0.0.1 10086
```

端口监听。例: 只监听 10086 口的 udp 协议

```
tcpdump -i any udp port 10086 -X -vv
```

监听 ATS 前端发给后端的信息

```
tcpdump -i any src 172.16.8.187 and dst port 10701 -A -vv
```

查看端口占用情况

```
netstat -tulnp
```

```
ss -tulnp
```

## 组包

Virtual Channel Data Unit (VCDU).
Channel Access Data Unit (CADU).
