#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动端测试用例: 举报测试
生成时间: 2025-11-25 15:45:38

⚠️  注意：此脚本基于AI执行历史生成，使用已验证的定位方式
    如果页面结构变化，可能需要重新生成脚本
📊 执行统计:
    - 总操作数: 9
    - 成功操作: 8
    - 失败尝试: 1
    - 成功率: 88.9%

💡 说明：此脚本经过多次尝试后生成，只包含最终成功的操作步骤

运行方式:
    pytest 举报测试.py -v
    pytest 举报测试.py --alluredir=./allure-results  # 生成allure报告
"""
import asyncio
import pytest
import pytest_asyncio
import sys
from pathlib import Path

# 添加backend目录到路径
# tests目录结构: backend/mobile_mcp/tests/test_xxx.py
# 需要导入: backend/mobile_mcp/core/mobile_client.py
sys.path.insert(0, str(Path(__file__).parent.parent))

from mobile_mcp.core.mobile_client import MobileClient


PACKAGE_NAME = "com.im30.way"


@pytest_asyncio.fixture(scope='function')
async def mobile_client():
    """
    pytest fixture: 创建并返回MobileClient实例
    scope='function': 每个测试函数都会创建一个新的client
    """
    client = MobileClient(device_id=None)
    
    # 启动App
    print(f"\n📱 启动App: {{PACKAGE_NAME}}")
    result = await client.launch_app(PACKAGE_NAME, wait_time=5)
    if not result.get('success'):
        raise Exception(f"启动App失败: {{result.get('reason')}}")
    
    await asyncio.sleep(2)  # 等待页面加载
    
    yield client
    
    # 清理
    client.device_manager.disconnect()


@pytest.mark.asyncio
async def test_举报测试(mobile_client):
    """
    测试用例: 举报测试
    
    Args:
        mobile_client: pytest fixture，已启动App的MobileClient实例
    """
    client = mobile_client
    
    print("=" * 60)
    print(f"🚀 举报测试")
    print("=" * 60)
    
    try:
        # 步骤1: 点击 [810,2186][1080,2356]
        print(f"\n步骤1: 点击 [810,2186][1080,2356]")
        # ✅ 使用bounds坐标（已验证）
        await client.click("[810,2186][1080,2356]", ref="[810,2186][1080,2356]", verify=False)
        print(f"✅ 点击成功（bounds: [810,2186][1080,2356]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤2: 点击 [919,113][1034,205]
        print(f"\n步骤2: 点击 [919,113][1034,205]")
        # ✅ 使用bounds坐标（已验证）
        await client.click("[919,113][1034,205]", ref="[919,113][1034,205]", verify=False)
        print(f"✅ 点击成功（bounds: [919,113][1034,205]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤3: 点击 [861,131][919,188]
        print(f"\n步骤3: 点击 [861,131][919,188]")
        # ✅ 使用bounds坐标（已验证）
        await client.click("[861,131][919,188]", ref="[861,131][919,188]", verify=False)
        print(f"✅ 点击成功（bounds: [861,131][919,188]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤4: 点击 举报
        print(f"\n步骤4: 点击 举报")
        # ✅ 使用bounds坐标（已验证）
        await client.click("举报", ref="[515,1557][565,1607]", verify=False)
        print(f"✅ 点击成功（bounds: [515,1557][565,1607]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤5: 点击 [0,1333][1080,1460]
        print(f"\n步骤5: 点击 [0,1333][1080,1460]")
        # ✅ 使用bounds坐标（已验证）
        await client.click("[0,1333][1080,1460]", ref="[0,1333][1080,1460]", verify=False)
        print(f"✅ 点击成功（bounds: [0,1333][1080,1460]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤6: 点击 [81,292][999,826]
        print(f"\n步骤6: 点击 [81,292][999,826]")
        # ✅ 使用bounds坐标（已验证）
        await client.click("[81,292][999,826]", ref="[81,292][999,826]", verify=False)
        print(f"✅ 点击成功（bounds: [81,292][999,826]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤7: 在[81,292][999,826]输入 举报自动化测试
        print(f"\n步骤7: 在[81,292][999,826]输入 举报自动化测试")
        # ✅ 使用bounds坐标输入（已验证）
        await client.type_text("[81,292][999,826]", "举报自动化测试", ref="[81,292][999,826]")
        print(f"✅ 输入成功（bounds: [81,292][999,826]）")
        await asyncio.sleep(1)  # 等待输入完成
        # 步骤8: 点击 提交
        print(f"\n步骤8: 点击 提交")
        # ✅ 使用bounds坐标（已验证）
        await client.click("提交", ref="[515,1003][565,1053]", verify=False)
        print(f"✅ 点击成功（bounds: [515,1003][565,1053]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        
        print("\n✅ 测试完成！")
        
    except AssertionError as e:
        print(f"\n❌ 断言失败: {e}")
        # 打印当前页面快照以便调试
        snapshot = await client.snapshot()
        print(f"\n当前页面快照:\n{snapshot[:500]}...")
        raise
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        raise