// Copy code button functionality
document.addEventListener('DOMContentLoaded', function() {
  // Find all code blocks
  const codeBlocks = document.querySelectorAll('pre code, pre');
  
  codeBlocks.forEach(function(block) {
    // Skip if already has copy button
    if (block.parentElement.querySelector('.copy-code-btn')) {
      return;
    }
    
    // Create copy button
    const button = document.createElement('button');
    button.className = 'copy-code-btn';
    button.innerHTML = '📋 Copy';
    button.setAttribute('aria-label', 'Copy code');
    
    // Style the button
    button.style.cssText = `
      position: absolute;
      top: 8px;
      right: 8px;
      padding: 6px 12px;
      background: rgba(102, 126, 234, 0.9);
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 12px;
      font-weight: 600;
      transition: all 0.2s;
      z-index: 10;
    `;
    
    // Make parent position relative
    const parent = block.parentElement.tagName === 'PRE' ? block.parentElement : block;
    if (parent.tagName === 'PRE') {
      parent.style.position = 'relative';
    }
    
    // Add click handler
    button.addEventListener('click', function() {
      const code = block.textContent || block.innerText;
      
      // Copy to clipboard
      if (navigator.clipboard) {
        navigator.clipboard.writeText(code).then(function() {
          button.innerHTML = '✅ Copied!';
          button.style.background = 'rgba(34, 197, 94, 0.9)';
          
          setTimeout(function() {
            button.innerHTML = '📋 Copy';
            button.style.background = 'rgba(102, 126, 234, 0.9)';
          }, 2000);
        }).catch(function(err) {
          console.error('Copy failed:', err);
          fallbackCopy(code, button);
        });
      } else {
        fallbackCopy(code, button);
      }
    });
    
    // Hover effect
    button.addEventListener('mouseenter', function() {
      button.style.background = 'rgba(102, 126, 234, 1)';
      button.style.transform = 'scale(1.05)';
    });
    
    button.addEventListener('mouseleave', function() {
      if (button.innerHTML === '📋 Copy') {
        button.style.background = 'rgba(102, 126, 234, 0.9)';
        button.style.transform = 'scale(1)';
      }
    });
    
    // Add button to DOM
    parent.appendChild(button);
  });
  
  // Fallback copy method for older browsers
  function fallbackCopy(text, button) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-9999px';
    document.body.appendChild(textArea);
    textArea.select();
    
    try {
      document.execCommand('copy');
      button.innerHTML = '✅ Copied!';
      button.style.background = 'rgba(34, 197, 94, 0.9)';
      
      setTimeout(function() {
        button.innerHTML = '📋 Copy';
        button.style.background = 'rgba(102, 126, 234, 0.9)';
      }, 2000);
    } catch (err) {
      console.error('Fallback copy failed:', err);
      button.innerHTML = '❌ Failed';
      setTimeout(function() {
        button.innerHTML = '📋 Copy';
      }, 2000);
    }
    
    document.body.removeChild(textArea);
  }
});
