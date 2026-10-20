import bpy
import math
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
import build_sacada_v2

PROJECT_ROOT = os.path.normpath(os.path.join(current_dir, ".."))
MM = 0.001

# ------------------------------------------------------------------
# DADOS OFICIAIS (MURANO_3D_TECHNICAL_CONTEXT.md + Prancha Técnica)
# ------------------------------------------------------------------
VAO_LARGURA = 1900.0 * MM          # 1900 mm
VAO_ALTURA = 860.0 * MM            # 860 mm
VENEZIANA_LARGURA = 150.0 * MM     # 150 mm
VENEZIANA_ALTURA = 860.0 * MM      # 860 mm
FOLHAS_QTD = 4                     # 4 folhas
FOLHA_LARGURA = 427.75 * MM        # 427.75 mm
VIDRO_ALTURA = 660.0 * MM          # 660 mm
VIDRO_ESPESSURA = 10.0 * MM        # 10 mm (Laminado 5+5)
FOLGA_LATERAL = 15.0 * MM
FOLGA_JUNCAO = 3.0 * MM

TRILHO_COMPRIMENTO = VAO_LARGURA   # 1900 mm
TRILHO_ALTURA = 60.0 * MM          # 60 mm
TRILHO_PROFUNDIDADE = 45.0 * MM    # 45 mm (Perfil U com canal de 24 mm)
LEITO_ALTURA = 40.0 * MM           # 40 mm
LEITO_PROFUNDIDADE = 24.0 * MM     # 24 mm
VENEZIANA_PASSO_ALETA = 30.0 * MM  # 30 mm (Norma NBR 13.303)


def setup_engine():
    scn = bpy.context.scene
    scn.render.engine = 'CYCLES'
    scn.cycles.device = 'CPU'
    scn.cycles.samples = 64
    scn.cycles.use_denoising = True
    scn.render.film_transparent = False
    scn.render.resolution_x = 1920
    scn.render.resolution_y = 1080
    scn.view_settings.view_transform = 'AgX' if 'AgX' in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items.keys() else 'Filmic'
    scn.view_settings.look = 'Medium High Contrast'

    try:
        scn.eevee.use_raytracing = True
        scn.eevee.taa_render_samples = 16
    except Exception:
        pass


def setup_collections():
    for cname in ["SACADA_SYSTEM", "ARCH_ENVIRONMENT", "LIGHTING", "CAMERAS"]:
        if cname not in bpy.data.collections:
            col = bpy.data.collections.new(cname)
            bpy.context.scene.collection.children.link(col)


def _box(name, size, loc, mat, col, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    obj.location = loc
    if mat:
        obj.data.materials.append(mat)
    if col:
        col.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)
    if parent:
        obj.parent = parent
    return obj


def _cylinder(name, radius, depth, loc, rot, mat, col, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    if col:
        col.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)
    if parent:
        obj.parent = parent
    return obj


