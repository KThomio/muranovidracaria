import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

export const SPEC = {
  larguraVao: 1.93, alturaVao: 1.46, alturaMureta: 0.90, profundidade: 2.2,
  numFolhas: 4, espessuraVidro: 0.010, alturaTrilho: 0.04, profundidadeTrilho: 0.07,
  corPerfil: 0xf4f4f4, abertura: 'esquerda'
};

const W = SPEC.larguraVao; const H = SPEC.alturaVao; const M = SPEC.alturaMureta; const D = SPEC.profundidade;
const T = 0.15; const ALTURA_TOTAL = M + H;
const FOLHA_L = W / SPEC.numFolhas; const FOLHA_A = H - 2 * SPEC.alturaTrilho;
const X_ESQ = -W / 2; const PASSO_PILHA = 0.06; const FOLGA_PAREDE = 0.03;

const panels = [];
let progress = 0; let target = 0; let tweenFrom = 0; let tweenStart = 0; let tweening = false;
const TWEEN_MS = 2600; const listeners = new Set();
const smooth = (t) => t * t * (3 - 2 * t);

export function setGlazingProgress(p) {
  progress = Math.min(1, Math.max(0, Number(p) || 0));
  tweening = false; target = progress >= 0.5 ? 1 : 0; applyProgress();
}
export function toggleGlazing() {
  target = target >= 0.5 ? 0 : 1; tweenFrom = progress; tweenStart = performance.now(); tweening = true; notify(); return target === 1;
}
export function getGlazingState() { return { progress, open: target === 1 }; }
export function onGlazingChange(fn) { listeners.add(fn); return () => listeners.delete(fn); }
function notify() { listeners.forEach((fn) => fn(getGlazingState())); }

function applyProgress() {
  const e = smooth(progress);
  panels.forEach((pivot, i) => {
    const xFechado = X_ESQ + i * FOLHA_L; const xAberto = X_ESQ + FOLGA_PAREDE + i * PASSO_PILHA;
    pivot.position.x = THREE.MathUtils.lerp(xFechado, xAberto, e);
    pivot.rotation.y = THREE.MathUtils.lerp(0, -Math.PI / 2, e);
  });
  notify();
}
function stepTween(now) {
  if (!tweening) return;
  const dur = TWEEN_MS * Math.abs(target - tweenFrom) || 1;
  const t = Math.min(1, (now - tweenStart) / dur);
  progress = THREE.MathUtils.lerp(tweenFrom, target, t);
  if (t >= 1) { progress = target; tweening = false; }
  applyProgress();
}

function canvasTexture(size, draw, repX = 1, repY = 1) {
  const c = document.createElement('canvas'); c.width = c.height = size; draw(c.getContext('2d'), size);
  const tex = new THREE.CanvasTexture(c); tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(repX, repY); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8; return tex;
}
function std(color, opts = {}) { return new THREE.MeshStandardMaterial({ color, roughness: 0.9, envMapIntensity: 0.35, ...opts }); }
function box(w, h, d, material, x, y, z, { cast = true, receive = true } = {}) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material); m.position.set(x, y, z); m.castShadow = cast; m.receiveShadow = receive; return m;
}

