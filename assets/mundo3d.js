// Mundo 3D de Jugada Maestra (Three.js r158, UMD en assets/vendor/three.min.js).
// Estilo: low-poly, ciudad nocturna con neón en la paleta del canal, pedestales con anillo de luz,
// paneles holográficos, personas de bloques y Tano en 3D. Todo se dibuja en función del tiempo
// (determinista): la página llama a M3D.render(escena, tiempoLocal) desde setTime(t).
(function () {
  const PAL = {
    noche: 0x0B0E1A, niebla: 0x141a33, amarillo: 0xF5B82E, rojo: 0xE8483B, verde: 0x3DDC84,
    crema: 0xF4F1EA, cian: 0x4FD6FF, gris: 0x8E949C, antifaz: 0x2B2E33, cara: 0xE9E6DF, negro: 0x14161A,
  };
  const M3D = { PAL, THREE };
  let R, S, C;

  // ---------- utilidades ----------
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const ease = p => { p = clamp(p); return p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; };
  const lerp = (a, b, p) => a + (b - a) * p;
  M3D.ease = ease; M3D.clamp = clamp; M3D.lerp = lerp;
  let semilla = 7;
  const rnd = () => (semilla = (semilla * 16807) % 2147483647) / 2147483647;
  M3D.rnd = rnd;

  function lienzo(w, h, dibujar) {
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    dibujar(c.getContext('2d'), w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    return t;
  }
  const hex = n => '#' + n.toString(16).padStart(6, '0');
  M3D.hex = hex;

  // ---------- arranque ----------
  M3D.init = function (contenedor, opciones = {}) {
    R = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    R.setSize(1080, 1920); R.setPixelRatio(1);
    R.outputColorSpace = THREE.SRGBColorSpace;
    R.toneMapping = THREE.NoToneMapping;
    R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
    contenedor.appendChild(R.domElement);
    S = new THREE.Scene();
    S.background = new THREE.Color(opciones.fondo ?? PAL.noche);
    // cielo: degradé (noche arriba, resplandor cálido en el horizonte) + estrellas
    const cielo = new THREE.Mesh(new THREE.SphereGeometry(450, 32, 16), new THREE.MeshBasicMaterial({ side: THREE.BackSide, fog: false, depthWrite: false,
      map: lienzo(8, 512, (x, w, h) => { const g = x.createLinearGradient(0, 0, 0, h);
        g.addColorStop(0, opciones.cieloArriba || '#05060f'); g.addColorStop(.38, opciones.cieloMedio || '#121a44');
        g.addColorStop(.49, opciones.horizonte || '#7a2d5a'); g.addColorStop(.52, '#2a1a3a'); g.addColorStop(1, '#05060f');
        x.fillStyle = g; x.fillRect(0, 0, w, h); }) }));
    S.add(cielo);
    const est = new THREE.BufferGeometry(), pos = [];
    for (let i = 0; i < 900; i++) { const a = rnd() * Math.PI * 2, y = .15 + rnd() * .85; const r = Math.sqrt(1 - y * y); pos.push(Math.cos(a) * r * 420, y * 420, Math.sin(a) * r * 420); }
    est.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    S.add(new THREE.Points(est, new THREE.PointsMaterial({ color: 0xffffff, size: 1.6, fog: false, transparent: true, opacity: .8 })));
    S.fog = new THREE.FogExp2(opciones.niebla ?? 0x1a1640, opciones.densidad ?? 0.018);
    C = new THREE.PerspectiveCamera(42, 1080 / 1920, 0.1, 600);
    S.add(new THREE.HemisphereLight(0xb8c6ff, 0x2a1830, 1.25));
    const sol = new THREE.DirectionalLight(0xffe2b0, 1.6);
    sol.position.set(8, 18, 10); sol.castShadow = true;
    sol.shadow.mapSize.set(1024, 1024); Object.assign(sol.shadow.camera, { left: -15, right: 15, top: 15, bottom: -15 });
    S.add(sol); M3D.sol = sol;
    M3D.R = R; M3D.S = S; M3D.C = C;
    return M3D;
  };

  // grupos por escena: solo se ve el de la escena activa
  M3D.escenas = [];
  M3D.escena = function (construir) { const g = new THREE.Group(); g.visible = false; S.add(g); const e = { g, ...construir(g) }; M3D.escenas.push(e); return e; };

  M3D.render = function (i, lt) {
    M3D.escenas.forEach((e, k) => e.g.visible = k === i);
    const e = M3D.escenas[i];
    if (e && e.cuadro) e.cuadro(lt);
    R.render(S, C);
  };

  // cámara: lista de [t, [x,y,z], [mirarX,mirarY,mirarZ], fov?] con interpolación suave
  M3D.camara = function (claves, t) {
    let k = 0; while (k < claves.length - 2 && t > claves[k + 1][0]) k++;
    const a = claves[k], b = claves[Math.min(k + 1, claves.length - 1)];
    const p = b[0] > a[0] ? ease((t - a[0]) / (b[0] - a[0])) : 0;
    C.position.set(lerp(a[1][0], b[1][0], p), lerp(a[1][1], b[1][1], p), lerp(a[1][2], b[1][2], p));
    C.lookAt(lerp(a[2][0], b[2][0], p), lerp(a[2][1], b[2][1], p), lerp(a[2][2], b[2][2], p));
    const f = lerp(a[3] ?? 42, b[3] ?? 42, p); if (C.fov !== f) { C.fov = f; C.updateProjectionMatrix(); }
  };

  // ---------- materiales ----------
  const mat = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: .7, metalness: .05, flatShading: true, ...o });
  const neon = (color, intensidad = 1) => new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(Math.min(1, intensidad)) });
  M3D.mat = mat; M3D.neon = neon;

  const texHalo = lienzo(256, 256, (x, w, h) => {
    const g = x.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2);
    g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.25, 'rgba(255,255,255,.55)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    x.fillStyle = g; x.fillRect(0, 0, w, h);
  });
  // halo aditivo (brillo sin postproceso)
  M3D.halo = function (color, tam = 3) {
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: texHalo, color, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: .8 }));
    s.scale.set(tam, tam, 1); return s;
  };

  // ---------- piezas del mundo ----------
  // suelo con grilla de neón
  M3D.grilla = function (color = PAL.amarillo, tam = 400, celda = 4) {
    const tex = lienzo(256, 256, (x, w, h) => {
      x.fillStyle = '#0a0c18'; x.fillRect(0, 0, w, h);
      x.strokeStyle = hex(color); x.lineWidth = 5; x.shadowColor = hex(color); x.shadowBlur = 22;
      x.strokeRect(0, 0, w, h);
    });
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(tam / celda, tam / celda);
    const m = new THREE.Mesh(new THREE.PlaneGeometry(tam, tam), new THREE.MeshStandardMaterial({ map: tex, emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: 1, roughness: .9 }));
    m.rotation.x = -Math.PI / 2; m.receiveShadow = true; return m;
  };

  // edificio con ventanas encendidas
  const texVentanas = [PAL.amarillo, PAL.cian, 0xffffff].map((c, k) => lienzo(64, 128, (x, w, h) => {
    x.fillStyle = '#0d1020'; x.fillRect(0, 0, w, h);
    for (let yy = 4; yy < h; yy += 10) for (let xx = 4; xx < w; xx += 10) {
      if (rnd() < .42) { x.fillStyle = hex(c); x.globalAlpha = .5 + rnd() * .5; x.fillRect(xx, yy, 5, 6); }
    }
    x.globalAlpha = 1;
  }));
  M3D.ciudad = function (g, { n = 90, desde = -8, hasta = -160, calle = 9, ancho = 60 } = {}) {
    const bordes = [PAL.amarillo, PAL.rojo, PAL.cian];
    for (let i = 0; i < n; i++) {
      const lado = i % 2 ? 1 : -1, w = 3 + rnd() * 5, h = 6 + rnd() * rnd() * 45, d = 3 + rnd() * 5;
      const tex = texVentanas[i % 3].clone(); tex.needsUpdate = true; tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(Math.ceil(w / 3), Math.ceil(h / 6));
      const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshStandardMaterial({ color: [0x1a1f3d, 0x22183a, 0x14233a][i % 3], emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: 1, roughness: .8 }));
      b.position.set(lado * (calle + w / 2 + rnd() * ancho * rnd()), h / 2, lerp(desde, hasta, rnd()));
      g.add(b);
      if (rnd() < .35) { // borde de neón en la terraza
        const t = new THREE.Mesh(new THREE.BoxGeometry(w + .1, .18, d + .1), neon(bordes[i % 3], 2.5));
        t.position.set(b.position.x, h, b.position.z); g.add(t);
      }
    }
  };

  // autopista con bordes de neón y líneas
  M3D.autopista = function (g, largo = 300) {
    const ruta = new THREE.Mesh(new THREE.PlaneGeometry(14, largo), mat(0x15182a, { roughness: .35, metalness: .3 }));
    ruta.rotation.x = -Math.PI / 2; ruta.position.set(0, .02, -largo / 2 + 20); ruta.receiveShadow = true; g.add(ruta);
    [-7, 7].forEach((x, k) => { const b = new THREE.Mesh(new THREE.BoxGeometry(.35, .25, largo), neon(k ? PAL.rojo : PAL.amarillo, 3)); b.position.set(x, .12, -largo / 2 + 20); g.add(b); });
    for (let z = 15; z > -largo + 20; z -= 8) { const l = new THREE.Mesh(new THREE.BoxGeometry(.3, .03, 3.2), neon(0xffffff, 1.4)); l.position.set(0, .04, z); g.add(l); }
  };

  // pedestal con anillo de luz
  M3D.pedestal = function (color = PAL.amarillo, r = 1.6) {
    const p = new THREE.Group();
    const base = new THREE.Mesh(new THREE.CylinderGeometry(r, r * 1.08, .3, 48), mat(0x1b2036, { metalness: .5, roughness: .3, flatShading: false }));
    base.position.y = .15; base.receiveShadow = true; p.add(base);
    const anillo = new THREE.Mesh(new THREE.TorusGeometry(r * 1.02, .07, 12, 96), neon(color, 3));
    anillo.rotation.x = Math.PI / 2; anillo.position.y = .31; p.add(anillo);
    const anillo2 = new THREE.Mesh(new THREE.TorusGeometry(r * 1.55, .045, 8, 96), neon(color, 2));
    anillo2.rotation.x = Math.PI / 2; anillo2.position.y = .03; p.add(anillo2);
    const h = M3D.halo(color, r * 4.2); h.position.y = .2; h.material.opacity = .35; p.add(h);
    p.anillo = anillo2; return p;
  };

  // persona low-poly de bloques
  M3D.persona = function ({ piel = 0xE9C9A8, ropa = 0x2B3A55, pantalon = 0x1f2433, pelo = 0x3A2A1A, alto = 1 } = {}) {
    const p = new THREE.Group();
    const caja = (w, h, d, c) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat(c)); m.castShadow = true; return m; };
    const pierna = k => { const q = new THREE.Group(); const m = caja(.24, .85, .26, pantalon); m.position.y = -.42; q.add(m); q.position.set(k * .15, .9, 0); return q; };
    const brazo = k => { const q = new THREE.Group(); const m = caja(.18, .72, .2, ropa); m.position.y = -.34; q.add(m); const mano = caja(.16, .14, .16, piel); mano.position.y = -.76; q.add(mano); q.position.set(k * .37, 1.62, 0); return q; };
    p.pi = pierna(-1); p.pd = pierna(1); p.bi = brazo(-1); p.bd = brazo(1);
    const torso = caja(.56, .76, .32, ropa); torso.position.y = 1.28;
    const cabeza = caja(.38, .42, .38, piel); cabeza.position.y = 1.9;
    const pelo_ = caja(.4, .14, .4, pelo); pelo_.position.y = 2.13;
    const ojo = k => { const o = caja(.05, .06, .02, 0x14161A); o.position.set(k * .09, 1.93, .195); return o; };
    p.add(p.pi, p.pd, p.bi, p.bd, torso, cabeza, pelo_, ojo(-1), ojo(1));
    p.scale.setScalar(alto);
    // pose de caminata (fase en segundos)
    p.caminar = (t, vel = 1) => { const a = Math.sin(t * 6 * vel) * .5; p.pi.rotation.x = a; p.pd.rotation.x = -a; p.bi.rotation.x = -a * .8; p.bd.rotation.x = a * .8; };
    p.quieto = (t) => { p.pi.rotation.x = p.pd.rotation.x = 0; p.bi.rotation.x = Math.sin(t * 2) * .04; p.bd.rotation.x = -Math.sin(t * 2) * .04; };
    return p;
  };

  // Tano, el mapache infiltrado, en 3D low-poly
  M3D.tano = function () {
    const T = new THREE.Group();
    const m = (geo, c, o) => { const x = new THREE.Mesh(geo, mat(c, o)); x.castShadow = true; return x; };
    const cuerpo = m(new THREE.IcosahedronGeometry(.62, 1), PAL.gris); cuerpo.scale.set(1, 1.12, .85); cuerpo.position.y = .95; T.add(cuerpo);
    const panza = m(new THREE.IcosahedronGeometry(.42, 1), PAL.cara); panza.scale.set(1, 1.1, .6); panza.position.set(0, .88, .33); T.add(panza);
    const cab = new THREE.Group(); cab.position.y = 1.95; T.add(cab); T.cabeza = cab;
    const craneo = m(new THREE.IcosahedronGeometry(.55, 1), PAL.gris); craneo.scale.set(1.12, .95, .95); cab.add(craneo);
    const cara = m(new THREE.IcosahedronGeometry(.36, 1), PAL.cara); cara.scale.set(1.25, .8, .7); cara.position.set(0, -.12, .32); cab.add(cara);
    const antifaz = m(new THREE.CylinderGeometry(.6, .58, .26, 24, 1, true, -Math.PI * .62, Math.PI * 1.24), PAL.antifaz, { side: THREE.DoubleSide });
    antifaz.scale.set(1.08, 1, .95); antifaz.position.set(0, .07, .03); cab.add(antifaz);
    const ojo = k => { const o = m(new THREE.SphereGeometry(.13, 16, 12), 0xffffff, { flatShading: false }); o.scale.z = .6; o.position.set(k * .22, .08, .53); const pu = m(new THREE.SphereGeometry(.065, 12, 10), PAL.negro, { flatShading: false }); pu.position.set(k * .22 + .02, .07, .6); const br = new THREE.Mesh(new THREE.SphereGeometry(.02, 6, 4), new THREE.MeshBasicMaterial({ color: 0xffffff })); br.position.set(k * .22 + .045, .1, .655); cab.add(o, pu, br); };
    ojo(-1); ojo(1);
    const ceja = m(new THREE.BoxGeometry(.22, .06, .05), PAL.negro); ceja.position.set(.22, .3, .5); ceja.rotation.z = .25; cab.add(ceja); T.ceja = ceja;
    const nariz = m(new THREE.SphereGeometry(.07, 8, 6), PAL.negro); nariz.position.set(0, -.12, .62); cab.add(nariz);
    const oreja = k => { const o = m(new THREE.ConeGeometry(.17, .3, 4), PAL.gris); o.position.set(k * .36, .5, 0); o.rotation.z = -k * .3; const i = m(new THREE.ConeGeometry(.09, .16, 4), PAL.antifaz); i.position.set(k * .36, .5, .07); i.rotation.z = -k * .3; cab.add(o, i); };
    oreja(-1); oreja(1);
    const pata = k => { const q = new THREE.Group(); q.add(m(new THREE.BoxGeometry(.2, .5, .22), PAL.gris)); q.children[0].position.y = -.2; q.position.set(k * .25, .45, 0); T.add(q); return q; };
    T.pi = pata(-1); T.pd = pata(1);
    const brazo = k => { const q = new THREE.Group(); const b = m(new THREE.BoxGeometry(.18, .55, .18), PAL.gris); b.position.y = -.26; q.add(b); q.position.set(k * .6, 1.3, 0); T.add(q); return q; };
    T.bi = brazo(-1); T.bd = brazo(1);
    // cola con anillos
    const cola = new THREE.Group(); cola.position.set(-.35, .7, -.45); cola.rotation.set(-.9, 0, .6); T.add(cola);
    for (let k = 0; k < 6; k++) { const s = m(new THREE.CylinderGeometry(.17 - k * .015, .19 - k * .015, .2, 8), k % 2 ? PAL.antifaz : PAL.gris); s.position.y = k * .19; cola.add(s); }
    T.cola = cola;
    // credencial con cordón rojo
    const cordon = m(new THREE.TorusGeometry(.32, .025, 6, 20, Math.PI), PAL.rojo); cordon.rotation.z = Math.PI; cordon.position.set(0, 1.42, .45); T.add(cordon);
    const cred = new THREE.Mesh(new THREE.BoxGeometry(.34, .24, .03), new THREE.MeshBasicMaterial({ map: lienzo(128, 90, (x, w, h) => {
      x.fillStyle = '#fff'; x.fillRect(0, 0, w, h); x.strokeStyle = '#14161A'; x.lineWidth = 8; x.strokeRect(0, 0, w, h);
      x.fillStyle = '#14161A'; x.font = '900 26px Inter, sans-serif'; x.textAlign = 'center'; x.fillText(document.documentElement.lang === 'en' ? 'VISITOR' : 'VISITA', w / 2, h / 2 + 9);
    }) }));
    cred.position.set(0, 1.12, .58); T.add(cred);
    // animaciones
    T.respirar = t => { cuerpo.scale.y = 1.12 + Math.sin(t * 2.4) * .02; cab.position.y = 1.95 + Math.sin(t * 2.4) * .02; cola.rotation.z = .6 + Math.sin(t * 2) * .15; };
    T.saludar = (t, p = 1) => { T.bd.rotation.z = lerp(0, 2.5, p) + Math.sin(t * 9) * .25 * p; };
    T.senalar = p => { T.bd.rotation.z = lerp(0, 2.2, p); T.bd.rotation.x = lerp(0, -.6, p); };
    T.cejas = t => { ceja.position.y = .3 + (Math.sin(t * 1.3) > .7 ? .06 : 0); };
    T.caminar = (t, vel = 1) => { const a = Math.sin(t * 7 * vel) * .45; T.pi.rotation.x = a; T.pd.rotation.x = -a; T.bi.rotation.x = -a; cuerpo.position.y = .95 + Math.abs(Math.sin(t * 7 * vel)) * .05; };
    return T;
  };

  // pila de monedas
  M3D.monedas = function (alto = 10, r = .5) {
    const geo = new THREE.CylinderGeometry(r, r, .12, 24);
    const mt = new THREE.MeshStandardMaterial({ color: 0xF5B82E, metalness: .85, roughness: .28, emissive: 0x6b4a00, emissiveIntensity: .4 });
    const im = new THREE.InstancedMesh(geo, mt, alto); im.castShadow = true;
    const o = new THREE.Object3D();
    for (let k = 0; k < alto; k++) { o.position.set((rnd() - .5) * .06, .06 + k * .125, (rnd() - .5) * .06); o.rotation.y = rnd(); o.updateMatrix(); im.setMatrixAt(k, o.matrix); }
    im.alto = alto; im.mostrar = p => { im.count = Math.max(0, Math.round(alto * clamp(p))); };
    return im;
  };

  // panel holográfico con texto (se redibuja con .poner(texto...))
  M3D.panel = function ({ ancho = 4, alto = 2.2, color = PAL.amarillo, dibujar } = {}) {
    const W = 1024, H = Math.round(1024 * alto / ancho);
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const x = c.getContext('2d');
    const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
    const m = new THREE.Mesh(new THREE.PlaneGeometry(ancho, alto), new THREE.MeshBasicMaterial({ map: tex, transparent: true, side: THREE.DoubleSide, depthWrite: false }));
    let ultimo = null;
    m.poner = (...a) => {
      const k = JSON.stringify(a); if (k === ultimo) return; ultimo = k;
      x.clearRect(0, 0, W, H);
      x.fillStyle = 'rgba(10,14,30,.78)'; x.fillRect(0, 0, W, H);
      x.strokeStyle = hex(color); x.lineWidth = 14; x.shadowColor = hex(color); x.shadowBlur = 30; x.strokeRect(10, 10, W - 20, H - 20); x.shadowBlur = 0;
      dibujar(x, W, H, ...a); tex.needsUpdate = true;
    };
    const h = M3D.halo(color, ancho * 1.6); h.material.opacity = .18; h.position.z = -.05; m.add(h);
    return m;
  };

  // edificio de tienda genérico (sin marcas)
  M3D.tienda = function ({ ancho = 16, alto = 6, fondo = 12, color = 0x2a3550, letrero = 'TIENDA', colorLetrero = PAL.amarillo } = {}) {
    const g = new THREE.Group();
    const cuerpo = new THREE.Mesh(new THREE.BoxGeometry(ancho, alto, fondo), mat(color)); cuerpo.position.y = alto / 2; cuerpo.castShadow = cuerpo.receiveShadow = true; g.add(cuerpo);
    const franja = new THREE.Mesh(new THREE.BoxGeometry(ancho + .1, .25, fondo + .1), neon(colorLetrero, 1)); franja.position.y = alto - .5; g.add(franja);
    const puerta = new THREE.Mesh(new THREE.BoxGeometry(3.2, 3, .1), neon(0xffc76a, .85)); puerta.position.set(0, 1.5, fondo / 2 + .03); g.add(puerta);
    const cartel = new THREE.Mesh(new THREE.PlaneGeometry(ancho * .6, 1.4), new THREE.MeshBasicMaterial({ map: lienzo(1024, 160, (x, w, h) => {
      x.fillStyle = '#14161A'; x.fillRect(0, 0, w, h); x.fillStyle = hex(colorLetrero); x.font = '900 110px Inter, sans-serif'; x.textAlign = 'center'; x.fillText(letrero, w / 2, h / 2 + 40);
    }) }));
    cartel.position.set(0, alto - 1.6, fondo / 2 + .06); g.add(cartel);
    return g;
  };

  window.M3D = M3D;
})();
