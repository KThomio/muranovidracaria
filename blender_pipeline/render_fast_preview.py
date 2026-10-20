import bpy
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(current_dir, ".."))
BLEND = os.path.join(ROOT, "murano_etapa3_1.blend")
OUT = os.path.join(ROOT, "assets", "videos", "preview_animacao.mp4")
KEYFRAMES_DIR = os.path.join(ROOT, "motion", "keyframes_ia")


def main():
    print("=== MURANO RENDER PIPELINE 1080P ===")
    print("OPEN BLEND:", BLEND)
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    scn = bpy.context.scene
    r = scn.render
    r.resolution_x = 1920
    r.resolution_y = 1080
    r.resolution_percentage = 100
    r.film_transparent = False

    is_keyframes = "--keyframes" in sys.argv
    is_still = "--still" in sys.argv

    # Configuração CYCLES para fotorrealismo de alta fidelidade
    if is_keyframes or is_still or "--cycles" in sys.argv:
        r.engine = 'CYCLES'
        scn.cycles.device = 'CPU'
        scn.cycles.samples = 64
        scn.cycles.use_denoising = True
        print("ENGINE = CYCLES (64 samples + Denoising 1080p)")
    else:
        r.engine = 'BLENDER_EEVEE'
        try:
            scn.eevee.use_raytracing = True
            scn.eevee.taa_render_samples = 16
        except Exception as e:
            print("WARN eevee config:", e)
        print("ENGINE = BLENDER_EEVEE (Raytracing 1080p)")

    # 1. RENDERIZAÇÃO DOS 3 KEYFRAMES FOTORREALISTAS (START / MID / END FRAME P/ IA)
    if is_keyframes:
        os.makedirs(KEYFRAMES_DIR, exist_ok=True)
        if hasattr(r.image_settings, "media_type"):
            r.image_settings.media_type = 'IMAGE'
        r.image_settings.file_format = 'PNG'

        keyframes_map = [
            (1, "keyframe_01_fechado.png"),
            (110, "keyframe_02_deslizando_giro.png"),
            (240, "keyframe_03_aberto_total.png")
        ]

        for frame_num, filename in keyframes_map:
            scn.frame_set(frame_num)
            dest = os.path.join(KEYFRAMES_DIR, filename)
            r.filepath = dest
            print(f"RENDERIZANDO KEYFRAME {frame_num} -> {dest}...")
            bpy.ops.render.render(write_still=True)
            print(f"KEYFRAME SALVO: {dest} (OK: {os.path.exists(dest)})")
        return

    # 2. RENDERIZAÇÃO STILL FRAME INDIVIDUAL
    if is_still:
        f = int(sys.argv[sys.argv.index("--still") + 1])
        scn.frame_set(f)
        if hasattr(r.image_settings, "media_type"):
            r.image_settings.media_type = 'IMAGE'
        r.image_settings.file_format = 'PNG'
        out = os.path.join(ROOT, f"preview_still_frame_{f:03d}.png")
        r.filepath = out
        print(f"RENDERIZANDO STILL FRAME {f} -> {out}...")
        bpy.ops.render.render(write_still=True)
        print("STILL_DONE:", out)
        return

    # 3. RENDERIZAÇÃO DA ANIMAÇÃO COMPLETA EM VÍDEO (1080p / H.264 All-Intra gopsize=1)
    if hasattr(r.image_settings, "media_type"):
        r.image_settings.media_type = 'VIDEO'
    r.image_settings.file_format = 'FFMPEG'
    r.ffmpeg.format = 'MPEG4'
    r.ffmpeg.codec = 'H264'
    r.ffmpeg.constant_rate_factor = 'HIGH'
    r.ffmpeg.ffmpeg_preset = 'GOOD'
    r.ffmpeg.gopsize = 1  # Scrubbing perfeito no Lenis / GSAP ScrollTrigger a 60fps

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    r.filepath = OUT
    print(f"RENDERIZANDO ANIMAÇÃO FULL HD {scn.frame_start}-{scn.frame_end} -> {OUT}...")
    bpy.ops.render.render(animation=True)
    ok = os.path.exists(OUT) and os.path.getsize(OUT) > 0
    print(f"ANIMAÇÃO CONCLUÍDA: {OUT} (Tamanho: {os.path.getsize(OUT)} bytes)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
