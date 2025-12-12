#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动端测试用例: 切换语言到English
生成时间: 2025-11-24 16:42:21

⚠️  注意：此脚本基于AI执行历史生成，使用已验证的定位方式
    如果页面结构变化，可能需要重新生成脚本

运行方式:
    pytest 切换语言到English.py -v
    pytest 切换语言到English.py --alluredir=./allure-results  # 生成allure报告
"""
import asyncio
import pytest
import sys
from pathlib import Path

# 添加backend目录到路径
# tests目录结构: backend/mobile_mcp/tests/test_xxx.py
# 需要导入: backend/mobile_mcp/core/mobile_client.py
sys.path.insert(0, str(Path(__file__).parent.parent))

from mobile_mcp.core.mobile_client import MobileClient


PACKAGE_NAME = "com.im30.way"


@pytest.fixture(scope='function')
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
async def test_切换语言到english(mobile_client):
    """
    测试用例: 切换语言到English
    
    Args:
        mobile_client: pytest fixture，已启动App的MobileClient实例
    """
    client = mobile_client
    
    print("=" * 60)
    print(f"🚀 切换语言到English")
    print("=" * 60)
    
    try:
        # 步骤1: 点击 [810,2186][1080,2356]
        print(f"\n步骤1: 点击 [810,2186][1080,2356]")
        # ✅ 使用bounds坐标（已验证）
        await client.click("[810,2186][1080,2356]", ref="[810,2186][1080,2356]", verify=False)
        print(f"✅ 点击成功（bounds: [810,2186][1080,2356]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤2: 点击 右上角图标
        print(f"\n步骤2: 点击 右上角图标")
        # ✅ 使用bounds坐标（已验证）
        await client.click("右上角图标", ref="[861,131][919,188]", verify=False)
        print(f"✅ 点击成功（bounds: [861,131][919,188]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤3: 点击 设置
        print(f"\n步骤3: 点击 设置")
        # ✅ 使用text/description定位（已验证）
        await client.click("设置", ref="设置", verify=False)
        print(f"✅ 点击成功（text/desc: 设置）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤4: 点击 语言
        print(f"\n步骤4: 点击 语言")
        # ✅ 使用bounds坐标（已验证）
        await client.click("语言", ref="[515,1170][565,1220]", verify=False)
        print(f"✅ 点击成功（bounds: [515,1170][565,1220]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤5: 点击 语言
        print(f"\n步骤5: 点击 语言")
        # ✅ 使用bounds坐标（已验证）
        await client.click("语言", ref="[515,1170][565,1220]", verify=False)
        print(f"✅ 点击成功（bounds: [515,1170][565,1220]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤6: 点击 [810,2186][1080,2356]
        print(f"\n步骤6: 点击 [810,2186][1080,2356]")
        # ✅ 使用bounds坐标（已验证）
        await client.click("[810,2186][1080,2356]", ref="[810,2186][1080,2356]", verify=False)
        print(f"✅ 点击成功（bounds: [810,2186][1080,2356]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤7: 点击 右上角设置
        print(f"\n步骤7: 点击 右上角设置")
        # ✅ 使用bounds坐标（已验证）
        await client.click("右上角设置", ref="[919,113][1034,205]", verify=False)
        print(f"✅ 点击成功（bounds: [919,113][1034,205]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤8: 点击 [861,131][919,188]
        print(f"\n步骤8: 点击 [861,131][919,188]")
        # ✅ 使用bounds坐标（已验证）
        await client.click("[861,131][919,188]", ref="[861,131][919,188]", verify=False)
        print(f"✅ 点击成功（bounds: [861,131][919,188]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤9: 点击 语言
        print(f"\n步骤9: 点击 语言")
        # ✅ 使用bounds坐标（已验证）
        await client.click("语言", ref="[515,1170][565,1220]", verify=False)
        print(f"✅ 点击成功（bounds: [515,1170][565,1220]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤10: 点击 [0,1075][1080,1202]
        print(f"\n步骤10: 点击 [0,1075][1080,1202]")
        # ✅ 使用bounds坐标（已验证）
        await client.click("[0,1075][1080,1202]", ref="[0,1075][1080,1202]", verify=False)
        print(f"✅ 点击成功（bounds: [0,1075][1080,1202]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤11: 点击 English
        print(f"\n步骤11: 点击 English")
        # ✅ 使用bounds坐标（已验证）
        await client.click("English", ref="[515,325][565,375]", verify=False)
        print(f"✅ 点击成功（bounds: [515,325][565,375]）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤12: 点击 保存
        print(f"\n步骤12: 点击 保存")
        # ✅ 使用text/description定位（已验证）
        await client.click("保存", ref="保存", verify=False)
        print(f"✅ 点击成功（text/desc: 保存）")
        await asyncio.sleep(1.5)  # 等待页面响应
        # 步骤13: 点击 重新启动
        print(f"\n步骤13: 点击 重新启动")
        # ✅ 使用text/description定位（已验证）
        await client.click("重新启动", ref="重新启动", verify=False)
        print(f"✅ 点击成功（text/desc: 重新启动）")
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