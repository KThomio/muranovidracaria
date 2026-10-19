import bpy
import sys
import os

# Adiciona o diretorio atual ao sys.path para importar build_sacada_v2
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import build_sacada_v2

print("\n\n" + "="*50)
print("INICIANDO DYNAMIC QA - ETAPA 2")
print("="*50)

# 1. Executa o script
try:
    build_sacada_v2.create_sacada()
    print("EXECUTION: PASS")
except Exception as e:
    print(f"EXECUTION: FAIL - {e}")
    sys.exit(1)

# 2. Colecoes
cols = ["Setup", "Perfis", "Folhas", "Mecanismos", "Debug"]
missing_cols = [c for c in cols if c not in bpy.data.collections]
if not missing_cols:
    print("COLEÇÕES: PASS")
else:
    print(f"COLEÇÕES: FAIL - Faltando {missing_cols}")

# 3. 4 Folhas Moveis e 4. Veneziana
folhas_m = [o for o in bpy.data.objects if o.name.startswith("FOLHA_") and o.name.endswith("_VIDRO")]
veneziana = bpy.data.objects.get("VENEZIANA_REF")

if len(folhas_m) == 4:
    print("4 FOLHAS: PASS")
else:
    print(f"4 FOLHAS: FAIL - Encontrado {len(folhas_m)}")

if veneziana:
    print("VENEZIANA: PASS")
else:
    print("VENEZIANA: FAIL")

# 5. Dimensoes das Folhas e 6. Veneziana
MM = 0.001
pass_dim = True
for f in folhas_m:
    dx, dy, dz = f.dimensions
    if abs(dx - 427.75 * MM) > 1e-4 or abs(dy - 10.0 * MM) > 1e-4 or abs(dz - 660.0 * MM) > 1e-4:
        pass_dim = False
        print(f"Dimensoes incorretas na folha {f.name}: {dx} x {dy} x {dz}")
if pass_dim and len(folhas_m) == 4:
    print("DIMENSÕES FOLHAS: PASS")
else:
    print("DIMENSÕES FOLHAS: FAIL")

if veneziana:
    dx, dz = veneziana.dimensions.x, veneziana.dimensions.z
    if abs(dx - 150.0 * MM) < 1e-4 and abs(dz - 860.0 * MM) < 1e-4:
        print("DIMENSÕES VENEZIANA: PASS")
    else:
        print(f"DIMENSÕES VENEZIANA: FAIL - {dx} x {dz}")

# 7. Propriedades e 8. Marcadores Visuais
pass_props = True
pass_markers = True
pass_movimento = True

for i in range(1, 5):
    slide = bpy.data.objects.get(f"FOLHA_{i:02d}_SLIDE")
    mec = bpy.data.objects.get(f"FOLHA_{i:02d}_CENTRO_MECANICO")
    if not slide:
        pass_props = False
        continue
    
    if "murano_x_fechado" not in slide or "murano_x_estacionado" not in slide:
        pass_props = False
    else:
        # Teste de Movimento (murano_x_fechado != murano_x_estacionado)
        if abs(slide["murano_x_fechado"] - slide["murano_x_estacionado"]) < 1e-5:
            pass_movimento = False

    if not mec:
        pass_markers = False

print(f"PROPRIEDADES: {'PASS' if pass_props else 'FAIL'}")
print(f"MARCADORES: {'PASS' if pass_markers else 'FAIL'}")
print(f"RIGGING VISUAL (DIFERENCA X): {'PASS' if pass_movimento else 'FAIL'}")

# 9. RIGGING_CALIBRATION
calib = build_sacada_v2.RIGGING_CALIBRATION
pass_calib = True
for k, v in calib.items():
    if v is not None:
        pass_calib = False
        print(f"CALIBRACAO INVALIDA: {k} = {v}")

print(f"CALIBRAÇÃO: {'PASS' if pass_calib else 'FAIL'}")

# 10. 30mm Rule
import inspect
source_lines = inspect.getsource(build_sacada_v2)
if "30.0 * MM" in source_lines and "distancia_disco_seguranca" not in source_lines:
    # Se aparecer sem explicacao
    print("30MM: CONFLICT")
else:
    print("30MM: SAFE")

print("MECÂNICA REAL: BLOCKED")

print("="*50)
print("DYNAMIC QA COMPLETED")
print("="*50)
