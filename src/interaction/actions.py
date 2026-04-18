"""
互动运营自动化 - 互动动作模块

职责：
- 定义互动动作
- 控制操作频率
- 记录互动数据
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class InteractionRecord:
    """互动记录"""
    action_type: str  # like, comment, collect, follow
    note_id: str
    note_url: str
    timestamp: datetime
    success: bool
    details: Optional[str] = None


class InteractionController:
    """互动控制器"""
    
    # 频率限制（每小时）
    HOURLY_LIMITS = {
        'like': 15,
        'comment': 10,
        'collect': 10,
        'follow': 5
    }
    
    # 频率限制（每天）
    DAILY_LIMITS = {
        'like': 50,
        'comment': 30,
        'collect': 20,
        'follow': 10
    }
    
    def __init__(self, data_dir: str = "/home/gem/.openclaw/workspace/lobster-journey/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.records_file = self.data_dir / "interaction_records.json"
        self.records: List[InteractionRecord] = []
        
        # 加载历史记录
        self._load_records()
        
    def _load_records(self):
        """加载历史记录"""
        if self.records_file.exists():
            with open(self.records_file, 'r') as f:
                data = json.load(f)
                self.records = [InteractionRecord(**r) for r in data]
                
    def _save_records(self):
        """保存记录"""
        data = [r.__dict__ for r in self.records]
        with open(self.records_file, 'w') as f:
            json.dump(data, f, default=str, indent=2)
            
    def can_perform_action(self, action_type: str) -> bool:
        """检查是否可以执行动作
        
        Args:
            action_type: 动作类型
            
        Returns:
            是否可以执行
        """
        now = datetime.now()
        
        # 检查每小时限制
        hour_ago = now - timedelta(hours=1)
        hourly_count = len([
            r for r in self.records
            if r.action_type == action_type 
            and r.timestamp > hour_ago
        ])
        
        if hourly_count >= self.HOURLY_LIMITS.get(action_type, 10):
            print(f"⚠️  每小时{action_type}次数已达上限: {hourly_count}")
            return False
            
        # 检查每天限制
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        daily_count = len([
            r for r in self.records
            if r.action_type == action_type
            and r.timestamp > today_start
        ])
        
        if daily_count >= self.DAILY_LIMITS.get(action_type, 30):
            print(f"⚠️  今日{action_type}次数已达上限: {daily_count}")
            return False
            
        return True
        
    def record_action(self, action_type: str, note_id: str, note_url: str, 
                     success: bool, details: Optional[str] = None):
        """记录动作
        
        Args:
            action_type: 动作类型
            note_id: 笔记ID
            note_url: 笔记URL
            success: 是否成功
            details: 详细信息
        """
        record = InteractionRecord(
            action_type=action_type,
            note_id=note_id,
            note_url=note_url,
            timestamp=datetime.now(),
            success=success,
            details=details
        )
        
        self.records.append(record)
        self._save_records()
        
        print(f"📝 记录动作: {action_type} - {note_id}")
        
    def get_random_interval(self, action_type: str) -> int:
        """获取随机间隔时间
        
        Args:
            action_type: 动作类型
            
        Returns:
            间隔时间（秒）
        """
        # 基础间隔（秒）
        base_intervals = {
            'like': 300,      # 5分钟
            'comment': 600,   # 10分钟
            'collect': 300,   # 5分钟
            'follow': 900     # 15分钟
        }
        
        base = base_intervals.get(action_type, 300)
        
        # 添加随机性（±50%）
        interval = base * (1 + random.uniform(-0.5, 0.5))
        
        return int(interval)
        
    def get_today_stats(self) -> Dict:
        """获取今日统计
        
        Returns:
            统计数据
        """
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        today_records = [
            r for r in self.records
            if r.timestamp > today_start
        ]
        
        stats = {
            'total': len(today_records),
            'by_type': {},
            'success_rate': 0
        }
        
        # 按类型统计
        for action_type in ['like', 'comment', 'collect', 'follow']:
            type_records = [r for r in today_records if r.action_type == action_type]
            stats['by_type'][action_type] = {
                'total': len(type_records),
                'success': len([r for r in type_records if r.success])
            }
            
        # 成功率
        if stats['total'] > 0:
            success_count = len([r for r in today_records if r.success])
            stats['success_rate'] = success_count / stats['total']
            
        return stats
        
    def should_pause(self) -> bool:
        """判断是否需要暂停
        
        Returns:
            是否需要暂停
        """
        now = datetime.now()
        hour = now.hour
        
        # 深夜时段（0-6点）降低活动
        if 0 <= hour < 6:
            return random.random() < 0.8  # 80%概率暂停
            
        # 高峰时段正常活动
        return False


def generate_comment(content_type: str = "general") -> str:
    """生成评论内容
    
    Args:
        content_type: 内容类型
        
    Returns:
        评论内容
    """
    templates = {
        'general': [
            "这个观点很有意思！感谢分享～",
            "写得很好，学习了！",
            "内容很实用，收藏了！",
            "很有启发，谢谢分享！"
        ],
        'tech': [
            "这个技术点讲得很清楚！",
            "刚好在研究这个，很有帮助！",
            "代码示例很棒，学习了～",
            "技术分享很实用，谢谢！"
        ],
        'ai': [
            "AI领域发展太快了，感谢总结！",
            "这个AI工具看起来很不错！",
            "对AI很感兴趣，可以交流一下～",
            "AI应用场景越来越广了！"
        ]
    }
    
    return random.choice(templates.get(content_type, templates['general']))


if __name__ == "__main__":
    # 测试
    controller = InteractionController()
    
    # 模拟记录
    controller.record_action(
        action_type='like',
        note_id='test123',
        note_url='https://www.xiaohongshu.com/explore/test123',
        success=True
    )
    
    # 检查限制
    print(f"可以点赞: {controller.can_perform_action('like')}")
    
    # 获取统计
    stats = controller.get_today_stats()
    print(f"今日统计: {json.dumps(stats, indent=2)}")
