import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

export const SPEC = {
  larguraVao: 1.90,
  alturaVao: 1.46,
  alturaMureta: 0.90,
  profundidade: 2.2,
  numFolhas: 4,
  larguraVeneziana: 0.15,
  espessuraVidro: 0.010, // 10mm (5+5 laminado)
  alturaPerfilVidro: 0.035, // perfis horizontais topo e base
  alturaTrilho: 0.04,
  profundidadeTrilho: 0.07,
  corPerfil: 0xf5f5f5, // Branco RAL 9003B
  abertura: 'esquerda'
};

const W = SPEC.larguraVao;
const H = SPEC.alturaVao;
const M = SPEC.alturaMureta;
const D = SPEC.profundidade;
const T = 0.15; // espessura paredes
const ALTURA_TOTAL = M + H;

// Largura do vão útil dos vidros descontando a veneziana fixa de 0.15m à direita
const LARGURA_VIDROS = W - SPEC.larguraVeneziana; // 1.75m
const FOLHA_L = LARGURA_VIDROS / SPEC.numFolhas;  // ~0.4375m (~0.43m)
const FOLHA_A = H - 2 * SPEC.alturaTrilho;

const X_ESQ = -W / 2; // Batente esquerdo
const X_PIVO = X_ESQ; // Ponto de giro na extrema esquerda
const OFFSET_PILHA_Z = 0.025; // 25mm de recuo por folha empilhada

const panels = [];
let progress = 0;
let target = 0;
let tweenFrom = 0;
let tweenStart = 0;
let tweening = false;
const TWEEN_MS = 2800;
const listeners = new Set();

const clamp = (v, min, max) => Math.min(max, Math.max(min, v));
const smooth = (t) => t * t * (3 - 2 * t);

export function setGlazingProgress(p) {
  progress = clamp(Number(p) || 0, 0, 1);
  tweening = false;
  target = progress >= 0.5 ? 1 : 0;
  applyProgress();
}

export function toggleGlazing() {
  target = target >= 0.5 ? 0 : 1;
  tweenFrom = progress;
  tweenStart = performance.now();
  tweening = true;
  notify();
  return target === 1;
}

export function getGlazingState() {
  return { progress, open: target === 1 };
}

export function onGlazingChange(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

function notify() {
  listeners.forEach((fn) => fn(getGlazingState()));
}

// Cinemática sequencial escalonada rigorosamente conforme especificação
function computePanelKinematics(index, p) {
  // Posição fechada original de cada folha ao longo do trilho
  const xFechado = X_ESQ + index * FOLHA_L;
  const zPilha = (index + 1) * OFFSET_PILHA_Z; // empilhamento para o lado interno

  if (index === 0) {
    // Folha 0 (extrema esquerda): Fica em X_pivô. Entre p=0.00 e p=0.25 gira de 0° a -90°
    const tGiro = smooth(clamp(p / 0.25, 0, 1));
    return {
      x: X_PIVO,
      z: zPilha,
      rotY: -tGiro * (Math.PI / 2)
    };
  }

  if (index === 1) {
    // Folha 1: desliza [0.20, 0.45], gira [0.45, 0.55]
    const tSlide = smooth(clamp((p - 0.20) / (0.45 - 0.20), 0, 1));
    const tGiro = smooth(clamp((p - 0.45) / (0.55 - 0.45), 0, 1));
    return {
      x: THREE.MathUtils.lerp(xFechado, X_PIVO, tSlide),
      z: zPilha,
      rotY: -tGiro * (Math.PI / 2)
    };
  }

  if (index === 2) {
    // Folha 2: desliza [0.50, 0.70], gira [0.70, 0.80]
    const tSlide = smooth(clamp((p - 0.50) / (0.70 - 0.50), 0, 1));
    const tGiro = smooth(clamp((p - 0.70) / (0.80 - 0.70), 0, 1));
    return {
      x: THREE.MathUtils.lerp(xFechado, X_PIVO, tSlide),
      z: zPilha,
      rotY: -tGiro * (Math.PI / 2)
    };
  }

  // Folha 3: desliza [0.75, 0.90], gira [0.90, 1.00]
  const tSlide = smooth(clamp((p - 0.75) / (0.90 - 0.75), 0, 1));
  const tGiro = smooth(clamp((p - 0.90) / (1.00 - 0.90), 0, 1));
  return {
    x: THREE.MathUtils.lerp(xFechado, X_PIVO, tSlide),
    z: zPilha,
    rotY: -tGiro * (Math.PI / 2)
  };
}

function applyProgress() {
  panels.forEach((item, i) => {
    const k = computePanelKinematics(i, progress);
    item.pivot.position.x = k.x;
    item.pivot.position.z = k.z;
    item.pivot.rotation.y = k.rotY;
  });
  notify();
}

function stepTween(now) {
  if (!tweening) return;
  const dur = TWEEN_MS * Math.abs(target - tweenFrom) || 1;
  const t = Math.min(1, (now - tweenStart) / dur);
  progress = THREE.MathUtils.lerp(tweenFrom, target, t);
  if (t >= 1) {
    progress = target;
    tweening = false;
  }
  applyProgress();
}

function canvasTexture(size, draw, repX = 1, repY = 1) {
  const c = document.createElement('canvas');
  c.width = c.height = size;
  draw(c.getContext('2d'), size);
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(repX, repY);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  return tex;
}

function std(color, opts = {}) {
  return new THREE.MeshStandardMaterial({ color, roughness: 0.9, envMapIntensity: 0.35, ...opts });
}

function box(w, h, d, material, x, y, z, { cast = true, receive = true } = {}) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
  m.position.set(x, y, z);
  m.castShadow = cast;
  m.receiveShadow = receive;
  return m;
}

