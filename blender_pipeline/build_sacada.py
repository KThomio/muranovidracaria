import bpy
import bmesh
import mathutils

# ==============================================================================
# SACADA MURANO - PIPELINE 3D PARAMÉTRICA - ETAPA 1
# Fonte de Verdade: MURANO_3D_TECHNICAL_CONTEXT.md
#
# Classificação: DOCUMENTADO / DERIVADO / HIPOTESE_VISUAL / HIPOTESE_ANIMACAO / DESCONHECIDO.
# ==============================================================================

MM = 0.001

# ------------------------------------------------------------------------------
# 1. PARÂMETROS DOCUMENTADOS E DERIVADOS
# ------------------------------------------------------------------------------
VAO_LARGURA = 1900.0 * MM
VAO_ALTURA = 860.0 * MM
VENEZIANA_LARGURA = 150.0 * MM
QUANTIDADE_FOLHAS_MOVEIS = 4
ESPESSURA_VIDRO = 10.0 * MM

FOLGA_ALTURA_DESCONTO = 200.0 * MM
FOLGA_LATERAL_TOTAL = 30.0 * MM
FOLGA_POR_JUNCAO = 3.0 * MM

DISTANCIA_ENTRE_DISCOS_CONSECUTIVOS = 30.0 * MM

ALTURA_VIDRO = VAO_ALTURA - FOLGA_ALTURA_DESCONTO
_JUNCOES = QUANTIDADE_FOLHAS_MOVEIS - 1
LARGURA_FOLHA = (VAO_LARGURA - VENEZIANA_LARGURA - FOLGA_LATERAL_TOTAL - _JUNCOES * FOLGA_POR_JUNCAO) / QUANTIDADE_FOLHAS_MOVEIS

# ------------------------------------------------------------------------------
# 2. HIPÓTESES
# ------------------------------------------------------------------------------
VIDRO_Z_BASE_HIPOTESE = 100.0 * MM      # HIPOTESE_VISUAL
OFFSET_PIVO_Y_HIPOTESE = 5.0 * MM       # HIPOTESE_VISUAL
ORDEM_ABERTURA = [1, 2, 3, 4]           # HIPOTESE_ANIMACAO

# ------------------------------------------------------------------------------
# 3. DESCONHECIDOS (None)
# ------------------------------------------------------------------------------
OFFSET_PIVO_X = None
PARKING_OFFSET = None
DISCOS_DIRECAO = None
ALOJAMENTO_LARGURA = None
ALOJAMENTO_PROFUNDIDADE = None
ALOJAMENTO_OFFSET = None
SECAO_TRILHO_S = None
SECAO_TRILHO_I = None
SECAO_LEITO = None
SECAO_ANCORAGEM = None

# ==============================================================================
# SISTEMA DE COORDENADAS E UTILITÁRIOS
# ==============================================================================

def setup_blender_units():
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = 'METERS'

def purge_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for coll in bpy.data.collections:
        bpy.data.collections.remove(coll)

def create_collections():
    collections = {}
    master = bpy.context.scene.collection
    for name in ["Setup", "Perfis", "Folhas", "Mecanismos", "Debug"]:
        col = bpy.data.collections.new(name)
        master.children.link(col)
        collections[name] = col
    return collections

def tag_object(obj, origem, fonte=""):
    obj["murano_origem"] = origem
    if fonte:
        obj["murano_fonte"] = fonte

# ==============================================================================
# CONSTRUTORES DE GEOMETRIA
# ==============================================================================

def create_environment_proxy(cols):
    """Cria os proxies abstratos do Vão e Veneziana."""
    # Vão (plano)
    mesh = bpy.data.meshes.new("VAO_REF")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("VAO_REF", mesh)
    obj.scale = (VAO_LARGURA, 0.001, VAO_ALTURA)
    obj.location = (VAO_LARGURA/2, 0, VAO_ALTURA/2)
    obj.display_type = 'WIRE'
    tag_object(obj, "DOCUMENTADO", "Planta Murano")
    cols["Setup"].objects.link(obj)

    # Veneziana (plano)
    mesh_v = bpy.data.meshes.new("VENEZIANA_REF")
    bm_v = bmesh.new()
    bmesh.ops.create_cube(bm_v, size=1.0)
    bm_v.to_mesh(mesh_v)
    bm_v.free()
    obj_v = bpy.data.objects.new("VENEZIANA_REF", mesh_v)
    obj_v.scale = (VENEZIANA_LARGURA, 0.001, VAO_ALTURA)
    obj_v.location = (VAO_LARGURA - VENEZIANA_LARGURA/2, 0, VAO_ALTURA/2)
    obj_v.display_type = 'WIRE'
    tag_object(obj_v, "DOCUMENTADO", "Planta Murano")
    cols["Perfis"].objects.link(obj_v)

