const buttons = document.querySelectorAll("[data-view-button]");
const panels = document.querySelectorAll("[data-view-panel]");

for (const button of buttons) {
  button.addEventListener("click", () => {
    const selected = button.dataset.viewButton;

    for (const candidate of buttons) {
      const active = candidate === button;
      candidate.classList.toggle("is-active", active);
      candidate.setAttribute("aria-pressed", String(active));
    }

    for (const panel of panels) {
      panel.hidden = panel.dataset.viewPanel !== selected;
    }
  });
}