def create_materials():
    # 1. Vidro Laminado Incolor 5+5 Cristalino Fotorrealista (Zero neon, Alta Fidelidade)
    mat_glass = bpy.data.materials.new(name="MAT_Vidro_Laminado_Incolor")
    mat_glass.use_nodes = True
    nt_g = mat_glass.node_tree
    bsdf_g = nt_g.nodes.get("Principled BSDF")
    if bsdf_g:
        # Vidro incolor neutro com leve borda esverdeada natural de óxido de ferro
        bsdf_g.inputs['Base Color'].default_value = (0.97, 0.99, 0.98, 1.0)
        if 'Transmission Weight' in bsdf_g.inputs:
            bsdf_g.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in bsdf_g.inputs:
            bsdf_g.inputs['Transmission'].default_value = 1.0
        bsdf_g.inputs['Roughness'].default_value = 0.005
        bsdf_g.inputs['IOR'].default_value = 1.52
        if 'Specular IOR Level' in bsdf_g.inputs:
            bsdf_g.inputs['Specular IOR Level'].default_value = 0.95

    try:
        mat_glass.surface_render_method = 'BLENDED'
        mat_glass.use_raytrace_refraction = True
        mat_glass.refraction_depth = VIDRO_ESPESSURA
    except Exception:
        pass

    # 2. Alumínio Estrutural Preto Fosco RAL 9005 Microtexturizado
    mat_alu = bpy.data.materials.new(name="MAT_Aluminio_Preto_RAL9005")
    mat_alu.use_nodes = True
    bsdf_alu = mat_alu.node_tree.nodes.get("Principled BSDF")
    if bsdf_alu:
        bsdf_alu.inputs['Base Color'].default_value = (0.025, 0.025, 0.028, 1.0)
        bsdf_alu.inputs['Metallic'].default_value = 0.88
        bsdf_alu.inputs['Roughness'].default_value = 0.28

    # 3. Escovas de Vedação 5x6 (Feltro preto de vedação interna)
    mat_escova = bpy.data.materials.new(name="MAT_Escova_Vedacao_5x6")
    mat_escova.use_nodes = True
    bsdf_esc = mat_escova.node_tree.nodes.get("Principled BSDF")
    if bsdf_esc:
        bsdf_esc.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1.0)
        bsdf_esc.inputs['Metallic'].default_value = 0.05
        bsdf_esc.inputs['Roughness'].default_value = 0.90

    # 4. Latão / Inox Mecânico (Pivôs, Discos e Pinos de Giro)
    mat_pivo = bpy.data.materials.new(name="MAT_Pivo_Inox_Latao")
    mat_pivo.use_nodes = True
    bsdf_pivo = mat_pivo.node_tree.nodes.get("Principled BSDF")
    if bsdf_pivo:
        bsdf_pivo.inputs['Base Color'].default_value = (0.85, 0.75, 0.52, 1.0)
        bsdf_pivo.inputs['Metallic'].default_value = 0.95
        bsdf_pivo.inputs['Roughness'].default_value = 0.18

    # 5. Concreto / Alvenaria da Varanda Arquitetônica
    mat_wall = bpy.data.materials.new(name="MAT_Alvenaria_Varanda")
    mat_wall.use_nodes = True
    bsdf_w = mat_wall.node_tree.nodes.get("Principled BSDF")
    if bsdf_w:
        bsdf_w.inputs['Base Color'].default_value = (0.16, 0.17, 0.20, 1.0)
        bsdf_w.inputs['Metallic'].default_value = 0.0
        bsdf_w.inputs['Roughness'].default_value = 0.85

    # 6. Piso Porcelanato Escuro
    mat_floor = bpy.data.materials.new(name="MAT_Piso_Porcelanato_Varanda")
    mat_floor.use_nodes = True
    bsdf_fl = mat_floor.node_tree.nodes.get("Principled BSDF")
    if bsdf_fl:
        bsdf_fl.inputs['Base Color'].default_value = (0.04, 0.045, 0.055, 1.0)
        bsdf_fl.inputs['Metallic'].default_value = 0.15
        bsdf_fl.inputs['Roughness'].default_value = 0.12

    return mat_glass, mat_alu, mat_escova, mat_pivo, mat_wall, mat_floor


