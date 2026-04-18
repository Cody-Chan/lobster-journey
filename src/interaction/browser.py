"""
互动运营自动化 - 浏览器自动化模块

职责：
- 管理浏览器会话
- 登录小红书
- 自动浏览笔记
- 执行互动操作
"""

import asyncio
import random
from pathlib import Path
from typing import Optional, List, Dict
from playwright.async_api import async_playwright, Page, Browser
import json
from datetime import datetime


class InteractionBot:
    """小红书互动机器人"""
    
    def __init__(self, cookie_path: str = "/home/gem/.openclaw/mcp/cookies.json"):
        self.cookie_path = Path(cookie_path)
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.context = None
        
    async def start(self, headless: bool = False):
        """启动浏览器"""
        print("🤖 启动浏览器...")
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context()
        
        # 加载Cookie
        await self._load_cookies()
        
        self.page = await self.context.new_page()
        print("✅ 浏览器已启动")
        
    async def _load_cookies(self):
        """加载Cookie"""
        if not self.cookie_path.exists():
            print("⚠️  Cookie文件不存在")
            return
            
        with open(self.cookie_path, 'r') as f:
            data = json.load(f)
            
        # 提取cookies数组
        if isinstance(data, dict) and 'cookies' in data:
            cookies = data['cookies']
        else:
            cookies = data
            
        await self.context.add_cookies(cookies)
        print(f"✅ 已加载 {len(cookies)} 个Cookie")
        
    async def _save_cookies(self):
        """保存Cookie"""
        await self.context.storage_state(path=str(self.cookie_path))
        print("✅ Cookie已保存")
        
    async def login(self) -> bool:
        """登录小红书"""
        print("🔐 检查登录状态...")
        
        await self.page.goto('https://www.xiaohongshu.com')
        await self.page.wait_for_timeout(3000)
        
        # 检查是否已登录
        try:
            # 查找用户头像或发布按钮
            user_avatar = await self.page.query_selector('[class*="avatar"]')
            
            if user_avatar:
                print("✅ 已登录")
                return True
            else:
                print("⚠️  未登录")
                
                # 访问登录页
                await self.page.goto('https://www.xiaohongshu.com/login')
                await self.page.wait_for_timeout(3000)
                
                # 截图
                screenshot_path = f"/tmp/xhs_login_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                await self.page.screenshot(path=screenshot_path)
                print(f"📸 登录页截图: {screenshot_path}")
                
                # 等待扫码登录
                print("⏳ 等待扫码登录（2分钟）...")
                await self.page.wait_for_timeout(120000)
                
                # 保存Cookie
                await self._save_cookies()
                return True
                
        except Exception as e:
            print(f"❌ 登录检查失败: {e}")
            return False
            
    async def browse_feed(self, duration: int = 60):
        """浏览首页推荐
        
        Args:
            duration: 浏览时长（秒）
        """
        print(f"📖 开始浏览首页推荐（{duration}秒）...")
        
        await self.page.goto('https://www.xiaohongshu.com')
        await self.page.wait_for_timeout(3000)
        
        start_time = datetime.now()
        notes_viewed = 0
        
        while (datetime.now() - start_time).seconds < duration:
            # 滚动浏览
            await self._human_scroll()
            
            # 随机浏览时长（5-15秒）
            browse_time = random.randint(5, 15)
            await self.page.wait_for_timeout(browse_time * 1000)
            
            notes_viewed += 1
            
        print(f"✅ 浏览完成，共浏览 {notes_viewed} 篇笔记")
        return notes_viewed
        
    async def _human_scroll(self):
        """模拟人类滚动"""
        # 随机滚动距离
        scroll_distance = random.randint(300, 800)
        
        await self.page.evaluate(f'''
            window.scrollBy({{
                top: {scroll_distance},
                behavior: 'smooth'
            }});
        ''')
        
        # 随机等待
        await self.page.wait_for_timeout(random.randint(500, 1500))
        
    async def like_note(self, note_url: str) -> bool:
        """点赞笔记
        
        Args:
            note_url: 笔记URL
            
        Returns:
            是否成功
        """
        try:
            print(f"❤️  点赞笔记: {note_url}")
            
            await self.page.goto(note_url)
            await self.page.wait_for_timeout(3000)
            
            # 查找点赞按钮
            like_btn = await self.page.query_selector('[class*="like"]')
            
            if like_btn:
                await like_btn.click()
                await self.page.wait_for_timeout(1000)
                print("✅ 点赞成功")
                return True
            else:
                print("⚠️  未找到点赞按钮")
                return False
                
        except Exception as e:
            print(f"❌ 点赞失败: {e}")
            return False
            
    async def comment_note(self, note_url: str, comment: str) -> bool:
        """评论笔记
        
        Args:
            note_url: 笔记URL
            comment: 评论内容
            
        Returns:
            是否成功
        """
        try:
            print(f"💬 评论笔记: {note_url}")
            
            await self.page.goto(note_url)
            await self.page.wait_for_timeout(3000)
            
            # 查找评论输入框
            comment_input = await self.page.query_selector('textarea')
            
            if comment_input:
                await comment_input.fill(comment)
                await self.page.wait_for_timeout(500)
                
                # 查找发布按钮
                submit_btn = await self.page.query_selector('button:has-text("发布")')
                if submit_btn:
                    await submit_btn.click()
                    await self.page.wait_for_timeout(1000)
                    print("✅ 评论成功")
                    return True
            else:
                print("⚠️  未找到评论输入框")
                return False
                
        except Exception as e:
            print(f"❌ 评论失败: {e}")
            return False
            
    async def collect_note(self, note_url: str) -> bool:
        """收藏笔记
        
        Args:
            note_url: 笔记URL
            
        Returns:
            是否成功
        """
        try:
            print(f"⭐ 收藏笔记: {note_url}")
            
            await self.page.goto(note_url)
            await self.page.wait_for_timeout(3000)
            
            # 查找收藏按钮
            collect_btn = await self.page.query_selector('[class*="collect"]')
            
            if collect_btn:
                await collect_btn.click()
                await self.page.wait_for_timeout(1000)
                print("✅ 收藏成功")
                return True
            else:
                print("⚠️  未找到收藏按钮")
                return False
                
        except Exception as e:
            print(f"❌ 收藏失败: {e}")
            return False
            
    async def search_notes(self, keyword: str, limit: int = 20) -> List[Dict]:
        """搜索笔记
        
        Args:
            keyword: 搜索关键词
            limit: 返回数量
            
        Returns:
            笔记列表
        """
        print(f"🔍 搜索笔记: {keyword}")
        
        # 访问搜索页
        search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
        await self.page.goto(search_url)
        await self.page.wait_for_timeout(3000)
        
        # 截图
        screenshot_path = f"/tmp/xhs_search_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        await self.page.screenshot(path=screenshot_path)
        print(f"📸 搜索结果截图: {screenshot_path}")
        
        # TODO: 解析搜索结果
        notes = []
        
        print(f"✅ 搜索完成，找到 {len(notes)} 篇笔记")
        return notes
        
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("✅ 浏览器已关闭")


async def main():
    """测试运行"""
    bot = InteractionBot()
    
    try:
        await bot.start(headless=False)
        
        # 登录
        await bot.login()
        
        # 浏览首页
        await bot.browse_feed(duration=30)
        
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
