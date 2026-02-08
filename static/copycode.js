window.decorateCodeBlocks = function(root) {
  if (!root) return;

  // Prefer Pygments output wrapper
  const boxes = root.querySelectorAll("div.codehilite");
  if (boxes.length) {
    boxes.forEach(box => {
      if (box.dataset.copyDecorated === "1") return;
      box.dataset.copyDecorated = "1";

      const pre = box.querySelector("pre");
      if (!pre) return;

      box.style.position = "relative";
      pre.style.paddingTop = "38px";
      pre.style.borderRadius = "10px";
      pre.style.overflow = "auto";

      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = "Copy";
      btn.style.position = "absolute";
      btn.style.top = "8px";
      btn.style.right = "8px";
      btn.style.padding = "6px 10px";
      btn.style.borderRadius = "10px";
      btn.style.border = "1px solid #ddd";
      btn.style.background = "#fff";
      btn.style.cursor = "pointer";
      btn.style.fontSize = "12px";

      btn.addEventListener("click", async () => {
        const text = pre.innerText;
        try {
          await navigator.clipboard.writeText(text);
        } catch (e) {
          const ta = document.createElement("textarea");
          ta.value = text;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand("copy");
          document.body.removeChild(ta);
        }
        const old = btn.textContent;
        btn.textContent = "Copied";
        setTimeout(() => (btn.textContent = old), 900);
      });

      box.prepend(btn);
    });
    return;
  }

  // Fallback for plain <pre><code>
  root.querySelectorAll("pre").forEach(pre => {
    if (pre.dataset.copyDecorated === "1") return;
    pre.dataset.copyDecorated = "1";
    const code = pre.querySelector("code") || pre;

    pre.style.position = "relative";
    pre.style.paddingTop = "38px";
    pre.style.border = "1px solid #e5e7eb";
    pre.style.borderRadius = "10px";
    pre.style.background = "#f9fafb";
    pre.style.overflow = "auto";

    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Copy";
    btn.style.position = "absolute";
    btn.style.top = "8px";
    btn.style.right = "8px";
    btn.style.padding = "6px 10px";
    btn.style.borderRadius = "10px";
    btn.style.border = "1px solid #ddd";
    btn.style.background = "#fff";
    btn.style.cursor = "pointer";
    btn.style.fontSize = "12px";

    btn.addEventListener("click", async () => {
      const text = code.innerText;
      try {
        await navigator.clipboard.writeText(text);
      } catch (e) {
        const ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
      }
      const old = btn.textContent;
      btn.textContent = "Copied";
      setTimeout(() => (btn.textContent = old), 900);
    });

    pre.prepend(btn);
  });
};
