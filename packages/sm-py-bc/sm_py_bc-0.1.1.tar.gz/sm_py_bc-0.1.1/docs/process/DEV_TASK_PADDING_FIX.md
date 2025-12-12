# 🔧 开发任务：修复填充方案实现

**优先级**: P1 (高)  
**预计时间**: 2-3 小时  
**状态**: 🔴 待修复

---

## 快速概览

**问题**: Python `bytes` 对象不可变，导致填充方案无法修改数据  
**影响**: 15/21 填充测试失败  
**解决方案**: 将 `bytes` 转换为 `bytearray` 进行就地修改

---

## 需要修复的 4 个文件

### ✅ 修复清单

- [ ] `src/sm_bc/crypto/paddings/pkcs7_padding.py`
- [ ] `src/sm_bc/crypto/paddings/iso7816_4_padding.py`
- [ ] `src/sm_bc/crypto/paddings/iso10126_padding.py`
- [ ] `src/sm_bc/crypto/paddings/zero_byte_padding.py`

---

## 🔨 修复模板

### 修复前（错误）

```python
def add_padding(self, input: bytes, in_off: int, in_len: int) -> int:
    input[in_off] = 0x80  # ❌ TypeError: bytes 不可变
```

### 修复后（正确）

```python
from typing import Union

def add_padding(
    self, 
    input: Union[bytes, bytearray], 
    in_off: int, 
    in_len: int
) -> Union[bytes, bytearray]:
    """添加填充到输入数据。"""
    # 转换为可变类型
    if isinstance(input, bytes):
        input = bytearray(input)
    
    # 现在可以安全修改
    input[in_off] = 0x80  # ✅ OK
    
    return input
```

---

## 🧪 测试验证

```bash
# 运行填充测试
cd D:\code\sm-bc\sm-py-bc
python -m pytest tests/unit/test_padding_schemes.py -v

# 预期结果: 21 passed (当前: 15 failed, 6 passed)
```

---

## 📋 详细步骤

### 1. PKCS7Padding

**文件**: `src/sm_bc/crypto/paddings/pkcs7_padding.py`

**修改点**:
```python
# 添加导入
from typing import Union

# 修改 add_padding 方法
def add_padding(
    self, 
    input: Union[bytes, bytearray], 
    in_off: int, 
    in_len: int
) -> Union[bytes, bytearray]:
    if isinstance(input, bytes):
        input = bytearray(input)
    
    code = self.block_size - (in_len % self.block_size)
    while in_off < len(input):
        input[in_off] = code
        in_off += 1
    
    return input
```

### 2. ISO7816-4Padding

**文件**: `src/sm_bc/crypto/paddings/iso7816_4_padding.py`

**修改点**:
```python
from typing import Union

def add_padding(
    self, 
    input: Union[bytes, bytearray], 
    in_off: int, 
    in_len: int
) -> Union[bytes, bytearray]:
    if isinstance(input, bytes):
        input = bytearray(input)
    
    input[in_off] = 0x80
    in_off += 1
    
    while in_off < len(input):
        input[in_off] = 0x00
        in_off += 1
    
    return input
```

### 3. ISO10126Padding

**文件**: `src/sm_bc/crypto/paddings/iso10126_padding.py`

**修改点**:
```python
from typing import Union
import secrets

def add_padding(
    self, 
    input: Union[bytes, bytearray], 
    in_off: int, 
    in_len: int
) -> Union[bytes, bytearray]:
    if isinstance(input, bytes):
        input = bytearray(input)
    
    code = self.block_size - (in_len % self.block_size)
    
    # 随机字节（除了最后一个）
    while in_off < len(input) - 1:
        input[in_off] = secrets.randbelow(256)
        in_off += 1
    
    # 最后一字节是填充长度
    input[in_off] = code
    
    return input
```

### 4. ZeroBytePadding

**文件**: `src/sm_bc/crypto/paddings/zero_byte_padding.py`

**修改点**:
```python
from typing import Union

def add_padding(
    self, 
    input: Union[bytes, bytearray], 
    in_off: int, 
    in_len: int
) -> Union[bytes, bytearray]:
    if isinstance(input, bytes):
        input = bytearray(input)
    
    while in_off < len(input):
        input[in_off] = 0x00
        in_off += 1
    
    return input
```

---

## ✅ 完成验证

修复后运行：

```bash
# 所有填充测试
python -m pytest tests/unit/test_padding_schemes.py -v

# 应该显示: 21 passed ✅

# 全部单元测试（确保无回归）
python -m pytest tests/unit/ -v
```

---

## 📝 注意事项

1. **保持向后兼容**: 接受 `bytes` 和 `bytearray`
2. **类型注解**: 使用 `Union[bytes, bytearray]`
3. **返回值**: 返回修改后的 `bytearray`（或原始 `bytes` 转换后的）
4. **文档**: 更新 docstring 说明类型转换

---

## 🎯 成功标准

- [x] 所有 21 个测试通过
- [x] 无新增错误或警告
- [x] 代码风格一致
- [x] 类型注解正确

---

## 📚 相关资源

- **详细文档**: `DEVELOPER_ISSUES_TO_FIX.md`
- **测试文件**: `tests/unit/test_padding_schemes.py`
- **进度追踪**: `TEST_ALIGNMENT_TRACKER.md`

---

**创建**: 2025-12-06  
**创建者**: Test Audit Agent  
**准备状态**: ✅ Ready

开始修复吧！🚀
