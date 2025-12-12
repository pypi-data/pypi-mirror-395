# 测试说明

## 运行测试

### 安装测试依赖

```bash
pip install pytest pytest-asyncio
```

### 运行所有测试

```bash
pytest test/
```

### 运行特定测试文件

```bash
pytest test/test_studies_api.py
```

### 运行特定测试用例

```bash
pytest test/test_studies_api.py::TestGetAllStudiesAndSeries::test_get_all_studies_and_series_success
```

### 显示详细输出

```bash
pytest test/ -v
```

### 显示覆盖率

```bash
pip install pytest-cov
pytest test/ --cov=src/api/studies_api --cov-report=html
```

## 测试内容

`test_studies_api.py` 包含以下测试用例：

1. **test_get_all_studies_and_series_success** - 测试成功获取所有病例和序列信息
2. **test_get_all_studies_and_series_missing_config** - 测试配置缺失时的错误处理
3. **test_get_all_studies_and_series_with_search** - 测试带搜索字符串的查询
4. **test_get_all_studies_and_series_pagination** - 测试分页功能
5. **test_get_series_by_study_instance_uid_success** - 测试根据 StudyInstanceUID 获取序列信息
6. **test_get_series_by_study_instance_uid_api_error** - 测试 API 错误处理
7. **test_get_series_by_study_instance_uid_request_exception** - 测试网络异常处理

## 环境变量配置

### 方式一：使用 .env 文件（推荐）

在项目根目录创建 `.env` 文件：

```env
base_url=http://192.168.4.220:26666
name=mozzie
password=!Az123
tel=18061205553
```

### 方式二：使用环境变量

```bash
export base_url="http://192.168.4.220:26666"
export name="mozzie"
export password="!Az123"
export tel="18061205553"
```

### 方式三：在 MCP 客户端配置中设置

```json
{
  "mcpServers": {
    "dicom-tools-python": {
      "command": "uvx",
      "args": ["dicomtoolsformcp"],
      "env": {
        "base_url": "http://192.168.4.220:26666",
        "name": "mozzie",
        "password": "!Az123",
        "tel": "18061205553"
      }
    }
  }
}
```

## 集成测试

运行集成测试（会实际调用 API）：

```bash
# 设置环境变量后运行
pytest test/test_integration.py -v -m integration
```

## 注意事项

- **单元测试** (`test_studies_api.py`) 使用 mock，不会实际调用 API
- **集成测试** (`test_integration.py`) 会实际调用 API，需要配置正确的环境变量
- 测试使用 pytest 和 pytest-asyncio 来支持异步函数测试
- 集成测试默认跳过，除非设置了必要的环境变量

