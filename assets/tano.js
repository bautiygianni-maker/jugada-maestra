// Tano, el mapache infiltrado. Uso: <div class="tano"></div> y luego pintarTano()
const TANO = `<svg viewBox="0 0 400 440" width="100%" height="100%" aria-hidden="true">
<g transform="rotate(-28 300 360)"><ellipse cx="300" cy="360" rx="40" ry="95" fill="#8E949C" stroke="#14161A" stroke-width="6"/>
<path d="M270 300 Q300 312 330 300" stroke="#2B2E33" stroke-width="16" fill="none" stroke-linecap="round"/>
<path d="M263 345 Q300 358 337 345" stroke="#2B2E33" stroke-width="16" fill="none" stroke-linecap="round"/>
<path d="M266 395 Q300 408 334 395" stroke="#2B2E33" stroke-width="16" fill="none" stroke-linecap="round"/></g>
<path d="M120 432 Q115 300 200 285 Q285 300 280 432 Z" fill="#8E949C" stroke="#14161A" stroke-width="6" stroke-linejoin="round"/>
<ellipse cx="200" cy="385" rx="52" ry="50" fill="#E9E6DF"/>
<path d="M272 345 L330 272" stroke="#14161A" stroke-width="40" stroke-linecap="round"/>
<path d="M272 345 L330 272" stroke="#8E949C" stroke-width="28" stroke-linecap="round"/>
<path d="M334 262 L338 228" stroke="#14161A" stroke-width="18" stroke-linecap="round"/>
<path d="M334 262 L338 228" stroke="#8E949C" stroke-width="8" stroke-linecap="round"/>
<path d="M165 300 L200 345 L235 300" stroke="#E8483B" stroke-width="6" fill="none" stroke-linejoin="round"/>
<rect x="170" y="342" width="60" height="40" rx="6" fill="#FFFFFF" stroke="#14161A" stroke-width="5"/>
<text x="200" y="367" text-anchor="middle" font-family="Inter" font-weight="800" font-size="12" fill="#14161A">VISITA</text>
<polygon points="112,122 128,40 182,92" fill="#8E949C" stroke="#14161A" stroke-width="6" stroke-linejoin="round"/>
<polygon points="132,100 137,64 162,88" fill="#2B2E33"/>
<polygon points="288,122 272,40 218,92" fill="#8E949C" stroke="#14161A" stroke-width="6" stroke-linejoin="round"/>
<polygon points="268,100 263,64 238,88" fill="#2B2E33"/>
<circle cx="200" cy="168" r="100" fill="#8E949C" stroke="#14161A" stroke-width="6"/>
<ellipse cx="200" cy="208" rx="64" ry="50" fill="#E9E6DF"/>
<path d="M108 154 Q150 122 200 144 Q250 122 292 154 Q290 194 250 196 Q220 196 200 176 Q180 196 150 196 Q110 194 108 154 Z" fill="#2B2E33"/>
<circle cx="158" cy="164" r="20" fill="#FFFFFF"/><circle cx="242" cy="164" r="22" fill="#FFFFFF"/>
<circle cx="164" cy="167" r="9" fill="#14161A"/><circle cx="248" cy="166" r="10" fill="#14161A"/>
<circle cx="168" cy="162" r="3" fill="#FFFFFF"/><circle cx="252" cy="161" r="3" fill="#FFFFFF"/>
<path d="M136 118 Q158 112 180 120" stroke="#14161A" stroke-width="6" fill="none" stroke-linecap="round"/>
<g class="a" style="transform-box:fill-box;transform-origin:center;animation:brow 2.2s ease-in-out .8s infinite both"><path d="M222 112 Q244 94 266 108" stroke="#14161A" stroke-width="6" fill="none" stroke-linecap="round"/></g>
<ellipse cx="200" cy="204" rx="14" ry="10" fill="#14161A"/>
<path d="M180 226 Q200 240 226 222" stroke="#14161A" stroke-width="5" fill="none" stroke-linecap="round"/>
</svg>`;
// la credencial dice VISITA en español y VISITOR en inglés (según <html lang>, que pone la página con ?lang=)
function pintarTano(){const svg=document.documentElement.lang==='en'?TANO.replace('>VISITA<','>VISITOR<'):TANO;document.querySelectorAll('.tano').forEach(e=>e.innerHTML=svg);}
