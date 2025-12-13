#!/usr/bin/env python3
"""
概念详情
https://q.10jqka.com.cn/gn/detail/code/300082/
"""

import aiohttp
import pandas as pd
from datetime import date, datetime
from typing import Dict, List, Any, Optional
import json
import py_mini_racer
from io import StringIO
from selenium import webdriver
import time
import random
import requests

def _get_file_content_ths(file: str = "ths.js") -> str:
    """
    获取 JS 文件的内容
    :param file:  JS 文件名
    :type file: str
    :return: 文件内容
    :rtype: str
    """
    import os
    # 首先尝试使用akshare的ths.js文件
    try:
        import akshare.datasets
        setting_file_path = akshare.datasets.get_ths_js(file)
        with open(setting_file_path, encoding="utf-8") as f:
            file_data = f.read()
        return file_data
    except:
        # 如果akshare的ths.js不可用，尝试在scripts目录下查找文件
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file)
        with open(file_path, encoding="utf-8") as f:
            file_data = f.read()
        return file_data


def _get_hexin_v() -> str:
    """
    同花顺 js方式获取 hexin-v值，但这里不适用
    :return: hexin-v 值
    :rtype: str
    """
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call("v")
    return v_code

def get_hexin_v():
    """获取hexin-v参数"""
    # 同花顺 js方式获取 hexin-v值，但这里不适用
    # try:
    #     return _get_hexin_v()
    # except Exception as e:
    #     print(f"使用akshare ths.js方法失败: {e}")
    #     print("尝试使用selenium方法...")
    
    # 如果akshare方法失败，再尝试selenium方法
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # 无头模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')  # 移除自动化控制标志
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 禁用自动化提示
    options.add_experimental_option('useAutomationExtension', False)  # 禁用扩展
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    # 使用webdriver-manager自动管理Chrome驱动
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # 执行JavaScript来隐藏自动化特征
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        driver.get("https://q.10jqka.com.cn/gn/detail/code/309034/")
        time.sleep(10)  # 等待更长时间让页面完全加载
        
        # 尝试多种方法获取hexin-v
        v_value = None
        
        # 方法1: 从cookie中获取
        cookies = driver.get_cookies()
        print(f"获取到的cookies数量: {len(cookies)}")
        for cookie in cookies:
            print(f"Cookie: {cookie['name']} = {cookie['value'][:20]}...")
            if cookie['name'] == 'v':
                v_value = cookie['value']
                print(f"从cookie中找到v值: {v_value[:20]}...")
                break
        
        # 方法2: 从localStorage获取
        if not v_value:
            try:
                v_value = driver.execute_script("return localStorage.getItem('v');")
                if v_value:
                    print(f"从localStorage中找到v值: {v_value[:20]}...")
            except:
                pass
        
        # 方法3: 从JavaScript变量获取
        if not v_value:
            try:
                v_value = driver.execute_script("return window.v;")
                if v_value:
                    print(f"从window.v中找到v值: {v_value[:20]}...")
            except:
                pass
        
        # 方法4: 从页面源代码中查找
        if not v_value:
            page_source = driver.page_source
            import re
            # 查找可能的hexin-v值模式
            v_patterns = [
                r'v=([A-Za-z0-9_-]{60})',
                r'"v":"([A-Za-z0-9_-]{60})"',
                r'hexin-v=([A-Za-z0-9_-]{60})'
            ]
            for pattern in v_patterns:
                match = re.search(pattern, page_source)
                if match:
                    v_value = match.group(1)
                    print(f"从页面源代码中找到v值: {v_value[:20]}...")
                    break
        
        if not v_value:
            print("警告: 未找到hexin-v值，使用默认值")
            # 返回一个默认值或抛出异常
            return None
        
        return v_value
    finally:
        driver.quit()

async def collect_page(
    code: str,
    page: int,
    field: str,
    order: str,
    v_code: str
) -> Optional[pd.DataFrame]:
    """
    收集单个页面的数据
    
    Args:
        code: 概念代码
        page: 页码
        field: 排序列id
        order: 排序方式
        v_code: hexin-v值
    Returns:
        pandas DataFrame 或 None（如果页面无数据）
    """
    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "hexin-v": v_code,
        "Host": "q.10jqka.com.cn",
        "Pragma": "no-cache",
        "Referer": f"https://q.10jqka.com.cn/gn/detail/code/{code}/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/90.0.4430.85 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    
    url = f'https://q.10jqka.com.cn/gn/detail/field/{field}/order/{order}/page/{page}/ajax/1/code/{code}'
    
    try:
        res = requests.get(url, headers=headers)
        temp_df = pd.read_html(StringIO(res.text))[0]
        return temp_df
    except Exception as e:
        print(f" {page} 页面 {url} 请求异常: {e}")
        return None


