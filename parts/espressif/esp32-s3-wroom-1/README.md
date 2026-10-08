> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# ESP32-S3-WROOM-1 模组

## 定位

适合需要 Wi-Fi、Bluetooth LE、原生 USB、较多 GPIO、音频/摄像头或较高算力的产品。WROOM-1 使用板载天线，WROOM-1U 使用外接天线接口，不能混为一个 PCB 方案。

## 变体确认

- Flash 与 PSRAM 容量随订购型号变化，生成固件分区表前必须确认完整料号。
- 带 PSRAM 的型号适合图像、音频缓存和较大 UI；普通传感器节点未必需要。

## 设计约束

- 3.0–3.6 V 供电，电源和去耦按无线峰值设计。
- USB D+/D-、启动脚、JTAG 和高速接口需要单独做引脚冲突检查。
- 使用板载天线型号时遵守天线净空；外接天线型号需确认连接器、天线和认证组合。

## 官方来源

[ESP32-S3-WROOM-1/1U Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
