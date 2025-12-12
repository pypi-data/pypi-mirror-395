# SM2/SM3/SM4 Python 实现指南

## 项目概述
本项目旨在基于 `sm-js-bc` (TypeScript) 和 `bc-java` (Java) 的实现，开发一个纯 Python 版本的国密算法库（SM2, SM3, SM4）。

## 核心要求
1.  **参考实现**：
    - 主要参考：`../sm-js-bc` (TypeScript 实现)
    - 次要参考：`bc-java` (Bouncy Castle Java 实现)
    - 逻辑应与参考实现保持高度一致，以确保跨语言兼容性。

2.  **技术栈**：
    - 语言：Python 3.10+
    - 类型系统：严格使用 Type Hints (typing模块)
    - 测试框架：`pytest`

3.  **零依赖原则**：
    - 不依赖任何第三方密码学库（如 `cryptography`, `pycryptodome` 等）。
    - 所有算法逻辑必须原生实现。
    - 仅允许使用 Python 标准库。
    - 开发/测试依赖允许使用 `pytest` 等工具。

4.  **代码风格**：
    - 遵循 PEP 8 规范。
    - 命名规范：
        - 类名：`PascalCase` (如 `SM3Digest`)
        - 方法/函数名：`snake_case` (如 `get_digest_size`) —— **注意**：为了保持与 BC 结构的一致性，对于核心算法类的公共 API，如果参考实现使用了特定的命名逻辑，在不违反 Python 严重习惯的前提下，尽量保持语义一致。但在 Python 中，通常强烈建议使用 `snake_case`。我们将采用 **Pythonic** 的命名方式（snake_case），但在文档或注释中需注明对应 Java/TS 的方法名，以便对照。
    - 必须包含详细的 Docstring，说明参数类型、返回值和对应 Java/TS 实现的逻辑。

5.  **开发流程**：
    - **测试驱动 (TDD)**：在实现功能前，先移植 `sm-js-bc` 中的测试用例。
    - **文档记录**：每个模块实现后，需更新对应文档。

## 目录结构映射

```
sm-py-bc/
├── src/
│   └── sm_bc/
│       ├── crypto/
│       │   ├── digests/      # SM3Digest 等
│       │   ├── engines/      # SM2Engine, SM4Engine 等
│       │   ├── signers/      # SM2Signer 等
│       │   └── ...
│       ├── math/             # 椭圆曲线数学运算
│       └── util/             # Pack, Arrays 等工具类
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
└── pyproject.toml
```

## 验证标准
- 所有单元测试必须通过。
- 输出结果必须与 `sm-js-bc` 的测试向量完全一致。
