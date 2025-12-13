import json
import os
import random
from typing import Any

import htmlmin
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage._elements.none_element import NoneElement
from fastmcp import FastMCP
from lxml import html, etree

html_source_code_local_save_path = os.path.join(os.getcwd(), "html-source-code")
browser_pool = {}


# 压缩html
def compress_html(content):
    doc = html.fromstring(content)
    # 删除 style 和 script 标签
    for element in doc.xpath('//style | //script'):
        element.getparent().remove(element)

    # 删除 link 标签
    for link in doc.xpath('//link[@rel="stylesheet"]'):
        link.getparent().remove(link)

    # 删除 style 属性
    for element in doc.xpath('//*[@style]'):
        element.attrib.pop('style')

    # 删除所有 on* 事件属性
    for element in doc.xpath('//*'):
        for attr in list(element.attrib.keys()):
            if attr.startswith('on'):
                element.attrib.pop(attr)

    result = etree.tostring(doc, encoding='unicode')
    result = htmlmin.minify((result))
    print(f"html压缩比=> {len(content) / len(result) * 100:.2f}%")
    return result


# 随机一个浏览器池中不存在的端口，创建一个浏览器，返回随机端口，和浏览器对象。
def create_browser():
    global browser_pool
    random_port = random.randint(9222, 9934)
    while random_port in browser_pool:
        random_port = random.randint(9222, 9934)
    co = ChromiumOptions().set_local_port(random_port)
    browser_pool[random_port] = ChromiumPage(co)
    return random_port, browser_pool[random_port]


# 根据传入的端口查找对应的浏览器对象
def get_page(port):
    return browser_pool.get(port, None)


def register_visit_url(mcp: FastMCP):
    @mcp.tool(name="visit_url", description="使用Drissionpage打开url访问某个网站")
    async def visit_url(url: str) -> dict[str, Any]:
        port, _browser = create_browser()
        tab = _browser.get_tab()
        tab.get(url)
        tab_id = tab.tab_id
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "message": f"已在[{port}]端口创建浏览器对象，并已打开链接：{url}",
                    "tab_id": tab_id,
                    "browser_port": port,
                }, ensure_ascii=False)
            }]
        }


def register_get_html(mcp: FastMCP):
    @mcp.tool(name="get_html", description="使用Drissionpage获取某一个tab页的html")
    async def get_html(browser_port: int, tab_id: str) -> dict[str, Any]:
        _browser = get_page(browser_port)
        tab = _browser.get_tab(tab_id)
        file_name = tab.title + f"_{tab_id}.html"
        abs_path = os.path.join(html_source_code_local_save_path, file_name)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(compress_html(tab.html))
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "message": f"已保存tab页：【{tab_id}】的html源码",
                    "tab_id": tab_id,
                    "html_local_path": abs_path
                }, ensure_ascii=False)
            }]
        }


def register_get_new_tab(mcp: FastMCP):
    @mcp.tool(name="get_new_tab", description="使用Drissionpage创建一个新的tab页，在新的tab页中打开url")
    async def get_new_tab(browser_port: int, url: str) -> dict[str, Any]:
        _browser = get_page(browser_port)
        tab = _browser.new_tab(url)
        _browser.activate_tab(tab)
        tab_id = tab.tab_id
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "message": f"已创建新的tab页，并打开链接：{url}",
                    "tab_id": tab_id,
                }, ensure_ascii=False)
            }]
        }


def register_switch_tab(mcp: FastMCP):
    @mcp.tool(name="switch_tab", description="根据传入的tab_id切换到对应的tab页", )
    async def switch_tab(browser_port: int, tab_id: str) -> dict[str, Any]:
        _browser = get_page(browser_port)
        _browser.activate_tab(tab_id)
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "message": f"已将tab页:【{tab_id}】切换至最前端",
                }, ensure_ascii=False)
            }]
        }


def register_close_tab(mcp: FastMCP):
    @mcp.tool(name="close_tab", description="根据传入的tab_id关闭tab页", )
    async def close_tab(browser_port, tab_id) -> dict[str, Any]:
        _browser = get_page(browser_port)
        _browser.close_tabs(tab_id)
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "message": f"已将tab页:【{tab_id}】关闭",
                }, ensure_ascii=False)
            }]
        }


def register_check_selector(mcp: FastMCP):
    @mcp.tool(name="check_selector", description="查找tab页中是否包含元素")
    async def check_selector(browser_port: int, tab_id: str, css_selector: str) -> dict[str, Any]:
        _browser = get_page(browser_port)
        target_tab = _browser.get_tab(tab_id)
        css_selector = css_selector
        if "css:" not in css_selector:
            css_selector = "css:" + css_selector
        target_ele = target_tab.ele(css_selector)
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "message": f"已完成tab页:【{tab_id}】对：【{css_selector}】的检查",
                    "tab_id": tab_id,
                    "selector": css_selector,
                    "selector_ele_exist": not isinstance(target_ele, NoneElement),
                }, ensure_ascii=False)
            }]
        }

# def main():
#     mcp.run()
#
#
# if __name__ == '__main__':
#     main()