function buildSky(scene) {
  const dome = new THREE.Mesh(
    new THREE.SphereGeometry(300, 32, 16),
    new THREE.ShaderMaterial({
      side: THREE.BackSide,
      depthWrite: false,
      toneMapped: false,
      uniforms: {
        top: { value: new THREE.Color(0x89c2ea) },
        horizon: { value: new THREE.Color(0xf0f5f9) },
        ground: { value: new THREE.Color(0xdde5e8) }
      },
      vertexShader: 'varying vec3 vDir; void main(){ vDir = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
      fragmentShader: 'varying vec3 vDir; uniform vec3 top; uniform vec3 horizon; uniform vec3 ground; void main(){ float h = vDir.y; vec3 c = h > 0.0 ? mix(horizon, top, pow(h, 0.55)) : mix(horizon, ground, smoothstep(0.0, -0.15, h)); gl_FragColor = vec4(c, 1.0); #include <colorspace_fragment> }'
    })
  );
  dome.frustumCulled = false;
  dome.renderOrder = -1;
  scene.add(dome);

  // Chão externo da paisagem urbana
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(900, 900), new THREE.MeshBasicMaterial({ color: 0xd4dce0, toneMapped: false }));
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -35;
  scene.add(ground);

  // Silhueta urbana suave de prédios ao longe
  let seed = 19;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  const tons = [0xc2cfd9, 0xd0dbe2, 0xb6c5d1, 0xd9e3e8, 0xc8d3db];
  for (let i = 0; i < 42; i++) {
    const w = 9 + rnd() * 15;
    const d = 9 + rnd() * 15;
    const h = 32 + rnd() * 48;
    const b = new THREE.Mesh(
      new THREE.BoxGeometry(w, h, d),
      new THREE.MeshBasicMaterial({ color: tons[i % tons.length], toneMapped: false })
    );
    b.position.set(-150 + i * 7.2 + rnd() * 3, -35 + h / 2, -65 - rnd() * 50);
    scene.add(b);
  }

  // Vegetação suave de copas de árvores ao fundo
  for (let i = 0; i < 24; i++) {
    const r = 3 + rnd() * 3.5;
    const t = new THREE.Mesh(
      new THREE.SphereGeometry(r, 10, 8),
      new THREE.MeshBasicMaterial({ color: 0xadc7aa, toneMapped: false })
    );
    t.position.set(-65 + i * 5.4 + rnd() * 2, -16 + rnd() * 2, -26 - rnd() * 12);
    scene.add(t);
  }
}

