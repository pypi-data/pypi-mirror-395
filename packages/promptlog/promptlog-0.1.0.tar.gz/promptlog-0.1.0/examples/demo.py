#!/usr/bin/env python3
"""
PromptLog 使用示例

这个文件展示了 PromptLog 库的各种功能，包括：
1. 创建和管理提示版本
2. 版本对比
3. 元数据记录和搜索
4. 版本历史管理
"""

from promptlog import PromptManager


def main():
    print("=== PromptLog 使用示例 ===\n")
    
    # 初始化 PromptManager
    pm = PromptManager("my_demo_project")
    print("已初始化 PromptManager，项目名称: my_demo_project")
    print(f"数据存储路径: {pm.storage_path}\n")
    
    # 创建第一个提示版本
    print("1. 创建第一个提示版本...")
    version1 = pm.save_prompt(
        name="customer_service_greeting",
        content="您好，欢迎联系我们的客户服务。请问有什么可以帮助您的吗？",
        description="初始客服问候语",
        author="张三",
        tags=["客服", "问候", "中文"]
    )
    print(f"   ✓ 创建成功，版本号: {version1}\n")
    
    # 创建第二个提示版本
    print("2. 创建第二个改进版本...")
    version2 = pm.save_prompt(
        name="customer_service_greeting",
        content="您好！欢迎联系我们的客户服务中心。我是您的专属客服助手，请问有什么可以帮助您的吗？",
        description="改进版客服问候语，增加了亲和力",
        author="李四",
        tags=["客服", "问候", "中文", "改进"]
    )
    print(f"   ✓ 创建成功，版本号: {version2}\n")
    
    # 创建第三个提示版本（英文版本）
    print("3. 创建第三个英文版本...")
    version3 = pm.save_prompt(
        name="customer_service_greeting",
        content="Hello! Welcome to our customer service center. I'm your dedicated service assistant. How may I help you today?",
        description="英文版本的客服问候语",
        author="王五",
        tags=["客服", "问候", "英文"]
    )
    print(f"   ✓ 创建成功，版本号: {version3}\n")
    
    # 列出所有版本
    print("4. 列出所有版本:")
    versions = pm.list_versions("customer_service_greeting")
    for v in versions:
        print(f"   版本 {v['version']} - {v['created_at']} - {v['author']} - {v['description']}")
    print()
    
    # 加载特定版本
    print("5. 加载版本 2 的内容:")
    prompt_v2 = pm.load_version("customer_service_greeting", version=2)
    print(f"   内容: {prompt_v2.content}")
    print(f"   描述: {prompt_v2.description}")
    print(f"   作者: {prompt_v2.author}")
    print(f"   标签: {prompt_v2.tags}")
    print(f"   创建时间: {prompt_v2.created_at}")
    print()
    
    # 对比两个版本
    print("6. 对比版本 1 和版本 2:")
    comparison = pm.compare_versions("customer_service_greeting", version1=1, version2=2)
    print(f"   版本 1: 作者 {comparison['version1']['author']}, 创建于 {comparison['version1']['created_at']}")
    print(f"   版本 2: 作者 {comparison['version2']['author']}, 创建于 {comparison['version2']['created_at']}")
    print(f"   差异: {comparison['differences']}")
    print()
    
    # 搜索提示
    print("7. 按标签搜索提示:")
    results = pm.search_prompts(tags=["客服"])
    for prompt_name, prompt_version in results:
        print(f"   {prompt_name} (版本 {prompt_version.version}): {prompt_version.content[:30]}...")
    
    print()
    print("8. 按作者搜索提示:")
    results = pm.search_prompts(author="李四")
    for prompt_name, prompt_version in results:
        print(f"   {prompt_name} (版本 {prompt_version.version}): {prompt_version.content[:30]}...")
    print()
    
    # 获取完整历史
    print("9. 获取完整的版本历史:")
    history = pm.get_prompt_history("customer_service_greeting")
    for i, prompt_version in enumerate(history, 1):
        print(f"   {i}. 版本 {prompt_version.version}")
        print(f"      内容: {prompt_version.content}")
        print(f"      作者: {prompt_version.author}")
        print(f"      描述: {prompt_version.description}")
        print(f"      标签: {prompt_version.tags}")
        print(f"      创建时间: {prompt_version.created_at}")
        print()
    
    print("=== 示例结束 ===")
    print("提示：您可以通过修改此文件来尝试不同的功能组合。")
    print("所有数据都存储在上面显示的路径中，您可以手动查看或删除这些数据。")


if __name__ == "__main__":
    main()