def query_concept_codes_from_db(username: str,password: str,host: str,port: str, database: str, query_date: str = None) -> List[Dict[str, str]]:
    """
    从数据库查询概念代码和名称
    
    Args:
        mysql_url: MySQL连接字符串
        query_date: 查询日期，默认为今天
        
    Returns:
        概念代码和名称列表，每个元素是包含'code'和'name'的字典
    """
    import pymysql
    from datetime import datetime
    
    if query_date is None:
        query_date = datetime.now().strftime('%Y-%m-%d')

    # SQL查询语句
    sql = """
    SELECT sbc.name, sbc.code FROM stock_fund_flow_concept sc
    inner join stock_board_concept sbc on sc.`行业` = sbc.name
    where sc.`日期` = %s and sc.行业 not in (SELECT DISTINCT `行业` from stock_board_concept_item)
    order by sc.`行业-涨跌幅` desc
    limit 50;
    """
    
    try:
        # 连接数据库
        connection = pymysql.connect(
            host=host,
            user=username,
            password=password,
            database=database,
            port=port,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            cursor.execute(sql, (query_date,))
            results = cursor.fetchall()
            
        connection.close()
        
        # 返回包含名称和代码的结果
        print(f"从数据库查询返回前 {len(results)} 个概念: {[(row['name'], row['code']) for row in results[:3]]}...")
        return results
        
    except Exception as e:
        print(f"数据库查询失败: {e}")
        return []


async def collect(
    config: Optional[Dict[str, Any]] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Collect stock data from a web API.
    
    This is the main function that will be called by the custom collector.
    It receives all parameters from the workflow configuration.
    
    Args:
        config: Collector configuration from workflow (config.config)
        collector_config: Full collector configuration
        **kwargs: Additional parameters from workflow (e.g., symbols, start_date, etc.)
        
    Returns:
        pandas DataFrame with stock data
    """
    # Get configuration
    config = config or {}
    
    # 从配置或kwargs中获取参数
    host = config.get("host", "localhost")
    port = int(config.get("port", 3306))
    database = config.get("database", "stock")
    username = config.get("username", "root")
    password = config.get("password", "123456")
    query_date = datetime.now().strftime("%Y-%m-%d")
    
    # 如果提供了mysql_url，则从数据库查询概念代码
    concept_result = query_concept_codes_from_db(username,password,host,port,database, query_date)
    
    # 如果没有从数据库获取到概念代码，使用默认值
    if not concept_result:
        concept_result = [{'code': '300082', 'name': '军工'}]
        print(f"使用默认概念: {concept_result}")
    
    # 其他参数
    start_page = kwargs.get('start_page', config.get('start_page', 1))
    end_page = kwargs.get('end_page', config.get('end_page', 5))
    field = kwargs.get('field', config.get('field', '199112')) # 排序列id
    order = kwargs.get('order', config.get('order', 'desc'))
    
    # 获取 hexin-v
    print("正在获取hexin-v...")
    v_code = get_hexin_v()
    if v_code is None:
        print("获取hexin_v失败")
        return pd.DataFrame()
    print(f"成功获取hexin-v: {v_code}...")
    
    # 收集所有概念代码的数据
    all_dfs = []
    
    for concept_item in concept_result:
        code = concept_item['code']
        name = concept_item['name']
        print(f"\n正在获取概念代码 {code} ({name}) 的数据...")
        concept_dfs = []
        for page in range(start_page, end_page + 1):
            print(f"  正在获取第 {page} 页数据...")
            try:
                df = await collect_page(code, page, field, order, v_code)
                if df is None:
                    print(f"  第 {page} 页重试一次")
                    df = await collect_page(code, page, field, order, v_code)
                if df is not None and not df.empty:
                    concept_dfs.append(df)
                else:
                    print(f"  第 {page} 页无数据或获取失败")
                    break
                time.sleep(random.uniform(3, 5))

            except Exception as e:
                print(f"  第 {page} 页获取异常: {e}")
                # 可以选择继续或中断
                continue

        # 合并当前概念的所有页面数据
        if concept_dfs:
            concept_df = pd.concat(concept_dfs, ignore_index=True)
            # 添加行业列，赋值为概念名称
            concept_df['行业'] = name
            concept_df['行业代码'] = code
            all_dfs.append(concept_df)
            print(f"概念代码 {code} ({name}) 获取完成，共 {len(concept_df)} 条数据")
        else:
            print(f"概念代码 {code} ({name}) 未获取到数据")
        # 重新获取hexinv
        v_code = get_hexin_v()
        time.sleep(random.uniform(2, 5))

    # 合并所有概念的数据
    if not all_dfs:
        print("未获取到任何数据")
        return pd.DataFrame()
    
    final_df = pd.concat(all_dfs, ignore_index=True)
    print(f"\n总共获取 {len(final_df)} 条数据，来自 {len(concept_result)} 个概念")
    
    return final_df


def main():
    """
    主函数，用于直接运行测试
    """
    import asyncio
    import sys
    
    async def test():
        try:
            print("开始测试 collect 函数...")
            df = await collect()
            print(f"成功获取数据！DataFrame 形状: {df.shape}")
            print(f"列名: {df.columns.tolist()}")
            print("\n前5行数据:")
            print(df.head())
            print("\n数据统计信息:")
            print(df.describe())
            
            # 保存到CSV文件用于检查
            output_file = "concept_detail_test.csv"
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"\n数据已保存到: {output_file}")
            
            return True
        except Exception as e:
            print(f"测试失败: {e}")
            return False
    
    # 运行测试
    success = asyncio.run(test())
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
