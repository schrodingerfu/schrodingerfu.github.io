/* ==========================================================================
   Personal Academic Homepage — interactions
   ========================================================================== */
(function () {
  "use strict";

  /* ---------- 1. 中英切换 ---------- */
  var body = document.body;
  var langBtn = document.getElementById("langSwitch");

  function setLang(lang) {
    var isEn = lang === "en";
    body.classList.toggle("en", isEn);
    document.documentElement.lang = isEn ? "en" : "zh-CN";
    try { localStorage.setItem("site-lang", lang); } catch (e) {}
  }

  var saved = null;
  try { saved = localStorage.getItem("site-lang"); } catch (e) {}
  setLang(saved || "zh");

  if (langBtn) {
    langBtn.addEventListener("click", function () {
      setLang(body.classList.contains("en") ? "zh" : "en");
    });
  }

  /* ---------- 2. 移动端菜单 ---------- */
  var menuBtn = document.getElementById("menuBtn");
  var nav = document.getElementById("nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      nav.classList.toggle("is-open");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) nav.classList.remove("is-open");
    });
  }

  /* ---------- 3. 导航高亮（滚动监听） ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav-link"));

  // 只跟踪页内锚点链接（形如 #about），外链如 ../index.html 直接跳过
  var tracked = [];
  links.forEach(function (a) {
    var href = a.getAttribute("href") || "";
    if (href.charAt(0) !== "#") return;
    var section = document.getElementById(href.slice(1));
    if (section) tracked.push({ link: a, section: section });
  });
  var sections = tracked.map(function (t) { return t.section; });

  if ("IntersectionObserver" in window && sections.length) {
    var visible = new Map();
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        visible.set(entry.target.id, entry.isIntersecting ? entry.intersectionRatio : 0);
      });
      var bestId = null, bestRatio = 0;
      visible.forEach(function (ratio, id) {
        if (ratio > bestRatio) { bestRatio = ratio; bestId = id; }
      });
      tracked.forEach(function (t) {
        t.link.classList.toggle("is-active", bestId && t.section.id === bestId);
      });
    }, { rootMargin: "-72px 0px -55% 0px", threshold: [0, 0.15, 0.4, 0.75] });

    sections.forEach(function (s) { observer.observe(s); });
  }

  /* ---------- 4. 论文筛选 ---------- */
  var filterBar = document.getElementById("pubFilters");
  var pubs = Array.prototype.slice.call(document.querySelectorAll("#pubList .pub"));

  if (filterBar && pubs.length) {
    filterBar.addEventListener("click", function (e) {
      var btn = e.target.closest(".filter");
      if (!btn) return;
      var type = btn.getAttribute("data-filter");
      filterBar.querySelectorAll(".filter").forEach(function (b) {
        b.classList.toggle("is-active", b === btn);
      });
      pubs.forEach(function (p) {
        p.classList.toggle("is-hidden", type !== "all" && p.getAttribute("data-type") !== type);
      });
    });
  }

  /* ---------- 5. 页脚年份 ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
