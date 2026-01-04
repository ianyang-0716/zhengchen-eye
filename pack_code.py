import os

# 1. 定义我们关心的核心代码目录
# 我们只看 main 目录下的逻辑，忽略 external components
TARGET_DIRS = [
    "main",
]

# 2. 定义根目录下需要包含的配置文件
ROOT_FILES = [
    "CMakeLists.txt",
    "sdkconfig.defaults",
    "sdkconfig.defaults.esp32s3",
    "README.md",
    "dependencies.lock"
]

# 3. 定义需要过滤掉的“噪音”目录
# main/assets 里通常是图片转换成的巨型 C 数组，不需要给 AI 看
# managed_components 是官方库，不需要看
IGNORE_DIRS = {
    "assets", 
    "srmodels", 
    "managed_components", 
    "build", 
    ".cache", 
    ".git", 
    ".vscode", 
    "docs",
    "build"
}

# 4. 定义需要提取的文件后缀
EXTENSIONS = {'.c', '.cc', '.cpp', '.h', '.hpp', '.txt', '.json', '.yml', '.md', '.projbuild'}

output_file = "zhengchen_code_context.txt"

def is_ignored(path):
    parts = path.split(os.sep)
    for part in parts:
        if part in IGNORE_DIRS:
            return True
    return False

print("正在提取核心代码...")

with open(output_file, 'w', encoding='utf-8') as outfile:
    # 1. 先添加根目录的关键配置
    for filename in ROOT_FILES:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    outfile.write(f"\n\n--- FILE: {filename} ---\n\n")
                    outfile.write(f.read())
            except Exception as e:
                print(f"Skipping {filename}: {e}")

    # 2. 遍历 main 目录
    for target_dir in TARGET_DIRS:
        if not os.path.exists(target_dir):
            continue
            
        for root, dirs, files in os.walk(target_dir):
            # 修改 dirs 列表以跳过忽略的目录 (原地修改)
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if os.path.splitext(file)[1] in EXTENSIONS:
                    full_path = os.path.join(root, file)
                    
                    # 二次检查路径是否包含被忽略的关键词
                    if is_ignored(full_path):
                        continue

                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # 简单的过滤：如果文件太大（比如超过100KB），可能是未过滤掉的资源数组，跳过
                            if len(content) > 100000: 
                                print(f"Skipping large file: {full_path}")
                                continue
                                
                            outfile.write(f"\n\n--- FILE: {full_path} ---\n\n")
                            outfile.write(content)
                            outfile.write(f"\n\n--- END OF FILE: {full_path} ---\n\n")
                    except Exception as e:
                        print(f"Error reading {full_path}: {e}")

print(f"完成！\n请将生成的 {output_file} 发送给我。")
print(f"该文件包含了所有 main 目录下的核心逻辑代码，但不包含图片资源和外部库。")