> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# STM32F446RE MCU

## 定位

Cortex-M4 系列通用高性能 MCU，适合电机控制、工业通信、USB、控制算法和需要成熟 STM32F4 生态的项目。NUCLEO-F446RE 是基于该 MCU 的开发板，但两者的供电、引脚和功耗事实必须分开保存。

## 主要资源

- 最高主频、Flash、SRAM、定时器、ADC 和通信外设以完整料号和官方数据手册为准。
- `RE` 后缀对应具体封装/容量组合，替换为其他后缀时必须重新检查封装与引脚。

## 设计约束

- 自研板需要重新设计去耦、复位、BOOT、时钟、SWD 和电源。
- USB、CAN 和高速时钟相关接口需要外部器件与 PCB 规则配合。
- 不能把 Nucleo 板的 ST-LINK、稳压和 Arduino 排针当成 MCU 内部能力。

## 工具链

STM32CubeMX / STM32CubeIDE、STM32CubeF4 HAL/LL、GCC/Clang/商业工具链。发布门禁要求目标构建日志和实际板卡运行证据。

## 官方来源

[STM32F446RE product page](https://www.st.com/en/microcontrollers-microprocessors/stm32f446re.html)