function buildBalcony(scene) {
  const g = new THREE.Group();

  // Piso em porcelanato acetinado claro
  const tileTex = canvasTexture(512, (ctx, s) => {
    ctx.fillStyle = '#f0eee9';
    ctx.fillRect(0, 0, s, s);
    for (let i = 0; i < 300; i++) {
      ctx.fillStyle = 'rgba(' + Math.floor(180 + Math.random() * 40) + ',' + Math.floor(180 + Math.random() * 40) + ',' + Math.floor(175 + Math.random() * 40) + ',0.04)';
      ctx.fillRect(Math.random() * s, Math.random() * s, 30 + Math.random() * 50, 30 + Math.random() * 50);
    }
    ctx.strokeStyle = '#d3cec4';
    ctx.lineWidth = 4;
    ctx.strokeRect(0, 0, s, s);
  }, W / 0.6, D / 0.6);

  const pisoMat = std(0xffffff, { map: tileTex, roughness: 0.35, metalness: 0.02, envMapIntensity: 0.5 });
  g.add(box(W + 2 * T, 0.1, D + 0.1, std(0xd8d4cb), 0, -0.05, (D - 0.1) / 2, { cast: false }));
  const floorPlane = new THREE.Mesh(new THREE.PlaneGeometry(W, D + 0.07), pisoMat);
  floorPlane.rotation.x = -Math.PI / 2;
  floorPlane.position.set(0, 0.001, (D - 0.07) / 2);
  floorPlane.receiveShadow = true;
  g.add(floorPlane);

  // Teto limpo em gesso sem spots circulares estourados
  const tetoMat = std(0xfbfbfa, { roughness: 0.95, envMapIntensity: 0.3 });
  g.add(box(W + 2 * T, 0.1, D + 0.1, tetoMat, 0, ALTURA_TOTAL + 0.05, (D - 0.1) / 2));

  // Paredes em off-white suave
  const paredeMat = std(0xf3efe7, { roughness: 0.94 });
  const zc = (D - 0.1) / 2;
  g.add(box(T, ALTURA_TOTAL, D + 0.1, paredeMat, -(W / 2 + T / 2), ALTURA_TOTAL / 2, zc));
  g.add(box(T, ALTURA_TOTAL, D + 0.1, paredeMat, W / 2 + T / 2, ALTURA_TOTAL / 2, zc));

  // Rodapé fino
  const rodapeMat = std(0xffffff, { roughness: 0.5 });
  [-1, 1].forEach((s) => {
    g.add(box(0.012, 0.08, D, rodapeMat, s * (W / 2 - 0.006), 0.04, D / 2, { cast: false }));
  });

  // Mureta de alvenaria estrutural da varanda (altura 0.90m)
  g.add(box(W, M, 0.14, std(0xece8df, { roughness: 0.92 }), 0, M / 2, 0));

  // Gradil metálico com barras verticais brancas finas pelo lado EXTERNO da mureta
  buildRailingExternal(g);

  // Churrasqueira na ponta direita
  buildBarbecue(g);

  scene.add(g);
}

// Gradil metálico externo (lado de fora da mureta)
function buildRailingExternal(parent) {
  const gradeMat = new THREE.MeshStandardMaterial({
    color: SPEC.corPerfil,
    roughness: 0.35,
    metalness: 0.2
  });

  const zGrade = -0.09; // face externa da mureta
  const hGrade = M; // cobre toda a altura da mureta

  // Travessa superior e inferior do gradil
  parent.add(box(W, 0.03, 0.03, gradeMat, 0, hGrade - 0.02, zGrade));
  parent.add(box(W, 0.03, 0.03, gradeMat, 0, 0.04, zGrade));

  // Barras verticais brancas finas
  const numBarras = 22;
  const passo = (W - 0.1) / (numBarras - 1);
  for (let i = 0; i < numBarras; i++) {
    const xBarra = -W / 2 + 0.05 + i * passo;
    parent.add(box(0.016, hGrade - 0.06, 0.016, gradeMat, xBarra, hGrade / 2, zGrade, { cast: true, receive: false }));
  }
}

