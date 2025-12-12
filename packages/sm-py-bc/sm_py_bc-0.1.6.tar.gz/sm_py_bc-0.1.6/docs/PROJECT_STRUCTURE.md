# 项目结构说明

## 📁 目录结构

```
sm-py-bc/
├── .github/              # GitHub 配置
│   └── workflows/       # CI/CD 工作流
│       ├── ci.yml                  # 持续集成
│       ├── daily-full-test.yml     # 每日完整测试
│       └── publish.yml             # PyPI 发布
│
├── src/                 # 源代码目录
│   └── sm_bc/          # 主包
│       ├── crypto/             # 密码学实现
│       │   ├── digests/        # SM3 哈希算法
│       │   ├── engines/        # SM2/SM4 引擎
│       │   ├── signers/        # SM2 签名器
│       │   ├── modes/          # 加密模式
│       │   ├── paddings/       # 填充方案
│       │   ├── params/         # 密码学参数
│       │   ├── agreement/      # 密钥交换
│       │   ├── kdf/            # 密钥派生
│       │   └── cipher.py       # 高层API
│       ├── math/               # 椭圆曲线数学
│       ├── util/               # 工具类
│       └── exceptions/         # 异常定义
│
├── tests/              # 测试目录
│   └── unit/          # 单元测试
│       ├── crypto/            # 密码学测试
│       ├── math/              # 数学测试
│       └── util/              # 工具测试
│
├── test/               # 集成测试
│   └── graalvm-integration/   # GraalVM 互操作测试
│
├── examples/           # 示例代码
│   ├── sm2_*.py              # SM2 示例
│   ├── sm3_*.py              # SM3 示例
│   ├── sm4_*.py              # SM4 示例
│   └── README.md             # 示例说明
│
├── docs/               # 文档目录
│   ├── README_EN.md          # 英文 README（备份）
│   ├── PROJECT_STRUCTURE.md  # 项目结构说明（本文件）
│   └── process/              # 开发过程文档
│       ├── GITHUB_SETUP.md
│       ├── PUBLISHING.md
│       ├── COMPLETE_SETUP_SUMMARY.md
│       └── ... （其他过程文档）
│
├── dist/               # 构建产物
│   ├── sm_py_bc-*.tar.gz     # 源码分发包
│   └── sm_py_bc-*.whl        # wheel 包
│
├── README.md           # 主 README（中文）
├── LICENSE             # MIT 许可证
├── pyproject.toml      # 项目配置
├── MANIFEST.in         # 包清单
└── .gitignore          # Git 忽略规则
```

## 📦 核心模块

### src/sm_bc/crypto/

#### digests/ - 哈希算法
- `sm3_digest.py` - SM3 哈希实现
- `general_digest.py` - 通用哈希基类

#### engines/ - 密码引擎
- `sm2_engine.py` - SM2 公钥加密引擎
- `sm4_engine.py` - SM4 分组密码引擎

#### modes/ - 加密模式
- `cbc_block_cipher.py` - CBC 模式
- `ctr_block_cipher.py` (sic) - CTR 模式
- `ofb_block_cipher.py` - OFB 模式
- `cfb_block_cipher.py` - CFB 模式
- `ecb_block_cipher.py` - ECB 模式
- `gcm_block_cipher.py` - GCM 模式（认证加密）

#### paddings/ - 填充方案
- `pkcs7_padding.py` - PKCS#7 填充（推荐）
- `iso7816_4_padding.py` - ISO 7816-4 填充
- `iso10126_padding.py` - ISO 10126 填充
- `zero_byte_padding.py` - 零字节填充
- `padded_buffered_block_cipher.py` - 带填充的缓冲密码器

#### signers/ - 签名器
- `sm2_signer.py` - SM2 数字签名
- `dsa_encoding.py` - DSA 编码
- `dsa_k_calculator.py` - DSA k 值计算

#### params/ - 密码学参数
- `ec_key_parameters.py` - 椭圆曲线密钥参数
- `key_parameter.py` - 密钥参数
- `parameters_with_iv.py` - 带 IV 的参数
- `aead_parameters.py` - AEAD 参数

#### agreement/ - 密钥协商
- `sm2_key_exchange.py` - SM2 密钥交换协议

### src/sm_bc/math/

椭圆曲线数学运算:
- `ec_point.py` - 椭圆曲线点
- `ec_curve.py` - 椭圆曲线定义
- `ec_field_element.py` - 有限域元素
- `ec_multiplier.py` - 点乘法器
- `ec_algorithms.py` - 椭圆曲线算法

### src/sm_bc/util/

