> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# NUCLEO-L476RG

## 定位

基于 STM32L476RG 的 Nucleo-64 低功耗开发板，适合电池传感器、数据记录器、便携仪表和需要 USB/丰富模拟外设的原型。

## 低功耗边界

- “L4 低功耗”指 MCU 能力，不代表带 ST-LINK、LED 和板载稳压器的整板自动达到芯片级电流。
- 低功耗验证需要断开或隔离调试器、LED 与外设，并记录模式、唤醒源、时钟和测量方法。
- 无原生无线能力；需要 BLE/Wi-Fi/LoRa 时应增加独立通信模组并重新计算电池容量。

## 板卡约束

Arduino Uno V3 与 ST morpho 排针便于原型连接，但量产板必须重新生成封装、引脚复用、电源与测试点设计。

## 官方来源

[NUCLEO-L476RG Product Page](https://www.st.com/en/evaluation-tools/nucleo-l476rg.html)
