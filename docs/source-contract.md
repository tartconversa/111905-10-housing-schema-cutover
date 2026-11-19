# 来源资料约定

两代成交交付契约、分区范围替代和固定研究引用。

v1行按合同，amount_yuan与area_sqm为十进制字符串，scope_members列明所含房屋业务键但不提供逐套金额。v2按contract_id/unit_id，price是currency/minor/value对象，minor=2表示货币小数位，area是value/unit/basis对象。

源文件声明在files，实际数据在legacy/new_rows中以file_id对应；deliveries的expected_files和complete声明一个交付的文件覆盖。替代声明replacement包含旧file_id及scope_members，不能由文件名推断范围。

contracts的effective_periods限制契约解释可作用的业务期间，revision是解释版本号；compatibility表示合作方明确担保的指标语义关系，不担保的口径不得假定等价。

consumers记录现有研究的固定contract_version、grain及metrics。references中的pin/release作用于指定published_version，撤回delivery不等于释放研究引用。原始源文件清理须尊重有效引用及资料依赖，不要求具体存储实现。

published_version是研究方要求固定的交付别名；baseline-oct指D-OLD在已交齐时建立的v1视图别名，并不表示本地已有实现。release终止对应pin后的后续引用，不撤销此前有效引用期间。

## 数据载体

每类资料位于 data 中同名的 NDJSON 文件，一行一个原始对象；字段和基本类型见 data/schema.json。data/manifest.json 固定资料行数与字节哈希。资料中的缺失、歧义、未完整交付及冲突声明属于来源事实，不由资料检查程序推断业务结论。

### contracts

语义契约声明。字段：contract_version (string)、revision (integer)、grain (string)、effective_periods (array)、currency_rule (string)、area_basis (string)、received (string)。

### legacy

合同粒度旧记录。字段：file_id (string)、city (string)、period (string)、contract_id (string)、scope_members (array)、amount_yuan (string)、area_sqm (string)。

### new_rows

新格式房屋行。字段：file_id (string)、city (string)、period (string)、contract_id (string)、unit_id (string)、price (object)、area (object)。

### files

交付文件身份。字段：file_id (string)、contract_version (string)、delivery_id (string)、city (string)、period (string)。

### deliveries

完整交付与范围替代。字段：receipt_id (string)、delivery_id (string)、expected_files (array)、arrived_files (array)、complete (boolean)、replacement (array)、received (string)、kind (string)。

### compatibility

得到担保的口径兼容关系。字段：record_id (string)、from_version (string)、to_version (string)、metric (string)、grain (string)、period (string)、compatible (boolean)。

### consumers

现有研究的读取契约。字段：consumer (string)、contract_version (string)、grain (string)、metrics (array)。

### references

研究引用及释放。字段：reference_id (string)、consumer (string)、published_version (string)、kind (string)、received (string)、reference (any)。