def setup_rail_profile_u(name, is_top, mat_alu, mat_escova, mat_pivo, col_sys):
    """Constrói o trilho usinado com rasgo/canal em 'U' real de 24mm de abertura interna,
    duas abas de 10.5mm, 2 escovas de vedação 5x6 e os 4 pivôs de alojamento à esquerda.
    """
    z_base = VAO_ALTURA - TRILHO_ALTURA / 2.0 if is_top else TRILHO_ALTURA / 2.0
    cx = VAO_LARGURA / 2.0
    half_th = 5.0 * MM
    wall_th = 10.5 * MM
    rail_obj = bpy.data.objects.new(name, None)
    rail_obj.location = (0, 0, 0)
    col_sys.objects.link(rail_obj)

    # 1. Base horizontal do perfil
    z_flange = z_base + (TRILHO_ALTURA / 2.0 - half_th / 2.0) if is_top else z_base - (TRILHO_ALTURA / 2.0 - half_th / 2.0)
    _box(f"{name}_BASE", (TRILHO_COMPRIMENTO, TRILHO_PROFUNDIDADE, half_th), (cx, 0, z_flange), mat_alu, col_sys, parent=rail_obj)

    # 2. Aba frontal e aba traseira formando o canal em U (abertura de 24mm interna)
    y_front = TRILHO_PROFUNDIDADE / 2.0 - wall_th / 2.0
    y_back = -y_front
    h_aba = TRILHO_ALTURA - half_th
    z_aba = z_base - half_th / 2.0 if is_top else z_base + half_th / 2.0

    _box(f"{name}_ABA_FRONT", (TRILHO_COMPRIMENTO, wall_th, h_aba), (cx, y_front, z_aba), mat_alu, col_sys, parent=rail_obj)
    _box(f"{name}_ABA_BACK", (TRILHO_COMPRIMENTO, wall_th, h_aba), (cx, y_back, z_aba), mat_alu, col_sys, parent=rail_obj)

    # 3. Frisos de Escova de Vedação 5x6 nas faces internas das abas
    esc_w = 4.0 * MM
    esc_h = 6.0 * MM
    y_esc_front = y_front - wall_th / 2.0 - esc_w / 2.0
    y_esc_back = y_back + wall_th / 2.0 + esc_w / 2.0
    z_esc = z_base - TRILHO_ALTURA / 2.0 + esc_h / 2.0 if is_top else z_base + TRILHO_ALTURA / 2.0 - esc_h / 2.0
    _box(f"{name}_ESCOVA_FRONT", (TRILHO_COMPRIMENTO, esc_w, esc_h), (cx, y_esc_front, z_esc), mat_escova, col_sys, parent=rail_obj)
    _box(f"{name}_ESCOVA_BACK", (TRILHO_COMPRIMENTO, esc_w, esc_h), (cx, y_esc_back, z_esc), mat_escova, col_sys, parent=rail_obj)

    # 4. Estação de Alojamento / Discos de Estacionamento Inox à Esquerda (x = 30mm, 60mm, 90mm, 120mm)
    if not is_top:
        for p_idx in range(4):
            px = 30.0 * MM + p_idx * 30.0 * MM
            _cylinder(f"PIVO_ALOJAMENTO_{p_idx+1:02d}", radius=5.0 * MM, depth=14.0 * MM,
                      loc=(px, 0, z_base + 6.0 * MM), rot=(0, 0, 0), mat=mat_pivo, col=col_sys, parent=rail_obj)

    return rail_obj


def setup_veneziana_3d(mat_alu, col_sys):
    """Constrói a Veneziana VZ 060-P064 oficial com moldura lateral e aletas 3D reais a cada 30mm."""
    vx = VAO_LARGURA - VENEZIANA_LARGURA / 2.0
    z_center = VAO_ALTURA / 2.0
    vz_parent = bpy.data.objects.new("VENEZIANA_COMPLETA_VZ060", None)
    vz_parent.location = (0, 0, 0)
    col_sys.objects.link(vz_parent)

    # Montantes laterais em alumínio preto
    mont_w = 12.0 * MM
    _box("VZ_MONTANTE_ESQ", (mont_w, TRILHO_PROFUNDIDADE, VIDRO_ALTURA), (VAO_LARGURA - VENEZIANA_LARGURA + mont_w / 2.0, 0, z_center), mat_alu, col_sys, parent=vz_parent)
    _box("VZ_MONTANTE_DIR", (mont_w, TRILHO_PROFUNDIDADE, VIDRO_ALTURA), (VAO_LARGURA - mont_w / 2.0, 0, z_center), mat_alu, col_sys, parent=vz_parent)

    # Aletas 3D horizontais com passo de 30mm e inclinação de 35 graus (NBR 13.303 ventilação)
    aleta_len = VENEZIANA_LARGURA - 2 * mont_w
    aleta_thick = 2.0 * MM
    aleta_prof = 32.0 * MM
    z_start = TRILHO_ALTURA + LEITO_ALTURA + 15.0 * MM
    z_end = VAO_ALTURA - TRILHO_ALTURA - LEITO_ALTURA - 10.0 * MM
    current_z = z_start

    idx = 1
    while current_z <= z_end:
        aleta = _box(f"VZ_ALETA_{idx:02d}", (aleta_len, aleta_prof, aleta_thick), (vx, 0, current_z), mat_alu, col_sys, parent=vz_parent)
        aleta.rotation_euler.x = math.radians(35)
        current_z += VENEZIANA_PASSO_ALETA
        idx += 1

    # Leitos superior e inferior da veneziana
    _box("VZ_LEITO_INF", (VENEZIANA_LARGURA, LEITO_PROFUNDIDADE, LEITO_ALTURA), (vx, 0, TRILHO_ALTURA + LEITO_ALTURA / 2.0), mat_alu, col_sys, parent=vz_parent)
    _box("VZ_LEITO_SUP", (VENEZIANA_LARGURA, LEITO_PROFUNDIDADE, LEITO_ALTURA), (vx, 0, VAO_ALTURA - TRILHO_ALTURA - LEITO_ALTURA / 2.0), mat_alu, col_sys, parent=vz_parent)

    # Marcador compatível com QA
    vz_ref = bpy.data.objects.get("VENEZIANA_REF")
    if vz_ref:
        vz_ref.scale = (0.001, 0.001, 0.001)
        vz_ref.location = (vx, 0, z_center)


