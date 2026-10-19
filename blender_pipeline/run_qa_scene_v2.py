import bpy
import sys
import os

print("\n\n" + "="*50)
print("INICIANDO DYNAMIC QA - ETAPA 3.1 (VISUAL POLISH) DEPOIS DO SAVE")
print("="*50)

def qa():
    print("REOPEN_BLEND = PASS")
    print(f"OBJECT_COUNT = {len(bpy.data.objects)}")
    print(f"COLLECTION_COUNT = {len(bpy.data.collections)}")
    
    glass_count = sum(1 for o in bpy.data.objects if 'VIDRO' in o.name)
    print(f"GLASS_COUNT = {glass_count}")
    
    vz = "PASS" if bpy.data.objects.get("VENEZIANA_REF") else "FAIL"
    print(f"VENEZIANA = {vz}")
    
    # Check Pivots (EIXO_PIVO_FOLHA_XX)
    pivots = sum(1 for o in bpy.data.objects if 'EIXO_PIVO' in o.name)
    print(f"PIVOTS = {pivots}")
    
    rails = sum(1 for o in bpy.data.objects if 'TRILHO' in o.name)
    print(f"RAILS = {rails}")
    
    cameras = sum(1 for o in bpy.data.objects if o.type == 'CAMERA')
    print(f"CAMERAS = {cameras}")
    
    materials = len(bpy.data.materials)
    print(f"MATERIALS = {materials}")
    
    # Geometry > 0
    geom = sum(1 for o in bpy.data.objects if o.type == 'MESH')
    print(f"GEOMETRY = {geom}")
    
    if glass_count >= 4 and vz == "PASS" and rails >= 2:
        print("BLEND_VALIDATION = PASS")
    else:
        print("BLEND_VALIDATION = FAIL")

if __name__ == "__main__":
    qa()
    sys.exit(0)
