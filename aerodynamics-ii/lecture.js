document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.querySelector(".menu-button");
  const siteNav = document.querySelector(".site-nav");
  const languageButtons = Array.from(document.querySelectorAll(".lang-button"));
  const languageSections = Array.from(document.querySelectorAll("[data-language]"));
  const translatableElements = Array.from(document.querySelectorAll("[data-ui-key]"));
  const year = document.getElementById("year");

  const ui = {
    en: {
      home: "Home",
      course: "Aerodynamics II",
      tools: "Computational tools",
      contents: "On this page",
      back: "Back to course",
      calculator: "Open calculator",
      calculatorDetails: "Calculator overview"
    },
    es: {
      home: "Inicio",
      course: "Aerodinámica II",
      tools: "Herramientas computacionales",
      contents: "En esta página",
      back: "Volver al curso",
      calculator: "Abrir calculadora",
      calculatorDetails: "Información de la calculadora"
    },
    de: {
      home: "Start",
      course: "Aerodynamik II",
      tools: "Rechnergestützte Werkzeuge",
      contents: "Auf dieser Seite",
      back: "Zurück zum Kurs",
      calculator: "Rechner öffnen",
      calculatorDetails: "Rechnerübersicht"
    }
  };

  function safeGetLanguage() {
    try {
      return localStorage.getItem("preferredLanguage");
    } catch (error) {
      return null;
    }
  }

  function safeStoreLanguage(language) {
    try {
      localStorage.setItem("preferredLanguage", language);
    } catch (error) {
      // The selector remains functional without storage.
    }
  }

  function setLanguage(language) {
    const selected = ["en", "es", "de"].includes(language) ? language : "en";

    languageSections.forEach((section) => {
      section.hidden = section.dataset.language !== selected;
    });

    languageButtons.forEach((button) => {
      const active = button.dataset.lang === selected;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });

    translatableElements.forEach((element) => {
      const key = element.dataset.uiKey;
      if (ui[selected][key]) {
        element.textContent = ui[selected][key];
      }
    });

    document.documentElement.lang = selected;
    safeStoreLanguage(selected);

    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetClear();
      window.MathJax.typesetPromise();
    }
  }

  if (menuButton && siteNav) {
    menuButton.addEventListener("click", () => {
      const open = siteNav.classList.toggle("open");
      menuButton.setAttribute("aria-expanded", String(open));
    });

    siteNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        siteNav.classList.remove("open");
        menuButton.setAttribute("aria-expanded", "false");
      });
    });
  }

  languageButtons.forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.lang));
  });

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  const stored = safeGetLanguage();
  const browser = (navigator.language || "en").slice(0, 2).toLowerCase();
  const initial = ["en", "es", "de"].includes(stored)
    ? stored
    : ["en", "es", "de"].includes(browser)
      ? browser
      : "en";

  setLanguage(initial);
});
