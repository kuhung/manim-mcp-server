#!/usr/bin/env python3
"""
演示重构后的Manim MCP Server工具使用

这个示例展示了如何使用新的细粒度工具来完成完整的Manim工作流。
"""

import json
from pathlib import Path

def print_tool_demo():
    """打印工具使用演示"""
    
    print("🎬 Manim MCP Server - 重构后工具演示")
    print("=" * 60)
    print()
    
    # 示例代码
    sample_code = '''
from manim import *

class RefactoredDemo(Scene):
    def construct(self):
        # 创建标题
        title = Text("重构后的工具架构", font_size=36)
        title.set_color(BLUE)
        
        # 创建副标题
        subtitle = Text("细粒度控制 + 灵活组合", font_size=24)
        subtitle.next_to(title, DOWN, buff=0.5)
        subtitle.set_color(GREEN)
        
        # 动画效果
        self.play(Write(title))
        self.wait(0.5)
        self.play(Write(subtitle))
        self.wait(1)
        
        # 展示工具列表
        tools = VGroup(
            Text("• create_script", font_size=20),
            Text("• validate_script", font_size=20),
            Text("• render_animation", font_size=20),
            Text("• find_videos", font_size=20),
            Text("• get_workspace_info", font_size=20),
            Text("• cleanup_files", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT)
        tools.next_to(subtitle, DOWN, buff=1)
        tools.set_color(YELLOW)
        
        self.play(FadeIn(tools))
        self.wait(2)
'''
    
    print("📝 工作流演示：使用细粒度工具")
    print("-" * 40)
    print()
    
    # 步骤1：创建脚本
    step1 = {
        "name": "create_script",
        "arguments": {
            "code": sample_code,
            "script_dir": "~/Documents/manim_demos/scripts",
            "script_name": "refactored_demo",
            "validate": True
        }
    }
    
    print("🔧 步骤1：创建脚本")
    print(json.dumps(step1, indent=2, ensure_ascii=False))
    print()
    
    # 步骤2：渲染动画
    step2 = {
        "name": "render_animation",
        "arguments": {
            "script_path": "~/Documents/manim_demos/scripts/refactored_demo.py",
            "output_dir": "~/Documents/manim_demos/videos",
            "quality": "high",
            "preview": True
        }
    }
    
    print("🎬 步骤2：渲染动画")
    print(json.dumps(step2, indent=2, ensure_ascii=False))
    print()
    
    # 步骤3：查找视频
    step3 = {
        "name": "find_videos",
        "arguments": {
            "search_dir": "~/Documents/manim_demos/videos",
            "pattern": "*.mp4",
            "recursive": True
        }
    }
    
    print("📹 步骤3：查找生成的视频")
    print(json.dumps(step3, indent=2, ensure_ascii=False))
    print()
    
    # 步骤4：获取工作区信息
    step4 = {
        "name": "get_workspace_info",
        "arguments": {
            "workspace_path": "~/Documents/manim_demos"
        }
    }
    
    print("📊 步骤4：获取工作区信息")
    print(json.dumps(step4, indent=2, ensure_ascii=False))
    print()
    
    print("🚀 便捷工具：一键完成（向后兼容）")
    print("-" * 40)
    
    # 便捷工具
    complete_tool = {
        "name": "execute_manim_complete",
        "arguments": {
            "code": sample_code,
            "script_dir": "~/Documents/manim_demos/scripts",
            "output_dir": "~/Documents/manim_demos/videos",
            "script_name": "complete_demo",
            "quality": "medium"
        }
    }
    
    print(json.dumps(complete_tool, indent=2, ensure_ascii=False))
    print()
    
    print("💡 工具对比")
    print("-" * 40)
    print("✅ 细粒度工具优势：")
    print("  • 精确控制每个步骤")
    print("  • 可以单独重试失败的步骤")
    print("  • 支持复杂的自定义工作流")
    print("  • 更好的错误隔离和调试")
    print()
    print("✅ 便捷工具优势：")
    print("  • 简单易用，一键完成")
    print("  • 适合快速原型和简单场景")
    print("  • 向后兼容，无需学习成本")
    print()
    
    print("🎯 使用建议")
    print("-" * 40)
    print("• 初学者：使用 execute_manim_complete")
    print("• 高级用户：组合使用细粒度工具")
    print("• 生产环境：使用细粒度工具获得更好的控制")
    print("• 调试场景：使用细粒度工具逐步排查问题")

def print_tool_comparison():
    """打印工具对比表"""
    print("\n📋 工具功能对比表")
    print("=" * 80)
    
    tools_info = [
        ("create_script", "创建脚本", "脚本管理", "支持自定义路径和验证"),
        ("validate_script", "验证脚本", "脚本管理", "独立的安全性检查"),
        ("render_animation", "渲染动画", "渲染控制", "支持质量控制和预览"),
        ("find_videos", "查找视频", "文件管理", "灵活的搜索和模式匹配"),
        ("get_workspace_info", "工作区信息", "文件管理", "详细的统计和状态"),
        ("cleanup_files", "清理文件", "文件管理", "精确的清理控制"),
        ("execute_manim_complete", "完整工作流", "便捷工具", "一键完成，向后兼容"),
    ]
    
    print(f"{'工具名称':<25} {'功能':<12} {'分类':<12} {'特点'}")
    print("-" * 80)
    
    for tool_name, function, category, feature in tools_info:
        print(f"{tool_name:<25} {function:<12} {category:<12} {feature}")

if __name__ == "__main__":
    print_tool_demo()
    print_tool_comparison() 