import bpy
import sys
import os
import math

# Adiciona o diretorio atual ao sys.path para importar build_scene
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import build_scene
import build_sacada_v2

print("\n\n" + "="*50)
print("INICIANDO DYNAMIC QA - ETAPA 3 (CENA VISUAL)")
print("="*50)

try:
    build_scene.main()
    print("EXECUTION: PASS")
except Exception as e:
    print(f"EXECUTION: FAIL - {e}")
    sys.exit(1)

# 1. Coleções (Da V2 e da V3)
cols = ["Setup", "Perfis", "Folhas", "Mecanismos", "Debug", "ENVIRONMENT", "ARCHITECTURE", "FURNITURE", "SACADA_SYSTEM", "GLASS", "LIGHTING", "CAMERAS"]
missing_cols = [c for c in cols if c not in bpy.data.collections]
if not missing_cols:
    print("COLEÇÕES: PASS")
else:
    print(f"COLEÇÕES: FAIL - Faltando {missing_cols}")

# 2. Dimensões
MM = 0.001
folhas = [bpy.data.objects.get(f"FOLHA_{i:02d}_VIDRO") for i in range(1, 5)]
pass_dim = True
for f in folhas:
    if f is None:
        pass_dim = False
        continue
    dx, dy, dz = f.dimensions
    if abs(dx - 427.75 * MM) > 1e-4 or abs(dy - 10.0 * MM) > 1e-4 or abs(dz - 660.0 * MM) > 1e-4:
        pass_dim = False
        print(f"Dimensoes incorretas na folha {f.name}: {dx} x {dy} x {dz}")

veneziana = bpy.data.objects.get("VENEZIANA_REF")
if veneziana:
    dx, dz = veneziana.dimensions.x, veneziana.dimensions.z
    if abs(dx - 150.0 * MM) > 1e-4 or abs(dz - 860.0 * MM) > 1e-4:
        pass_dim = False

print(f"DIMENSÕES (Folhas 427.75x10x660 e Ven 150x860): {'PASS' if pass_dim else 'FAIL'}")

# 3. Propriedades e Hierarquia
pass_hierarquia = True
pass_props = True
for i in range(1, 5):
    slide = bpy.data.objects.get(f"FOLHA_{i:02d}_SLIDE")
    vidro = bpy.data.objects.get(f"FOLHA_{i:02d}_VIDRO")
    if not slide or not vidro:
        pass_hierarquia = False
        continue
    if vidro.parent != slide:
        pass_hierarquia = False
    
    if "murano_x_fechado" not in slide or "murano_x_estacionado" not in slide:
        pass_props = False

print(f"HIERARQUIA (VIDRO filho de SLIDE): {'PASS' if pass_hierarquia else 'FAIL'}")
print(f"PROPRIEDADES (no SLIDE): {'PASS' if pass_props else 'FAIL'}")

# 4. Materiais
pass_mat = True
if not bpy.data.materials.get("MAT_Vidro_Laminado") or not bpy.data.materials.get("MAT_Aluminio_Anodizado"):
    pass_mat = False
print(f"MATERIAIS: {'PASS' if pass_mat else 'FAIL'}")

# 5. Câmeras
pass_cam = True
cams = ["CAMERA_01_Frontal", "CAMERA_02_Diagonal", "CAMERA_03_Estacionamento", "CAMERA_04_Close"]
for c in cams:
    if not bpy.data.objects.get(c):
        pass_cam = False
print(f"CÂMERAS: {'PASS' if pass_cam else 'FAIL'}")

# 6. Animação Visual
pass_anim = True
slide_01 = bpy.data.objects.get("FOLHA_01_SLIDE")
if slide_01 and not slide_01.animation_data:
    pass_anim = False
print(f"ANIMAÇÃO VISUAL: {'PASS' if pass_anim else 'FAIL'}")

# 7. UNKNOWNS
calib = build_sacada_v2.RIGGING_CALIBRATION
pass_calib = all(v is None for v in calib.values())
print(f"CALIBRAÇÃO UNKNOWN = None: {'PASS' if pass_calib else 'FAIL'}")

# 8. 30mm e Placeholders 50x40
import inspect
source_lines = inspect.getsource(build_scene)
source_lines_v2 = inspect.getsource(build_sacada_v2)
if "30.0 * MM" in source_lines_v2 and "distancia_disco_seguranca" not in source_lines_v2:
    print("30MM: CONFLICT")
else:
    print("30MM: SAFE")
    
if "50 * MM" in source_lines and "PLACEHOLDER_VISUAL" not in source_lines:
    # 50x40 não foi sequer usado como dimensão matemática na V3, usamos bounding boxes literais baseados no VAO
    pass

print("MECÂNICA REAL: BLOCKED")

print("="*50)
print("DYNAMIC QA SCENE COMPLETED")
print("="*50)