function buildBarbecue(parent) {
  const xParede = W / 2;
  const larg = 0.55;
  const prof = 0.95;
  const zC = 1.28;
  const xC = xParede - larg / 2;

  const tijolo = canvasTexture(256, (ctx, s) => {
    ctx.fillStyle = '#b7ab9c';
    ctx.fillRect(0, 0, s, s);
    const bh = s / 8, bw = s / 4;
    for (let r = 0; r < 8; r++) {
      for (let c = -1; c < 5; c++) {
        const x = c * bw + (r % 2 ? bw / 2 : 0);
        const tone = 150 + Math.random() * 40;
        ctx.fillStyle = 'rgb(' + (tone + 25) + ',' + (tone - 40) + ',' + (tone - 60) + ')';
        ctx.fillRect(x + 2, r * bh + 2, bw - 4, bh - 4);
      }
    }
  }, 1.1, 2.4);

  const inox = new THREE.MeshStandardMaterial({ color: 0xd2d6da, metalness: 0.95, roughness: 0.25, envMapIntensity: 1 });
  const pedra = std(0x484b50, { roughness: 0.55, envMapIntensity: 0.5 });
  const escuro = std(0x181818, { roughness: 1, envMapIntensity: 0.1 });

  const revest = new THREE.Mesh(new THREE.PlaneGeometry(prof + 0.2, ALTURA_TOTAL), std(0xffffff, { map: tijolo, roughness: 0.85 }));
  revest.rotation.y = -Math.PI / 2;
  revest.position.set(xParede - 0.004, ALTURA_TOTAL / 2, zC);
  revest.receiveShadow = true;
  parent.add(revest);

  parent.add(box(larg, 0.8, prof, pedra, xC, 0.4, zC));
  parent.add(box(0.03, 0.34, prof - 0.3, escuro, xC - larg / 2 + 0.002, 0.52, zC, { cast: false }));
  parent.add(box(0.012, 0.012, prof - 0.3, inox, xC - larg / 2 - 0.004, 0.70, zC, { cast: false }));
  parent.add(box(larg + 0.04, 0.04, prof + 0.04, inox, xC - 0.02, 0.82, zC));

  const coifa = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.36, 0.42, 4, 1), inox);
  coifa.rotation.y = Math.PI / 4;
  coifa.scale.set(1, 1, 1.35);
  coifa.position.set(xC, 1.55, zC);
  coifa.castShadow = true;
  parent.add(coifa);

  const alturaDuto = ALTURA_TOTAL - 1.76;
  parent.add(box(0.22, alturaDuto, 0.22, inox, xC + 0.1, 1.76 + alturaDuto / 2, zC));
}

// Trilhos horizontais no topo e base do vão (correm pelo lado interno do gradil)
function buildRails(scene) {
  const aluminio = new THREE.MeshPhysicalMaterial({
    color: SPEC.corPerfil,
    roughness: 0.35,
    metalness: 0.25,
    clearcoat: 0.3,
    clearcoatRoughness: 0.4,
    envMapIntensity: 0.8
  });

  const { alturaTrilho: h, profundidadeTrilho: d } = SPEC;
  // Trilho inferior sobre a mureta (M)
  scene.add(box(W, h, d, aluminio, 0, M + h / 2, 0));
  // Trilho superior no teto do vão (ALTURA_TOTAL)
  scene.add(box(W, h, d, aluminio, 0, ALTURA_TOTAL - h / 2, 0));

  return aluminio;
}

// Veneziana fixa de 0.15m com aletas de alumínio branco RAL 9003B na ponta direita
function buildFixedLouver(scene, aluminio) {
  const louverWidth = SPEC.larguraVeneziana; // 0.15m
  const louverHeight = FOLHA_A;
  const xCentro = W / 2 - louverWidth / 2;
  const yCentro = M + SPEC.alturaTrilho + louverHeight / 2;

  const molduraEsp = 0.025;
  const louverGroup = new THREE.Group();
  louverGroup.position.set(xCentro, yCentro, 0);

  // Molduras do módulo da veneziana
  louverGroup.add(box(louverWidth, molduraEsp, 0.05, aluminio, 0, louverHeight / 2 - molduraEsp / 2, 0));
  louverGroup.add(box(louverWidth, molduraEsp, 0.05, aluminio, 0, -louverHeight / 2 + molduraEsp / 2, 0));
  louverGroup.add(box(molduraEsp, louverHeight, 0.05, aluminio, -louverWidth / 2 + molduraEsp / 2, 0, 0));
  louverGroup.add(box(molduraEsp, louverHeight, 0.05, aluminio, louverWidth / 2 - molduraEsp / 2, 0, 0));

  // Aletas horizontais inclinadas em alumínio branco RAL 9003B
  const numAletas = 26;
  const passoAleta = (louverHeight - 2 * molduraEsp) / numAletas;
  for (let i = 0; i < numAletas; i++) {
    const yAleta = -louverHeight / 2 + molduraEsp + (i + 0.5) * passoAleta;
    const aleta = new THREE.Mesh(
      new THREE.BoxGeometry(louverWidth - 2 * molduraEsp, 0.003, 0.04),
      aluminio
    );
    aleta.rotation.x = Math.PI / 5; // aletas inclinadas a ~36° para respiro e ventilação
    aleta.position.set(0, yAleta, 0);
    louverGroup.add(aleta);
  }

  scene.add(louverGroup);
}