def setup_arch_environment(mat_wall, mat_floor, mat_alu, mat_glass):
    """Constrói o ambiente arquitetônico completo: varanda, mureta de apoio, teto,
    paredes laterais e Guarda-Corpo GC-VARANDA (1930mm, 3 módulos de 610mm, vidro laminado incolor 8mm).
    """
    col_env = bpy.data.collections.get("ARCH_ENVIRONMENT")
    cx = VAO_LARGURA / 2.0

    # 1. Mureta de apoio de alvenaria sob o trilho inferior (altura 1.05m da laje)
    mureta_w = 2.20
    mureta_h = 1.05
    mureta_prof = 0.22
    _box("MURETA_APOIO", (mureta_w, mureta_prof, mureta_h), (cx, 0, -mureta_h / 2.0), mat_wall, col_env)

    # 2. Piso interno da varanda (revestido de porcelanato escuro com reflexo suave)
    _box("PISO_VARANDA", (3.20, 2.60, 0.05), (cx, -1.30, -mureta_h - 0.025), mat_floor, col_env)

    # 3. Teto / Viga Superior da varanda
    viga_h = 0.40
    _box("VIGA_SUPERIOR", (mureta_w, mureta_prof, viga_h), (cx, 0, VAO_ALTURA + viga_h / 2.0), mat_wall, col_env)

    # 4. Parede lateral esquerda (com o alojamento de recolhimento) e parede direita
    wall_thick = 0.25
    wall_prof = 2.20
    wall_h = VAO_ALTURA + viga_h + mureta_h
    _box("PAREDE_ESQUERDA", (wall_thick, wall_prof, wall_h), (-wall_thick / 2.0 - 0.01, -wall_prof / 2.0 + mureta_prof / 2.0, (VAO_ALTURA - mureta_h) / 2.0), mat_wall, col_env)
    _box("PAREDE_DIREITA", (wall_thick, wall_prof, wall_h), (VAO_LARGURA + wall_thick / 2.0 + 0.01, -wall_prof / 2.0 + mureta_prof / 2.0, (VAO_ALTURA - mureta_h) / 2.0), mat_wall, col_env)

    # 5. Guarda-Corpo GC-VARANDA (Prancha Oficial: 1930mm, 3 módulos de 610mm [V1 | V2 | V1])
    gc_parent = bpy.data.objects.new("GC_VARANDA_MODULOS", None)
    gc_parent.location = (0, 0, 0)
    col_env.objects.link(gc_parent)

    corrimao_h = 35.0 * MM
    corrimao_w = 50.0 * MM
    gc_z_topo = -0.02
    gc_alt_vidro = 0.85
    _box("GC_CORRIMAO", (1.93, corrimao_w, corrimao_h), (cx, 0.08, gc_z_topo - corrimao_h / 2.0), mat_alu, col_env, parent=gc_parent)

    # 4 colunas verticais divisórias de 610mm + 3 vidros laminados de 8mm
    for c_i in range(4):
        col_x = (cx - 1.93 / 2.0 + 0.05) + c_i * 0.61
        _box(f"GC_MONTANTE_{c_i+1}", (40.0 * MM, 40.0 * MM, gc_alt_vidro), (col_x, 0.08, gc_z_topo - gc_alt_vidro / 2.0), mat_alu, col_env, parent=gc_parent)

    for v_i in range(3):
        v_x = (cx - 1.93 / 2.0 + 0.05 + 0.305) + v_i * 0.61
        _box(f"GC_VIDRO_MODULO_{v_i+1}", (0.58, 8.0 * MM, gc_alt_vidro - 0.08), (v_x, 0.08, gc_z_topo - gc_alt_vidro / 2.0), mat_glass, col_env, parent=gc_parent)


