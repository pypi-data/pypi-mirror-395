[根目录](../../../CLAUDE.md) > [src](../../) > [mcpstore](../) > **adapters**

# 适配器模块文档

## 模块职责

适配器模块是 MCPStore 与各大 AI 框架之间的桥梁，负责：

- **格式转换**: 将 MCP 工具定义转换为各框架原生格式
- **参数处理**: 智能参数映射和类型转换
- **错误处理**: 统一的错误处理和异常转换
- **懒加载**: 按需加载适配器，减少依赖
- **兼容性**: 确保与各框架版本的兼容性

## 入口与启动

### 适配器懒加载机制

**包入口懒加载** (`../__init__.py:82-100`):
```python
def __getattr__(name: str):
    """懒加载公共对象以减少导入开销"""

    # 适配器类映射
    adapters_mapping = {
        "LangChainAdapter": "langchain_adapter",
        "OpenAIAdapter": "openai_adapter",
        "AutoGenAdapter": "autogen_adapter",
        "LlamaIndexAdapter": "llamaindex_adapter",
        "CrewAIAdapter": "crewai_adapter",
        "SemanticKernelAdapter": "semantic_kernel_adapter",
    }

    if name in adapters_mapping:
        module_name = adapters_mapping[name]
        try:
            module = __import__(f"mcpstore.adapters.{module_name}", fromlist=[name])
            adapter_class = getattr(module, name)
        except ImportError:
            adapter_class = None  # 如果未安装依赖，返回 None

        globals()[name] = adapter_class
        return adapter_class
```

### 上下文集成接口

**MCPStoreContext 适配器方法** (`../core/context/base_context.py`):
```python
class MCPStoreContext:
    def for_langchain(self, response_format: str = "text"):
        """获取 LangChain 适配器"""
        from ..adapters.langchain_adapter import LangChainAdapter
        return LangChainAdapter(self, response_format)

    def for_openai(self):
        """获取 OpenAI 适配器"""
        from ..adapters.openai_adapter import OpenAIAdapter
        return OpenAIAdapter(self)

    def for_autogen(self):
        """获取 AutoGen 适配器"""
        from ..adapters.autogen_adapter import AutoGenAdapter
        return AutoGenAdapter(self)

    def for_llamaindex(self):
        """获取 LlamaIndex 适配器"""
        from ..adapters.llamaindex_adapter import LlamaIndexAdapter
        return LlamaIndexAdapter(self)

    def for_crewai(self):
        """获取 CrewAI 适配器"""
        from ..adapters.crewai_adapter import CrewAIAdapter
        return CrewAIAdapter(self)

    def for_semantic_kernel(self):
        """获取 Semantic Kernel 适配器"""
        from ..adapters.semantic_kernel_adapter import SemanticKernelAdapter
        return SemanticKernelAdapter(self)
```

## 对外接口

### LangChain 适配器

**智能适配器** (`langchain_adapter.py`):
```python
class LangChainAdapter:
    def __init__(self, context: 'MCPStoreContext', response_format: str = "text"):
        self._context = context
        self._response_format = response_format  # "text" 或 "content_and_artifact"

    def list_tools(self) -> List[StructuredTool]:
        """返回与 LangChain 兼容的工具列表"""
        tools = self._context.list_tools()
        langchain_tools = []

        for tool in tools:
            # 前端防御：增强工具描述
            enhanced_description = self._enhance_tool_description(tool)

            # 创建 StructuredTool
            langchain_tool = StructuredTool.from_function(
                func=lambda **kwargs: self._safe_tool_call(tool.name, kwargs),
                name=tool.display_name or tool.name,
                description=enhanced_description,
                args_schema=self._create_pydantic_model(tool)
            )
            langchain_tools.append(langchain_tool)

        return langchain_tools

    def _safe_tool_call(self, tool_name: str, parameters: dict):
        """后端守护：安全的工具调用"""
        try:
            result = self._context.call_tool(tool_name, parameters)

            if self._response_format == "content_and_artifact":
                # 返回文本和工件
                return self._format_content_and_artifact(result)
            else:
                return result.content or str(result)

        except Exception as e:
            # 统一错误处理
            raise ToolException(f"Tool {tool_name} failed: {str(e)}")
```

**使用示例**:
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
store.for_store().add_service({"name": "calculator", "url": "https://api.calc.com/mcp"})

# 获取 LangChain 工具
tools = store.for_store().for_langchain().list_tools()

# 带工件支持的适配器
adapter = store.for_store().for_langchain(response_format="content_and_artifact")
tools = adapter.list_tools()
```

### OpenAI 适配器

**函数调用适配器** (`openai_adapter.py`):
```python
class OpenAIAdapter:
    def list_tools(self) -> List[dict]:
        """返回 OpenAI 函数调用格式的工具定义"""
        tools = self._context.list_tools()
        openai_tools = []

        for tool in tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool.display_name or tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema
                }
            }
            openai_tools.append(openai_tool)

        return openai_tools

    def format_response(self, tool_call_result):
        """格式化工具调用结果为 OpenAI 格式"""
        return {
            "role": "tool",
            "content": str(tool_call_result.content),
            "tool_call_id": tool_call_result.get("tool_call_id")
        }