def build_profile_guides(cols):
    """Cria linhas-guia ou empties para os perfis sem seção inventada."""
    # Trilhos S e I como empties tipo Single Arrow
    ts = bpy.data.objects.new("TRILHO_S_GUIA", None)
    ts.empty_display_type = 'SINGLE_ARROW'
    ts.empty_display_size = 0.5
    ts.location = (VAO_LARGURA/2, 0, VAO_ALTURA)
    tag_object(ts, "DESCONHECIDO", "Seção não documentada")
    cols["Perfis"].objects.link(ts)

    ti = bpy.data.objects.new("TRILHO_I_GUIA", None)
    ti.empty_display_type = 'SINGLE_ARROW'
    ti.empty_display_size = 0.5
    ti.location = (VAO_LARGURA/2, 0, 0)
    tag_object(ti, "DESCONHECIDO", "Seção não documentada")
    cols["Perfis"].objects.link(ti)

def build_sheet_rig(cols):
    """Cria a hierarquia de folhas com parâmetros tolerantes a None."""
    sheets_x_start = []
    current_x = 15.0 * MM
    for i in range(QUANTIDADE_FOLHAS_MOVEIS):
        sheets_x_start.append(current_x)
        current_x += LARGURA_FOLHA + FOLGA_POR_JUNCAO

    pivot_x_efetivo = OFFSET_PIVO_X if OFFSET_PIVO_X is not None else 0.0
    pivot_status = "DOCUMENTADO" if OFFSET_PIVO_X is not None else "NAO_CALIBRADO"
    
    pivot_y_efetivo = OFFSET_PIVO_Y_HIPOTESE
    z_base = VIDRO_Z_BASE_HIPOTESE

    for i in range(QUANTIDADE_FOLHAS_MOVEIS):
        idx = i + 1
        x_base = sheets_x_start[i]

        # 1. SLIDE (Translada em X)
        slide_name = f"FOLHA_{idx:02d}_SLIDE"
        slide = bpy.data.objects.new(slide_name, None)
        slide.empty_display_type = 'PLAIN_AXES'
        slide.location = (x_base + pivot_x_efetivo, pivot_y_efetivo, z_base)
        tag_object(slide, "DERIVADO")
        cols["Folhas"].objects.link(slide)

        # 2. PIVOT (Gira em Z)
        pivot_name = f"FOLHA_{idx:02d}_PIVOT"
        pivot = bpy.data.objects.new(pivot_name, None)
        pivot.empty_display_type = 'ARROWS'
        pivot.empty_display_size = 0.2
        pivot.parent = slide
        tag_object(pivot, pivot_status)
        cols["Folhas"].objects.link(pivot)

        # 3. VIDRO (Mesh)
        vidro_name = f"FOLHA_{idx:02d}_VIDRO"
        mesh = bpy.data.meshes.new(vidro_name)
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        for v in bm.verts:
            v.co.x = (v.co.x + 0.5) * LARGURA_FOLHA - pivot_x_efetivo
            v.co.y = (v.co.y + 0.5) * ESPESSURA_VIDRO - ESPESSURA_VIDRO/2 - pivot_y_efetivo
            v.co.z = (v.co.z + 0.5) * ALTURA_VIDRO
            
        bm.to_mesh(mesh)
        bm.free()
        
        vidro = bpy.data.objects.new(vidro_name, mesh)
        vidro.parent = pivot
        tag_object(vidro, "DERIVADO")
        vidro["murano_centro_local"] = [LARGURA_FOLHA/2 - pivot_x_efetivo, 0.0 - pivot_y_efetivo, ALTURA_VIDRO/2]
        cols["Folhas"].objects.link(vidro)

        # 4. DISCOS E ALOJAMENTOS (Mecanismos)
        disco_sup = bpy.data.objects.new(f"FOLHA_{idx:02d}_DISCO_SUP", None)
        disco_sup.empty_display_type = 'CIRCLE'
        disco_sup.empty_display_size = 0.05
        disco_sup.parent = pivot
        disco_sup.location = (0, 0, ALTURA_VIDRO)
        tag_object(disco_sup, "DESCONHECIDO")
        cols["Mecanismos"].objects.link(disco_sup)

        disco_inf = bpy.data.objects.new(f"FOLHA_{idx:02d}_DISCO_INF", None)
        disco_inf.empty_display_type = 'CIRCLE'
        disco_inf.empty_display_size = 0.05
        disco_inf.parent = pivot
        disco_inf.location = (0, 0, 0)
        tag_object(disco_inf, "DESCONHECIDO")
        cols["Mecanismos"].objects.link(disco_inf)

