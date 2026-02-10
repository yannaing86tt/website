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
      btn.style.border = "1px solid rgba(102, 126, 234, 0.3)";
      btn.style.background = "rgba(102, 126, 234, 0.9)";
      btn.style.color = "#ffffff";
      btn.style.cursor = "pointer";
      btn.style.fontSize = "12px";
      btn.style.fontWeight = "600";
      btn.style.transition = "all 0.3s ease";
      // ✅ Prevent button from being selected
      btn.style.userSelect = "none";
      btn.style.webkitUserSelect = "none";
      btn.style.mozUserSelect = "none";
      btn.style.msUserSelect = "none";

      btn.addEventListener("mouseover", () => {
        btn.style.background = "rgba(102, 126, 234, 1)";
        btn.style.transform = "translateY(-2px)";
      });

      btn.addEventListener("mouseout", () => {
        btn.style.background = "rgba(102, 126, 234, 0.9)";
        btn.style.transform = "translateY(0)";
      });

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
        btn.textContent = "Copied!";
        btn.style.background = "rgba(16, 185, 129, 0.9)";
        setTimeout(() => {
          btn.textContent = old;
          btn.style.background = "rgba(102, 126, 234, 0.9)";
        }, 900);
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
    pre.style.border = "1px solid #2d3748";
    pre.style.borderRadius = "10px";
    pre.style.background = "#1a202c";
    pre.style.overflow = "auto";

    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Copy";
    btn.style.position = "absolute";
    btn.style.top = "8px";
    btn.style.right = "8px";
    btn.style.padding = "6px 10px";
    btn.style.borderRadius = "10px";
    btn.style.border = "1px solid rgba(102, 126, 234, 0.3)";
    btn.style.background = "rgba(102, 126, 234, 0.9)";
    btn.style.color = "#ffffff";
    btn.style.cursor = "pointer";
    btn.style.fontSize = "12px";
    btn.style.fontWeight = "600";
    btn.style.transition = "all 0.3s ease";
    // ✅ Prevent button from being selected
    btn.style.userSelect = "none";
    btn.style.webkitUserSelect = "none";
    btn.style.mozUserSelect = "none";
    btn.style.msUserSelect = "none";

    btn.addEventListener("mouseover", () => {
      btn.style.background = "rgba(102, 126, 234, 1)";
      btn.style.transform = "translateY(-2px)";
    });

    btn.addEventListener("mouseout", () => {
      btn.style.background = "rgba(102, 126, 234, 0.9)";
      btn.style.transform = "translateY(0)";
    });

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
      btn.textContent = "Copied!";
      btn.style.background = "rgba(16, 185, 129, 0.9)";
      setTimeout(() => {
        btn.textContent = old;
        btn.style.background = "rgba(102, 126, 234, 0.9)";
      }, 900);
    });

    pre.prepend(btn);
  });
};
