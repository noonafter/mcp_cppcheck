# MCP Cppcheck 插件需求文档

## 项目背景

开发一个 MCP (Model Context Protocol) 插件，对 cppcheck 静态分析工具进行智能封装，提供项目感知能力和输出优化，使其更适合 LLM 使用（符合Harness工程原则）。

---

## 核心目标

1. **智能化**：自动检测项目配置，提高工具针对性
2. **上下文感知**：识别项目类型，应用相应的检查策略
3. **输出优化**：清洗和过滤输出，控制信息量
4. **易用性**：通过 MCP 协议提供统一接口

---

## 功能需求

### 1. 预处理增强

#### 1.1 项目配置自动检测
- 向上查找项目根目录
- 检测 `compile_commands.json` 并自动使用
- 检测 `.cppcheck` 配置文件

#### 1.2 项目类型识别
- 判断目标是项目文件还是独立代码
- 根据项目类型应用不同策略，如果是项目根目录或者是项目文件，尝试搜索compile_commands.json，并启用--project；如果是普通目录或文件，尝试通过-I优化头文件搜索目录

### 2. MCP 工具接口

#### 2.1 check_code
**功能**：检查代码（支持文件或目录）

**参数**：
- `target_path` (string, 必需)：文件或目录路径
- `mode` (string, 可选)：检查模式
  - `"quick"`：快速检查（默认），只启用 warning
  - `"full"`：完整检查，启用所有检查项--enable=all

**行为**：
- 自动判断是文件还是目录
- 如果target_path是工程文件（），应用到--project，而不是源文件
- 自动检测并使用 `compile_commands.json`等工程文件
- 自动应用 cppcheck 配置文件
- 返回清洗后的 XML 格式结果

#### 2.2 check_with_config
**功能**：使用指定的 cppcheck 配置文件检查

**参数**：
- `target_path` (string, 必需)：文件或目录路径
- `config_file` (string, 必需)：cppcheck 配置文件路径

**行为**：
- 使用指定配置文件覆盖自动检测
- 返回清洗后的 XML 格式结果

#### 2.3 get_project_context
**功能**：获取项目环境信息（调试用）

**参数**：
- `target_path` (string, 必需)：文件或目录路径

**返回**：JSON 格式的项目信息
- `is_project_file`：是否是项目文件
- `project_root`：项目根目录
- `compile_commands`：compile_commands.json 路径
- `cppcheck_config`：.cppcheck 配置路径

### 3. 输出优化

#### 3.1 XML 格式清洗
- 保持 cppcheck 原生 XML 格式
- 移除 `verbose` 属性（冗余的详细说明）
- 移除 `column` 属性（列号信息）
- 保留字段：`id`, `severity`, `msg`, `file`, `line`

#### 3.2 输出示例
```xml
<?xml version="1.0" encoding="UTF-8"?>
<results version="2">
  <cppcheck version="2.20.0"/>
  <errors>
    <error id="missingIncludeSystem" severity="information" msg="Include file: <stdio.h> not found...">
      <location file="src/common/err.h" line="9"/>
    </error>
  </errors>
</results>
```

---

## 技术需求

### 1. 开发环境
- Python >= 3.10
- uv 包管理器
- cppcheck 工具（需预先安装）

### 2. 依赖库
- `mcp >= 1.0.0`：MCP SDK
- `pywin32 >= 306`：Windows 平台支持（仅 Windows）

### 3. MCP开发方式
- 使用FastMCP方式

---

## 非功能需求

### 1. 性能
- 不对 cppcheck 执行过程进行干预
- 只在输出阶段进行清洗，开销最小

### 2. 兼容性
- 支持 Windows、Linux、macOS
- 兼容 cppcheck 2.x 版本

### 3. 可维护性
- 模块化设计，职责分离
- 代码简洁，避免过度工程

### 4. 易用性
- 自动检测配置，零配置可用
- 提供配置示例和文档

---

## 设计决策

### 1. 为什么不区分项目和单文件？
cppcheck 本身支持文件和目录，统一处理更简单。通过项目检测自动应用配置即可。

### 2. 为什么输出 XML 而不是 JSON？
- 保持与 cppcheck 原生格式一致
- LLM 可以理解 XML
- 避免信息丢失

### 3. 为什么过滤功能未完全实现？
当前 XML 清洗已满足基本需求，过滤功能预留接口，可按需扩展。

### 4. 为什么使用FastMCP 而不是 底层 Server API？
- 针对业务逻辑，而不是协议层面的逻辑。
- 如果以后想做一个“中转服务器”，同时为几百个用户提供 Cppcheck 服务，并且需要处理复杂的令牌桶限流、用户身份隔离时，才需要切换到底层 API。

---

## 使用场景

1. **LLM 辅助代码审查**
   - LLM 调用 `check_code` 分析代码
   - 获取结构化的问题报告
   - 提供修复建议

2. **CI/CD 集成**
   - 通过 MCP 协议统一接口
   - 自动检测项目配置
   - 输出标准化报告

3. **IDE 集成**
   - 实时代码检查
   - 项目感知的智能提示
   - 过滤无关警告

---

## 未来优化项

### 1. 智能提取编译参数
当检查普通文件/目录时，如果找到 compile_commands.json，可以：
- 解析 JSON 提取 include paths (`-I` 参数)
- 提取预定义宏 (`-D` 参数)
- 提取编译标准 (`-std=c++17` 等)
- 应用到 cppcheck 命令，减少误报

**实现思路**：
```python
def _extract_compile_flags(compile_commands_path):
    # 解析 compile_commands.json
    # 提取 -I, -D, -std 等参数
    # 返回 include_paths, defines, std_version
```

### 2. 常见 include 目录智能检测
除了项目根目录，还可以自动添加：
- `{project_root}/include`
- `{project_root}/src`
- `{project_root}/lib`

### 3. 提供一些屏蔽常见误报的接口
比如关闭/去掉关于qt宏的报错
用户指定关闭一些特定类型的报错