def build_alojamentos(cols):
    """Alojamentos genéricos."""
    for i in range(QUANTIDADE_FOLHAS_MOVEIS):
        idx = i + 1
        aloj = bpy.data.objects.new(f"ALOJAMENTO_{idx:02d}", None)
        aloj.empty_display_type = 'CUBE'
        aloj.empty_display_size = 0.1
        offset = ALOJAMENTO_OFFSET if ALOJAMENTO_OFFSET is not None else 0
        aloj.location = (offset, 0, VAO_ALTURA)
        tag_object(aloj, "DESCONHECIDO")
        cols["Mecanismos"].objects.link(aloj)

# ==============================================================================
# VALIDAÇÃO E EXECUÇÃO
# ==============================================================================
def validate_all(cols):
    print("\n--- RELATÓRIO DE VALIDAÇÃO DA ETAPA 1 ---")
    vidros = [obj for obj in cols["Folhas"].objects if obj.type == 'MESH']
    print(f"[{'PASS' if len(vidros) == 4 else 'FAIL'}] Quantidade de folhas móveis: {len(vidros)}")
    
    if len(vidros) > 0:
        v = vidros[0]
        dim_x = v.dimensions.x
        dim_y = v.dimensions.y
        dim_z = v.dimensions.z
        pass_x = abs(dim_x - 427.75 * MM) < 1e-5
        pass_y = abs(dim_y - 10.0 * MM) < 1e-5
        pass_z = abs(dim_z - 660.0 * MM) < 1e-5
        print(f"[{'PASS' if pass_x and pass_y and pass_z else 'FAIL'}] Dimensões do vidro: {dim_x*1000:.2f} x {dim_y*1000:.2f} x {dim_z*1000:.2f} mm")
    
    v_ref = cols["Perfis"].objects.get("VENEZIANA_REF")
    if v_ref:
        pass_vz = abs(v_ref.dimensions.x - 150.0 * MM) < 1e-5 and abs(v_ref.dimensions.z - 860.0 * MM) < 1e-5
        print(f"[{'PASS' if pass_vz else 'FAIL'}] Veneziana: {v_ref.dimensions.x*1000:.2f} x {v_ref.dimensions.z*1000:.2f} mm")
    
    pivo_status = "NAO_CALIBRADO" if OFFSET_PIVO_X is None else "CALIBRADO"
    print(f"[{'PASS' if pivo_status == 'NAO_CALIBRADO' else 'WARNING'}] OFFSET_PIVO_X: {pivo_status}")
    print(f"[{'PASS' if PARKING_OFFSET is None else 'WARNING'}] PARKING_OFFSET: {'DESCONHECIDO' if PARKING_OFFSET is None else 'CALIBRADO'}")
    print("-----------------------------------------")

def main():
    setup_blender_units()
    purge_scene()
    cols = create_collections()
    
    create_environment_proxy(cols)
    build_profile_guides(cols)
    build_sheet_rig(cols)
    build_alojamentos(cols)
    
    validate_all(cols)

# Executa o código incondicionalmente para funcionar com exec() e Text Editor
try:
    main()
except Exception as e:
    print("Erro durante a execução do build_sacada.py:", e)
