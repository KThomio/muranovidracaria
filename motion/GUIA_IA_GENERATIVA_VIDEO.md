# 🎬 GUIA DE GERAÇÃO: VÍDEO CINEMATOGRÁFICO HIPER-REALISTA COM IA GENERATIVA

Este guia descreve como utilizar os **3 Keyframes Fotorrealistas em 1080p** gerados pelo Blender CAD para criar um vídeo comercial de nível cinematográfico no **Kling AI 1.6** ou **Runway Gen-3 Alpha** sem derreter nem deformar os perfis de alumínio.

---

## 📁 1. Seus Arquivos Base (1920x1080 Full HD)
Os arquivos estão salvos na pasta:
👉 `clients/murano-vidracaria/motion/keyframes_ia/`

1. **`keyframe_01_fechado.png`** (Início): Sacada totalmente fechada com as 4 folhas alinhadas, veneziana VZ 060 à direita e guarda-corpo inferior.
2. **`keyframe_02_deslizando_giro.png`** (Intermediário): Folha 01 aberta a 90° no alojamento, Folha 02 no pivô e Folhas 03/04 correndo no trilho U.
3. **`keyframe_03_aberto_total.png`** (Fim): Abertura total de 100% com as 4 folhas recolhidas e empilhadas a 90° à esquerda.

---

## 🤖 2. Como Gerar no Kling AI 1.6 (Recomendado - Modo Start/End Frame)

1. Acesse o **Kling AI** (`klingai.com`).
2. Selecione a ferramenta **AI Video** $\rightarrow$ Escolha o modo **Image to Video**.
3. Ative a opção **Start Frame** e **End Frame**:
   - **Start Frame:** Faça upload de `keyframe_01_fechado.png`.
   - **End Frame:** Faça upload de `keyframe_03_aberto_total.png`.
4. **Configurações:**
   - Duração: `5s` ou `10s`.
   - Mode: `Professional Mode`.
   - Creativity / Freedom: `0.3` a `0.4` (baixo para respeitar com rigor a física dos perfis de alumínio).
5. **Prompt de Movimento (Copie e Cole em Inglês):**
   ```text
   Cinematic architectural commercial film of a luxury apartment balcony. The 4 smooth frameless glass panels slide gracefully along the matte black aluminum ceiling and floor rails to the left wall and pivot open 90 degrees one by one, opening up the entire panoramic view. Ultra-realistic natural lighting, soft reflections on crystal clear tempered laminated glass, pristine architectural photography, 8k resolution, Arri Alexa Mini LF footage, highly detailed matte black aluminum texture, zero distortion.
   ```
6. **Negative Prompt (Evitar Erros):**
   ```text
   blurry, low quality, warped profiles, melting metal, cartoon, fake CGI, bad glass reflection, distorted rails, extra panels.
   ```

---

## 🎞️ 3. Como Gerar no Runway Gen-3 Alpha

1. Acesse o **RunwayML** (`runwayml.com`) $\rightarrow$ **Gen-3 Alpha**.
2. No menu **Input**, selecione **Image to Video** e adicione o `keyframe_01_fechado.png`.
3. Adicione o `keyframe_03_aberto_total.png` no slot de **Last Frame**.
4. Cole o mesmo prompt em inglês acima e clique em **Generate**.

---

## ⚙️ 4. Como Integrar o Vídeo Gerado de Volta na Landing Page

Quando você baixar o arquivo `.mp4` gerado pelo Kling AI ou Runway, para que ele funcione com o **Scrollytelling do GSAP/Lenis** liso a 60fps sem engasgar no navegador, converta-o para formato **All-Intra (`gopsize = 1`)**:

Abra o terminal e execute:
```bash
ffmpeg -i video_do_kling.mp4 -vcodec libx264 -crf 18 -preset slow -g 1 -an clients/murano-vidracaria/assets/videos/preview_animacao.mp4
```

Assim que substituir o arquivo `preview_animacao.mp4`, dê um `git push` e a sua Vercel exibirá o vídeo gerado por IA no ar imediatamente!
