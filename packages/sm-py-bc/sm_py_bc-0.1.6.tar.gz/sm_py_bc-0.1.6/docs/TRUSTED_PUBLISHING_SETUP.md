# Trusted Publishing 配置指南

## 📋 配置状态

**当前状态**: ⚠️ 等待在 PyPI 上配置 Trusted Publisher

**Workflow 状态**: ✅ 已配置完成  
**GitHub 配置**: ✅ 已就绪  
**PyPI 配置**: ❌ 需要手动配置

---

## 🔍 问题诊断

### 错误信息
```
Trusted publishing exchange failure:
Token request failed: the server refused the request for the following reasons:
* `invalid-publisher`: valid token, but no corresponding publisher 
  (Publisher with matching claims was not found)
```

### 原因
PyPI 上还没有为 `sm-py-bc` 配置 Trusted Publisher。

---

## ✅ 配置步骤

### 步骤 1: 登录 PyPI

访问: https://pypi.org/account/login/

### 步骤 2: 进入项目设置

访问 Publishing 设置页面:
https://pypi.org/manage/project/sm-py-bc/settings/publishing/

### 步骤 3: 添加 Trusted Publisher

点击 **"Add a new pending publisher"** 或 **"Add a new publisher"**

填写以下信息:

| 字段 | 值 |
|------|-----|
| **PyPI Project Name** | `sm-py-bc` |
| **Owner** | `lihongjie0209` |
| **Repository name** | `sm-py-bc` |
| **Workflow name** | `publish.yml` |
| **Environment name** | (留空或填 `release`) |

**重要**: 
- Owner 必须是 GitHub 用户名: `lihongjie0209`
- Repository 必须是仓库名: `sm-py-bc`
- Workflow 必须是文件名: `publish.yml`

### 步骤 4: 保存配置

点击 **"Add"** 按钮保存。

---

## 🧪 测试自动发布

配置完成后，测试流程:

### 方法 A: 创建新 tag (推荐)

```bash
# 升级版本号
# 编辑 pyproject.toml 和 src/sm_bc/__init__.py

# 提交版本更新
git add .
git commit -m "chore: bump version to v0.1.3"
git push

# 创建并推送 tag
git tag -a v0.1.3 -m "Release v0.1.3"
git push origin v0.1.3
```

### 方法 B: 手动触发 workflow

```bash
gh workflow run publish.yml -f repository=pypi
```

### 方法 C: 创建 GitHub Release

通过 GitHub UI 或 CLI 创建 Release，会自动触发发布。

---

## 📊 验证发布

### 1. 检查 GitHub Actions

访问: https://github.com/lihongjie0209/sm-py-bc/actions

查看最新的 "Publish to PyPI" workflow run:
- ✅ Status: completed
- ✅ Result: success

### 2. 检查 PyPI

访问: https://pypi.org/project/sm-py-bc/

确认新版本已发布。

### 3. 测试安装

```bash
pip install --upgrade sm-py-bc
python -c "import sm_bc; print(sm_bc.__version__)"
```

---

## 🔐 Trusted Publishing 的优势

### 安全性
- ✅ 无需管理 API tokens
- ✅ 使用 OpenID Connect (OIDC) 认证
- ✅ 自动轮换凭证
- ✅ 减少凭证泄露风险

### 便利性
- ✅ 自动认证
- ✅ 无需配置 secrets
- ✅ GitHub 官方支持
- ✅ PyPI 官方推荐

### 可维护性
- ✅ 无过期时间
- ✅ 无需手动更新
- ✅ 配置一次，永久有效
- ✅ 更少的维护工作

---

## ❓ 常见问题

### Q1: 为什么会出现 "invalid-publisher" 错误？

**A**: PyPI 上还没有配置 Trusted Publisher。需要先在 PyPI 项目设置中添加。

### Q2: Environment name 应该填什么？

**A**: 可以留空，或者填 `release`。如果留空，任何触发 workflow 的 tag/release 都会发布。

### Q3: 如何知道配置是否正确？

**A**: 推送一个测试 tag，查看 GitHub Actions 的日志。如果成功，会显示 "Successfully published to PyPI"。

### Q4: 可以同时使用 token 和 Trusted Publishing 吗？

**A**: 可以，但不推荐。建议完全迁移到 Trusted Publishing。

### Q5: 如果配置错误怎么办？

**A**: 在 PyPI 项目设置中删除错误的 publisher，重新添加正确的配置。

---

## 📚 参考文档

- **PyPI Trusted Publishing Guide**: https://docs.pypi.org/trusted-publishers/
- **GitHub OIDC**: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- **pypa/gh-action-pypi-publish**: https://github.com/pypa/gh-action-pypi-publish

---

## 🔄 回退到 Token 方式

如果 Trusted Publishing 遇到问题，可以回退到 token 方式:

### 步骤 1: 修改 workflow

将 `.github/workflows/publish.yml` 中的发布步骤改回:

```yaml
- name: Publish to PyPI
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
  run: |
    twine upload dist/*
```

### 步骤 2: 移除 id-token 权限

```yaml
permissions:
  contents: read  # 移除 id-token: write
```

---

## ✅ 配置完成后的工作流

配置 Trusted Publishing 后，发布流程变得非常简单:

```bash
# 1. 更新代码
git commit -am "feat: add new feature"
git push

# 2. 更新版本
# 编辑 pyproject.toml 和 __init__.py
git commit -am "chore: bump version to v0.x.x"
git push

# 3. 创建 tag
git tag -a v0.x.x -m "Release v0.x.x"
git push origin v0.x.x

# 4. 等待自动发布完成 (约 1-2 分钟)
# 5. 完成! 🎉
```

---

## 📞 获取帮助

如果遇到问题:

1. **检查 PyPI 配置**: https://pypi.org/manage/project/sm-py-bc/settings/publishing/
2. **查看 Actions 日志**: https://github.com/lihongjie0209/sm-py-bc/actions
3. **提交 Issue**: https://github.com/lihongjie0209/sm-py-bc/issues

---

**最后更新**: 2025-12-06  
**Workflow 文件**: `.github/workflows/publish.yml`  
**状态**: ⏳ 等待 PyPI 配置
