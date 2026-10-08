> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# ESP32-H2-MINI-1 模组

## 定位

面向 Bluetooth LE 与 802.15.4 低功耗终端。适合 Zigbee、Thread 和 Matter over Thread 设备，不具备 Wi-Fi，不能用于要求直接接入 Wi-Fi 的方案。

## 选型与协议约束

- 必须明确 Zigbee 或 Thread/Matter 的网络角色、上报模型和配网方式。
- MINI-1 与 MINI-1U 的天线方案不同，PCB 和认证条件也不同。
- 低功耗目标必须以整机实测为准，模组数据手册数值不能代替底板和传感器功耗。

## 硬件约束

3.0–3.6 V 供电；保留下载、调试和量产测试点，按官方布局处理天线净空与射频区域。

## 官方来源

[ESP32-H2-MINI-1/1U Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-h2-mini-1_mini-1u_datasheet_en.pdf)