def setup_leaves_and_leitos(mat_glass, mat_alu, mat_pivo):
    """Configura os vidros laminados incolores de 10mm com perfis leito chanfrados
    e pinos de giro cilíndricos visíveis a 30mm da extremidade."""
    col_sys = bpy.data.collections.get("SACADA_SYSTEM")
    offset_z = (VIDRO_ALTURA / 2.0) + (LEITO_ALTURA / 2.0)  # 350 mm

    for i in range(1, FOLHAS_QTD + 1):
        vidro = bpy.data.objects[f"FOLHA_{i:02d}_VIDRO"]
        vidro.modifiers.clear()
        bev = vidro.modifiers.new("Bevel", 'BEVEL')
        bev.width = 1.2 * MM
        bev.segments = 2
        vidro.data.materials.clear()
        vidro.data.materials.append(mat_glass)

        slide = bpy.data.objects[f"FOLHA_{i:02d}_SLIDE"]
        # Perfil Leito Superior e Inferior
        for tag, sz in (("SUP", +1.0), ("INF", -1.0)):
            l_obj = _box(f"FOLHA_{i:02d}_LEITO_{tag}", (FOLHA_LARGURA, LEITO_PROFUNDIDADE, LEITO_ALTURA),
                         (0, 0, sz * offset_z), mat_alu, col_sys, parent=slide)
            b = l_obj.modifiers.new("Bevel", 'BEVEL')
            b.width = 1.5 * MM
            b.segments = 2

        # Pino de Giro em Latão/Inox no eixo a 30mm da borda
        pivo_local_x = -FOLHA_LARGURA / 2.0 + 30.0 * MM
        _cylinder(f"FOLHA_{i:02d}_PINO_GIRO_INF", radius=4.5 * MM, depth=18.0 * MM,
                  loc=(pivo_local_x, 0, -offset_z - LEITO_ALTURA / 2.0), rot=(0, 0, 0), mat=mat_pivo, col=col_sys, parent=slide)
        _cylinder(f"FOLHA_{i:02d}_PINO_GIRO_SUP", radius=4.5 * MM, depth=18.0 * MM,
                  loc=(pivo_local_x, 0, +offset_z + LEITO_ALTURA / 2.0), rot=(0, 0, 0), mat=mat_pivo, col=col_sys, parent=slide)


def align_leaves():
    z_center = VAO_ALTURA / 2.0   # 430 mm
    offset_pivo = build_sacada_v2.obter_offset_pivo()
    dist_eixos = build_sacada_v2.obter_distancia_eixos()
    parking = build_sacada_v2.obter_parking_offset()

    info = {}
    for n in range(1, FOLHAS_QTD + 1):
        slide = bpy.data.objects[f"FOLHA_{n:02d}_SLIDE"]
        x_closed = FOLGA_LATERAL + (n - 1) * (FOLHA_LARGURA + FOLGA_JUNCAO) + FOLHA_LARGURA / 2.0
        x_park = parking + (n - 1) * dist_eixos
        slide.location.x = x_closed
        slide.location.z = z_center
        slide["murano_x_fechado"] = x_closed
        slide["murano_x_estacionado"] = x_park
        eixo = bpy.data.objects.get(f"EIXO_PIVO_FOLHA_{n:02d}")
        if eixo:
            eixo.location.x -= (FOLHA_LARGURA - 2.0 * offset_pivo)
        info[n] = (slide, x_closed, x_park)
    return info, offset_pivo


