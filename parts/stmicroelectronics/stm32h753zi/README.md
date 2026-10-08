> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# STM32H753ZI MCU

## 定位

480 MHz Cortex-M7 高性能 MCU，带双精度 FPU、Cache、大容量片上存储、外部存储接口、JPEG 与硬件密码加速，适合高吞吐控制和边缘处理。

## 自研板约束

- 供电域、VCAP、去耦、复位、BOOT、时钟、SWD 和散热必须按数据手册与硬件设计指南逐项实现。
- Ethernet、USB HS、外部 SDRAM/SDRAM、并行显示和高速 ADC 数据通路需要专门的时序与信号完整性设计。
- CAN FD 控制器不包含物理层收发器。

## 固件约束

- 明确 DTCM/AXI SRAM/DMA 可访问性，设计 Cache clean/invalidate 策略。
- 启用硬件密码功能时同时定义密钥写入、固件签名、安全启动和升级恢复流程。
- 所有资源数必须绑定完整料号 `STM32H753ZIT6` 等，不得仅凭系列名分配引脚。

## 官方来源

[STM32H753ZI Product Page](https://www.st.com/en/microcontrollers-microprocessors/stm32h753zi.html)
