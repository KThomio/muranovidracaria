import bpy
import mathutils

MM = 0.001

# 2. Dados geometricos fixos
VAO_LARGURA = 1900.0 * MM
VAO_ALTURA = 860.0 * MM
VENEZIANA_LARGURA = 150.0 * MM
VENEZIANA_ALTURA = 860.0 * MM
FOLHAS_QTD = 4
VIDRO_ESPESSURA = 10.0 * MM
VIDRO_ALTURA = 660.0 * MM
FOLHA_LARGURA = 427.75 * MM
ABERTURA_DIRECAO = "DIR_ESQ"

# 3. Dicionario RIGGING_CALIBRATION no topo do codigo
RIGGING_CALIBRATION = {
    "offset_pivo_x": None,
    "distancia_eixos": None,
    "largura_perfil_leito": None,
    "parking_offset": None,
    "dimensoes_alojamento": None
}

used_placeholders = []

def obter_offset_pivo():
    if RIGGING_CALIBRATION["offset_pivo_x"] is None:
        if "offset_pivo_x" not in used_placeholders: used_placeholders.append("offset_pivo_x")
        return 40.0 * MM # VISUAL_PLACEHOLDER
    return RIGGING_CALIBRATION["offset_pivo_x"]

def obter_distancia_eixos():
    # PROIBIDO usar 30.0 para eixos, espaçamento ou offset.
    if RIGGING_CALIBRATION["distancia_eixos"] is None:
        if "distancia_eixos" not in used_placeholders: used_placeholders.append("distancia_eixos")
        return 50.0 * MM # VISUAL_PLACEHOLDER
    return RIGGING_CALIBRATION["distancia_eixos"]

def obter_largura_perfil_leito():
    if RIGGING_CALIBRATION["largura_perfil_leito"] is None:
        if "largura_perfil_leito" not in used_placeholders: used_placeholders.append("largura_perfil_leito")
        return 45.0 * MM # VISUAL_PLACEHOLDER
    return RIGGING_CALIBRATION["largura_perfil_leito"]

def obter_parking_offset():
    if RIGGING_CALIBRATION["parking_offset"] is None:
        if "parking_offset" not in used_placeholders: used_placeholders.append("parking_offset")
        return FOLHA_LARGURA / 2.0 # VISUAL_PLACEHOLDER
    return RIGGING_CALIBRATION["parking_offset"]

def validar_calibracao():
    print("VALIDAÇÃO:")
    if used_placeholders:
        print(f"Chaves que usaram VISUAL_PLACEHOLDER: {', '.join(used_placeholders)}")
    else:
        print("Nenhuma chave usou VISUAL_PLACEHOLDER.")

def create_sacada():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # Collections
    cols = {}
    for cname in ["Setup", "Perfis", "Folhas", "Mecanismos", "Debug"]:
        col = bpy.data.collections.new(cname)
        bpy.context.scene.collection.children.link(col)
        cols[cname] = col

    offset_pivo = obter_offset_pivo()
    dist_eixos = obter_distancia_eixos()
    largura_leito = obter_largura_perfil_leito()
    parking_off = obter_parking_offset()
    
    # 9. Alojamento e Perfil Leito (PLACEHOLDER)
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, VAO_ALTURA))
    alojamento = bpy.context.active_object
    alojamento.name = "PLACEHOLDER_ALOJAMENTO"
    cols["Mecanismos"].objects.link(alojamento)
    bpy.context.scene.collection.objects.unlink(alojamento)
    
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    perfil_leito = bpy.context.active_object
    perfil_leito.name = "PLACEHOLDER_PERFIL_LEITO"
    cols["Perfis"].objects.link(perfil_leito)
    bpy.context.scene.collection.objects.unlink(perfil_leito)

    # Veneziana
    bpy.ops.mesh.primitive_cube_add(size=1)
    vz = bpy.context.active_object
    vz.name = "VENEZIANA_REF"
    vz.scale = (VENEZIANA_LARGURA, 10.0 * MM, VENEZIANA_ALTURA)
    vz.location = (VAO_LARGURA - VENEZIANA_LARGURA/2, 0, VENEZIANA_ALTURA/2)
    cols["Perfis"].objects.link(vz)
    bpy.context.scene.collection.objects.unlink(vz)

    # Criando as folhas
    for i in range(FOLHAS_QTD):
        idx = i + 1
        slide_name = f"FOLHA_{idx:02d}_SLIDE"
        vidro_name = f"FOLHA_{idx:02d}_VIDRO"
        
        pos_x_fechado = VAO_LARGURA - (i * FOLHA_LARGURA) - (FOLHA_LARGURA / 2.0)
        pos_x_estacionado = parking_off + (i * dist_eixos)
        
        # SLIDE (Carrinho)
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(pos_x_fechado, 0, VIDRO_ALTURA / 2.0))
        slide = bpy.context.active_object
        slide.name = slide_name
        
        slide["murano_x_fechado"] = pos_x_fechado
        slide["murano_x_estacionado"] = pos_x_estacionado
        
        cols["Folhas"].objects.link(slide)
        bpy.context.scene.collection.objects.unlink(slide)
        
        # VIDRO
        bpy.ops.mesh.primitive_cube_add(size=1)
        vidro = bpy.context.active_object
        vidro.name = vidro_name
        vidro.scale = (FOLHA_LARGURA, VIDRO_ESPESSURA, VIDRO_ALTURA)
        vidro.location = (pos_x_fechado, 0, VIDRO_ALTURA / 2.0)
        
        vidro.parent = slide
        vidro.matrix_parent_inverse = slide.matrix_world.inverted()
        
        cols["Folhas"].objects.link(vidro)
        bpy.context.scene.collection.objects.unlink(vidro)
        
        # Marcadores
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(pos_x_fechado, 0, VIDRO_ALTURA))
        centro_mec = bpy.context.active_object
        centro_mec.name = f"CENTRO_MECANICO_FOLHA_{idx:02d}"
        centro_mec.parent = slide
        centro_mec.matrix_parent_inverse = slide.matrix_world.inverted()
        cols["Debug"].objects.link(centro_mec)
        bpy.context.scene.collection.objects.unlink(centro_mec)

        pivo_x = pos_x_fechado + (FOLHA_LARGURA / 2.0) - offset_pivo
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(pivo_x, 0, VIDRO_ALTURA))
        eixo_pivo = bpy.context.active_object
        eixo_pivo.name = f"EIXO_PIVO_FOLHA_{idx:02d}"
        eixo_pivo.parent = slide
        eixo_pivo.matrix_parent_inverse = slide.matrix_world.inverted()
        cols["Debug"].objects.link(eixo_pivo)
        bpy.context.scene.collection.objects.unlink(eixo_pivo)

    validar_calibracao()

if __name__ == "__main__":
    create_sacada()