def setup_lighting():
    col_light = bpy.data.collections.get("LIGHTING")
    scn = bpy.context.scene
    world = scn.world
    if not world:
        world = bpy.data.worlds.new("World")
        scn.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()

    n_out = nt.nodes.new(type="ShaderNodeOutputWorld")
    n_sky = nt.nodes.new(type="ShaderNodeTexSky")
    n_sky.sky_type = 'HOSEK_WILKIE'
    n_sky.sun_direction = (0.5, 0.8, 0.4)
    n_sky.turbidity = 2.2

    n_bg = nt.nodes.new(type="ShaderNodeBackground")
    n_bg.inputs['Strength'].default_value = 1.25
    nt.links.new(n_sky.outputs['Color'], n_bg.inputs['Color'])
    nt.links.new(n_bg.outputs['Background'], n_out.inputs['Surface'])

    # 1. Luz Solar Natural Externa (Simulando o horizonte iluminado de Sorocaba)
    sun_data = bpy.data.lights.new(name="Sun_Exterior_Daylight", type='SUN')
    sun_data.energy = 4.2
    sun_data.angle = math.radians(1.5)
    sun_data.color = (1.0, 0.98, 0.93)
    sun_obj = bpy.data.objects.new("Sun_Exterior_Daylight", sun_data)
    col_light.objects.link(sun_obj)
    sun_obj.location = (2.5, 5.0, 4.0)
    sun_obj.rotation_euler = (math.radians(-42), math.radians(35), math.radians(-110))

    # 2. Key Light Suave Interna da Varanda Gourmet (Refletindo no teto e perfis)
    key_data = bpy.data.lights.new(name="Key_Interior_Ceiling", type='AREA')
    key_data.energy = 160.0
    key_data.size = 2.4
    key_data.color = (1.0, 0.96, 0.90)
    key_obj = bpy.data.objects.new("Key_Interior_Ceiling", key_data)
    col_light.objects.link(key_obj)
    key_obj.location = (VAO_LARGURA / 2.0, -1.8, VAO_ALTURA + 0.8)
    _point_at(key_obj, (VAO_LARGURA / 2.0, 0.0, VAO_ALTURA / 2.0))

    # 3. Rim Light Ciano Exclusivo Murano #2BD9E0 (Realce milimétrico das bordas de 10mm do vidro laminado)
    rim_data = bpy.data.lights.new(name="Rim_Cyan_Glass_Edge", type='AREA')
    rim_data.energy = 85.0
    rim_data.size = 2.0
    rim_data.color = (0.17, 0.85, 0.88)
    rim_obj = bpy.data.objects.new("Rim_Cyan_Glass_Edge", rim_data)
    col_light.objects.link(rim_obj)
    rim_obj.location = (0.2, 1.8, 0.5)
    _point_at(rim_obj, (0.35, 0.0, 0.43))


def _point_at(obj, target_loc):
    dx = target_loc[0] - obj.location.x
    dy = target_loc[1] - obj.location.y
    dz = target_loc[2] - obj.location.z
    dist_xy = math.hypot(dx, dy)
    obj.rotation_euler = (
        math.atan2(dist_xy, dz) if dist_xy else 0,
        0,
        math.atan2(-dx, dy)
    )


def setup_camera():
    col_cam = bpy.data.collections.get("CAMERAS")
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0.85, 0.0, 0.43))
    target = bpy.context.active_object
    target.name = "CAMERA_TARGET"
    col_cam.objects.link(target)
    bpy.context.scene.collection.objects.unlink(target)

    cdata = bpy.data.cameras.new("CAMERA_Cinematica_35mm")
    cdata.lens = 35.0
    cam = bpy.data.objects.new("CAMERA_Cinematica_35mm", cdata)
    col_cam.objects.link(cam)
    tt = cam.constraints.new(type='TRACK_TO')
    tt.target = target
    tt.track_axis = 'TRACK_NEGATIVE_Z'
    tt.up_axis = 'UP_Y'
    bpy.context.scene.camera = cam

    # Câmera cinematográfica suave: Frame 1 panorâmica -> Frame 240 foco no empilhamento à esquerda
    cam.location = (1.10, -2.25, 0.50)
    cam.keyframe_insert(data_path="location", frame=1)
    cam.location = (0.50, -1.85, 0.46)
    cam.keyframe_insert(data_path="location", frame=240)


