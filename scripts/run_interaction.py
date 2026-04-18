#!/usr/bin/env python3
"""
互动运营自动化 - 主程序

职责：
- 协调各个模块
- 执行定时任务
- 记录运行日志
"""

import asyncio
import sys
import random
from pathlib import Path
from datetime import datetime

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.interaction.browser import InteractionBot
from src.interaction.actions import InteractionController, generate_comment
from src.data.collector import DataCollector


class InteractionOrchestrator:
    """互动运营协调器"""
    
    def __init__(self):
        self.bot = InteractionBot()
        self.controller = InteractionController()
        self.collector = DataCollector()
        
    async def run_daily_task(self, duration: int = 60):
        """执行每日互动任务
        
        Args:
            duration: 运行时长（分钟）
        """
        print("="*60)
        print(f"🦞 龙虾巡游记 - 互动运营自动化")
        print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"运行时长: {duration}分钟")
        print("="*60)
        
        try:
            # 启动浏览器
            await self.bot.start(headless=False)
            
            # 登录
            login_success = await self.bot.login()
            if not login_success:
                print("❌ 登录失败，退出")
                return
                
            # 浏览首页
            print("\n📖 开始浏览首页...")
            await self.bot.browse_feed(duration=min(duration * 60, 1800))
            
            # 执行互动
            print("\n🎯 开始执行互动...")
            await self._perform_interactions(duration)
            
            # 保存数据
            print("\n💾 保存数据...")
            output_path = project_root / "data" / f"interaction_{datetime.now().strftime('%Y%m%d')}.json"
            self.collector.export_to_json(str(output_path))
            
            # 打印统计
            self._print_stats()
            
        except Exception as e:
            print(f"❌ 运行出错: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            await self.bot.close()
            
    async def _perform_interactions(self, duration: int):
        """执行互动操作
        
        Args:
            duration: 运行时长（分钟）
        """
        start_time = datetime.now()
        duration_seconds = duration * 60
        
        while (datetime.now() - start_time).seconds < duration_seconds:
            # 检查是否需要暂停
            if self.controller.should_pause():
                print("⏸️  暂停休息...")
                await asyncio.sleep(300)  # 休息5分钟
                continue
                
            # 随机选择互动类型
            action_type = random.choice(['like', 'comment', 'collect'])
            
            # 检查频率限制
            if not self.controller.can_perform_action(action_type):
                print(f"⚠️  {action_type}频率已达上限，切换其他动作")
                await asyncio.sleep(60)
                continue
                
            # TODO: 从搜索或首页获取笔记
            # 这里需要实际实现笔记获取逻辑
            
            # 记录互动
            self.controller.record_action(
                action_type=action_type,
                note_id='demo_note',
                note_url='https://www.xiaohongshu.com/explore/demo',
                success=True
            )
            
            # 保存到数据库
            self.collector.save_interaction(action_type, 'demo_note', True)
            
            # 随机间隔
            interval = self.controller.get_random_interval(action_type)
            print(f"⏳ 等待 {interval}秒 后继续...")
            await asyncio.sleep(interval)
            
    def _print_stats(self):
        """打印统计信息"""
        stats = self.controller.get_today_stats()
        
        print("\n" + "="*60)
        print("📊 今日互动统计")
        print("="*60)
        print(f"总互动次数: {stats['total']}")
        print(f"成功率: {stats['success_rate']:.2%}")
        print("\n按类型统计:")
        
        for action_type, data in stats['by_type'].items():
            success_rate = data['success'] / data['total'] if data['total'] > 0 else 0
            print(f"  {action_type}: {data['total']}次 (成功{success_rate:.2%})")
            
        print("="*60)


async def main():
    """主函数"""
    orchestrator = InteractionOrchestrator()
    await orchestrator.run_daily_task(duration=30)  # 运行30分钟


if __name__ == "__main__":
    asyncio.run(main())
