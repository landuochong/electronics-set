# 数据模型 v0.1

## 身份与关系

`id` 为厂家命名空间下稳定 ID，`legacy_ids` 仅供迁移查找。`manufacturer_id` 是登记的实体；`manufacturer_role` 区分真实产品厂家与仅已知参考芯片厂家。型号不明确时允许 `mpn: null`。不要由描述性名称自动推断精确订货号。

`product_type` 区分 `chip`、`module`、`board`、`reference_design`、`component`、`instrument`。`legacy.kind` 保留原库的更细类型。类别仅用于检索，不决定电路兼容性。

`relations` 使用 `{type, target}`：`uses_chip`、`uses_module`、`variant_of`、`candidate_alternative`。目标必须存在。候选替代不代表引脚、电平、驱动、封装或功能可直接替换。迁移不凭名字自动创建未经证实的关系。

## 参数与单位

`specifications` 的通用数值必须有 `unit`；范围采用 `min/typ/max`。工作范围与 `absolute_maximum` 必须分开。供电的 `port`、功耗的 `conditions` 在缺失时列入 unresolved。`null` 表示未知，不等于零。

从旧库迁移的供电值标为 `legacy_unspecified`，需要复核其工作/极限语义。旧接口列表只是历史声明，不代表所有接口引脚可同时使用。

`legacy` 是未完全标准化的原始结构快照，保留估算值、价格和置信度，不是权威参数。没有采集时间的旧价格不得用于实时采购决策。

## 来源、复核与测试

每份来源带稳定局部 ID、标题、URL、authority 和可选版本/章节。`evidence` 用 JSON Pointer 指向具体字段，注明来源、定位信息及 binding。迁移仅建立 `inherited_unreviewed` 关联，不声称原厂文档确实支持每个旧参数。

`source_reviewed` 要求关键事实有 `explicit` 证据和人工审核记录；自动校验只检查结构和覆盖率，无法判断引文真实性。`validation.tests` 单独保存有限条件下的实测记录。

引脚文件必须引用本条目的 source ID，标明 `partial_gpio_extract` 或 `complete_physical_pinout`。初次导入 7 份引脚为部分 GPIO 摘录，硬件版本保持历史描述，仍需复核。

## Schema 演进

核心结构禁止未知字段，附加数据放 extensions。Schema 和词表存入版本控制；不兼容变更升级主版本并提供迁移说明。业务平台应锁定知识库版本而不是读取浮动最新版。
