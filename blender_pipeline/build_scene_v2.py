import bpy
import math
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
import build_sacada_v2

# ------------------------------------------------------------------
# DADOS (fonte: MURANO_3D_TECHNICAL_CONTEXT.md)
# ------------------------------------------------------------------
MM = 0.001
VAO_LARGURA = 1900.0 * MM          # DOCUMENTADO
VAO_ALTURA = 860.0 * MM            # DOCUMENTADO
VENEZIANA_LARGURA = 150.0 * MM     # DOCUMENTADO
VENEZIANA_ALTURA = 860.0 * MM      # DOCUMENTADO
FOLHAS_QTD = 4                     # DOCUMENTADO
FOLHA_LARGURA = 427.75 * MM        # DERIVADO
VIDRO_ALTURA = 660.0 * MM          # DERIVADO (VAO_MENOR - 200)
VIDRO_ESPESSURA = 10.0 * MM        # DOCUMENTADO
FOLGA_LATERAL = 15.0 * MM          # DOCUMENTADO (30 total, 15 por lado)
FOLGA_JUNCAO = 3.0 * MM            # DOCUMENTADO

# Trilhos: comprimento = vao (DOCUMENTADO). Secao transversal NAO documentada:
# RAIL_ALTURA = metade da deducao de 200 mm (VAO - 200) -> HIPOTESE, ajustavel.
TRILHO_COMPRIMENTO = VAO_LARGURA
RAIL_ALTURA_HIPOTESE = 100.0 * MM
RAIL_PROFUNDIDADE_HIPOTESE = 50.0 * MM

BACKPLATE = os.path.normpath(os.path.join(
    current_dir, "..", "assets", "images",
    "WhatsApp Image 2026-10-03 at 20.15.37(1).jpeg"))


def setup_engine():
    scn = bpy.context.scene
    scn.render.engine = 'CYCLES'
    scn.cycles.device = 'CPU'
    scn.cycles.samples = 32
    scn.cycles.use_denoising = True
    scn.render.film_transparent = True      # VFX: fundo transparente
    scn.render.resolution_x = 1280
    scn.render.resolution_y = 720
    # Standard: preserva as cores reais da fotografia no composite
    scn.view_settings.view_transform = 'Standard'
    scn.view_settings.look = 'None'


def setup_collections():
    for cname in ["SACADA_SYSTEM", "GLASS", "LIGHTING", "CAMERAS"]:
        if cname not in bpy.data.collections:
            col = bpy.data.collections.new(cname)
            bpy.context.scene.collection.children.link(col)


def create_materials():
    mat_glass = bpy.data.materials.new(name="MAT_Vidro_Laminado")
    mat_glass.use_nodes = True
    bsdf = mat_glass.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.55, 0.70, 0.66, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.0
        bsdf.inputs['IOR'].default_value = 1.52
        # Vidro semi-transparente por alpha: deixa a fotografia aparecer atraves dele
        if 'Alpha' in bsdf.inputs:
            bsdf.inputs['Alpha'].default_value = 0.18
    try:
        mat_glass.surface_render_method = 'BLENDED'
    except Exception:
        pass

    mat_alu = bpy.data.materials.new(name="MAT_Aluminio_Branco_RAL9003")
    mat_alu.use_nodes = True
    bsdf = mat_alu.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.70, 0.70, 0.68, 1.0)  # Branco RAL 9003
        bsdf.inputs['Metallic'].default_value = 0.6
        bsdf.inputs['Roughness'].default_value = 0.35
    return mat_glass, mat_alu


def setup_lighting():
    col_light = bpy.data.collections.get("LIGHTING")
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    bg = nodes.get("Background")
    sky = nodes.new(type="ShaderNodeTexSky")
    sky.sun_elevation = math.radians(35)
    sky.sun_rotation = math.radians(135)
    links.new(sky.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 0.12

    # Luz de preenchimento frontal (suave) para ler os perfis brancos
    area_data = bpy.data.lights.new(name="Area_Fill_Frontal", type='AREA')
    area_data.energy = 20.0
    area_data.size = 2.5
    area = bpy.data.objects.new(name="Area_Fill_Frontal", object_data=area_data)
    col_light.objects.link(area)
    area.location = (VAO_LARGURA / 2, -2.2, VAO_ALTURA + 0.6)
    area.rotation_euler = (math.radians(70), 0, 0)  # aponta para a sacada


def setup_cameras():
    col_cam = bpy.data.collections.get("CAMERAS")
    center = (VAO_LARGURA / 2, 0, VAO_ALTURA / 2)
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=center)
    target = bpy.context.active_object
    target.name = "CAMERA_TARGET"
    col_cam.objects.link(target)
    bpy.context.scene.collection.objects.unlink(target)

    def create_cam(name, lens, loc):
        cdata = bpy.data.cameras.new(name)
        cdata.lens = lens
        c = bpy.data.objects.new(name, object_data=cdata)
        col_cam.objects.link(c)
        c.location = loc
        tt = c.constraints.new(type='TRACK_TO')
        tt.target = target
        tt.track_axis = 'TRACK_NEGATIVE_Z'
        tt.up_axis = 'UP_Y'
        return c

    create_cam("CAMERA_01_Frontal", 50, (VAO_LARGURA / 2, -3.6, VAO_ALTURA / 2))
    create_cam("CAMERA_02_Diagonal", 50, (-0.8, -3.0, 0.75))
    bpy.context.scene.camera = bpy.data.objects["CAMERA_01_Frontal"]


