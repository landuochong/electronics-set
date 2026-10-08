# electronics-set

开放、跨厂家的电子元器件与模块知识库。面向人工选型、AI 检索和工程工具，不依赖 ForgeAI 或任何在线服务。

仓库：`git@github.com:landuochong/electronics-set.git`。

## 从这里开始

- [器件索引](INDEX.md)：按厂家浏览。
- [数据规范](docs/data-model.md)：如何准确描述芯片、模组和开发板。
- [贡献指南](CONTRIBUTING.md)：新增厂家、器件、来源和实测记录。
- [迁移报告](docs/migration-report.md)：现有资料的覆盖范围和待复核事项。
- [发布与接入](docs/releases.md)：数据导出与下游版本锁定。
- [授权说明](docs/licensing.md)：原创资料与第三方资料的边界。

## 文件结构

```text
parts/<manufacturer>/<part-id>/part.json   # 机器可读的唯一参数源
parts/<manufacturer>/<part-id>/README.md   # 人工维护的工程知识
parts/<manufacturer>/<part-id>/pinout.json # 可选：带来源的板卡引脚
manufacturers/*.json                      # 厂家及别名
schemas/*.json                           # JSON Schema 2020-12
vocabulary/taxonomy.json                  # 跨厂家的分类/能力/接口词表
tools/                                   # 导入、校验、导出
tests/                                   # 数据和工具的回归测试
```

## 本地使用

需要 Python 3.10+。无需数据库、AI 密钥或平台服务器。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/validate.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tools/export.py --output dist
```

`dist/catalog.json` 包含结构化条目；`dist/knowledge.json` 同时包含 Markdown 正文及引脚，可用于全文/向量检索；`dist/manifest.json` 包含文件哈希。生成物无需人工维护。

## 信任边界

格式校验成功不代表参数正确、接线安全或产品可量产。初次迁移条目均为 `needs_review`；历史验证标签只保留在 `legacy` 中。必须按证据进行人工核对，实物测试单独记录。

本仓库不提供自动下单、生产许可或器件绝对互换保证。量产前需核查原厂最新资料、板卡版本和实际供货情况。

## 许可

原创工具、规范及协作文档采用仓库原有的 [MIT LICENSE](LICENSE)；从 ForgeAI 迁移的器件数据和工程笔记保留 [BSD-3-Clause](LICENSES/BSD-3-Clause.txt)，以条目 provenance 为准。第三方文档仅引用链接，不自动获得原厂文档、商标、图片或模型的再分发权。