```

### AutoGen 适配器

**AutoGen 函数适配器** (`autogen_adapter.py`):
```python
class AutoGenAdapter:
    def get_functions(self) -> List[dict]:
        """返回 AutoGen 兼容的函数定义"""
        tools = self._context.list_tools()
        functions = []

        for tool in tools:
            function_def = {
                "name": tool.display_name or tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": tool.input_schema.get("properties", {}),
                    "required": tool.input_schema.get("required", [])
                }
            }
            functions.append(function_def)

        return functions

    def execute_function(self, function_name: str, arguments: dict):
        """执行 AutoGen 函数调用"""
        return self._context.call_tool(function_name, arguments)
```

## 关键依赖与配置

### 可选依赖管理

**pyproject.toml 配置**:
```toml
[project.optional-dependencies]
# LangChain 集成
langchain = [
    "langchain>=0.1.0",
    "langchain-core>=0.1.0",
    "langchain-openai>=0.1.0"
]

# LlamaIndex 集成
llamaindex = ["llama-index>=0.10.0"]

# AutoGen 集成
autogen = ["autogen>=0.2.0"]

# Semantic Kernel 集成
semantic-kernel = ["semantic-kernel>=0.5.0"]

# 所有适配器
all = [
    "langchain>=0.1.0",
    "langchain-core>=0.1.0",
    "langchain-openai>=0.1.0",
    "llama-index>=0.10.0",
    "autogen>=0.2.0",
    "semantic-kernel>=0.5.0"
]
```

### 依赖检查机制

**适配器可用性检查**:
```python
# 在每个适配器中的依赖检查
try:
    import langchain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

def check_langchain_availability():
    """检查 LangChain 是否可用"""
    if not LANGCHAIN_AVAILABLE:
        raise ImportError(
            "LangChain adapter requires langchain to be installed. "
            "Install with: pip install mcpstore[langchain]"
        )
```

## 数据模型

### 适配器响应格式

**LangChain 格式**:
```python
# 返回 List[StructuredTool]
from langchain_core.tools import StructuredTool
from pydantic import BaseModel

tools = [
    StructuredTool.from_function(
        func=lambda **kwargs: tool_call_result,
        name="weather_get_current",
        description="获取当前天气信息",
        args_schema=WeatherInput  # Pydantic 模型
    )
]
```

**OpenAI 格式**:
```python
# 返回 OpenAI 函数调用格式
tools = [
    {
        "type": "function",
        "function": {
            "name": "weather_get_current",
            "description": "获取当前天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["city"]
            }
        }
    }
]
```

**AutoGen 格式**:
```python
# 返回 AutoGen 函数定义格式
functions = [
    {
        "name": "weather_get_current",
        "description": "获取当前天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"},
                "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    }
]
```

## 测试与质量

### 适配器测试策略

**单元测试结构**:
```python
# tests/adapters/test_langchain_adapter.py
import pytest
from mcpstore.adapters.langchain_adapter import LangChainAdapter

class TestLangChainAdapter:
    @pytest.fixture
    def mock_context(self):
        """模拟上下文对象"""
        # 创建模拟的 MCPStoreContext

    @pytest.fixture
    def adapter(self, mock_context):
        return LangChainAdapter(mock_context)

    def test_list_tools_returns_structured_tools(self, adapter):
        """测试返回 LangChain StructuredTool 列表"""
        tools = adapter.list_tools()
        assert all(isinstance(tool, StructuredTool) for tool in tools)

    def test_tool_enhancement(self, adapter):
        """测试工具描述增强"""
        # 测试前端防御机制

    def test_safe_tool_call(self, adapter):
        """测试安全工具调用"""
        # 测试后端守护机制

    def test_error_handling(self, adapter):
        """测试错误处理"""
        # 测试 ToolException 转换
```

### 集成测试

**框架集成测试**:
```python
# tests/integration/test_langchain_integration.py
def test_langchain_agent_integration():
    """测试与 LangChain Agent 的集成"""
    from mcpstore import MCPStore
    from langchain.agents import create_tool_calling_agent, AgentExecutor
    from langchain_openai import ChatOpenAI

    store = MCPStore.setup_store()
    store.for_store().add_service({"name": "test", "url": "https://test.com/mcp"})

    # 获取 LangChain 工具
    tools = store.for_store().for_langchain().list_tools()

    # 创建 Agent
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    # 测试工具调用
    response = agent_executor.invoke({"input": "调用测试工具"})
    assert response is not None
