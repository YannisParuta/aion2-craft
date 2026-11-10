/* Moteur de calcul — même modèle que le calculateur guidemmo.com
   - Paliers 1-3 (w/e/a) : le jalon est la version éclatante (requise par le palier suivant) -> réussite p, combo 25 %, réussite du combo p : essais = 1/(p·0,25·p)
   - Étoilé (s1) : essais = 1/p
   - Étoilé éclatant (s1s) : 1 Étoilé + (1 - 0,25·p) × ingrédients
   - Noir / Sombre (s2/s3) : transfert garanti : 1 éclatant précédent + ingrédients
   - Noir / Sombre éclatant (s2s/s3s) : 1 objet + 0,75 × ingrédients (25 % de combo direct)
*/
(function (root) {
  var COMBO = 0.25;

  function chance(D, lv, k, L) {
    if (lv == null) return 1;
    var d = L - lv;
    if (d < 0) return 0;
    var t = D.tabs[k] || D.tabs.w;
    return t[Math.min(d, t.length - 1)] / 100;
  }

  function target(st) { return /^(w|e|a)$/.test(st.k) ? st.combo : st.n; }

  /* Objectifs proposés pour un type d'objet */
  function goals(D, type) {
    var out = [];
    D.chains[type].forEach(function (st, i) {
      // Paliers 1-3 : le jalon est la version éclatante (obtenue par le combo),
      // c'est elle que demande le palier suivant. L'objet normal n'est pas un objectif.
      if (/^(w|e|a)$/.test(st.k)) out.push({ name: st.combo, step: i, k: st.k, splendent: true, milestone: true });
      else out.push({ name: st.n, step: i, k: st.k, splendent: /s$/.test(st.k), milestone: true });
    });
    return out;
  }

  /* Recettes "attendues" (quantités moyennes par unité produite) */
  function recipes(D, type, L) {
    var R = {}, ch = D.chains[type], pStar = 1;
    Object.keys(D.inter).forEach(function (n) {
      R[n] = { comps: D.inter[n].map(function (x) { return [x[0], x[1]]; }), crafts: 1, succ: 1, kind: 'inter' };
    });
    ch.forEach(function (st, i) {
      var prev = i ? target(ch[i - 1]) : null, p, mult;
      var scale = function (m) { return st['in'].map(function (x) { return [x[0], x[1] * m]; }); };
      if (/^(w|e|a)$/.test(st.k)) {
        p = chance(D, st.lv, st.k, L);
        var q = p * COMBO * p;
        R[st.combo] = { comps: q ? scale(1 / q) : scale(Infinity), crafts: q ? 1 / q : Infinity, succ: p, comboSucc: q, lv: st.lv, kind: 'chain', k: st.k, splendent: true };
        R[st.n] = { comps: p ? scale(1 / p) : scale(Infinity), crafts: p ? 1 / p : Infinity, succ: p, lv: st.lv, kind: 'chain', k: st.k };
      } else if (st.k === 's1') {
        p = chance(D, st.lv, 's1', L); pStar = p;
        R[st.n] = { comps: p ? scale(1 / p) : scale(Infinity), crafts: p ? 1 / p : Infinity, succ: p, lv: st.lv, kind: 'chain', k: st.k };
      } else if (/s$/.test(st.k)) {
        mult = 1 - COMBO * (st.k === 's1s' ? pStar : 1);
        R[st.n] = { comps: [[prev, 1]].concat(scale(mult)), crafts: mult, succ: 1, kind: 'chain', k: st.k, transfer: true, splendent: true };
      } else {
        R[st.n] = { comps: [[prev, 1]].concat(scale(1)), crafts: 1, succ: 1, kind: 'chain', k: st.k, transfer: true };
      }
    });
    return R;
  }

  /*
    opts : { type, goal, qty, lvl, decompose, buy:{nom:true}, stock:{nom:n}, margin }
    -> { leaves:[{n,need,stock,net}], steps:[{n,produce,crafts,succ,...}], blocked:[noms] }
  */
  /* Ancien objectif "objet normal" d'un palier 1-3 -> sa version éclatante */
  function normalizeGoal(D, type, name) {
    var st = D.chains[type].filter(function (x) { return x.n === name && /^(w|e|a)$/.test(x.k); })[0];
    return st ? st.combo : name;
  }

  /* Tentatives nécessaires pour avoir `conf` (ex. 0,9) de chances d'au moins une réussite à la probabilité q */
  function attemptsFor(q, conf) {
    if (!(q > 0)) return Infinity;
    if (q >= 1) return 1;
    return Math.ceil(Math.log(1 - conf) / Math.log(1 - q));
  }

  function compute(D, o) {
    var R = recipes(D, o.type, o.lvl);
    var isCraft = function (n) {
      if (!R[n]) return false;
      if (o.buy && o.buy[n] && n !== o.goal) return false;
      if (R[n].kind === 'inter' && !o.decompose) return false;
      return true;
    };
    // ordre topologique (parents avant enfants)
    var order = [], seen = {};
    (function visit(n) {
      if (seen[n]) return; seen[n] = 1;
      if (isCraft(n)) R[n].comps.forEach(function (c) { visit(c[0]); });
      order.push(n);
    })(o.goal);
    order.reverse();
    var gross = {}; gross[o.goal] = o.qty;
    var leaves = [], steps = [], blocked = [];
    order.forEach(function (n) {
      var g = gross[n] || 0, st = (o.stock && +o.stock[n]) || 0;
      var net = Math.max(0, g - st);
      if (isCraft(n)) {
        var r = R[n];
        if (!isFinite(r.crafts)) blocked.push(n);
        r.comps.forEach(function (c) { gross[c[0]] = (gross[c[0]] || 0) + net * c[1]; });
        steps.push({ n: n, gross: g, stock: st, produce: net, crafts: net * r.crafts, perUnit: r.crafts, succ: r.succ, comboSucc: r.comboSucc, lv: r.lv, kind: r.kind, k: r.k, transfer: !!r.transfer, splendent: !!r.splendent });
      } else {
        var m = 1 + (o.margin || 0) / 100;
        leaves.push({ n: n, need: g * m, stock: st, net: Math.max(0, g * m - st), bought: !!R[n] });
      }
    });
    steps.reverse(); // feuilles -> objectif
    return { leaves: leaves, steps: steps, blocked: blocked, recipes: R };
  }

  root.AionEngine = { chance: chance, target: target, goals: goals, normalizeGoal: normalizeGoal, attemptsFor: attemptsFor, recipes: recipes, compute: compute };
  if (typeof module !== 'undefined') module.exports = root.AionEngine;
})(typeof window !== 'undefined' ? window : globalThis);