function buildSky(scene) {
  const dome = new THREE.Mesh(
    new THREE.SphereGeometry(300, 32, 16),
    new THREE.ShaderMaterial({
      side: THREE.BackSide, depthWrite: false, toneMapped: false,
      uniforms: { top: { value: new THREE.Color(0x7db7e6) }, horizon: { value: new THREE.Color(0xeaf3f8) }, ground: { value: new THREE.Color(0xd9e2e4) } },
      vertexShader: 'varying vec3 vDir; void main(){ vDir = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
      fragmentShader: 'varying vec3 vDir; uniform vec3 top; uniform vec3 horizon; uniform vec3 ground; void main(){ float h = vDir.y; vec3 c = h > 0.0 ? mix(horizon, top, pow(h, 0.55)) : mix(horizon, ground, smoothstep(0.0, -0.12, h)); gl_FragColor = vec4(c, 1.0); #include <colorspace_fragment> }'
    })
  );
  dome.frustumCulled = false; dome.renderOrder = -1; scene.add(dome);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(900, 900), new THREE.MeshBasicMaterial({ color: 0xd3dcdc, toneMapped: false }));
  ground.rotation.x = -Math.PI / 2; ground.position.y = -40; scene.add(ground);
  let seed = 7; const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  const tons = [0xb7c6d2, 0xc4d1da, 0xaebdca, 0xcfd9df, 0xbdc9d1];
  for (let i = 0; i < 38; i++) {
    const w = 8 + rnd() * 14, d = 8 + rnd() * 14, h = 30 + rnd() * 45;
    const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshBasicMaterial({ color: tons[i % tons.length], toneMapped: false }));
    b.position.set(-140 + i * 7.4 + rnd() * 3, -40 + h / 2, -70 - rnd() * 55); scene.add(b);
  }
  for (let i = 0; i < 26; i++) {
    const r = 3 + rnd() * 3.5;
    const t = new THREE.Mesh(new THREE.SphereGeometry(r, 10, 8), new THREE.MeshBasicMaterial({ color: 0xa9c7a3, toneMapped: false }));
    t.position.set(-60 + i * 4.8 + rnd() * 2, -17 + rnd() * 3, -22 - rnd() * 14); scene.add(t);
  }
}

function buildBalcony(scene) {
  const g = new THREE.Group();
  const tileTex = canvasTexture(512, (ctx, s) => {
    ctx.fillStyle = '#dedbd4'; ctx.fillRect(0, 0, s, s);
    for (let i = 0; i < 400; i++) { ctx.fillStyle = 'rgba(' + Math.floor(150 + Math.random() * 60) + ',' + Math.floor(150 + Math.random() * 60) + ',' + Math.floor(145 + Math.random() * 60) + ',0.05)'; ctx.fillRect(Math.random() * s, Math.random() * s, 40 + Math.random() * 60, 40 + Math.random() * 60); }
    ctx.strokeStyle = '#b9b5ac'; ctx.lineWidth = 5; ctx.strokeRect(0, 0, s, s);
  }, W / 0.6, D / 0.6);
  const piso = std(0xffffff, { map: tileTex, roughness: 0.28, metalness: 0.0, envMapIntensity: 0.6 });
  g.add(box(W + 2 * T, 0.1, D + 0.1, std(0xcfcac2), 0, -0.05, (D - 0.1) / 2, { cast: false }));
  const floorPlane = new THREE.Mesh(new THREE.PlaneGeometry(W, D + 0.07), piso); floorPlane.rotation.x = -Math.PI / 2; floorPlane.position.set(0, 0.001, (D - 0.07) / 2); floorPlane.receiveShadow = true; g.add(floorPlane);
  const gesso = std(0xfafaf7, { roughness: 0.95, envMapIntensity: 0.4 });
  g.add(box(W + 2 * T, 0.1, D + 0.1, gesso, 0, ALTURA_TOTAL + 0.05, (D - 0.1) / 2));
  const sancaL = 0.18, sancaH = 0.07;
  [-1, 1].forEach((s) => { g.add(box(sancaL, sancaH, D - 0.1, gesso, s * (W / 2 - sancaL / 2), ALTURA_TOTAL - sancaH / 2, (D - 0.1) / 2 + 0.05, { receive: false })); });
  const led = new THREE.MeshBasicMaterial({ color: 0xfff1d0, toneMapped: false });
  [-1, 1].forEach((s) => { g.add(box(0.03, 0.006, D - 0.5, led, s * (W / 2 - sancaL - 0.02), ALTURA_TOTAL - 0.003, (D - 0.1) / 2 + 0.1, { cast: false, receive: false })); });
  [[-0.4, 0.9], [0.4, 0.9], [-0.4, 1.7], [0.4, 1.7]].forEach(([x, z]) => { const spot = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.012, 20), led); spot.position.set(x, ALTURA_TOTAL - 0.006, z); g.add(spot); });
  const parede = std(0xece8df, { roughness: 0.95 }); const zc = (D - 0.1) / 2 - 0.0;
  g.add(box(T, ALTURA_TOTAL, D + 0.1, parede, -(W / 2 + T / 2), ALTURA_TOTAL / 2, zc)); g.add(box(T, ALTURA_TOTAL, D + 0.1, parede, W / 2 + T / 2, ALTURA_TOTAL / 2, zc));
  const rodape = std(0xffffff, { roughness: 0.6 }); [-1, 1].forEach((s) => g.add(box(0.012, 0.08, D, rodape, s * (W / 2 - 0.006), 0.04, D / 2, { cast: false })));
  g.add(box(W, M, 0.14, std(0xe4dfd5, { roughness: 0.92 }), 0, M / 2, 0));
  buildBarbecue(g); scene.add(g);
}

