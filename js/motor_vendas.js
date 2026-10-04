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
  espessuraVidro: 0.010, // 10mm laminado
  alturaPerfilVidro: 0.035, // perfil horizontal base/topo
  alturaTrilho: 0.04,
  profundidadeTrilho: 0.07,
  corPerfil: 0xf4f4f4, // RAL 9003B
};

const W = SPEC.larguraVao;
const H = SPEC.alturaVao;
const M = SPEC.alturaMureta;
const D = SPEC.profundidade;
const T = 0.15;
const ALTURA_TOTAL = M + H;

const LARGURA_VIDROS = W - SPEC.larguraVeneziana; // 1.75m
const FOLHA_L = LARGURA_VIDROS / SPEC.numFolhas;
const FOLHA_A = H - 2 * SPEC.alturaTrilho;

const X_ESQ = -W / 2;
const X_PIVO = X_ESQ;
const OFFSET_PILHA_Z = 0.025;

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

function computePanelKinematics(index, p) {
  const xFechado = X_ESQ + index * FOLHA_L;
  const zPilha = (index + 1) * OFFSET_PILHA_Z;

  if (index === 0) {
    const tGiro = smooth(clamp(p / 0.25, 0, 1));
    return { x: X_PIVO, z: zPilha, rotY: -tGiro * (Math.PI / 2) };
  }
  if (index === 1) {
    const tSlide = smooth(clamp((p - 0.20) / (0.45 - 0.20), 0, 1));
    const tGiro = smooth(clamp((p - 0.45) / (0.55 - 0.45), 0, 1));
    return { x: THREE.MathUtils.lerp(xFechado, X_PIVO, tSlide), z: zPilha, rotY: -tGiro * (Math.PI / 2) };
  }
  if (index === 2) {
    const tSlide = smooth(clamp((p - 0.50) / (0.70 - 0.50), 0, 1));
    const tGiro = smooth(clamp((p - 0.70) / (0.80 - 0.70), 0, 1));
    return { x: THREE.MathUtils.lerp(xFechado, X_PIVO, tSlide), z: zPilha, rotY: -tGiro * (Math.PI / 2) };
  }
  const tSlide = smooth(clamp((p - 0.75) / (0.90 - 0.75), 0, 1));
  const tGiro = smooth(clamp((p - 0.90) / (1.00 - 0.90), 0, 1));
  return { x: THREE.MathUtils.lerp(xFechado, X_PIVO, tSlide), z: zPilha, rotY: -tGiro * (Math.PI / 2) };
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
  if (t >= 1) { progress = target; tweening = false; }
  applyProgress();
}

function std(color, opts = {}) {
  return new THREE.MeshStandardMaterial({ color, roughness: 0.9, ...opts });
}

function box(w, h, d, material, x, y, z, { cast = true, receive = true } = {}) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
  m.position.set(x, y, z);
  m.castShadow = cast;
  m.receiveShadow = receive;
  return m;
}

function buildBalcony(scene) {
  const g = new THREE.Group();

  // Piso porcelanato PBR
  const pisoMat = std(0xf0efe9, { roughness: 0.2, metalness: 0.05 });
  const floorPlane = new THREE.Mesh(new THREE.PlaneGeometry(W, D + 0.07), pisoMat);
  floorPlane.rotation.x = -Math.PI / 2;
  floorPlane.position.set(0, 0.001, (D - 0.07) / 2);
  floorPlane.receiveShadow = true;
  g.add(floorPlane);

  // Teto
  const tetoMat = std(0xfafafa, { roughness: 0.95 });
  g.add(box(W + 2 * T, 0.1, D + 0.1, tetoMat, 0, ALTURA_TOTAL + 0.05, (D - 0.1) / 2));

  // Parede grafite (#3d3b40)
  const paredeContornoMat = std(0x3d3b40, { roughness: 0.8 });
  const zContorno = 0; 
  g.add(box(W, 0.2, T, paredeContornoMat, 0, ALTURA_TOTAL + 0.1, zContorno));
  g.add(box(T, ALTURA_TOTAL, T, paredeContornoMat, -(W / 2 + T / 2), ALTURA_TOTAL / 2, zContorno));
  g.add(box(T, ALTURA_TOTAL, T, paredeContornoMat, W / 2 + T / 2, ALTURA_TOTAL / 2, zContorno));

  // Laterais e mureta (cinza claro #e2dfd9)
  const paredeLateralMat = std(0xe2dfd9, { roughness: 0.9 });
  const zc = (D - 0.1) / 2;
  g.add(box(T, ALTURA_TOTAL, D - 0.05, paredeLateralMat, -(W / 2 + T / 2), ALTURA_TOTAL / 2, zc + 0.1));
  g.add(box(T, ALTURA_TOTAL, D - 0.05, paredeLateralMat, W / 2 + T / 2, ALTURA_TOTAL / 2, zc + 0.1));

  // Mureta
  g.add(box(W, M - 0.03, 0.14, paredeLateralMat, 0, (M - 0.03) / 2, 0));
  
  // Peitoril granito claro PBR
  const peitorilGranito = std(0xd0cec7, { roughness: 0.4, metalness: 0.1 });
  g.add(box(W, 0.03, 0.18, peitorilGranito, 0, M - 0.015, 0));

  buildKitchenette(g);
  scene.add(g);
}

