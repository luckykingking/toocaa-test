// Tiny helper: highlight active nav link
(function(){
  const path = window.location.pathname.replace(/index\.html$/, "");
  document.querySelectorAll(".nav a").forEach(a=>{
    const href = a.getAttribute("href") || "";
    // Only mark internal links (no http)
    if(href.startsWith("http")) return;
    // Normalize
    const resolved = new URL(href, window.location.href).pathname.replace(/index\.html$/, "");
    if(resolved === path) a.classList.add("active");
  });
})();