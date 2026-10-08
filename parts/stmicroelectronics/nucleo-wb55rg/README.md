> 迁移待复核：以下为历史工程笔记，包含旧参数及验证措辞，不表示新仓库已审核通过。结构化参数以 part.json 为准。

# NUCLEO-WB55RG

## 定位

基于 STM32WB55RG 的双核 2.4 GHz 无线开发板，适合 BLE、Zigbee、Thread/Matter 与低功耗无线设备原型。

## 协议与架构边界

- 应用运行在 Cortex-M4，实时无线底层由专用 Cortex-M0+ 处理；固件升级和无线栈兼容需遵循 STM32CubeWB 流程。
- 支持 IEEE 802.15.4 不等于产品已通过 Zigbee、Thread 或 Matter 认证。
- 板载 PCB 天线、SMA 预留和匹配网络属于参考板设计，量产天线必须重新做射频与法规验证。

## 低功耗边界

开发板上的 ST-LINK、LED、稳压和调试连接会影响功耗；知识库不使用 MCU 典型值代替整板实测。

## 官方来源

[NUCLEO-WB55RG Product Page](https://www.st.com/en/evaluation-tools/nucleo-wb55rg.html)
