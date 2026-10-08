> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# STM32G071RB MCU

## 定位

Cortex-M0+ 经济型通用 MCU，适合成本敏感的传感器节点、控制面板、简单工业 I/O 和替代传统 8/16 位 MCU 的项目。

## 选型提示

- 与 F4/U5 相比算力和高级外设更少，但成本、复杂度和基础控制开发负担较低。
- 需要 Wi-Fi、BLE、Zigbee 或 Thread 时必须增加外部通信模组。
- CAN 项目必须区分 MCU 控制器能力与外部收发器、终端电阻和防护电路。

## 自研板约束

重新设计电源、去耦、复位、BOOT、SWD、时钟和量产测试点；根据封装复核可用 ADC、定时器和通信复用引脚。

## 官方来源

[STM32G071RB product page](https://www.st.com/en/microcontrollers-microprocessors/stm32g071rb.html)