function buildBarbecue(parent) {
  const xParede = W / 2; const larg = 0.55, prof = 0.95, zC = 1.28; const xC = xParede - larg / 2;
  const tijolo = canvasTexture(256, (ctx, s) => {
    ctx.fillStyle = '#b9ad9f'; ctx.fillRect(0, 0, s, s); const bh = s / 8, bw = s / 4;
    for (let r = 0; r < 8; r++) {
      for (let c = -1; c < 5; c++) { const x = c * bw + (r % 2 ? bw / 2 : 0); const tone = 150 + Math.random() * 40; ctx.fillStyle = 'rgb(' + (tone + 25) + ',' + (tone - 40) + ',' + (tone - 60) + ')'; ctx.fillRect(x + 2, r * bh + 2, bw - 4, bh - 4); }
    }
  }, 1.1, 2.4);
  const inox = new THREE.MeshStandardMaterial({ color: 0xc9cdd1, metalness: 1, roughness: 0.28, envMapIntensity: 1 });
  const pedra = std(0x4b4f55, { roughness: 0.55, envMapIntensity: 0.5 }); const escuro = std(0x161616, { roughness: 1, envMapIntensity: 0.1 });
  const revest = new THREE.Mesh(new THREE.PlaneGeometry(prof + 0.2, ALTURA_TOTAL), std(0xffffff, { map: tijolo, roughness: 0.85 })); revest.rotation.y = -Math.PI / 2; revest.position.set(xParede - 0.004, ALTURA_TOTAL / 2, zC); revest.receiveShadow = true; parent.add(revest);
  parent.add(box(larg, 0.8, prof, pedra, xC, 0.4, zC));
  parent.add(box(0.03, 0.34, prof - 0.3, escuro, xC - larg / 2 + 0.002, 0.52, zC, { cast: false }));
  parent.add(box(0.012, 0.012, prof - 0.3, inox, xC - larg / 2 - 0.004, 0.70, zC, { cast: false }));
  parent.add(box(larg + 0.04, 0.04, prof + 0.04, inox, xC - 0.02, 0.82, zC));
  const coifa = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.36, 0.42, 4, 1), inox); coifa.rotation.y = Math.PI / 4; coifa.scale.set(1, 1, 1.35); coifa.position.set(xC, 1.55, zC); coifa.castShadow = true; parent.add(coifa);
  const alturaDuto = ALTURA_TOTAL - 1.76; parent.add(box(0.22, alturaDuto, 0.22, inox, xC + 0.1, 1.76 + alturaDuto / 2, zC));
}

function buildRails(scene) {
  const aluminio = new THREE.MeshPhysicalMaterial({ color: SPEC.corPerfil, roughness: 0.4, metalness: 0.3, clearcoat: 0.3, clearcoatRoughness: 0.5, envMapIntensity: 0.8 });
  const { alturaTrilho: h, profundidadeTrilho: d } = SPEC;
  scene.add(box(W, h, d, aluminio, 0, M + h / 2, 0)); scene.add(box(W, h, d, aluminio, 0, ALTURA_TOTAL - h / 2, 0));
  return aluminio;
}

