> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# ESP32-C6-WROOM-1 模组

## 定位

面向 Wi-Fi 6、Bluetooth LE 与 802.15.4 产品，可用于 Zigbee 或 Thread/Matter 终端和边缘设备。

## 协议边界

- Zigbee 与 Thread/Matter 需要明确选择协议栈、角色和认证目标。
- “支持 802.15.4”不等于产品已经完成 Zigbee、Thread 或 Matter 认证。
- 同一固件需要多协议共存时，必须单独验证射频时分、内存和实时性。

## 硬件约束

3.0–3.6 V 供电；遵守天线净空、电源峰值、启动脚和 USB/调试接口设计要求，并按完整订购料号确认 Flash 变体。

## 官方来源

[ESP32-C6-WROOM-1 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c6-wroom-1_datasheet_en.pdf)