function buildKitchenette(parent) {
  const larg = 0.65;
  const prof = 1.1;
  const zC = 1.4;
  const xParede = W / 2;
  const xC = xParede - larg / 2;

  // Gabinete
  const gabMat = std(0xf4f4f4, { roughness: 0.9 });
  parent.add(box(larg, 0.8, prof, gabMat, xC, 0.4, zC));
  
  const puxadorMat = new THREE.MeshStandardMaterial({ color: 0x888888, metalness: 0.8, roughness: 0.3 });
  parent.add(box(0.01, 0.02, 0.4, puxadorMat, xC - larg/2 - 0.005, 0.75, zC - 0.2));
  parent.add(box(0.01, 0.02, 0.4, puxadorMat, xC - larg/2 - 0.005, 0.75, zC + 0.2));

  // Bancada Granito PBR
  const granitoMat = std(0xbbbbbb, { roughness: 0.4, metalness: 0.1 });
  parent.add(box(larg + 0.02, 0.03, prof + 0.02, granitoMat, xC - 0.01, 0.815, zC));

  // Cuba e Inox PBR
  const inox = new THREE.MeshPhysicalMaterial({ color: 0xc8cacc, metalness: 1.0, roughness: 0.2, clearcoat: 0.2 });
  const zCuba = zC - 0.3;
  parent.add(box(0.3, 0.01, 0.3, inox, xC - 0.05, 0.825, zCuba, { cast: false }));
  
  const torneira = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.2), inox);
  torneira.position.set(xC + 0.05, 0.93, zCuba);
  parent.add(torneira);
  const torneiraBica = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.15), inox);
  torneiraBica.rotation.x = Math.PI / 2;
  torneiraBica.position.set(xC + 0.05, 1.02, zCuba - 0.07);
  parent.add(torneiraBica);

  // Churrasqueira
  const zBBQ = zC + 0.25;
  parent.add(box(0.45, 0.3, 0.45, inox, xC - 0.02, 0.98, zBBQ));
  const escuro = std(0x111111, { roughness: 0.8 });
  parent.add(box(0.41, 0.2, 0.41, escuro, xC - 0.04, 0.98, zBBQ, { cast: false }));

  // Coifa inox
  const hDuto = ALTURA_TOTAL - 1.28;
  const duto = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, hDuto, 24), inox);
  duto.position.set(xC - 0.02, 1.28 + hDuto / 2, zBBQ);
  duto.castShadow = true;
  parent.add(duto);

  // Prateleira aramada
  const aramadoMat = std(0xffffff, { metalness: 0.5, roughness: 0.4 });
  const hPrat = 1.6;
  parent.add(box(larg - 0.1, 0.02, 0.3, aramadoMat, xC, hPrat, zC - 0.3));
  parent.add(box(0.02, ALTURA_TOTAL - hPrat, 0.02, aramadoMat, xC - 0.2, hPrat + (ALTURA_TOTAL - hPrat)/2, zC - 0.4));
  parent.add(box(0.02, ALTURA_TOTAL - hPrat, 0.02, aramadoMat, xC - 0.2, hPrat + (ALTURA_TOTAL - hPrat)/2, zC - 0.2));
  
  const vaso = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.03, 0.1), std(0xddaa88));
  vaso.position.set(xC - 0.1, hPrat + 0.06, zC - 0.3);
  parent.add(vaso);
  const planta = new THREE.Mesh(new THREE.SphereGeometry(0.06), std(0x558855));
  planta.position.set(xC - 0.1, hPrat + 0.15, zC - 0.3);
  parent.add(planta);
}

function buildRails(scene) {
  const aluminio = new THREE.MeshPhysicalMaterial({
    color: SPEC.corPerfil, roughness: 0.4, metalness: 0.4
  });

  const { alturaTrilho: h, profundidadeTrilho: d } = SPEC;
  scene.add(box(W, h, d, aluminio, 0, M + h / 2, 0));
  scene.add(box(W, h, d, aluminio, 0, ALTURA_TOTAL - h / 2, 0));

  return aluminio;
}