工具类:
- `arrays.py` - 数组操作
- `pack.py` - 打包/解包
- `big_integers.py` - 大整数运算
- `integers.py` - 整数运算
- `secure_random.py` - 安全随机数

## 🧪 测试结构

### tests/unit/

单元测试，按模块组织:
- `crypto/` - 密码学测试
  - `digests/` - SM3 测试
  - `signers/` - SM2 签名测试
  - `agreement/` - 密钥交换测试
  - `kdf/` - 密钥派生测试
- `math/` - 椭圆曲线数学测试
- `util/` - 工具类测试
- `test_sm2_engine.py` - SM2 引擎测试
- `test_sm3_digest.py` - SM3 摘要测试
- `test_sm4_engine.py` - SM4 引擎测试
- `test_*_mode.py` - 加密模式测试
- `test_padding*.py` - 填充方案测试

### test/graalvm-integration/

GraalVM 互操作性测试（Java 调用 Python）

## 📚 文档结构

### docs/

- `README_EN.md` - 英文版 README（备份）
- `PROJECT_STRUCTURE.md` - 本文件，项目结构说明

### docs/process/

开发过程文档（已归档）:
- **设置指南**:
  - `GITHUB_SETUP.md` - GitHub 设置指南
  - `PUBLISHING.md` - PyPI 发布指南
  - `QUICK_PUBLISH.md` - 快速发布指南
  - `RELEASE_CHECKLIST.md` - 发布检查清单

- **项目总结**:
  - `COMPLETE_SETUP_SUMMARY.md` - 完整设置总结
  - `GITHUB_DEPLOYMENT_SUMMARY.md` - GitHub 部署总结
  - `PYPI_PREPARATION_SUMMARY.md` - PyPI 准备总结
  - `PACKAGE_READY.md` - 包就绪状态

- **开发记录**:
  - `IMPLEMENTATION_SUMMARY.md` - 实现总结
  - `IMPLEMENTATION_COMPARISON.md` - 实现对比
  - `PROGRESS.md` - 进度跟踪
  - `SESSION_*.md` - 开发会话记录

- **测试文档**:
  - `TESTING_STATUS.md` - 测试状态
  - `TEST_*.md` - 各种测试报告

## 🔨 构建产物

### dist/

构建的包文件:
- `sm_py_bc-0.1.0.tar.gz` - 源码分发包（~107 KB）
- `sm_py_bc-0.1.0-py3-none-any.whl` - wheel 包（~80 KB）

这些文件由 `python -m build` 生成，用于发布到 PyPI。

## ⚙️ 配置文件

### 根目录

- `pyproject.toml` - 项目配置和依赖
  - 包元数据
  - 构建系统配置
  - pytest 配置
  
- `MANIFEST.in` - 包清单
  - 指定要包含的文件
  
- `.gitignore` - Git 忽略规则
  - Python 相关忽略
  - IDE 配置忽略
  - 构建产物忽略
  
- `.gitattributes` - Git 属性
  - 行尾规范化
  - 文件类型标记

- `.pypirc.example` - PyPI 配置示例
  - 凭证配置模板

## 📊 统计信息

### 代码规模
- **源文件**: 70+ Python 模块
- **测试文件**: 40+ 测试文件
- **测试用例**: 200+ 单元测试
- **代码行数**: ~15,000+ 行
- **文档**: 25+ markdown 文件

### 测试覆盖
- SM2: 29 个测试
- SM3: 18 个测试
- SM4: 18 个测试
- 加密模式: 60 个测试
- 填充方案: 40 个测试
- 数学库: 35 个测试
- 总计: 200+ 个测试（100% 通过）

## 🎯 使用指南

### 开发

```bash
# 克隆仓库
git clone https://github.com/lihongjie0209/sm-py-bc.git
cd sm-py-bc

# 安装开发依赖
pip install -e ".[test]"

# 运行测试
pytest tests/unit/

# 构建包
python -m build
```

### 文档导航

1. **快速开始**: 查看 `README.md`
2. **API 参考**: 查看源代码注释和 docstrings
3. **示例代码**: 查看 `examples/` 目录
4. **发布指南**: 查看 `docs/process/PUBLISHING.md`
5. **GitHub 设置**: 查看 `docs/process/GITHUB_SETUP.md`

## 🔗 相关链接

- **GitHub**: https://github.com/lihongjie0209/sm-py-bc
- **Issues**: https://github.com/lihongjie0209/sm-py-bc/issues
- **Actions**: https://github.com/lihongjie0209/sm-py-bc/actions
- **PyPI**: (即将上线)

---

**最后更新**: 2025-12-06  
**版本**: 0.1.0
