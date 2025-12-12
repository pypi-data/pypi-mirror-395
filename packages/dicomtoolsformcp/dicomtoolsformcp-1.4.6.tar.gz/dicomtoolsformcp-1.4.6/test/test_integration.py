"""
集成测试 - 需要真实环境变量配置
注意：这些测试会实际调用 API，需要配置正确的环境变量
"""
import pytest
import os
import asyncio
from src.api.studies_api import get_all_studies_and_series


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_all_studies_and_series_integration():
    """
    集成测试：实际调用 API 获取所有病例和序列信息
    
    运行前需要设置环境变量：
    - base_url
    - name
    - password
    - tel (可选)
    """
    # 检查必要的环境变量
    base_url = os.getenv("base_url")
    name = os.getenv("name")
    password = os.getenv("password")
    
    if not all([base_url, name, password]):
        pytest.skip("缺少必要的环境变量，跳过集成测试")
    
    # 执行测试
    result = await get_all_studies_and_series()
    
    # 验证结果
    assert result is not None
    assert "content" in result
    assert len(result["content"]) > 0
    
    import json
    result_text = result["content"][0]["text"]
    result_data = json.loads(result_text)
    
    # 检查是否有错误
    if result_data.get("error"):
        pytest.fail(f"API 调用失败: {result_data.get('message')}")
    
    assert result_data.get("success") is True
    assert "total_studies" in result_data
    assert "studies" in result_data
    
    print(f"\n成功获取 {result_data['total_studies']} 个病例")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_all_studies_and_series_with_search_integration():
    """
    集成测试：使用搜索字符串查询病例
    
    运行前需要设置环境变量
    """
    base_url = os.getenv("base_url")
    name = os.getenv("name")
    password = os.getenv("password")
    
    if not all([base_url, name, password]):
        pytest.skip("缺少必要的环境变量，跳过集成测试")
    
    # 执行测试（使用搜索字符串）
    result = await get_all_studies_and_series(search_str="test")
    
    # 验证结果
    assert result is not None
    assert "content" in result
    
    import json
    result_text = result["content"][0]["text"]
    result_data = json.loads(result_text)
    
    if result_data.get("error"):
        pytest.fail(f"API 调用失败: {result_data.get('message')}")
    
    assert result_data.get("success") is True
    print(f"\n搜索 'test' 找到 {result_data['total_studies']} 个病例")


if __name__ == "__main__":
    # 设置环境变量（仅用于测试）
    os.environ["base_url"] = "http://192.168.4.220:26666"
    os.environ["name"] = "mozzie"
    os.environ["password"] = "!Az123"
    os.environ["tel"] = "18061205553"
    
    # 运行测试
    pytest.main([__file__, "-v", "-m", "integration"])

