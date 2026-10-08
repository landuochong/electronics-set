> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# ESP32-P4-Function-EV-Board

## 定位

面向相机、显示、H.264 编码、USB 与多媒体人机界面的 ESP32-P4 评估板，适合门铃、摄像头、中控屏、仪表和本地视觉原型。

## 必须区分的能力来源

- ESP32-P4 提供高性能计算、MIPI-CSI/DSI、H.264 编码与 USB 等多媒体能力。
- **ESP32-P4 芯片本身不集成 Wi-Fi 或 Bluetooth。** 该评估板通过板载 ESP32-C6-MINI-1 模组提供 Wi-Fi/BLE。
- 将 P4 用于自研量产板时，如果需要联网，必须把外部无线模组、固件通信和供电纳入架构。

## 板卡约束

- v1.4、v1.5.2 与 P4X 芯片修订版的连接和已知问题不同，设计证据必须绑定硬件版本。
- 7 英寸屏、摄像头、音频和无线模组是评估板资源，不是 P4 裸芯片自带器件。
- 摄像头/显示高速接口、PSRAM、USB 和网络并发时需独立验证带宽、内存、散热与电源峰值。

## 官方来源

[ESP32-P4-Function-EV-Board v1.5.2 User Guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html)