def _box(name, size, loc, mat, col):
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    obj.location = loc
    obj.data.materials.append(mat)
    col.objects.link(obj)
    bpy.context.scene.collection.objects.unlink(obj)
    return obj


def setup_system_visuals(mat_glass, mat_alu):
    col_sys = bpy.data.collections.get("SACADA_SYSTEM")

    # Trilhos: 1900 mm. Inferior e superior; vidros encaixam entre eles.
    rail_size = (TRILHO_COMPRIMENTO, RAIL_PROFUNDIDADE_HIPOTESE, RAIL_ALTURA_HIPOTESE)
    for name, z in (("TRILHO_INF_PLACEHOLDER_VISUAL_ONLY", RAIL_ALTURA_HIPOTESE / 2),
                    ("TRILHO_SUP_PLACEHOLDER_VISUAL_ONLY", VAO_ALTURA - RAIL_ALTURA_HIPOTESE / 2)):
        r = _box(name, rail_size, (VAO_LARGURA / 2, 0, z), mat_alu, col_sys)
        bev = r.modifiers.new("Bevel", 'BEVEL')
        bev.width = 2 * MM
        bev.segments = 3

    # Veneziana fixa: 150 x 860 mm, extrema direita (x = 1750..1900 mm)
    vz = bpy.data.objects.get("VENEZIANA_REF")
    if vz:
        vz.scale = (VENEZIANA_LARGURA, 10.0 * MM, VENEZIANA_ALTURA)
        vz.location = (VAO_LARGURA - VENEZIANA_LARGURA / 2, 0, VENEZIANA_ALTURA / 2)
        vz.data.materials.clear()
        vz.data.materials.append(mat_alu)

    for i in range(1, FOLHAS_QTD + 1):
        vidro = bpy.data.objects.get(f"FOLHA_{i:02d}_VIDRO")
        if vidro:
            bev = vidro.modifiers.new("Bevel", 'BEVEL')
            bev.width = 1.5 * MM
            bev.segments = 2
            vidro.data.materials.clear()
            vidro.data.materials.append(mat_glass)
            vidro.hide_render = False


def align_leaves():
    """Posiciona as folhas (numeracao 01 = esquerda ... 04 = junto a veneziana).

    X fechado (DERIVADO): borda esquerda da folha n = 15 + (n-1)*(427.75 + 3) mm.
      -> ocupa 15..1735 mm, sem invadir a veneziana (1750..1900).
    Z (DERIVADO): vidro 660 mm encaixado entre os trilhos (z = 100..760 mm).
    Estacionado: usa os getters de calibracao (valores UNKNOWN = placeholder visual).
    """
    z_off = (VAO_ALTURA - VIDRO_ALTURA) / 2.0          # 100 mm
    offset_pivo = build_sacada_v2.obter_offset_pivo()    # UNKNOWN (placeholder)
    dist_eixos = build_sacada_v2.obter_distancia_eixos() # UNKNOWN (placeholder)
    parking = build_sacada_v2.obter_parking_offset()     # UNKNOWN (placeholder)

    info = {}
    for n in range(1, FOLHAS_QTD + 1):
        slide = bpy.data.objects.get(f"FOLHA_{n:02d}_SLIDE")
        if not slide:
            continue
        x_closed = FOLGA_LATERAL + (n - 1) * (FOLHA_LARGURA + FOLGA_JUNCAO) + FOLHA_LARGURA / 2
        x_park = parking + (n - 1) * dist_eixos
        slide.location.x = x_closed
        slide.location.z = z_off + VIDRO_ALTURA / 2.0
        slide["murano_x_fechado"] = x_closed
        slide["murano_x_estacionado"] = x_park
        # Marcador EIXO_PIVO: lado esquerdo (borda de entrada no alojamento)
        eixo = bpy.data.objects.get(f"EIXO_PIVO_FOLHA_{n:02d}")
        if eixo:
            eixo.location.x -= (FOLHA_LARGURA - 2 * offset_pivo)
        info[n] = (slide, x_closed, x_park)
    return info, offset_pivo


