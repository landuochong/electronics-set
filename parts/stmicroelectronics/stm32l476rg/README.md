> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# STM32L476RG MCU

## 定位

80 MHz Cortex-M4F 超低功耗 MCU，适合需要较成熟 STM32 生态、丰富模拟/通信外设和电池运行的通用设备。

## 选型边界

- L4 不集成 Wi-Fi、BLE、Zigbee 或 Thread；无线需求必须增加外部模组。
- 低功耗指标依赖电源模式、时钟、RAM 保持、唤醒源、温度和外设状态，不能复制数据手册单点典型值作为整机结论。
- `RG` 对应特定封装/容量组合，换用 RC、VG 等后缀必须重新审核引脚与存储。

## 自研板约束

按官方参考设计实现电源、去耦、复位、BOOT、时钟、SWD、USB 和模拟参考；模拟地、参考电压及 ADC 前端需单独评审。

## 官方来源

[STM32L476RG Product Page](https://www.st.com/en/microcontrollers-microprocessors/stm32l476rg.html)
