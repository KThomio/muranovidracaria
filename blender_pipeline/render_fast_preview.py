import bpy
import os
import sys

ROOT = r"C:\Users\kauez\Projetos-IA\_AI-AGENCY\murano-vidracaria"
BLEND = os.path.join(ROOT, "murano_etapa3_1.blend")
OUT = os.path.join(ROOT, "assets", "videos", "preview_animacao.mp4")


def main():
    print("OPEN BLEND")
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    scn = bpy.context.scene
    r = scn.render

    # Motor rapido (EEVEE, samples minimos). O compositor roda normalmente
    # sobre o resultado, entao o MP4 mostra a mecanica SOBRE a foto real.
    r.engine = 'BLENDER_EEVEE'
    try:
        scn.eevee.taa_render_samples = 4
    except Exception as e:
        print("WARN eevee samples:", e)

    r.film_transparent = True      # necessario para o Alpha Over
    r.use_compositing = True       # compositor ATIVO no render
    if scn.compositing_node_group is None and getattr(scn, "node_tree", None) is None:
        print("FAIL: compositor sem node tree")
        sys.exit(1)

    # Saida FFmpeg / MPEG-4 / H.264 / 1280x720
    r.resolution_x = 1280
    r.resolution_y = 720
    r.resolution_percentage = 100
    if hasattr(r.image_settings, "media_type"):
        r.image_settings.media_type = 'VIDEO'
    r.image_settings.file_format = 'FFMPEG'
    r.ffmpeg.format = 'MPEG4'
    r.ffmpeg.codec = 'H264'
    r.ffmpeg.constant_rate_factor = 'MEDIUM'
    r.ffmpeg.ffmpeg_preset = 'REALTIME'

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    r.filepath = OUT  # caminho absoluto (evita problema do prefixo //)

    # Modo opcional: um unico frame de teste  (blender ... -- --still 120)
    if "--still" in sys.argv:
        f = int(sys.argv[sys.argv.index("--still") + 1])
        scn.frame_set(f)
        if hasattr(r.image_settings, "media_type"):
            r.image_settings.media_type = 'IMAGE'
        r.image_settings.file_format = 'PNG'
        r.filepath = os.path.join(ROOT, f"scratch_frame_{f:03d}.png")
        bpy.ops.render.render(write_still=True)
        print("STILL_DONE", r.filepath)
        return

    print(f"RENDER {scn.frame_start}-{scn.frame_end} @ {r.fps}fps -> {OUT}")
    bpy.ops.render.render(animation=True)

    ok = os.path.exists(OUT) and os.path.getsize(OUT) > 0
    print("MP4_EXISTS =", ok)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