def setup_compositor():
    scn = bpy.context.scene
    scn.render.film_transparent = True
    scn.use_nodes = True
    tree = getattr(scn, "node_tree", None)
    use_group = False
    if tree is None:  # Blender 5.x
        tree = bpy.data.node_groups.new("MuranoCompositor", 'CompositorNodeTree')
        scn.compositing_node_group = tree
        use_group = True
    tree.nodes.clear()

    n_rl = tree.nodes.new('CompositorNodeRLayers')
    n_img = tree.nodes.new('CompositorNodeImage')
    n_sc = tree.nodes.new('CompositorNodeScale')
    n_ao = tree.nodes.new('CompositorNodeAlphaOver')
    n_rl.location = (-500, 200)
    n_img.location = (-700, -150)
    n_sc.location = (-450, -150)
    n_ao.location = (-150, 0)
    n_img.image = bpy.data.images.load(BACKPLATE)

    # Backplate ajustado ao tamanho do render (cobre o frame)
    try:
        n_sc.inputs['Type'].default_value = 'Render Size'
        n_sc.inputs['Frame Type'].default_value = 'Crop'
    except Exception as e:
        print("WARN scale node:", e)

    if use_group:
        tree.interface.new_socket("Image", in_out='OUTPUT', socket_type='NodeSocketColor')
        n_out = tree.nodes.new('NodeGroupOutput')
    else:
        n_out = tree.nodes.new('CompositorNodeComposite')
    n_out.location = (150, 0)

    L = tree.links.new
    L(n_img.outputs['Image'], n_sc.inputs[0])
    L(n_sc.outputs['Image'], n_ao.inputs['Background'])   # fundo = foto real
    L(n_rl.outputs['Image'], n_ao.inputs['Foreground'])   # frente = sacada renderizada (com alpha)
    L(n_ao.outputs['Image'], n_out.inputs[0])


def setup_animation(info, offset_pivo):
    """Sequencial, sem sobreposicao: Folha 01 gira; 02 desliza->para->gira; 03...; 04.
    O giro de 90 graus e feito em torno do EIXO_PIVO (borda esquerda + offset), nao do centro.
    """
    scn = bpy.context.scene
    scn.render.fps = 24
    scn.frame_start = 1
    scn.frame_end = 240
    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'BEZIER'

    SLOT, START, T_HOLD, T_TURN = 58, 6, 5, 20
    max_dist = max(abs(x_c - x_p) for (_, x_c, x_p) in info.values()) or 1.0
    a = FOLHA_LARGURA / 2.0 - offset_pivo     # centro - pivo (eixo local x)

    def ease(t):
        return t * t * (3 - 2 * t)

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
        key(f_arr, x_park, 0.0, 0.0)      # chega ao alojamento e PARA
        key(f_t0, x_park, 0.0, 0.0)
        # giro 90 graus (sentido horario visto de cima: folha abre em direcao a camera)
        for f in range(f_t0 + 2, f_t1 + 1, 2):
            th = -math.radians(90) * ease((f - f_t0) / float(T_TURN))
            key(f, x_park - a + a * math.cos(th), a * math.sin(th), th)
        key(f_t1, x_park - a, -a, -math.radians(90))
    scn.frame_set(1)


def main():
    print("BUILD SCENE")
    build_sacada_v2.create_sacada()
    setup_engine()
    setup_collections()
    mat_glass, mat_alu = create_materials()
    setup_system_visuals(mat_glass, mat_alu)
    info, offset_pivo = align_leaves()
    setup_lighting()
    setup_cameras()
    setup_compositor()
    setup_animation(info, offset_pivo)

    print("VALIDATE SCENE")
    if len(bpy.data.objects) == 0:
        print("FAIL - NO OBJECTS")
        sys.exit(1)

    print("SAVE .BLEND")
    filepath = r"C:\Users\kauez\Projetos-IA\_AI-AGENCY\murano-vidracaria\murano_etapa3_1.blend"
    bpy.ops.wm.save_as_mainfile(filepath=filepath)

    print("CONFIRM SAVE")
    if os.path.exists(filepath):
        print("EXIT")
        sys.exit(0)
    else:
        print("FAIL TO SAVE")
        sys.exit(1)


if __name__ == "__main__":
    main()

