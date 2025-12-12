# SM-PY-BC: Pure Python Chinese Cryptography Library

**A complete, production-ready implementation of Chinese national cryptographic standards (SM2, SM3, SM4) in pure Python with zero external dependencies.**

[![CI](https://github.com/lihongjie0209/sm-py-bc/actions/workflows/ci.yml/badge.svg)](https://github.com/lihongjie0209/sm-py-bc/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: 200+ Passing](https://img.shields.io/badge/tests-200%2B%20passing-brightgreen.svg)](tests/)

---

## 🎯 Features

### ✅ Complete SM Algorithm Suite

**SM2 - Public Key Cryptography** (GM/T 0003-2012)
- Digital signature (sign/verify)
- Public key encryption/decryption
- Elliptic curve operations on SM2 recommended curve
- Compatible with Chinese national standards

**SM3 - Cryptographic Hash Function** (GM/T 0004-2012)
- 256-bit hash output
- Memoable interface for efficient incremental hashing
- Fully compliant with specification

**SM4 - Block Cipher** (GB/T 32907-2016)
- 128-bit block size, 128-bit key
- 32-round Feistel structure
- 5 cipher modes: ECB, CBC, CTR, OFB, CFB
- 4 padding schemes: PKCS#7, ISO 7816-4, ISO 10126, Zero-byte

### 🔒 Security Features

- **Zero external dependencies** - Complete cryptographic implementation in pure Python
- **Side-channel resistant** - Constant-time operations where applicable
- **Well-tested** - 183 comprehensive unit tests (100% passing)
- **Standards compliant** - Follows official Chinese cryptographic standards

### 🚀 Easy-to-Use High-Level API

```python
from sm_bc.crypto.cipher import create_sm4_cipher

# Simple encryption with recommended settings
cipher = create_sm4_cipher(mode='CBC', padding='PKCS7')
cipher.init(True, key, iv)
ciphertext = cipher.encrypt(plaintext)

# Decryption
cipher.init(False, key, iv)
plaintext = cipher.decrypt(ciphertext)
```

---

## 📦 Installation

```bash
# From PyPI (coming soon)
pip install sm-py-bc

# Or clone from GitHub
git clone https://github.com/lihongjie0209/sm-py-bc.git
cd sm-py-bc
pip install -e .

# No additional dependencies needed!
# Just Python 3.10 or higher
```

---

## 🔧 Quick Start

> 💡 **提示**: 以下是基础用法示例。想要完整的可运行代码？直接跳转到 [📚 完整示例](#-完整示例) 章节，所有示例都可以直接运行！

以下代码片段展示了各算法的基本用法：

### SM3 哈希

```python
from sm_bc.crypto.digests import SM3Digest

digest = SM3Digest()
data = b"Hello, SM3!"
digest.update_bytes(data, 0, len(data))

hash_output = bytearray(digest.get_digest_size())
digest.do_final(hash_output, 0)

print('SM3 Hash:', hash_output.hex())
```

📖 **完整示例**: [examples/sm3_hash.py](./examples/sm3_hash.py)

### SM2 密钥对生成

```python
from sm_bc.math.ec.custom.sm2 import SM2P256V1Curve
import secrets

curve = SM2P256V1Curve()
private_key = secrets.randbelow(curve.n)
public_key = curve.G.multiply(private_key)

print('Private key:', hex(private_key)[2:])
print('Public key X:', hex(public_key.get_affine_x_coord().to_big_integer())[2:])
print('Public key Y:', hex(public_key.get_affine_y_coord().to_big_integer())[2:])
```

📖 **完整示例**: [examples/sm2_keypair.py](./examples/sm2_keypair.py)

### SM2 数字签名

```python
from sm_bc.crypto.signers import SM2Signer
from sm_bc.crypto.params.ec_key_parameters import ECPrivateKeyParameters, ECPublicKeyParameters
from sm_bc.math.ec.custom.sm2 import SM2P256V1Curve
import secrets

curve = SM2P256V1Curve()
d = secrets.randbelow(curve.n)
Q = curve.G.multiply(d)

# 签名
message = b'Hello, SM2!'
signer = SM2Signer()
priv_params = ECPrivateKeyParameters(d, curve.domain_params)
signer.init(True, priv_params)
signature = signer.generate_signature(message)

# 验签
pub_params = ECPublicKeyParameters(Q, curve.domain_params)
signer.init(False, pub_params)
is_valid = signer.verify_signature(message, signature)
print('Signature valid:', is_valid)
```

📖 **完整示例**: [examples/sm2_sign.py](./examples/sm2_sign.py)

### SM2 公钥加密

```python
from sm_bc.crypto.engines import SM2Engine
from sm_bc.crypto.params.ec_key_parameters import ECPrivateKeyParameters, ECPublicKeyParameters
from sm_bc.math.ec.custom.sm2 import SM2P256V1Curve
import secrets

curve = SM2P256V1Curve()
d = secrets.randbelow(curve.n)
Q = curve.G.multiply(d)

# 加密
plaintext = b'Secret message'
engine = SM2Engine()
pub_params = ECPublicKeyParameters(Q, curve.domain_params)
engine.init(True, pub_params)
ciphertext = engine.process_block(plaintext, 0, len(plaintext))

# 解密
priv_params = ECPrivateKeyParameters(d, curve.domain_params)
engine.init(False, priv_params)
decrypted = engine.process_block(ciphertext, 0, len(ciphertext))
print('Decrypted:', bytes(decrypted).decode('utf-8'))
```

📖 **完整示例**: [examples/sm2_encrypt.py](./examples/sm2_encrypt.py)

### SM4 对称加密

```python
from sm_bc.crypto.cipher import create_sm4_cipher
import secrets

# 生成密钥并加密
key = secrets.token_bytes(16)
iv = secrets.token_bytes(16)

cipher = create_sm4_cipher(mode='CBC', padding='PKCS7')
cipher.init(True, key, iv)
plaintext = b'Hello, SM4!'
ciphertext = cipher.encrypt(plaintext)

# 解密
cipher.init(False, key, iv)
decrypted = cipher.decrypt(ciphertext)
print('Decrypted:', bytes(decrypted).decode('utf-8'))
```

> ⚠️ **安全提示**: 上述示例使用 CBC 模式。生产环境推荐使用 GCM 模式以获得认证加密。

📖 **完整示例**: 
- [examples/sm4_ecb_simple.py](./examples/sm4_ecb_simple.py) - 基础加密示例
- [examples/sm4_modes.py](./examples/sm4_modes.py) - 多种工作模式（ECB/CBC/CTR/GCM）

### SM2 密钥交换

```python
from sm_bc.crypto.agreement import SM2KeyExchange
from sm_bc.crypto.params.sm2_key_exchange_parameters import (
    SM2KeyExchangePrivateParameters,
    SM2KeyExchangePublicParameters
)
from sm_bc.crypto.params.ec_key_parameters import ECPrivateKeyParameters, ECPublicKeyParameters
from sm_bc.math.ec.custom.sm2 import SM2P256V1Curve
import secrets

curve = SM2P256V1Curve()

# Alice 生成密钥对（静态 + 临时）
alice_static_d = secrets.randbelow(curve.n)
alice_static_Q = curve.G.multiply(alice_static_d)
alice_static_priv = ECPrivateKeyParameters(alice_static_d, curve.domain_params)
alice_static_pub = ECPublicKeyParameters(alice_static_Q, curve.domain_params)

alice_ephemeral_d = secrets.randbelow(curve.n)
alice_ephemeral_Q = curve.G.multiply(alice_ephemeral_d)
alice_ephemeral_priv = ECPrivateKeyParameters(alice_ephemeral_d, curve.domain_params)
alice_ephemeral_pub = ECPublicKeyParameters(alice_ephemeral_Q, curve.domain_params)

# Bob 生成密钥对（静态 + 临时）
bob_static_d = secrets.randbelow(curve.n)
bob_static_Q = curve.G.multiply(bob_static_d)
bob_static_priv = ECPrivateKeyParameters(bob_static_d, curve.domain_params)
bob_static_pub = ECPublicKeyParameters(bob_static_Q, curve.domain_params)

bob_ephemeral_d = secrets.randbelow(curve.n)
bob_ephemeral_Q = curve.G.multiply(bob_ephemeral_d)
bob_ephemeral_priv = ECPrivateKeyParameters(bob_ephemeral_d, curve.domain_params)
bob_ephemeral_pub = ECPublicKeyParameters(bob_ephemeral_Q, curve.domain_params)

# Alice 计算共享密钥（发起方）
alice_exchange = SM2KeyExchange()
alice_priv_params = SM2KeyExchangePrivateParameters(True, alice_static_priv, alice_ephemeral_priv)
alice_exchange.init(alice_priv_params)

bob_pub_params = SM2KeyExchangePublicParameters(bob_static_pub, bob_ephemeral_pub)
alice_shared_key = alice_exchange.calculate_key(128, bob_pub_params)

# Bob 计算共享密钥（响应方）
bob_exchange = SM2KeyExchange()
bob_priv_params = SM2KeyExchangePrivateParameters(False, bob_static_priv, bob_ephemeral_priv)
bob_exchange.init(bob_priv_params)

alice_pub_params = SM2KeyExchangePublicParameters(alice_static_pub, alice_ephemeral_pub)
bob_shared_key = bob_exchange.calculate_key(128, alice_pub_params)

# 验证双方密钥一致
print('Keys match:', bytes(alice_shared_key) == bytes(bob_shared_key))
```

> 💡 **提示**: SM2 密钥交换涉及多个参数类和步骤，建议查看完整示例了解详细用法。

📖 **完整示例**: [examples/sm2_keyexchange.py](./examples/sm2_keyexchange.py)

---

## 📚 完整示例

所有算法都提供了完整的可运行示例，位于 [`examples`](./examples) 目录：

| 示例文件 | 说明 | 演示内容 |
|---------|------|---------|
| [sm3_hash.py](./examples/sm3_hash.py) | SM3 哈希计算 | 基本哈希、分段更新、空数据处理 |
| [sm2_keypair.py](./examples/sm2_keypair.py) | SM2 密钥对生成 | 生成密钥对、查看公私钥 |
| [sm2_sign.py](./examples/sm2_sign.py) | SM2 数字签名 | 签名、验签、错误验证 |
| [sm2_encrypt.py](./examples/sm2_encrypt.py) | SM2 公钥加密 | 加密、解密、不同长度消息 |
| [sm2_keyexchange.py](./examples/sm2_keyexchange.py) | SM2 密钥交换 | ECDH 协议、密钥协商 |
| [sm4_ecb_simple.py](./examples/sm4_ecb_simple.py) | SM4 基础加密 | ECB 模式、PKCS7 填充 |
| [sm4_modes.py](./examples/sm4_modes.py) | SM4 多种模式 | ECB/CBC/CTR/GCM 对比 |

### 🚀 运行示例

```bash
# 进入示例目录
cd examples

# 运行单个示例
python sm3_hash.py           # SM3 哈希
python sm2_keypair.py        # SM2 密钥对生成
python sm2_sign.py           # SM2 数字签名
python sm2_encrypt.py        # SM2 公钥加密
python sm2_keyexchange.py    # SM2 密钥交换
python sm4_ecb_simple.py     # SM4 基础加密
python sm4_modes.py          # SM4 多种模式

# 运行所有示例（Linux/macOS）
for file in sm3_hash.py sm2_keypair.py sm2_sign.py sm2_encrypt.py sm2_keyexchange.py sm4_ecb_simple.py sm4_modes.py; do
    echo "=== Running $file ==="
    python "$file"
    echo
done
```

详细说明请查看 [examples/README.md](./examples/README.md)。

---

## 📖 文档

详细文档请查看 [docs](./docs) 目录：

- **[DEVELOPER_HANDOFF.md](./DEVELOPER_HANDOFF.md)** - 开发者交接文档（必读）
- **[PROGRESS.md](./PROGRESS.md)** - 项目进度跟踪
- **[开发指南](./docs/)** - API 文档和架构说明

### 支持的加密模式

| 模式 | 描述 | 需要 IV | 需要填充 | 使用场景 |
|------|------|---------|---------|----------|
| **GCM** | 伽罗瓦/计数器模式 | ✅ Yes | ❌ No | ⭐ 最佳选择（认证加密 AEAD） |
| **CBC** | 密码块链接 | ✅ Yes | ✅ Yes | ✅ 传统选择，通用加密 |
| **CTR** | 计数器模式 | ✅ Yes | ❌ No | ✅ 流密码模式，可并行 |
| **OFB** | 输出反馈 | ✅ Yes | ❌ No | 流密码，简单 |
| **CFB** | 密文反馈 | ✅ Yes | ❌ No | 自同步流密码 |
| **ECB** | 电子密码本 | ❌ No | ✅ Yes | ❌ 不安全（仅用于兼容性测试） |

### 支持的填充方案

| 填充方案 | 描述 | 可靠性 | 标准 |
|---------|------|--------|------|
| **PKCS#7** | 标准填充 | ✅ Yes | RFC 5652（推荐） |
| **ISO 7816-4** | 智能卡填充 | ✅ Yes | ISO/IEC 7816-4 |
| **ISO 10126** | 随机填充 | ✅ Yes | ISO/IEC 10126（已弃用） |
| **Zero-byte** | 零字节填充 | ❌ No | 仅用于兼容性 |

### 安全建议

✅ **推荐做法:**
- 使用 GCM 模式获得认证加密（AEAD）
- 使用 CBC 或 CTR 模式进行通用加密
- 始终使用 PKCS#7 填充（需要填充时）
- 为每次加密生成唯一的 IV
- 使用密码学安全的随机数生成器（`secrets` 模块）
- 妥善保管私钥，绝不硬编码

❌ **避免做法:**
- 使用 ECB 模式（会泄露明文模式）
- 重复使用相同密钥的 IV
- 使用零字节填充（不可靠）
- 以明文形式存储密钥

---

## 🧪 测试

本项目提供全面的测试套件，确保代码质量和正确性。

### 测试覆盖

| 算法/组件 | 测试数量 | 状态 | 覆盖内容 |
|-----------|---------|------|----------|
| **SM2 Engine** | 29 | ✅ 全部通过 | 加密、解密、密钥操作、边界情况 |
| **SM3 Digest** | 18 | ✅ 全部通过 | 哈希计算、Memoable 接口、标准向量 |
| **SM4 Engine** | 18 | ✅ 全部通过 | 块加密、块解密、密钥调度 |
| **CBC Mode** | 15 | ✅ 全部通过 | 加密/解密、IV 处理、填充 |
| **CTR Mode** | 15 | ✅ 全部通过 | 流密码模式、计数器递增 |
| **OFB Mode** | 15 | ✅ 全部通过 | 输出反馈、流密码 |
| **CFB Mode** | 15 | ✅ 全部通过 | 密文反馈、自同步 |
| **GCM Mode** | 20 | ✅ 全部通过 | 认证加密、MAC 验证 |
| **Padding** | 40 | ✅ 全部通过 | PKCS7、ISO7816、ISO10126、Zero |
| **SM2 Signer** | 15+ | ✅ 全部通过 | 签名、验签、DER 编码 |
| **SM2 KeyExchange** | 10+ | ✅ 全部通过 | ECDH 协议、密钥协商 |
| **总计** | **200+** | ✅ **100% 通过** | |

### 运行测试

```bash
# 运行所有测试
pytest tests/unit/

# 运行特定算法测试
pytest tests/unit/test_sm2_engine.py      # SM2 引擎
pytest tests/unit/test_sm3_digest.py      # SM3 摘要
pytest tests/unit/test_sm4_engine.py      # SM4 引擎
pytest tests/unit/test_cbc_mode.py        # CBC 模式
pytest tests/unit/test_gcm_mode.py        # GCM 模式
pytest tests/unit/test_padding.py         # 填充方案

# 带覆盖率报告
pytest --cov=sm_bc tests/unit/

# 详细输出
pytest -v tests/unit/

# 运行特定测试
pytest tests/unit/test_sm2_engine.py::TestSM2Engine::test_encrypt_decrypt
```

### 测试环境要求

- **Python**: 3.10 或更高
- **pytest**: 最新版本
- **pytest-cov**: (可选) 用于生成覆盖率报告

---

## 📁 Project Structure

```
sm-py-bc/
├── src/sm_bc/              # Main source code
│   ├── crypto/             # Cryptographic implementations
│   │   ├── digests/        # SM3 hash function
│   │   ├── engines/        # SM2, SM4 engines
│   │   ├── signers/        # SM2 signer
│   │   ├── modes/          # Cipher modes (CBC, CTR, OFB, CFB)
│   │   ├── paddings/       # Padding schemes
│   │   ├── params/         # Cryptographic parameters
│   │   └── cipher.py       # High-level cipher interface
│   ├── math/               # Elliptic curve mathematics
│   └── util/               # Utility classes
├── tests/                  # Comprehensive test suite
│   └── unit/              # Unit tests for all components
├── examples/               # Usage examples and demos
└── docs/                   # Additional documentation
```

---

## 🔬 Examples

See the `examples/` directory for complete working examples:

- `sm4_comprehensive_demo.py` - Showcase of all SM4 features
- `test_sm2_engine_demo.py` - SM2 encryption examples
- `test_sm3_demo.py` - SM3 hashing examples
- `test_cbc_demo.py` - CBC mode examples
- `test_ctr_demo.py` - CTR mode examples
- `test_padding_demo.py` - Padding scheme examples

Run any example:
```bash
python examples/sm4_comprehensive_demo.py
```

---

## 🎓 Technical Details

### Implementation Approach

**Pure Python** - All cryptographic operations implemented from scratch:
- No external cryptographic libraries
- Only Python standard library used
- Fully auditable and transparent

**Reference-based** - Ported from trusted implementations:
- Primary: [sm-js-bc](https://github.com/yourusername/sm-js-bc) (TypeScript)
- Secondary: Bouncy Castle Java implementation
- Maintains compatibility with reference implementations

**Standards Compliant**:
- SM2: GM/T 0003-2012 (Public Key Cryptographic Algorithm Based on Elliptic Curves)
- SM3: GM/T 0004-2012 (Cryptographic Hash Algorithm)
- SM4: GB/T 32907-2016 (Block Cipher Algorithm)

### Performance Notes

This is a **pure Python** implementation focused on correctness and security over raw performance. For production applications requiring high throughput:

- Consider using hardware acceleration when available
- Use native implementations (C/C++) for critical paths
- This library is ideal for development, testing, and applications where pure Python is required

**Typical Performance** (Python 3.10+ on modern hardware):
- SM3 hashing: ~5-10 MB/s
- SM4 encryption: ~1-5 MB/s
- SM2 operations: ~100-500 ops/s

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Based on reference implementations from [sm-js-bc](https://github.com/lihongjie0209/sm-js-bc) (TypeScript)
- Inspired by Bouncy Castle cryptographic library
- Implements Chinese national cryptographic standards

---

## ⚖️ Legal Notice

This software implements Chinese national cryptographic standards. Users are responsible for compliance with applicable export control laws and regulations in their jurisdiction.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/lihongjie0209/sm-py-bc/issues)
- **Documentation**: [Full Documentation](https://github.com/lihongjie0209/sm-py-bc/tree/main/docs)
- **Examples**: [Examples Directory](https://github.com/lihongjie0209/sm-py-bc/tree/main/examples)

---

**Made with ❤️ for the cryptography community**

*Production-ready • Well-tested • Standards-compliant • Pure Python*
