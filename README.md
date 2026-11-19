# 跨机构住房明细契约切换与可重述湖表

两代成交交付契约、分区范围替代和固定研究引用。本仓库当前包含原始合成资料、来源格式文档和资料检查程序，尚无业务入仓、事实生成或数据查询实现。

## 环境

使用 Python 3.11，依赖精确版本记录在 requirements.txt。DuckDB 用于本地分析存储，具体业务表尚未建立。

    python3 -m pip install -r requirements.txt

## 当前可用入口

检查资料字节、行数与字段形状：

    python3 tools/inspect_source.py

执行资料和运行时检查：

    python3 -m unittest discover -s tests -v

检查 Python 文件能否编译：

    python3 -m compileall -q tools tests

这些命令只验证资料完整性及存储运行时，不代表任何业务能力已经完成。资料格式和来源语义见 docs/source-contract.md；data 内均为本地合成记录。业务运行方式需随实际程序补充。
