# SM2/SM3/SM4 Python 实现计划

## Phase 1: 基础设施与工具类 (Infrastructure)
**目标**: 搭建项目骨架，实现基础工具类，为后续算法实现打下基础。

- [ ] **项目初始化**
    - 配置 `pyproject.toml` (依赖 `pytest`)
    - 配置 `pytest.ini`
- [ ] **基础工具类 (`src/sm_bc/util/`)**
    - `pack.py`: 大端序整数与字节数组转换 (对应 `Pack.ts`)
    - `arrays.py`: 数组操作工具 (对应 `Arrays.ts`)
    - `integers.py`: 整数操作工具 (对应 `Integers.ts`, 旋转移位等)
    - `memoable.py`: `Memoable` 接口/协议
- [ ] **测试**
    - 移植对应的单元测试

## Phase 2: SM3 消息摘要算法 (SM3 Digest)
**目标**: 实现 SM3 哈希算法。

- [ ] **接口定义 (`src/sm_bc/crypto/`)**
    - `digest.py`: `Digest` 协议/抽象基类
    - `extended_digest.py`: `ExtendedDigest` 协议
- [ ] **通用基类 (`src/sm_bc/crypto/digests/`)**
    - `general_digest.py`: `GeneralDigest` 实现 (MD4家族基类)
- [ ] **SM3 实现 (`src/sm_bc/crypto/digests/`)**
    - `sm3_digest.py`: `SM3Digest` 核心逻辑
- [ ] **测试**
    - 使用 `sm-js-bc` 的标准测试向量进行验证
    - 验证 `update` 分段处理、`reset` 等功能

## Phase 3: 椭圆曲线数学库 (EC Math)
**目标**: 实现有限域运算和椭圆曲线点运算，支持 SM2。

- [ ] **基础数学 (`src/sm_bc/math/`)**
    - `ec_constants.py`
    - `raw/nat.py`: 大数运算辅助 (Python 原生支持大数，可能只需部分功能)
- [ ] **EC 核心**
    - `ec_field_element.py`: 有限域元素
    - `ec_curve.py`: 椭圆曲线定义
    - `ec_point.py`: 椭圆曲线点运算 (加法、倍点等)
    - `ec_multiplier.py`: 点乘算法 (如 FixedPointComb)
- [ ] **测试**
    - 验证点加、点乘等基础运算正确性

## Phase 4: SM2 签名与加密 (SM2)
**目标**: 实现 SM2 的签名、验证、加密、解密。

- [ ] **参数与辅助类**
    - `cipher_parameters.py`
    - `ec_domain_parameters.py`
    - `key_parameters.py`
- [ ] **SM2 签名**
    - `sm2_signer.py`: 签名与验签逻辑
    - `dsa_k_calculator.py`: 随机数 K 生成
- [ ] **SM2 加密**
    - `sm2_engine.py`: 加密引擎 (C1C2C3/C1C3C2)
- [ ] **SM2 密钥交换**
    - `sm2_key_exchange.py`
- [ ] **测试**
    - 移植 SM2 签名和加密的测试向量

## Phase 5: SM4 分组密码 (SM4)
**目标**: 实现 SM4 对称加密及其工作模式。

- [ ] **SM4 引擎**
    - `sm4_engine.py`: 基础 BlockCipher
- [ ] **工作模式**
    - `ecb_block_cipher.py`
    - `cbc_block_cipher.py`
    - `gcm_block_cipher.py`
- [ ] **填充**
    - `pkcs7_padding.py`
- [ ] **测试**
    - 验证各模式下的加密解密一致性

## Phase 6: 综合测试与发布
- [ ] 跨语言一致性测试 (与 JS/Java 版本输出对比)
- [ ] 性能基准测试
- [ ] 打包发布
