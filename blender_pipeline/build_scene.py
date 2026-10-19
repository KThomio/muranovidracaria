import bpy
import math
import sys
import os

# Importa a engine paramétrica validada da Etapa 2
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
import build_sacada_v2

# Reutilizar constantes matemáticas
MM = 0.001
VAO_LARGURA = 1900.0 * MM
VAO_ALTURA = 860.0 * MM

def setup_collections():
    # Mantém as coleções da V2 e adiciona as novas focadas em apresentação
    novas_cols = [
        "ENVIRONMENT", "ARCHITECTURE", "FURNITURE", "SACADA_SYSTEM", 
        "GLASS", "LIGHTING", "CAMERAS"
    ]
    for cname in novas_cols:
        if cname not in bpy.data.collections:
            col = bpy.data.collections.new(cname)
            bpy.context.scene.collection.children.link(col)

def create_materials():
    # MATERIAL 1: Vidro Laminado
    mat_glass = bpy.data.materials.new(name="MAT_Vidro_Laminado")
    mat_glass.use_nodes = True
    nodes = mat_glass.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.85, 0.95, 0.9, 1.0) # Tonalidade esverdeada
        # Para Eevee/Cycles vidro
        if 'Transmission Weight' in bsdf.inputs:
            bsdf.inputs['Transmission Weight'].default_value = 1.0 # Blender 4.0+
        elif 'Transmission' in bsdf.inputs:
            bsdf.inputs['Transmission'].default_value = 1.0 # Blender <4.0
        bsdf.inputs['Roughness'].default_value = 0.0
        bsdf.inputs['IOR'].default_value = 1.52

    # MATERIAL 2: Alumínio Anodizado Premium (Não Branco, RAL Escuro visual)
    mat_alu = bpy.data.materials.new(name="MAT_Aluminio_Anodizado")
    mat_alu.use_nodes = True
    nodes = mat_alu.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0) # Preto Fosco / Bronze escuro
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = 0.4

    # MATERIAL 3: Genérico para Sombras (Paredes/Base)
    mat_wall = bpy.data.materials.new(name="MAT_Architecture_ShadowCatcher")
    mat_wall.use_nodes = True
    nodes = mat_wall.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.9
        
    return mat_glass, mat_alu, mat_wall

def apply_materials(mat_glass, mat_alu):
    # Aplica Vidro nas Folhas
    for i in range(1, 5):
        vidro = bpy.data.objects.get(f"FOLHA_{i:02d}_VIDRO")
        if vidro:
            if len(vidro.data.materials) == 0:
                vidro.data.materials.append(mat_glass)
            else:
                vidro.data.materials[0] = mat_glass
            
            # Reorganiza o vidro visualmente na collection GLASS
            col_glass = bpy.data.collections.get("GLASS")
            if col_glass and vidro.name not in col_glass.objects:
                col_glass.objects.link(vidro)
    
    # Aplica Alumínio na Veneziana Fixa
    veneziana = bpy.data.objects.get("VENEZIANA_REF")
    if veneziana:
        if len(veneziana.data.materials) == 0:
            veneziana.data.materials.append(mat_alu)
        else:
            veneziana.data.materials[0] = mat_alu
            
    # Aplica Alumínio aos Placeholders de Trilho/Alojamento (apenas representação)
    for p in ["PLACEHOLDER_ALOJAMENTO", "PLACEHOLDER_PERFIL_LEITO"]:
        obj = bpy.data.objects.get(p)
        if obj and obj.type == 'MESH': # Só se for malha, empties não tem material
            if len(obj.data.materials) == 0:
                obj.data.materials.append(mat_alu)
            else:
                obj.data.materials[0] = mat_alu

def setup_lighting():
    col_light = bpy.data.collections.get("LIGHTING")
    
    # Key Light: Simulação de Overcast/Golden Hour Direcional
    light_data = bpy.data.lights.new(name="Sun_Exterior", type='SUN')
    light_data.energy = 2.5
    light_data.angle = math.radians(10.0) # Sombra mais difusa
    sun = bpy.data.objects.new(name="Sun_Exterior", object_data=light_data)
    if col_light: col_light.objects.link(sun)
    sun.location = (VAO_LARGURA/2, -10.0, 5.0)
    sun.rotation_euler = (math.radians(60), 0, math.radians(45))
    
    # Fill Light: Interior Quente (3000K)
    area_data = bpy.data.lights.new(name="Area_Interior_3000K", type='AREA')
    area_data.energy = 300.0
    area_data.color = (1.0, 0.8, 0.6) # Simulação 3000K
    area_data.size = 2.0
    area = bpy.data.objects.new(name="Area_Interior_3000K", object_data=area_data)
    if col_light: col_light.objects.link(area)
    area.location = (VAO_LARGURA/2, 2.0, VAO_ALTURA/2)
    area.rotation_euler = (math.radians(-90), 0, 0)

