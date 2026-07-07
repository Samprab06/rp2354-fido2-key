import re
import sys

def modify_kicad_sch(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Rename RD+ to R6 and RD- to R7
    content = re.sub(r'"Reference" "RD\+"', '"Reference" "R6"', content)
    content = re.sub(r'\(reference "RD\+"', '(reference "R6"', content)
    
    content = re.sub(r'"Reference" "RD\-"', '"Reference" "R7"', content)
    content = re.sub(r'\(reference "RD\-"', '(reference "R7"', content)

    # 2. Change D1 footprint
    content = content.replace(
        '"Package_DFN_QFN:QFN-60-1EP_7x7mm_P0.4mm_EP3.4x3.4mm"', 
        '"Package_DFN_QFN:QFN-60-1EP_7x7mm_P0.4mm_EP3.4x3.4mm"' # just checking
    )
    content = content.replace(
        'LED_SMD:LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm',
        'LED_SMD:LED_WS2812B-2020_PLCC4_2.0x2.0mm'
    )
    
    # 3. Change global_label "dvdd" to "+3V3"
    content = re.sub(r'global_label "dvdd"', 'global_label "+3V3"', content)
    
    # 4. We will add footprints later in GUI or via specific targeted script
    # For C8, C9: let's change 15pf to 27pf
    # We will do this safely by looking for 15pf (since there are only two, and both need to be 27pf)
    content = re.sub(r'"Value" "15pf"', '"Value" "27pf"', content)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Modifications applied successfully.")

if __name__ == "__main__":
    modify_kicad_sch(sys.argv[1])