function buildPanels(scene, aluminio) {
  const vidro = new THREE.MeshPhysicalMaterial({ color: 0xf4fbff, roughness: 0.1, transmission: 0.9, transparent: true, opacity: 1, reflectivity: 0.5, ior: 1.5, thickness: SPEC.espessuraVidro, envMapIntensity: 1 });
  const yCentro = M + SPEC.alturaTrilho + FOLHA_A / 2; const mont = 0.02;
  panels.length = 0;
  for (let i = 0; i < SPEC.numFolhas; i++) {
    const pivot = new THREE.Group(); pivot.position.set(X_ESQ + i * FOLHA_L, yCentro, 0);
    const folha = new THREE.Group(); folha.position.x = FOLHA_L / 2;
    const pane = new THREE.Mesh(new THREE.BoxGeometry(FOLHA_L - 0.004, FOLHA_A, SPEC.espessuraVidro), vidro); folha.add(pane);
    folha.add(box(mont, FOLHA_A, 0.03, aluminio, -FOLHA_L / 2 + mont / 2, 0, 0, { cast: false }));
    folha.add(box(mont, FOLHA_A, 0.03, aluminio, FOLHA_L / 2 - mont / 2, 0, 0, { cast: false }));
    pivot.add(folha); scene.add(pivot); panels.push(pivot);
  }
}

export function init3DScene(container) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0xeaf3f8);
  const w0 = container.clientWidth || 1280; const h0 = container.clientHeight || 720;
  const camera = new THREE.PerspectiveCamera(60, w0 / h0, 0.05, 800);
  const alvo = new THREE.Vector3(0, 1.3, -0.8); camera.position.set(0, 1.45, 1.95); camera.lookAt(alvo);
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); renderer.setSize(w0, h0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.15;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.domElement.style.display = 'block'; container.appendChild(renderer.domElement);
  const pmrem = new THREE.PMREMGenerator(renderer); scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.copy(alvo); controls.enableDamping = true; controls.enablePan = false;
  controls.minDistance = 1.2; controls.maxDistance = 2.9;
  controls.minAzimuthAngle = -0.4; controls.maxAzimuthAngle = 0.4;
  controls.minPolarAngle = Math.PI * 0.35; controls.maxPolarAngle = Math.PI * 0.58; controls.update();
  scene.add(new THREE.HemisphereLight(0xdcecff, 0xcfc8bc, 0.9));
  const sun = new THREE.DirectionalLight(0xfff3dc, 2.4);
  sun.position.set(-3.5, 5, -7); sun.target.position.set(0, 0.5, 1); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048); sun.shadow.camera.left = -4; sun.shadow.camera.right = 4;
  sun.shadow.camera.top = 4; sun.shadow.camera.bottom = -4; sun.shadow.camera.near = 1; sun.shadow.camera.far = 25;
  sun.shadow.bias = -0.0005; sun.shadow.radius = 4; scene.add(sun, sun.target);
  [[0, 2.2, 0.9], [0, 2.2, 1.7]].forEach(([x, y, z]) => { const p = new THREE.PointLight(0xffe2b5, 1.2, 4, 2); p.position.set(x, y, z); scene.add(p); });
  buildSky(scene); buildBalcony(scene); const aluminio = buildRails(scene); buildPanels(scene, aluminio); applyProgress();
  const resize = () => { const w = container.clientWidth; const h = container.clientHeight; if (!w || !h) return; camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h); };
  new ResizeObserver(resize).observe(container); resize();
  (function animate(now) { requestAnimationFrame(animate); stepTween(now); controls.update(); renderer.render(scene, camera); })(performance.now());
  return { scene, camera, renderer, controls };
}