// Folhas de vidro laminado límpido 10mm (5+5) translúcido SEM montantes verticais
function buildPanels(scene, aluminio) {
  const vidro = new THREE.MeshPhysicalMaterial({
    color: 0xf2f9fd,
    roughness: 0.08,
    transmission: 0.94,
    transparent: true,
    opacity: 0.92,
    reflectivity: 0.6,
    ior: 1.52,
    thickness: SPEC.espessuraVidro,
    envMapIntensity: 1.1
  });

  const hVidro = FOLHA_A - 2 * SPEC.alturaPerfilVidro;
  const yCentro = M + SPEC.alturaTrilho + FOLHA_A / 2;

  panels.length = 0;

  for (let i = 0; i < SPEC.numFolhas; i++) {
    // Grupo pivô de giro (seu centro fica no ponto de giro à esquerda de cada folha)
    const pivot = new THREE.Group();
    pivot.position.set(X_ESQ + i * FOLHA_L, yCentro, 0);

    // Grupo folha com offset da largura para girar pelo canto esquerdo
    const folha = new THREE.Group();
    folha.position.set(FOLHA_L / 2, 0, 0);

    // 1. Painel de vidro laminado (SEM nenhum perfil vertical nas bordas)
    const pane = new THREE.Mesh(
      new THREE.BoxGeometry(FOLHA_L - 0.003, hVidro, SPEC.espessuraVidro),
      vidro
    );
    folha.add(pane);

    // 2. Perfis de alumínio branco RAL 9003B SOMENTE na base e no topo (leitos das roldanas)
    const perfilTopo = box(FOLHA_L, SPEC.alturaPerfilVidro, 0.032, aluminio, 0, FOLHA_A / 2 - SPEC.alturaPerfilVidro / 2, 0, { cast: false });
    const perfilBase = box(FOLHA_L, SPEC.alturaPerfilVidro, 0.032, aluminio, 0, -FOLHA_A / 2 + SPEC.alturaPerfilVidro / 2, 0, { cast: false });
    folha.add(perfilTopo);
    folha.add(perfilBase);

    pivot.add(folha);
    scene.add(pivot);
    panels.push({ pivot, folha });
  }
}

export function init3DScene(container) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xeef4f8);

  const w0 = container.clientWidth || 1280;
  const h0 = container.clientHeight || 720;

  // Câmera posicionada no interior da varanda com enquadramento amplo focado no recolhimento
  const camera = new THREE.PerspectiveCamera(56, w0 / h0, 0.05, 800);
  const alvo = new THREE.Vector3(-0.35, 1.45, 0.15);
  camera.position.set(-0.25, 1.52, 2.25);
  camera.lookAt(alvo);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(w0, h0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.12;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.domElement.style.display = 'block';
  container.appendChild(renderer.domElement);

  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.copy(alvo);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.enablePan = false;
  controls.minDistance = 1.2;
  controls.maxDistance = 3.2;
  controls.minAzimuthAngle = -0.55;
  controls.maxAzimuthAngle = 0.55;
  controls.minPolarAngle = Math.PI * 0.32;
  controls.maxPolarAngle = Math.PI * 0.56;
  controls.update();

  // Iluminação equilibrada e realista
  scene.add(new THREE.HemisphereLight(0xdceaff, 0xd0c9bd, 0.95));

  const sun = new THREE.DirectionalLight(0xfff6e4, 2.3);
  sun.position.set(-3.5, 5.2, -7.0);
  sun.target.position.set(0, 0.5, 1);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.camera.left = -4;
  sun.shadow.camera.right = 4;
  sun.shadow.camera.top = 4;
  sun.shadow.camera.bottom = -4;
  sun.shadow.camera.near = 1;
  sun.shadow.camera.far = 25;
  sun.shadow.bias = -0.0005;
  sun.shadow.radius = 3.5;
  scene.add(sun, sun.target);

  // Luz ambiente suave interna de preenchimento
  const fillLight = new THREE.PointLight(0xfff0da, 0.8, 5, 2);
  fillLight.position.set(0, 2.2, 1.3);
  scene.add(fillLight);

  buildSky(scene);
  buildBalcony(scene);

  const aluminio = buildRails(scene);
  buildFixedLouver(scene, aluminio);
  buildPanels(scene, aluminio);

  applyProgress();

  const resize = () => {
    const w = container.clientWidth;
    const h = container.clientHeight;
    if (!w || !h) return;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  };
  new ResizeObserver(resize).observe(container);
  resize();

  (function animate(now) {
    requestAnimationFrame(animate);
    stepTween(now);
    controls.update();
    renderer.render(scene, camera);
  })(performance.now());

  return { scene, camera, renderer, controls };
}
