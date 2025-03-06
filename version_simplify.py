import json
import os

def rename_fields():
    # 读取原始的 version.json 文件
    input_path = 'version.json'
    output_path = 'version_simplify.json'
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            
        # 处理每个主版本
        for main_version in data:
            version_list = main_version['version_list']
            # 处理每个具体版本
            for version in version_list:
                # 重命名字段
                version['code'] = version.pop('version_code')
                version['date'] = version.pop('version_build_date')
                version['hub'] = version.pop('unity_hub_url')
                # 移除不需要的字段
                version.pop('install_link', None)
                version.pop('releases_link', None)
        
        # 写入重命名后的文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            
        print(f"处理完成！重命名后的文件已保存为: {output_path}")
        print(f"原始文件大小: {os.path.getsize(input_path)} 字节")
        print(f"处理后文件大小: {os.path.getsize(output_path)} 字节")
        
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_path}")
    except Exception as e:
        print(f"处理过程中出现错误：{str(e)}")

if __name__ == '__main__':
    rename_fields()