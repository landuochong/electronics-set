> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# ESP32-C5-WROOM-1 模组

## 定位

面向双频 Wi-Fi 6 与多协议低功耗无线产品的量产模组。WROOM-1 使用板载 PCB 天线，WROOM-1U 使用外部天线连接器，不能共用同一套结构与射频结论。

## 主要能力

- 2.4 GHz 与 5 GHz 双频 Wi-Fi 6。
- Bluetooth LE 与 IEEE 802.15.4，可用于 Zigbee、Thread/Matter。
- 提供 USB Serial/JTAG、ADC、I2C、SPI、UART、PWM 与 CAN FD 控制器等资源。

## 设计约束

- 3.0–3.6 V 供电，按无线发射峰值设计电源、去耦与地回流，不能按平均电流选稳压器。
- 遵守官方 land pattern、天线净空、模组边缘位置和禁布要求。
- 按完整订购料号确认 Flash、PSRAM、工作温度与天线版本。
- 模组认证不自动覆盖最终整机；外壳、天线环境和目标市场变化时应复核法规测试。

## 官方来源

[ESP32-C5-WROOM-1/1U Datasheet](https://documentation.espressif.com/esp32-c5-wroom-1_wroom-1u_datasheet_en.html)
