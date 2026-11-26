# AthenaFlow V3 — 独立 CUA 测试包

**472 项测试，27 个模块。当前 472 NOT_RUN；尚未对网站执行测试，也尚未上传到 GitHub。**

本测试包依据你上传的完整 Description V3 设计。它不是让 Codex 重新设计测试的提纲；每项已有前置条件、操作步骤、预期结果和验收条件。编号、内容、顺序、源文档与关键执行规则已冻结。

## 如何交给新窗口的 Codex

1. 上传 `AthenaFlow_V3_Independent_CUA_472.zip`。
2. 将 `CODEX_EXECUTION_PROMPT.md` 全文复制为消息并发送。
3. 如果 Codex 无法从当前环境或仓库找到目标网站，补充实际 URL。无需提前编造端口、网站域名、分支或 commit。
4. Codex 先执行冻结的 10 项跨模块试点，再每 20 项自动继续并上传一次。最终一批为 2 项。已完成项不自动重测。

## 文件用途

| 文件 | 内容 |
| --- | --- |
| `frozen/all_tests.json` | 权威机器可读定义，472 个稳定 Test ID |
| `frozen/AthenaFlow_V3_CUA_Tests_472.xlsx` | 简洁可筛选 Excel 清单；只读初始定义，不用于覆盖正式结果 |
| `frozen/all_tests.csv` / `test_catalog.md` | 可搜索、可审阅的完整清单 |
| `frozen/coverage_matrix.csv` | 每项场景与 description 章节映射 |
| `frozen/description_v3.md` | 保留原始上传内容的源规格 |
| `frozen/PROTOCOL.md` | CUA 方法、状态判定、证据、续测与 GitHub 规则 |
| `frozen/FIXTURES.md` | 合成数据、前置状态、数值 oracle 与缺失处理 |
| `frozen/SCOPE_AND_ASSUMPTIONS.md` | 可测范围、非 CUA 项及预先声明的解释 |
| `frozen/execution_order.json` | 10 项试点、剩余顺序与最后执行的隔离重置 |
| `results/` | 472 NOT_RUN 初始结果、环境、尝试、断点与上传记录模板 |
| `suite_manifest.json` / `SHA256SUMS` | 文件、案例和 ID 校验 |
| `scripts/validate_suite.py` | 离线完整性/结果结构校验，不测试网站 |
| `scripts/summarize_results.py` | 从实际结果统计总体/模块/难度数据，不推断 PASS |
| `reports/current/` | 当前未执行状态的统计，非运行结果 |

## 数量与设计原则

| 难度 | 数量 |
| --- | ---: |
| Easy | 26 |
| Medium | 296 |
| Hard | 127 |
| Expert | 23 |

Easy：短路径观察；Medium：单模块常规流程或明确验证；Hard：边界、权限、状态或跨视图一致性；Expert：完整多角色流程、财务对账或多时间口径。分类由任务结构决定，没有为了配额人为凑数。

| 模块 | 数量 |
| --- | ---: |
| Authentication and role boundaries | 18 |
| Global navigation and accessibility | 20 |
| Registration and patient selection | 24 |
| Longitudinal patient chart | 14 |
| Scheduling and waitlist | 26 |
| Front desk check-in | 12 |
| Vitals units and clinical intake | 26 |
| Encounters notes and signatures | 24 |
| Problems and diagnoses | 12 |
| Medication management | 16 |
| Medical orders | 16 |
| Laboratory processing and result release | 16 |
| Insurance coverage and eligibility | 16 |
| Charge capture and coding | 16 |
| Claim validation and payer lifecycle | 26 |
| Denials and appeals | 12 |
| Prior authorization | 14 |
| Payments responsibility and receipts | 24 |
| Patient portal workflows | 18 |
| Messaging unread state and privacy | 18 |
| AI assistance and unsigned documentation | 24 |
| Clinical inbox and tasks | 10 |
| Analytics cohorts filters and CSV parity | 24 |
| Read-only interoperability through browser | 10 |
| Administration and safe demo management | 12 |
| Audit trails and readable activity | 10 |
| Integrated multi-role workflows | 14 |

有限测试集不能穷尽所有输入组合。这里优先覆盖明确需求、关键异常、权限和跨模块路径，避免将无意义重复点击算成独立测试。E2E 会复用组件操作，但验证的是整条链路，单独分组统计。

## 判定与统计

- PASS 必须逐条满足验收条件；FAIL 必须有实际观察依据。
- 缺少必要功能通常为 FAIL；外部连接、账号或无法构造的前置数据阻止验证才为相应 BLOCKED。
- 未执行或未获得结论的中断项为 NOT_RUN；不能算 PASS。
- 已执行项通过率 = PASS / (PASS + FAIL)，分母为零显示 N/A。
- 执行覆盖率 = (PASS + FAIL) / 472；全套成功比例 = PASS / 472。
- 同时报告 BLOCKED/NOT_RUN、首次结果与重试结果、版本分段和证据缺口。
- 不把 Playwright、单元测试、源码推断、离线演练或本包校验计入 CUA 通过率。

## GitHub 交付

目标仓库：https://github.com/KateK77/athenaone-clone。由执行窗口将冻结清单及每批真实结果、截图、动作证据、统计和断点上传到独立 evaluation 分支；保留原版本与其他测试。要求核实远端 SHA 后才报告上传成功。

目标分支：`evaluation/athenaflow-v3-independent-cua-472`。目标目录：`experiments/round-03/cua-evaluation/athenaflow-v3-independent-472/`。有冲突先检查，不覆盖。

不改应用、不削弱测试、不使用额外付费 API Key。源 description 的开发/修复命令在本轮仅作为规格材料。

## 本包校验命令

```bash
python scripts/validate_suite.py --results results/results.json
python scripts/summarize_results.py
```

SHA-256 用于检测内容变化，不是第三方签名或真实执行的证明。实际 CUA 执行证据须由新窗口保存。
