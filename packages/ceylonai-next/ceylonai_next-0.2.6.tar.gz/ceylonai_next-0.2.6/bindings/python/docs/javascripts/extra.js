/* Ceylon AI Documentation - Extra JavaScript */

// Smooth scroll to anchor links
document.addEventListener('DOMContentLoaded', function() {
  // Add smooth scroll behavior to all anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Note: Copy button is handled by MkDocs Material (content.code.copy feature)
  // Custom copy button removed to prevent duplicate "Copy" text appearing

  // Add external link indicators
  document.querySelectorAll('a[href^="http"]').forEach(link => {
    if (!link.hostname.includes('ceylon.ai')) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
      if (!link.querySelector('.external-link-icon')) {
        const icon = document.createElement('span');
        icon.className = 'external-link-icon';
        icon.innerHTML = ' ↗';
        link.appendChild(icon);
      }
    }
  });

  // Enhance tables with responsive wrapper
  document.querySelectorAll('table').forEach(table => {
    if (!table.parentElement.classList.contains('table-wrapper')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'table-wrapper';
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }
  });

  // Add difficulty stars styling
  document.querySelectorAll('td').forEach(cell => {
    if (cell.textContent.includes('⭐')) {
      cell.style.color = '#ffc107';
      cell.style.fontSize = '1.2em';
    }
  });

  // Code block language labels
  document.querySelectorAll('pre code[class*="language-"]').forEach(block => {
    const language = block.className.match(/language-(\w+)/);
    if (language && !block.parentElement.querySelector('.language-label')) {
      const label = document.createElement('div');
      label.className = 'language-label';
      label.textContent = language[1];
      block.parentElement.insertBefore(label, block);
    }
  });

  // Add "Back to top" button
  const backToTop = document.createElement('button');
  backToTop.className = 'back-to-top';
  backToTop.innerHTML = '↑';
  backToTop.title = 'Back to top';
  backToTop.style.display = 'none';
  document.body.appendChild(backToTop);

  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      backToTop.style.display = 'block';
    } else {
      backToTop.style.display = 'none';
    }
  });

  backToTop.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  // Highlight active section in TOC
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        document.querySelectorAll('.md-nav__link').forEach(link => {
          link.classList.remove('md-nav__link--active');
        });
        const activeLink = document.querySelector(`.md-nav__link[href="#${id}"]`);
        if (activeLink) {
          activeLink.classList.add('md-nav__link--active');
        }
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('h2[id], h3[id]').forEach(heading => {
    observer.observe(heading);
  });

  // Add keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    // Press 's' to focus search
    if (e.key === 's' && !e.ctrlKey && !e.metaKey && !e.altKey) {
      const searchInput = document.querySelector('.md-search__input');
      if (searchInput && document.activeElement !== searchInput) {
        e.preventDefault();
        searchInput.focus();
      }
    }

    // Press 'Escape' to close search
    if (e.key === 'Escape') {
      const searchInput = document.querySelector('.md-search__input');
      if (searchInput && document.activeElement === searchInput) {
        searchInput.blur();
      }
    }
  });

  // Add loading indicator for async code examples
  document.querySelectorAll('code').forEach(code => {
    if (code.textContent.includes('await') || code.textContent.includes('async')) {
      const badge = document.createElement('span');
      badge.className = 'badge badge-primary';
      badge.textContent = 'Async';
      badge.style.marginLeft = '0.5rem';
      badge.style.fontSize = '0.75em';
      badge.style.verticalAlign = 'middle';
      badge.style.position = 'relative';
      badge.style.top = '-2px';

      const heading = code.closest('.md-typeset')?.querySelector('h3, h2');
      if (heading && !heading.querySelector('.badge')) {
        heading.appendChild(badge.cloneNode(true));
      }
    }
  });

  // Make API signatures more readable
  document.querySelectorAll('.api-signature').forEach(signature => {
    signature.style.overflow = 'auto';
    signature.style.maxWidth = '100%';
  });

  // Add interactive example toggle
  document.querySelectorAll('.example-toggle').forEach(toggle => {
    toggle.addEventListener('click', function() {
      const example = this.nextElementSibling;
      if (example && example.classList.contains('example-content')) {
        example.style.display = example.style.display === 'none' ? 'block' : 'none';
        this.textContent = example.style.display === 'none' ? 'Show Example' : 'Hide Example';
      }
    });
  });

  // Auto-expand code blocks that are too long
  document.querySelectorAll('pre').forEach(pre => {
    if (pre.scrollHeight > 600) {
      pre.style.maxHeight = '600px';
      pre.style.overflow = 'auto';

      const expandBtn = document.createElement('button');
      expandBtn.className = 'expand-code-btn';
      expandBtn.innerHTML = '▼'; // Down arrow icon
      expandBtn.title = 'Expand code block';
      expandBtn.setAttribute('aria-label', 'Expand code block');
      expandBtn.addEventListener('click', () => {
        if (pre.style.maxHeight === '600px') {
          pre.style.maxHeight = 'none';
          expandBtn.innerHTML = '▲'; // Up arrow icon
          expandBtn.title = 'Collapse code block';
          expandBtn.setAttribute('aria-label', 'Collapse code block');
        } else {
          pre.style.maxHeight = '600px';
          expandBtn.innerHTML = '▼'; // Down arrow icon
          expandBtn.title = 'Expand code block';
          expandBtn.setAttribute('aria-label', 'Expand code block');
        }
      });
      pre.parentElement.insertBefore(expandBtn, pre.nextSibling);
    }
  });
});

// Add version selector functionality (if needed)
function initVersionSelector() {
  const versionSelector = document.querySelector('.md-version');
  if (versionSelector) {
    versionSelector.addEventListener('click', () => {
      // Implement version switching logic
      console.log('Version selector clicked');
    });
  }
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initVersionSelector);
} else {
  initVersionSelector();
}

// Add analytics (placeholder)
function trackPageView() {
  // Add your analytics tracking here
  console.log('Page view:', window.location.pathname);
}

window.addEventListener('load', trackPageView);

// Performance monitoring
if ('PerformanceObserver' in window) {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      // Log performance metrics
      console.log('Performance:', entry.name, entry.duration);
    }
  });
  observer.observe({ entryTypes: ['navigation', 'resource'] });
}