function buildFixedLouver(scene, aluminio) {
  const louverWidth = SPEC.larguraVeneziana;
  const louverHeight = FOLHA_A;
  const xCentro = W / 2 - louverWidth / 2;
  const yCentro = M + SPEC.alturaTrilho + louverHeight / 2;
  const molduraEsp = 0.025;

  const louverGroup = new THREE.Group();
  louverGroup.position.set(xCentro, yCentro, 0);

  louverGroup.add(box(louverWidth, molduraEsp, 0.05, aluminio, 0, louverHeight / 2 - molduraEsp / 2, 0));
  louverGroup.add(box(louverWidth, molduraEsp, 0.05, aluminio, 0, -louverHeight / 2 + molduraEsp / 2, 0));
  louverGroup.add(box(molduraEsp, louverHeight, 0.05, aluminio, -louverWidth / 2 + molduraEsp / 2, 0, 0));
  louverGroup.add(box(molduraEsp, louverHeight, 0.05, aluminio, louverWidth / 2 - molduraEsp / 2, 0, 0));

  const numAletas = 26;
  const passoAleta = (louverHeight - 2 * molduraEsp) / numAletas;
  for (let i = 0; i < numAletas; i++) {
    const yAleta = -louverHeight / 2 + molduraEsp + (i + 0.5) * passoAleta;
    const aleta = new THREE.Mesh(new THREE.BoxGeometry(louverWidth - 2 * molduraEsp, 0.003, 0.04), aluminio);
    aleta.rotation.x = Math.PI / 5;
    aleta.position.set(0, yAleta, 0);
    louverGroup.add(aleta);
  }

  scene.add(louverGroup);
}

function buildPanels(scene, aluminio) {
  // Física dos Vidros - PBR sem shaders manuais
  const vidro = new THREE.MeshPhysicalMaterial({
    color: 0xffffff,
    transmission: 0.95,
    transparent: true,
    opacity: 1,
    roughness: 0.02,
    ior: 1.5,
    thickness: 0.02,
    clearcoat: 1.0
  });

  const hVidro = FOLHA_A - 2 * SPEC.alturaPerfilVidro;
  const yCentro = M + SPEC.alturaTrilho + FOLHA_A / 2;

  panels.length = 0;
  for (let i = 0; i < SPEC.numFolhas; i++) {
    const pivot = new THREE.Group();
    pivot.position.set(X_ESQ + i * FOLHA_L, yCentro, 0);
    const folha = new THREE.Group();
    folha.position.set(FOLHA_L / 2, 0, 0);

    const pane = new THREE.Mesh(new THREE.BoxGeometry(FOLHA_L - 0.003, hVidro, SPEC.espessuraVidro), vidro);
    folha.add(pane);

    // Perfis base e topo apenas (SEM AROS VERTICAIS)
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
  scene.background = new THREE.Color(0xdcecf8);
  
  const w0 = container.clientWidth || 1280;
  const h0 = container.clientHeight || 720;

  const camera = new THREE.PerspectiveCamera(58, w0 / h0, 0.05, 800);
  const alvo = new THREE.Vector3(0.2, 1.4, 0.4);
  camera.position.set(-0.5, 1.5, 2.0);
  camera.lookAt(alvo);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(w0, h0);
  
  // Configurações PBR avançadas
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.domElement.style.display = 'block';
  container.appendChild(renderer.domElement);

  // Iluminação Global (HDRI via PMREM)
  const pmremGenerator = new THREE.PMREMGenerator(renderer);
  const roomEnv = new RoomEnvironment();
  scene.environment = pmremGenerator.fromScene(roomEnv, 0.04).texture;

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.copy(alvo);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.minDistance = 1.0;
  controls.maxDistance = 3.5;
  controls.minAzimuthAngle = -0.7;
  controls.maxAzimuthAngle = 0.7;
  controls.minPolarAngle = Math.PI * 0.25;
  controls.maxPolarAngle = Math.PI * 0.65;
  controls.update();

  // Sol projetando sombras
  const sun = new THREE.DirectionalLight(0xfff8ed, 2.5);
  sun.position.set(-4.0, 6.0, -5.0);
  sun.target.position.set(0.5, 0.5, 1.5);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.camera.left = -3;
  sun.shadow.camera.right = 3;
  sun.shadow.camera.top = 3;
  sun.shadow.camera.bottom = -3;
  sun.shadow.camera.near = 1;
  sun.shadow.camera.far = 20;
  sun.shadow.bias = -0.0005;
  sun.shadow.radius = 4;
  scene.add(sun, sun.target);

  const fillLight = new THREE.PointLight(0xfff0da, 0.6, 6, 2);
  fillLight.position.set(0, 2.0, 1.5);
  scene.add(fillLight);

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
