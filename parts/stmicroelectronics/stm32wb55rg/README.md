> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# STM32WB55RG 无线 MCU

## 定位

集成 Cortex-M4 应用核、Cortex-M0+ 无线核和 2.4 GHz 收发器的低功耗无线 MCU，可用于 BLE 5.4、IEEE 802.15.4、Zigbee、Thread 和 Matter 设备。

## 射频设计约束

- 裸 MCU 不是预认证无线模组；需要射频匹配、滤波/巴伦、50 Ω 走线、天线、晶振和法规测试。
- 优先参考 ST 官方天线、匹配网络和 Nucleo/参考设计，任何堆叠、外壳或天线变化都需要重新验证。
- RF 区域的电源噪声、地平面和布局会直接影响灵敏度与发射性能。

## 软件与生产约束

- 无线协处理器固件、协议栈版本和应用固件必须建立兼容矩阵。
- OTA 需要同时考虑应用映像、无线栈升级、回滚与断电恢复。
- 量产烧录需定义密钥、设备身份、校准、MAC/地址和射频测试流程。

## 官方来源

[STM32WB55RG Product Page](https://www.st.com/en/microcontrollers-microprocessors/stm32wb55rg.html)
