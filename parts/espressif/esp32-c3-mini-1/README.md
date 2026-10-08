> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# ESP32-C3-MINI-1 模组

## 定位

面向小尺寸 Wi-Fi + Bluetooth LE 产品的 ESP32-C3 集成模组。适合从 C3 开发板原型转向自研底板。

## 选型要点

- 3.0–3.6 V 供电，不能直接接 5 V。
- 支持 2.4 GHz Wi-Fi 与 Bluetooth LE，不支持经典蓝牙。
- 使用前必须确认具体后缀、Flash 容量、天线形式和模组版本。

## PCB 与射频约束

- 天线净空、地平面、模组边缘位置必须按官方推荐布局执行。
- 电源需要覆盖无线发射峰值，并在模组附近布置去耦。
- 下载/启动脚、EN、UART/JTAG 与量产烧录测试点必须预留。

## 与开发板的区别

开发板上的 USB、稳压、自动下载和指示灯不属于 MINI-1 模组。切换到自研底板时必须重新设计这些外围电路。

## 官方来源

[ESP32-C3-MINI-1 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3-mini-1_datasheet_en.pdf)
