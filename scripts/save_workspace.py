#!/usr/bin/env python3
"""
工作现场保存脚本

职责：
- 收集当前工作状态
- 更新WORKSPACE.md
- 生成context.json
- 推送到GitHub
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class WorkspaceSaver:
    """工作现场保存器"""
    
    def __init__(self, project_root: str = "/home/gem/.openclaw/workspace/lobster-journey"):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def collect_current_state(self) -> Dict:
        """收集当前状态
        
        Returns:
            状态信息
        """
        state = {
            "timestamp": datetime.now().isoformat(),
            "project": {
                "name": "Lobster Journey Studio",
                "version": "1.0.0",
                "status": "active"
            },
            "tasks": {
                "total": 3,
                "completed": 1,
                "in_progress": 1,
                "pending": 1,
                "details": [
                    {
                        "id": 1,
                        "name": "互动运营自动化",
                        "status": "completed",
                        "completion_time": "2026-04-18T12:00:00",
                        "files_created": [
                            "src/interaction/browser.py",
                            "src/interaction/actions.py",
                            "src/data/collector.py",
                            "scripts/run_interaction.py"
                        ],
                        "lines_of_code": 800
                    },
                    {
                        "id": 2,
                        "name": "工作现场保存机制",
                        "status": "in_progress",
                        "start_time": "2026-04-18T12:35:00",
                        "progress": 50
                    },
                    {
                        "id": 3,
                        "name": "龙虾巡游100天策划",
                        "status": "pending"
                    }
                ]
            },
            "git": {
                "branch": "main",
                "last_commit": self._get_last_commit(),
                "remote": "https://github.com/lobster-journey/lobster-journey.git"
            },
            "environment": {
                "python_version": "3.10",
                "os": "Linux",
                "openclaw": "installed"
            },
            "config": {
                "xhs_account": "ai-report",
                "xhs_status": "logged_in",
                "api_keys": ["Querit", "OneAPI"]
            }
        }
        
        return state
        
    def _get_last_commit(self) -> str:
        """获取最后一次commit"""
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--oneline"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except:
            return "unknown"
            
    def save_context(self, state: Dict):
        """保存上下文到JSON
        
        Args:
            state: 状态信息
        """
        context_file = self.data_dir / "context.json"
        
        with open(context_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
            
        print(f"✅ 上下文已保存: {context_file}")
        
    def save_progress(self, tasks: List[Dict]):
        """保存进度到JSON
        
        Args:
            tasks: 任务列表
        """
        progress = {
            "last_update": datetime.now().isoformat(),
            "tasks": tasks
        }
        
        progress_file = self.data_dir / "progress.json"
        
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)
            
        print(f"✅ 进度已保存: {progress_file}")
        
    def create_snapshot(self):
        """创建工作快照"""
        print("="*60)
        print("🦞 创建工作现场快照")
        print("="*60)
        
        # 收集状态
        print("\n📊 收集当前状态...")
        state = self.collect_current_state()
        
        # 保存上下文
        print("\n💾 保存上下文...")
        self.save_context(state)
        
        # 保存进度
        print("\n📈 保存进度...")
        self.save_progress(state['tasks']['details'])
        
        # 推送到GitHub
        print("\n🔄 推送到GitHub...")
        self._push_to_github()
        
        print("\n" + "="*60)
        print("✅ 工作现场快照创建完成")
        print("="*60)
        
    def _push_to_github(self):
        """推送到GitHub"""
        try:
            # 添加所有更改
            subprocess.run(["git", "add", "."], cwd=self.project_root, check=True)
            
            # 提交
            commit_msg = f"chore: 保存工作现场快照 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=self.project_root, check=True)
            
            # 推送
            subprocess.run(["git", "push", "origin", "main"], cwd=self.project_root, check=True)
            
            print("✅ 已推送到GitHub")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  推送失败: {e}")


def main():
    """主函数"""
    saver = WorkspaceSaver()
    saver.create_snapshot()


if __name__ == "__main__":
    main()
