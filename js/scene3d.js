import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

// Dimensões em metros (vão reto retangular ~1930 x ~1460 mm)
const W = 1.93;
const H = 1.46;
const LEAVES = 4;
const LEAF_W = W / LEAVES;
const GLASS_T = 0.01; // laminado 10 mm (5+5)
const RAIL = 0.04;

export function createScene(container) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a1128);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.appendChild(renderer.domElement);

  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 50);
  camera.position.set(1.2, 1.4, 4.2);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.set(0, H / 2 + 0.2, 0);
  controls.enableDamping = true;
  controls.maxPolarAngle = Math.PI * 0.55;
  controls.minDistance = 1.5;
  controls.maxDistance = 8;

  // Luzes
  scene.add(new THREE.HemisphereLight(0xdfefff, 0x0a1128, 0.6));
  const sun = new THREE.DirectionalLight(0xffffff, 1.6);
  sun.position.set(-3, 5, 4);
  sun.castShadow = true;
  scene.add(sun);
  const cyan = new THREE.PointLight(0x22d3ee, 8, 8);
  cyan.position.set(0, 2.2, 1.5);
  scene.add(cyan);

  // Materiais
  const white = new THREE.MeshStandardMaterial({ color: 0xf1f0ea, roughness: 0.35, metalness: 0.4 }); // RAL 9003B
  const wall = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.9 });
  const floorMat = new THREE.MeshStandardMaterial({ color: 0x111a33, roughness: 0.8 });
  const brick = new THREE.MeshStandardMaterial({ color: 0x7c3f2b, roughness: 0.95 });
  const steel = new THREE.MeshStandardMaterial({ color: 0x2b2f38, roughness: 0.5, metalness: 0.7 });
  const glassMat = new THREE.MeshPhysicalMaterial({
    color: 0xbfeaf5, transparent: true, opacity: 0.28, roughness: 0.05,
    metalness: 0, transmission: 0.6, side: THREE.DoubleSide
  });

  const add = (geo, mat, x, y, z, parent = scene) => {
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x, y, z);
    m.castShadow = m.receiveShadow = true;
    parent.add(m);
    return m;
  };

  // Piso
  add(new THREE.BoxGeometry(8, 0.1, 8), floorMat, 0, -0.05, 0);

  // Paredes laterais do vão
  add(new THREE.BoxGeometry(0.2, H + 0.3, 0.3), wall, -W / 2 - 0.1, (H + 0.3) / 2, 0); // esquerda
  add(new THREE.BoxGeometry(0.2, H + 0.3, 0.3), wall, W / 2 + 0.1, (H + 0.3) / 2, 0);  // direita
  add(new THREE.BoxGeometry(W + 0.4, 0.3, 0.3), wall, 0, H + 0.15, 0);                  // laje superior
  add(new THREE.BoxGeometry(W + 0.4, 0.1, 0.3), wall, 0, 0.05, 0);                      // soleira

  // Trilhos brancos (inferior e superior)
  add(new THREE.BoxGeometry(W, RAIL, 0.08), white, 0, 0.1 + RAIL / 2, 0);
  add(new THREE.BoxGeometry(W, RAIL, 0.08), white, 0, H - RAIL / 2, 0);

  // Churrasqueira à direita (lado interno da varanda)
  const grill = new THREE.Group();
  add(new THREE.BoxGeometry(0.7, 0.9, 0.6), brick, 0, 0.45, 0, grill);
  add(new THREE.BoxGeometry(0.76, 0.05, 0.66), steel, 0, 0.925, 0, grill);
  add(new THREE.BoxGeometry(0.4, 0.3, 0.02), new THREE.MeshStandardMaterial({ color: 0x050505 }), 0, 0.55, 0.31, grill);
  add(new THREE.BoxGeometry(0.3, 1.4, 0.3), brick, 0, 1.6, -0.1, grill); // coifa/chaminé
  grill.position.set(W / 2 + 0.55, 0, 0.55);
  scene.add(grill);

  // 4 folhas: pivô na borda esquerda de cada vão, giram 90° para dentro (+z)
  const leaves = [];
  const glassH = H - 0.1 - RAIL - RAIL - 0.02;
  for (let i = 0; i < LEAVES; i++) {
    const pivot = new THREE.Group();
    pivot.position.set(-W / 2 + i * LEAF_W, 0.1 + RAIL + 0.01, 0);
    scene.add(pivot);

    const glass = add(new THREE.BoxGeometry(LEAF_W - 0.006, glassH, GLASS_T), glassMat, LEAF_W / 2, glassH / 2, 0, pivot);
    glass.castShadow = false;
    // Perfis brancos da folha
    add(new THREE.BoxGeometry(0.025, glassH, 0.03), white, 0.0125, glassH / 2, 0, pivot);
    add(new THREE.BoxGeometry(0.025, glassH, 0.03), white, LEAF_W - 0.0125, glassH / 2, 0, pivot);
    leaves.push(pivot);
  }

  // progress: 0 = fechado, 1 = aberto (90°)
  function setProgress(p) {
    const t = Math.min(1, Math.max(0, p));
    leaves.forEach((l, i) => {
      // leve defasagem entre folhas para efeito sequencial
      const local = Math.min(1, Math.max(0, (t * (1 + 0.15 * (LEAVES - 1)) - 0.15 * i)));
      l.rotation.y = -local * Math.PI / 2; // -y leva a borda direita para +z (para dentro)
    });
  }
  setProgress(0);

  function resize() {
    const w = container.clientWidth || 1;
    const h = container.clientHeight || 1;
    renderer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(container);
  resize();

  renderer.setAnimationLoop(() => {
    controls.update();
    renderer.render(scene, camera);
  });

  return { setProgress };
}
