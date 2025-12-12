#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动端自动化测试: 堆糖搜索测试
生成时间: 2025-11-26 15:39:24

依赖: pip install uiautomator2 pytest pytest-asyncio

运行方式:
    pytest test_测试.py -v -s
    pytest test_测试.py --alluredir=./allure-results  # 生成allure报告
"""

import time
import pytest
import uiautomator2 as u2


PACKAGE_NAME = "com.duitang.main"
DEVICE_ID = "BEWGF6LFZ5RGS875"  # 本地iOS设备  # None表示自动选择第一个设备


@pytest.fixture(scope='function')
def device():
    """
    pytest fixture: 创建并返回设备连接
    scope='function': 每个测试函数都会创建一个新的连接
    """
    # 连接设备
    d = u2.connect(DEVICE_ID)  # None表示自动选择第一个设备
    print(f"\n📱 连接设备: {d.device_info}")
    
    # 启动App
    print(f"🚀 启动App: {PACKAGE_NAME}")
    d.app_start(PACKAGE_NAME, stop=True)
    time.sleep(3)  # 等待App启动
    
    yield d
    
    # 清理（可选：关闭App）
    # d.app_stop(PACKAGE_NAME)


def test_堆糖搜索测试(device):
    """
    测试用例: 堆糖搜索测试
    
    测试步骤:
    1. 打开com.duitang.main
    2. 点击底部"我"
    3. 点击"不同意"
    4. 点击"首页"
    5. 搜索框输入"测试"
    6. 点击"搜索"
    7. 点击返回
    8. 点击返回
    9. 断言回到了首页
    
    Args:
        device: pytest fixture，已启动App的设备连接
    """
    d = device
    
    # 步骤1: 点击底部"我"
    print(f"\n步骤1: 点击底部'我'")
    d.click(972, 2288)  # 使用MCP验证过的坐标
    time.sleep(1.5)

    # 步骤2: 点击"不同意"
    print(f"\n步骤2: 点击'不同意'")
    d(resourceId="com.duitang.main:id/welcome_policies_disagree").click()
    time.sleep(1.5)

    # 步骤3: 点击"首页"
    print(f"\n步骤3: 点击'首页'")
    d(resourceId="com.duitang.main:id/ex_tab_title", text="首页").click()
    time.sleep(1.5)

    # 步骤4: 点击搜索框
    print(f"\n步骤4: 点击搜索框")
    d.click(540, 338)  # 使用MCP验证过的坐标
    time.sleep(1.5)

    # 步骤5: 点击搜索输入框
    print(f"\n步骤5: 点击搜索输入框")
    d(resourceId="com.duitang.main:id/etSearch").click()
    time.sleep(1.5)

    # 步骤6: 点击最近搜索"测试"
    print(f"\n步骤6: 点击最近搜索'测试'")
    d.click(118, 396)  # 使用MCP验证过的坐标
    time.sleep(1.5)

    # 步骤7: 点击"搜索"
    print(f"\n步骤7: 点击'搜索'")
    d(resourceId="com.duitang.main:id/search_bar_search_btn").click()
    time.sleep(1.5)

    # 步骤8: 点击返回
    print(f"\n步骤8: 点击返回")
    d.press("back")
    time.sleep(1.5)

    # 步骤9: 点击返回
    print(f"\n步骤9: 点击返回")
    d.press("back")
    time.sleep(1.5)

    # 步骤10: 断言回到了首页
    print(f"\n步骤10: 断言回到了首页")
    assert d(text="首页").exists(), "断言失败: 未能回到首页"
    
    # ✅ 测试完成
    print("✅ 测试通过")
