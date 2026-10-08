> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# NUCLEO-G071RB

## 定位

STMicroelectronics 的 development_board，在 ForgeAI 中用于 `i2c`、`spi`、`uart`、`adc`、`can`。

## 适用场景

- 快速验证与该器件能力匹配的嵌入式原型。
- 需要 `STM32G0` 生态或现有工具链的项目。

## 核心能力

- 能力：i2c、spi、uart、adc、can
- 接口：I2C、SPI、UART、CAN、GPIO
- 供电：typ=5.0V
- 验证等级：`source_verified`

## 设计约束

- 开发板功耗、尺寸和板载外围不能直接代表最终量产模组。
- 物理引脚必须结合板卡版本、启动脚、USB/JTAG 和板载器件占用复核。
- 知识库没有整板休眠电流实测值，不能用芯片典型值代替。

## 选型提示

- 根据无线协议、外设数量、存储、功耗、成本和供货状态与同系列器件比较。
- 原型阶段优先开发板；进入小型化或低功耗阶段再切换到模组/自研底板。

## 开发与验证

- 生成代码后必须完成目标工具链编译，不能只做主机语法检查。
- 首次上电使用限流电源，并保留启动日志、固件哈希和板卡版本。

## 官方来源

[NUCLEO-G071RB product page](https://www.st.com/en/evaluation-tools/nucleo-g071rb.html)