def setup_compositor():
    scn = bpy.context.scene
    scn.render.film_transparent = False
    scn.use_nodes = True
    tree = getattr(scn, "node_tree", None)
    use_group = False
    if tree is None:
        tree = bpy.data.node_groups.new("MuranoCompositor", 'CompositorNodeTree')
        scn.compositing_node_group = tree
        use_group = True
    tree.nodes.clear()

    n_rl = tree.nodes.new('CompositorNodeRLayers')
    n_rl.location = (-200, 0)

    if use_group:
        tree.interface.new_socket("Image", in_out='OUTPUT', socket_type='NodeSocketColor')
        n_out = tree.nodes.new('NodeGroupOutput')
    else:
        n_out = tree.nodes.new('CompositorNodeComposite')
    n_out.location = (200, 0)

    tree.links.new(n_rl.outputs['Image'], n_out.inputs[0])


def setup_animation(info, offset_pivo):
    scn = bpy.context.scene
    scn.render.fps = 24
    scn.frame_start = 1
    scn.frame_end = 240
    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'BEZIER'

    SLOT, START, T_HOLD, T_TURN = 58, 6, 5, 20
    max_dist = max(abs(x_c - x_p) for (_, x_c, x_p) in info.values()) or 1.0
    a = FOLHA_LARGURA / 2.0 - offset_pivo

    def ease(t):
        return t * t * (3.0 - 2.0 * t)

    for n in sorted(info):
        slide, x_closed, x_park = info[n]
        f0 = START + (n - 1) * SLOT
        dist = abs(x_closed - x_park)
        t_slide = max(6, int(round(30 * dist / max_dist)))
        f_arr = f0 + t_slide
        f_t0 = f_arr + T_HOLD
        f_t1 = f_t0 + T_TURN

        def key(frame, x, y, rz):
            slide.location.x = x
            slide.location.y = y
            slide.rotation_euler.z = rz
            slide.keyframe_insert(data_path="location", index=0, frame=frame)
            slide.keyframe_insert(data_path="location", index=1, frame=frame)
            slide.keyframe_insert(data_path="rotation_euler", index=2, frame=frame)

        key(1, x_closed, 0.0, 0.0)
        key(f0, x_closed, 0.0, 0.0)
        key(f_arr, x_park, 0.0, 0.0)
        key(f_t0, x_park, 0.0, 0.0)
        for f in range(f_t0 + 2, f_t1 + 1, 2):
            th = -math.radians(90) * ease((f - f_t0) / float(T_TURN))
            key(f, x_park - a + a * math.cos(th), a * math.sin(th), th)
        key(f_t1, x_park - a, -a, -math.radians(90))
    scn.frame_set(1)


def main():
    print("=== INICIANDO BUILD SCENE V2 (PERFIS CAD REAIS + ARQUITETURA 1080P) ===")
    build_sacada_v2.create_sacada()
    setup_engine()
    setup_collections()
    mat_glass, mat_alu, mat_escova, mat_pivo, mat_wall, mat_floor = create_materials()

    col_sys = bpy.data.collections.get("SACADA_SYSTEM")
    setup_rail_profile_u("TRILHO_INF", is_top=False, mat_alu=mat_alu, mat_escova=mat_escova, mat_pivo=mat_pivo, col_sys=col_sys)
    setup_rail_profile_u("TRILHO_SUP", is_top=True, mat_alu=mat_alu, mat_escova=mat_escova, mat_pivo=mat_pivo, col_sys=col_sys)
    setup_veneziana_3d(mat_alu, col_sys)
    setup_arch_environment(mat_wall, mat_floor, mat_alu, mat_glass)
    info, offset_pivo = align_leaves()
    setup_leaves_and_leitos(mat_glass, mat_alu, mat_pivo)
    setup_lighting()
    setup_camera()
    setup_compositor()
    setup_animation(info, offset_pivo)

    print("VALIDATE SCENE OBJECTS")
    if len(bpy.data.objects) < 20:
        print("FAIL - OBJETOS INSUFICIENTES")
        sys.exit(1)

    filepath = os.path.join(PROJECT_ROOT, "murano_etapa3_1.blend")
    print(f"SALVANDO .BLEND EM: {filepath}")
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    print("CONFIRM SAVE: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