```

## 常见问题 (FAQ)

### Q: 如何添加新的框架适配器？

**A**: 创建新适配器并注册到上下文：

```python
# 1. 创建适配器 src/mcpstore/adapters/new_framework_adapter.py
class NewFrameworkAdapter:
    def __init__(self, context: 'MCPStoreContext'):
        self._context = context

    def list_tools(self):
        """转换工具为新框架格式"""
        tools = self._context.list_tools()
        converted_tools = []

        for tool in tools:
            # 转换逻辑
            converted_tool = self._convert_tool(tool)
            converted_tools.append(converted_tool)

        return converted_tools

    def _convert_tool(self, tool):
        """工具格式转换逻辑"""
        pass

# 2. 在上下文中添加方法
# src/mcpstore/core/context/base_context.py
def for_new_framework(self):
    """获取新框架适配器"""
    from ..adapters.new_framework_adapter import NewFrameworkAdapter
    return NewFrameworkAdapter(self)

# 3. 更新包导出
# src/mcpstore/__init__.py
adapters_mapping = {
    # ... 现有适配器
    "NewFrameworkAdapter": "new_framework_adapter",
}
```

### Q: 如何处理适配器兼容性问题？

**A**: 使用版本检查和适配器模式：

```python
# 适配器版本检查
def check_framework_compatibility():
    """检查框架兼容性"""
    try:
        import framework
        version = framework.__version__
        if version < REQUIRED_VERSION:
            raise ImportError(f"Framework version {version} not supported")
        return True
    except ImportError:
        return False

# 适配器模式处理版本差异
class VersionAwareAdapter:
    def __init__(self, context):
        self.context = context
        self.framework_version = self._detect_version()

    def _detect_version(self):
        """检测框架版本"""
        try:
            import framework
            return framework.__version__
        except ImportError:
            return None

    def list_tools(self):
        """根据版本调用不同实现"""
        if self.framework_version and self.framework_version >= "2.0.0":
            return self._list_tools_v2()
        else:
            return self._list_tools_v1()
```

### Q: 如何优化适配器性能？

**A**: 性能优化策略：

```python
# 1. 缓存转换结果
class CachedAdapter:
    def __init__(self, context):
        self.context = context
        self._tool_cache = {}
        self._cache_version = 0

    def list_tools(self):
        current_version = self._get_tools_version()

        if (self._cache_version != current_version or
            not self._tool_cache):

            tools = self.context.list_tools()
            self._tool_cache = [self._convert_tool(tool) for tool in tools]
            self._cache_version = current_version

        return self._tool_cache

# 2. 批量转换
def batch_convert_tools(self, tools):
    """批量转换工具以提高性能"""
    return [self._convert_tool(tool) for tool in tools]

# 3. 懒加载大型依赖
def lazy_import_heavy_dependency(self):
    """懒加载重型依赖"""
    if not hasattr(self, '_heavy_module'):
        import heavy_dependency
        self._heavy_module = heavy_dependency
    return self._heavy_module
```

### Q: 如何调试适配器问题？

**A**: 调试技巧：

```python
# 1. 启用详细日志
import logging
logging.getLogger("mcpstore.adapters").setLevel(logging.DEBUG)

# 2. 添加调试信息
class DebugAdapter:
    def list_tools(self):
        tools = self.context.list_tools()
        logging.debug(f"Found {len(tools)} tools to convert")

        for i, tool in enumerate(tools):
            logging.debug(f"Converting tool {i}: {tool.name}")
            converted = self._convert_tool(tool)
            logging.debug(f"Converted tool {i}: {converted}")

        return converted_tools

# 3. 验证转换结果
def validate_conversion(self, original_tool, converted_tool):
    """验证转换结果"""
    assert converted_tool.name == original_tool.name
    assert converted_tool.description == original_tool.description
    # 其他验证逻辑
```

## 相关文件清单

### 核心适配器
- `langchain_adapter.py` - LangChain/LangGraph 适配器
- `openai_adapter.py` - OpenAI 函数调用适配器
- `autogen_adapter.py` - AutoGen 适配器
- `llamaindex_adapter.py` - LlamaIndex 适配器
- `crewai_adapter.py` - CrewAI 适配器
- `semantic_kernel_adapter.py` - Semantic Kernel 适配器

### 工具和辅助文件
- `__init__.py` - 适配器包初始化
- `utils.py` - 适配器工具函数
- `exceptions.py` - 适配器专用异常
- `base_adapter.py` - 适配器基类（如果存在）

### 测试文件
- `tests/adapters/test_langchain_adapter.py` - LangChain 适配器测试
- `tests/adapters/test_openai_adapter.py` - OpenAI 适配器测试
- `tests/adapters/test_autogen_adapter.py` - AutoGen 适配器测试
- `tests/integration/test_framework_adapters.py` - 框架集成测试

## 变更记录 (Changelog)

### 2025-11-24
- 创建初始适配器模块文档
- 分析现有适配器架构
- 记录懒加载机制
- 整理各框架适配器接口
- 记录依赖管理和兼容性策略