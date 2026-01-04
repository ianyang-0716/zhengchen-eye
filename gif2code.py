import sys
import os

# 配置：这里填你的 GIF 文件名
INPUT_GIF = "eye666.gif"  
OUTPUT_FILE = "happy.c"
VAR_NAME = "happy_map" 
STRUCT_NAME = "happy"  

def convert_gif_to_c():
    if not os.path.exists(INPUT_GIF):
        print(f"错误：找不到文件 {INPUT_GIF}")
        return

    with open(INPUT_GIF, 'rb') as f:
        data = f.read()

    file_size = len(data)
    
    c_code = []
    
    # 1. 头部包含
    c_code.append('#ifdef __has_include')
    c_code.append('    #if __has_include("lvgl.h")')
    c_code.append('        #ifndef LV_LVGL_H_INCLUDE_SIMPLE')
    c_code.append('            #define LV_LVGL_H_INCLUDE_SIMPLE')
    c_code.append('        #endif')
    c_code.append('    #endif')
    c_code.append('#endif')
    c_code.append('')
    c_code.append('#if defined(LV_LVGL_H_INCLUDE_SIMPLE)')
    c_code.append('    #include "lvgl.h"')
    c_code.append('#else')
    c_code.append('    #include "lvgl/lvgl.h"')
    c_code.append('#endif')
    c_code.append('')
    
    # 2. 数组定义
    c_code.append(f'const uint8_t {VAR_NAME}[] = {{')
    
    hex_data = []
    for i, byte in enumerate(data):
        hex_data.append(f"0x{byte:02x}")
        if (i + 1) % 16 == 0:
            c_code.append("    " + ", ".join(hex_data) + ",")
            hex_data = []
    
    if hex_data:
        c_code.append("    " + ", ".join(hex_data))
        
    c_code.append('};')
    c_code.append('')
    
    # 3. 结构体定义 (同时兼容 LVGL v8 和 v9)
    c_code.append(f'const lv_image_dsc_t {STRUCT_NAME} = {{')
    c_code.append('  .header.w = 0,')
    c_code.append('  .header.h = 0,')
    c_code.append(f'  .data_size = {file_size},')
    
    # 这里使用条件编译来处理版本差异
    c_code.append('#if LV_VERSION_CHECK(9, 0, 0)')
    c_code.append('  .header.cf = LV_COLOR_FORMAT_RAW,')
    c_code.append('  .header.magic = LV_IMAGE_HEADER_MAGIC,')
    c_code.append('#else')
    c_code.append('  .header.cf = LV_IMG_CF_RAW,')
    c_code.append('  .header.always_zero = 0,')
    c_code.append('#endif')
    
    c_code.append(f'  .data = {VAR_NAME},')
    c_code.append('};')

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(c_code))
        
    print(f"转换成功！已生成 {OUTPUT_FILE} (v8/v9兼容)")

if __name__ == "__main__":
    convert_gif_to_c()