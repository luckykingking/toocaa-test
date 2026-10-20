"use strict";

(() => {
  const sectionNav = document.querySelector(".section-nav > .shell");
  const alignCurrentSection = () => {
    const current = sectionNav?.querySelector("[aria-current]");
    if (!current) return;
    const bounds = sectionNav.getBoundingClientRect();
    const tab = current.getBoundingClientRect();
    if (tab.right > bounds.right - 16) sectionNav.scrollLeft += tab.right - bounds.right + 16;
    else if (tab.left < bounds.left + 16) sectionNav.scrollLeft -= bounds.left + 16 - tab.left;
  };
  document.fonts.ready.then(alignCurrentSection);
  window.addEventListener("resize", alignCurrentSection);

  const nav = document.querySelector(".site-nav");
  const menu = document.querySelector(".menu-button");
  const closeMenus = () => {
    document.querySelectorAll(".nav-group.is-open").forEach(group => {
      group.classList.remove("is-open");
      group.querySelector(".nav-toggle").setAttribute("aria-expanded", "false");
    });
  };
  menu?.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    menu.setAttribute("aria-expanded", String(open));
    menu.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
    if (!open) closeMenus();
  });
  document.querySelectorAll(".nav-toggle").forEach(button => {
    const group = button.closest(".nav-group");
    button.addEventListener("click", () => {
      const open = !group.classList.contains("is-open");
      closeMenus();
      group.classList.toggle("is-open", open);
      button.setAttribute("aria-expanded", String(open));
    });
    group.addEventListener("pointerenter", event => {
      if (event.pointerType !== "mouse" || !matchMedia("(min-width: 1001px)").matches) return;
      closeMenus();
      group.classList.add("is-open");
      button.setAttribute("aria-expanded", "true");
    });
    group.addEventListener("pointerleave", () => {
      if (!matchMedia("(min-width: 1001px)").matches || group.contains(document.activeElement)) return;
      group.classList.remove("is-open");
      button.setAttribute("aria-expanded", "false");
    });
    group.addEventListener("focusout", event => {
      if (group.contains(event.relatedTarget)) return;
      group.classList.remove("is-open");
      button.setAttribute("aria-expanded", "false");
    });
  });
  nav?.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      closeMenus();
      nav.classList.remove("is-open");
      menu?.setAttribute("aria-expanded", "false");
      menu?.setAttribute("aria-label", "Open navigation");
    });
  });
  document.addEventListener("click", event => {
    if (!event.target.closest(".nav-group")) closeMenus();
  });
  document.addEventListener("keydown", event => {
    if (event.key !== "Escape") return;
    const focusedGroup = event.target.closest(".nav-group.is-open");
    closeMenus();
    focusedGroup?.querySelector(".nav-toggle").focus();
    if (nav?.classList.contains("is-open")) {
      nav.classList.remove("is-open");
      menu.setAttribute("aria-expanded", "false");
      menu.setAttribute("aria-label", "Open navigation");
      menu.focus();
    }
  });

  const query = document.querySelector("#guideQuery");
  const filterButtons = [...document.querySelectorAll("[data-category-filter]")];
  if (query) {
    const cards = [...document.querySelectorAll("[data-guide]")];
    const params = new URLSearchParams(location.search);
    let category = params.get("category") || "all";
    if (!filterButtons.some(button => button.dataset.categoryFilter === category)) category = "all";
    query.value = params.get("q") || "";
    const apply = () => {
      const terms = query.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        const visible = (category === "all" || card.dataset.category === category) && terms.every(term => text.includes(term));
        card.hidden = !visible;
        if (visible) count++;
      });
      filterButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.categoryFilter === category)));
      document.querySelector("#resultCount").textContent = `${count} ${count === 1 ? "guide" : "guides"}`;
      document.querySelector("#emptyResult").hidden = count > 0;
    };
    filterButtons.forEach(button => button.addEventListener("click", () => {
      category = button.dataset.categoryFilter;
      apply();
    }));
    query.addEventListener("input", apply);
    apply();
  }

  const lookup = document.querySelector("#lookupResult");

  const settingsFilters = [...document.querySelectorAll("[data-setting-filter]")];
  if (settingsFilters.length) {
    const rows = [...document.querySelectorAll("#materialSettingsTable tbody tr")];
    const filterSettings = () => {
      let count = 0;
      rows.forEach(row => {
        row.hidden = !settingsFilters.every(select => select.value === "all" || row.dataset[select.dataset.settingFilter] === select.value);
        if (!row.hidden) count++;
      });
      document.querySelector("#materialSettingsCount").textContent = count ? `${count} matching reference ${count === 1 ? "row" : "rows"}` : "No published L2 row matches this combination. Do not calculate a substitute.";
    };
    settingsFilters.forEach(select => select.addEventListener("change", filterSettings));
    filterSettings();
  }

  const issueQuery = document.querySelector("#issueQuery");
  if (issueQuery) {
    const modelButtons = [...document.querySelectorAll("[data-machine]")];
    const issueSections = [...document.querySelectorAll("[data-issue-section]")];
    let model = "all";
    const filterIssues = () => {
      const terms = issueQuery.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      let count = 0;
      issueSections.forEach(section => {
        let visible = 0;
        section.querySelectorAll("[data-guide]").forEach(item => {
          const matchModel = model === "all" || item.dataset.models.split(",").includes(model);
          const text = item.textContent.toLowerCase();
          item.hidden = !(matchModel && terms.every(term => text.includes(term)));
          if (!item.hidden) visible++;
        });
        section.hidden = visible === 0;
        const jump = document.querySelector(`.issue-jumps a[href="#${section.id}"]`);
        if (jump) jump.hidden = section.hidden;
        count += visible;
      });
      modelButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.machine === model)));
      document.querySelector("#issueCount").textContent = `${count} ${count === 1 ? "guide" : "guides"}`;
      document.querySelector("#issueEmpty").hidden = count > 0;
    };
    issueQuery.addEventListener("input", filterIssues);
    modelButtons.forEach(button => button.addEventListener("click", () => {
      model = button.dataset.machine;
      filterIssues();
    }));
    filterIssues();
  }

  if (lookup) {
    const data = JSON.parse(document.querySelector("#settingsData").textContent);
    const material = document.querySelector("#woodMaterial");
    const moduleSelect = document.querySelector("#woodPowerClass");
    const mode = document.querySelector("#woodMode");
    const update = () => {
      const rows = data.rows.filter(row => row.key === material.value && row.module === Number(moduleSelect.value) && row.mode === mode.value);
      lookup.replaceChildren();
      if (!rows.length) {
        lookup.textContent = "No L2 setting is listed for this combination. Check the full TOOCAA material table or contact support with your material and module details.";
        return;
      }
      rows.forEach(row => {
        const p = document.createElement("p");
        p.textContent = `${data.model} ${row.module}W · ${row.material}, ${row.thickness} mm · ${row.mode}: ${row.power}% power / ${row.speed} mm/min / ${row.passes} ${row.passes === 1 ? "pass" : "passes"}.`;
        lookup.append(p);
      });
    };
    [material, moduleSelect, mode].forEach(select => select.addEventListener("change", update));
    update();
  }

  const searchData = document.querySelector("#searchData");
  if (searchData) {
    const pages = JSON.parse(searchData.textContent);
    const input = document.querySelector("#siteQuery");
    input.value = new URLSearchParams(location.search).get("q") || "";
    const render = () => {
      const terms = input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      const matches = pages.filter(page => terms.every(term => `${page.title} ${page.description} ${page.keywords} ${page.group}`.toLowerCase().includes(term)));
      const results = document.querySelector("#searchResults");
      results.replaceChildren();
      matches.forEach(page => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = "../" + page.path;
        const category = document.createElement("span");
        category.className = "category";
        category.textContent = page.group;
        const heading = document.createElement("h3");
        heading.textContent = page.title;
        const summary = document.createElement("p");
        summary.textContent = page.description;
        a.append(category, heading, summary);
        li.append(a);
        results.append(li);
      });
      document.querySelector("#searchCount").textContent = matches.length ? `${matches.length} ${matches.length === 1 ? "result" : "results"}` : "No matching guides. Try a material, setup task, or symptom.";
    };
    input.addEventListener("input", render);
    document.querySelector("#siteSearchForm").addEventListener("submit", event => { event.preventDefault(); render(); });
    render();
  }

  const ticketForm = document.querySelector("#ticketForm");
  if (ticketForm) {
    const output = document.querySelector("#ticketOutput");
    const copy = document.querySelector("#copyTicket");
    const status = document.querySelector("#copyStatus");
    ticketForm.addEventListener("submit", event => {
      event.preventDefault();
      const values = new FormData(ticketForm);
      output.value = `Machine and module: ${values.get("machine")}\n\nMaterial and settings: ${values.get("settings")}\n\nProblem and checks: ${values.get("symptom")}\n\nSoftware and firmware versions:\nExact error message:\nRelevant photos or file details:`;
      output.hidden = false;
      copy.hidden = false;
      status.textContent = "Notes prepared locally. Review them before sending through the official contact page.";
    });
    copy.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(output.value);
        status.textContent = "Support notes copied.";
      } catch {
        output.focus();
        output.select();
        status.textContent = "The notes are selected. Use your browser's copy command.";
      }
    });
  }
})();
