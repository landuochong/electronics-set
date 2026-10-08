> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# ESP32-C5-DevKitC-1

## 定位

ESP32-C5-WROOM-1(U) 模组开发板，适合验证需要 2.4/5 GHz 双频 Wi-Fi 6、Bluetooth LE、Zigbee 或 Thread 的联网设备。

## 关键能力

- 双频 Wi-Fi 6 是 C5 相对 C3/C6/S3 的重要选型点。
- 同时具备 BLE 与 IEEE 802.15.4，Zigbee/Thread/Matter 仍需选择协议栈、设备角色和认证目标。
- CAN FD 只表示控制器能力，实际总线仍需要外部收发器、终端和保护。

## 板卡边界

- 开发板包含 5 V 转 3.3 V 电源与下载调试连接，不能直接替代量产模组的供电、EMC 和功耗设计。
- v1.1 与 v1.2 的排针功能存在差异；物理引脚计划必须绑定板卡版本。
- 整板休眠电流暂无内部实测，低功耗承诺必须在目标样机上验证。

## 官方来源

[ESP32-C5-DevKitC-1 v1.2 User Guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32c5/esp32-c5-devkitc-1/user_guide.html)