def setup_cameras():
    col_cam = bpy.data.collections.get("CAMERAS")
    
    # CAMERA 01 - Frontal Principal (50mm)
    cam1_data = bpy.data.cameras.new("CAMERA_01_Frontal")
    cam1_data.lens = 50
    cam1 = bpy.data.objects.new("CAMERA_01_Frontal", object_data=cam1_data)
    if col_cam: col_cam.objects.link(cam1)
    cam1.location = (VAO_LARGURA/2, -3.0, VAO_ALTURA/2)
    cam1.rotation_euler = (math.radians(90), 0, 0)
    
    # CAMERA 02 - Diagonal (50mm)
    cam2_data = bpy.data.cameras.new("CAMERA_02_Diagonal")
    cam2_data.lens = 50
    cam2 = bpy.data.objects.new("CAMERA_02_Diagonal", object_data=cam2_data)
    if col_cam: col_cam.objects.link(cam2)
    cam2.location = (-1.0, -2.5, VAO_ALTURA * 0.8)
    cam2.rotation_euler = (math.radians(75), 0, math.radians(-30))
    
    # CAMERA 03 - Estacionamento (Para focar no agrupamento visual)
    cam3_data = bpy.data.cameras.new("CAMERA_03_Estacionamento")
    cam3_data.lens = 50
    cam3 = bpy.data.objects.new("CAMERA_03_Estacionamento", object_data=cam3_data)
    if col_cam: col_cam.objects.link(cam3)
    cam3.location = (-0.5, -1.0, VAO_ALTURA * 0.5)
    cam3.rotation_euler = (math.radians(85), 0, math.radians(-60))
    
    # CAMERA 04 - Close-up Premium (85mm com DOF)
    cam4_data = bpy.data.cameras.new("CAMERA_04_Close")
    cam4_data.lens = 85
    cam4_data.dof.use_dof = True
    cam4_data.dof.focus_distance = 1.2
    cam4_data.dof.aperture_fstop = 2.8
    cam4 = bpy.data.objects.new("CAMERA_04_Close", object_data=cam4_data)
    if col_cam: col_cam.objects.link(cam4)
    cam4.location = (VAO_LARGURA * 0.8, -1.0, VAO_ALTURA * 0.3)
    cam4.rotation_euler = (math.radians(85), 0, math.radians(20))

def setup_architecture(mat_wall):
    col_arch = bpy.data.collections.get("ARCHITECTURE")
    
    # Guarda-corpo Abstrato (Base)
    bpy.ops.mesh.primitive_cube_add(size=1)
    base = bpy.context.active_object
    base.name = "PLACEHOLDER_VISUAL_GUARDA_CORPO"
    base.scale = (VAO_LARGURA * 1.5, 0.2, 1.0)
    base.location = (VAO_LARGURA/2, 0, -0.5)
    if len(base.data.materials) == 0: base.data.materials.append(mat_wall)
    if col_arch: col_arch.objects.link(base)
    bpy.context.scene.collection.objects.unlink(base)
    
    # Teto Abstrato
    bpy.ops.mesh.primitive_cube_add(size=1)
    teto = bpy.context.active_object
    teto.name = "PLACEHOLDER_VISUAL_TETO"
    teto.scale = (VAO_LARGURA * 1.5, 2.0, 0.2)
    teto.location = (VAO_LARGURA/2, 0, VAO_ALTURA + 0.1)
    if len(teto.data.materials) == 0: teto.data.materials.append(mat_wall)
    if col_arch: col_arch.objects.link(teto)
    bpy.context.scene.collection.objects.unlink(teto)

def setup_visual_animation():
    # Representação abstrata do movimento (Não é mecânica real)
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 200
    
    for i in range(1, 5):
        slide = bpy.data.objects.get(f"FOLHA_{i:02d}_SLIDE")
        if slide and "murano_x_fechado" in slide and "murano_x_estacionado" in slide:
            # SHOT 01 - Fechado (Frames 1 a 30)
            slide.location.x = slide["murano_x_fechado"]
            slide.keyframe_insert(data_path="location", index=0, frame=1)
            slide.keyframe_insert(data_path="location", index=0, frame=30)
            
            # SHOT 03 - Deslocamento Progressivo
            # SHOT 05 - Estacionadas
            frame_estacionar = 80 + (i * 20)
            slide.location.x = slide["murano_x_estacionado"]
            slide.keyframe_insert(data_path="location", index=0, frame=frame_estacionar)

def main():
    # 1. Executa a V2 Limpa (Engine Paramétrica Intocável)
    build_sacada_v2.create_sacada()
    
    # 2. Configura a camada superior de Apresentação (Visual)
    setup_collections()
    mat_glass, mat_alu, mat_wall = create_materials()
    apply_materials(mat_glass, mat_alu)
    setup_architecture(mat_wall)
    setup_lighting()
    setup_cameras()
    setup_visual_animation()
    
    print("ETAPA 3 SCENE BUILD COMPLETED: VISUAL ABSTRACTION READY")

if __name__ == "__main__":
    main()
