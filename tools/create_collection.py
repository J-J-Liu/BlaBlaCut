import json
import sys
import os
from pathlib import Path

def aggregate_papers_from_list(notes_list, docs_notes_repo_dir):
    """从论文名称列表中聚合论文数据"""
    aggregated_papers = []
    
    for note_name in notes_list:
        note_folder = docs_notes_repo_dir / note_name
        json_file = note_folder / "info.json"

        if not note_folder.exists():
            print(f"  [跳过] 找不到笔记文件夹: {note_name}")
            continue

        if not json_file.exists():
            print(f"  [跳过] 找不到 info.json: {note_name}")
            continue
        
        try:
            with open(json_file, 'r', encoding='utf-8') as jf:
                data = json.load(jf)
                # 统一处理列表或字典，并注入来源文件夹名
                if isinstance(data, dict):
                    data['_source_folder'] = note_name
                    aggregated_papers.append(data)
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            item['_source_folder'] = note_name
                    aggregated_papers.extend(data)
            print(f"  [成功] 已合并: {note_name}")
        except Exception as e:
            print(f"  [错误] 读取 {note_name} 失败: {e}")
    
    return aggregated_papers

def generate_collection_data():
    print("--- MkDocs 集合数据与页面生成工具 ---")
    
    # 1. 确定配置文件路径
    script_dir = Path(__file__).resolve().parent
    
    # 默认检查脚本同级目录，或者接受命令行参数
    config_path = script_dir / "collection_config.json"
    
    if len(sys.argv) > 1:
        user_arg_path = Path(sys.argv[1])
        # 如果是相对路径，基于当前工作目录解析
        config_path = user_arg_path.resolve() if user_arg_path.is_absolute() else (Path.cwd() / user_arg_path).resolve()

    if not config_path.exists():
        print(f"错误: 找不到配置文件: {config_path}")
        print("用法: python create_collection_page.py [配置文件路径]")
        return

    print(f"正在读取配置文件: {config_path}")

    # 2. 读取用户写好的配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print("错误: 配置文件格式不正确，请确保是标准的 JSON 格式。")
        return
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return

    # 获取配置项
    target_dir = config_path.parent
    collection_title = config.get("title")
    collection_description = config.get("description", "") # 获取描述，默认为空
    
    # 检查是否有分类结构
    has_categories = "categories" in config and isinstance(config.get("categories"), list) and len(config.get("categories", [])) > 0
    notes_list = config.get("papers", [])  # 向后兼容：如果没有分类，使用 papers

    if not collection_title:
        print("错误: 配置文件中缺少 'title' (集合标题)。")
        return
    
    if not has_categories and not notes_list:
        print("警告: 配置文件中既没有 'categories' 也没有 'papers' (论文列表) 为空。")

    # 3. 确定数据源目录
    # 假设论文笔记位于脚本目录同级的 ../docs/notes_repo
    docs_notes_repo_dir = (script_dir / "../docs/notes_repo").resolve()

    if not docs_notes_repo_dir.exists():
        print(f"错误: 无法找到论文笔记源目录: {docs_notes_repo_dir}")
        return

    print(f"目标位置: {target_dir}")
    print(f"数据来源: {docs_notes_repo_dir}")

    # 4. 聚合数据
    print(f"\n开始为集合 '{collection_title}' 查找并合并数据...")
    
    if has_categories:
        # 按分类处理
        categories_data = []
        
        for category in config.get("categories", []):
            cat_title = category.get("title", "未命名分类")
            cat_description = category.get("description", "")
            cat_papers_list = category.get("papers", [])
            
            print(f"\n处理分类: {cat_title}")
            aggregated_papers = aggregate_papers_from_list(cat_papers_list, docs_notes_repo_dir)
            
            categories_data.append({
                "title": cat_title,
                "description": cat_description,
                "papers": aggregated_papers
            })
        
        # 构建最终的 JSON 数据结构（带分类）
        final_output = {
            "title": collection_title,
            "description": collection_description,
            "categories": categories_data
        }
        aggregated_papers = None  # 标记为分类模式
    else:
        # 单层结构（向后兼容）
        aggregated_papers = aggregate_papers_from_list(notes_list, docs_notes_repo_dir)
        
        # 构建最终的 JSON 数据结构（单层）
        final_output = {
            "title": collection_title,
            "description": collection_description,
            "papers": aggregated_papers
        }
        categories_data = None  # 标记为单层模式

    # 6. 保存 JSON 结果 (文件名改为 collected_info.json)
    output_json_path = target_dir / "collected_info.json"
    try:
        with open(output_json_path, 'w', encoding='utf-8') as out_f:
            json.dump(final_output, out_f, indent=4, ensure_ascii=False)
        print(f"\n[1/2] JSON 数据已保存至: {output_json_path}")
    except Exception as e:
        print(f"保存 JSON 文件失败: {e}")

    # 7. 生成 MkDocs Markdown 文件 (文件名改为 index.md)
    try:
        output_md_path = target_dir / "index.md"

        # 计算从目标目录(Markdown所在目录)到论文笔记目录的相对路径
        relative_path_to_notes = os.path.relpath(docs_notes_repo_dir, target_dir)
        relative_path_to_notes = Path(relative_path_to_notes).as_posix()

        md_content = []
        md_content.append(f"# {collection_title}")
        md_content.append("")
        
        # 如果有描述，显示描述
        if collection_description:
            md_content.append(collection_description)
            md_content.append("")

        # 生成论文条目的辅助函数
        def generate_paper_entry(paper, md_content, heading_level=2):
            # 提取字段
            p_title = paper.get('paper_title', paper.get('title', 'Unknown Title'))
            desc = paper.get('description', '暂无描述')
            source_folder = paper.get('_source_folder', '')
            
            # 提取 metadata
            meta = paper.get('metadata', {})
            
            # 鲁棒性处理：Authors
            authors_raw = meta.get('authors', [])
            if isinstance(authors_raw, list):
                authors = ", ".join([str(x) for x in authors_raw if x])
            else:
                authors = str(authors_raw) if authors_raw else "Unknown Authors"

            # 鲁棒性处理：Affiliations
            affiliations_raw = meta.get('affiliations', [])
            if isinstance(affiliations_raw, list):
                affiliations = ", ".join([str(x) for x in affiliations_raw if x])
            else:
                affiliations = str(affiliations_raw) if affiliations_raw else ""
                
            # 鲁棒性处理：Venue & Year
            venue = str(meta.get('venue', 'Unknown Venue')).strip()
            year = str(meta.get('year', '')).strip()
            
            # 提取和处理 DOI
            doi_raw = meta.get('doi')
            doi = None
            if doi_raw and str(doi_raw).strip().lower() not in ['null', 'none', '']:
                doi_str = str(doi_raw).strip()
                # 如果 DOI 包含完整 URL，提取 DOI 部分
                if doi_str.startswith('http://doi.org/') or doi_str.startswith('https://doi.org/'):
                    doi = doi_str.split('doi.org/')[-1]
                elif doi_str.startswith('doi:'):
                    doi = doi_str.replace('doi:', '').strip()
                else:
                    doi = doi_str
            
            # 构建路径
            base_link = f"{relative_path_to_notes}/{source_folder}"

            # 构建 Markdown 内容块（根据 heading_level 动态生成标题级别）
            heading_prefix = "#" * heading_level
            md_content.append(f"{heading_prefix} {p_title}")
            md_content.append(f"> **Authors:** {authors}  ")
            
            if affiliations:
                md_content.append(f"> **Affiliations:** {affiliations}  ")
                
            md_content.append(f"> **Venue:** {venue} {year}")
            md_content.append("")
            md_content.append(f"{desc}")
            md_content.append("")
            
            links = []
            links.append(f"[📄 论文笔记]({base_link}/paper_notes.md)")
            links.append(f"[📊 图表解析]({base_link}/figs_notes.md)")
            links.append(f"[👶 ELI5 解释]({base_link}/ELI5_notes.md)")
            
            # 如果 DOI 有效，添加直达原文链接（使用 HTML 格式以在新标签页打开）
            if doi:
                links.append(f'<a href="https://doi.org/{doi}" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>')
            
            md_content.append(" | ".join(links))
            md_content.append("")
            md_content.append("---")
            md_content.append("")

        if has_categories:
            # 按分类组织显示
            total_papers_count = sum(len(cat.get("papers", [])) for cat in categories_data)
            md_content.append(f"本页面共收录了 {total_papers_count} 篇论文笔记，分为 {len(categories_data)} 个分类。")
            md_content.append("")
            
            for category in categories_data:
                cat_title = category.get("title", "未命名分类")
                cat_description = category.get("description", "")
                cat_papers = category.get("papers", [])
                
                md_content.append(f"## {cat_title}")
                md_content.append("")
                
                if cat_description:
                    md_content.append(cat_description)
                    md_content.append("")
                
                md_content.append(f"*本分类包含 {len(cat_papers)} 篇论文*")
                md_content.append("")
                
                for paper in cat_papers:
                    generate_paper_entry(paper, md_content, heading_level=3)
        else:
            # 单层结构显示（向后兼容）
            md_content.append(f"本页面共收录了 {len(aggregated_papers)} 篇论文笔记。")
            md_content.append("")
            
            for paper in aggregated_papers:
                generate_paper_entry(paper, md_content)

        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_content))
        
        if has_categories:
            total_count = sum(len(cat.get("papers", [])) for cat in categories_data)
            print(f"[2/2] Markdown 页面已生成至: {output_md_path}")
            print(f"\n处理完成！共包含 {len(categories_data)} 个分类，{total_count} 篇论文。")
        else:
            print(f"[2/2] Markdown 页面已生成至: {output_md_path}")
            print(f"\n处理完成！共包含 {len(aggregated_papers)} 篇论文。")
        
    except Exception as e:
        print(f"生成 Markdown 文件失败: {e}")

if __name__ == "__main__":
    generate_collection_data()