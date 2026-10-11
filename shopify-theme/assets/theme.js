document.addEventListener('DOMContentLoaded', () => {
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

  const menuToggle = $('[data-menu-toggle]');
  const mobileMenu = $('[data-mobile-menu]');
  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
      const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', String(!isOpen));
      mobileMenu.hidden = isOpen;
      const label = $('.visually-hidden', menuToggle);
      if (label) label.textContent = isOpen ? 'Open menu' : 'Close menu';
    });
  }

  $$("[data-quantity-plus], [data-quantity-minus]").forEach((button) => {
    button.addEventListener('click', () => {
      const input = $('input', button.parentElement);
      if (!input) return;
      const current = parseInt(input.value, 10) || 1;
      const min = parseInt(input.min, 10) || 0;
      input.value = button.hasAttribute('data-quantity-plus') ? current + 1 : Math.max(min, current - 1);
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });
  });

  const openWhatsApp = (number, message) => {
    if (!number) return;
    window.open(`https://wa.me/${number}?text=${encodeURIComponent(message)}`, '_blank', 'noopener');
  };

  const bindWhatsApp = () => {
    $$('[data-whatsapp-product]').forEach((button) => {
      if (button.dataset.bound) return;
      button.dataset.bound = 'true';
      button.addEventListener('click', () => {
        const title = button.dataset.productTitle || 'this piece';
        const variant = button.dataset.variantTitle && button.dataset.variantTitle !== 'Default Title' ? `, size ${button.dataset.variantTitle}` : '';
        openWhatsApp(button.dataset.whatsappNumber, `Hi Ababeel Fashions! I would like to know more about ${title}${variant}. Is it available?`);
      });
    });
    $$('[data-whatsapp-cart]').forEach((button) => {
      if (button.dataset.bound) return;
      button.dataset.bound = 'true';
      button.addEventListener('click', () => {
        const items = [...document.querySelectorAll('.cart-item__details h2, .drawer-item h3')].map((item) => item.textContent.trim());
        const message = items.length ? `Hi Ababeel Fashions! I need help with my cart: ${items.join(', ')}.` : 'Hi Ababeel Fashions! I need help choosing an outfit.';
        openWhatsApp(button.dataset.whatsappNumber, message);
      });
    });
  };
  bindWhatsApp();

  const variantSelect = $('[data-variant-select]');
  if (variantSelect) {
    variantSelect.addEventListener('change', () => {
      const selected = variantSelect.options[variantSelect.selectedIndex];
      const whatsappButton = $('[data-whatsapp-product]');
      if (whatsappButton && selected) whatsappButton.dataset.variantTitle = selected.textContent.split(' — ')[0].trim();
    });
  }

  const updateCartCount = (count) => {
    $$('.cart-count').forEach((counter) => { counter.textContent = count; });
    $$('[data-cart-count]').forEach((counter) => { counter.textContent = `(${count})`; });
  };

  const drawerElement = () => $('[data-cart-drawer]');
  const setDrawerState = (open) => {
    const drawer = drawerElement();
    if (!drawer) return;
    drawer.classList.toggle('is-open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    document.body.classList.toggle('cart-drawer-open', open);
    if (open) $('.cart-drawer__close', drawer)?.focus();
  };

  const bindDrawer = () => {
    const drawer = drawerElement();
    if (!drawer) return;
    $$('[data-cart-close]', drawer).forEach((button) => {
      if (button.dataset.bound) return;
      button.dataset.bound = 'true';
      button.addEventListener('click', () => setDrawerState(false));
    });
  };
  bindDrawer();

  const refreshDrawer = async () => {
    const drawer = drawerElement();
    if (!drawer) return;
    try {
      const response = await fetch('/?sections=cart-drawer', { headers: { Accept: 'application/json' } });
      if (!response.ok) return;
      const sections = await response.json();
      if (!sections['cart-drawer']) return;
      const wrapper = document.createElement('div');
      wrapper.innerHTML = sections['cart-drawer'];
      const nextDrawer = wrapper.firstElementChild;
      if (nextDrawer) {
        drawer.replaceWith(nextDrawer);
        bindDrawer();
        bindWhatsApp();
        bindDrawerQuantity();
        updateFreeShip();
      }
    } catch (error) { console.warn('Cart drawer refresh failed', error); }
  };

  $$('.commerce-cart').forEach((link) => {
    link.addEventListener('click', (event) => {
      if (drawerElement()) { event.preventDefault(); setDrawerState(true); }
    });
  });

  $$('[data-ajax-add]').forEach((form) => {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const button = $('button[type="submit"]', form);
      if (!button || button.disabled) return;
      const originalText = button.innerHTML;
      button.disabled = true;
      button.innerHTML = 'Adding…';
      try {
        const formData = new FormData(form);
        const response = await fetch('/cart/add.js', { method: 'POST', headers: { Accept: 'application/json' }, body: formData });
        if (!response.ok) throw new Error('Unable to add item');
        const cartResponse = await fetch('/cart.js', { headers: { Accept: 'application/json' } });
        const cart = await cartResponse.json();
        updateCartCount(cart.item_count);
        await refreshDrawer();
        button.innerHTML = 'Added ✓';
        setDrawerState(true);
        setTimeout(() => { button.innerHTML = originalText; button.disabled = false; }, 1300);
      } catch (error) {
        button.innerHTML = 'Try again';
        button.disabled = false;
        console.warn(error);
      }
    });
  });

  const wishlistKey = 'ababeel-wishlist';
  let wishlist = [];
  try { wishlist = JSON.parse(localStorage.getItem(wishlistKey) || '[]'); } catch (error) { wishlist = []; }
  const saveWishlist = () => localStorage.setItem(wishlistKey, JSON.stringify(wishlist));
  $$('[data-wishlist]').forEach((button) => {
    const handle = button.dataset.wishlist;
    const active = wishlist.includes(handle);
    button.classList.toggle('is-wishlisted', active);
    button.setAttribute('aria-pressed', String(active));
    button.addEventListener('click', () => {
      const index = wishlist.indexOf(handle);
      if (index === -1) wishlist.push(handle); else wishlist.splice(index, 1);
      const isActive = wishlist.includes(handle);
      button.classList.toggle('is-wishlisted', isActive);
      button.setAttribute('aria-pressed', String(isActive));
      button.setAttribute('aria-label', `${isActive ? 'Remove' : 'Add'} ${handle} ${isActive ? 'from' : 'to'} wishlist`);
      saveWishlist();
    });
  });

  const searchInput = $('.commerce-search input');
  if (searchInput) {
    let searchTimer;
    const searchForm = searchInput.closest('form');
    const resultBox = document.createElement('div');
    resultBox.className = 'predictive-search-results';
    resultBox.setAttribute('aria-live', 'polite');
    searchForm?.appendChild(resultBox);
    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimer);
      const term = searchInput.value.trim();
      if (term.length < 2) { resultBox.innerHTML = ''; resultBox.hidden = true; return; }
      searchTimer = setTimeout(async () => {
        try {
          const response = await fetch(`/search/suggest.json?q=${encodeURIComponent(term)}&resources[type]=product&resources[limit]=5`);
          const data = await response.json();
          const products = data.resources?.results?.products || [];
          resultBox.innerHTML = products.length ? products.map((product) => `<a href="${product.url}"><span>${product.title}</span><small>${product.price}</small></a>`).join('') : '<p>No pieces found. Try another search.</p>';
          resultBox.hidden = false;
        } catch (error) { resultBox.hidden = true; }
      }, 220);
    });
    document.addEventListener('click', (event) => { if (!searchForm?.contains(event.target)) resultBox.hidden = true; });
  }

  const filterToggle = $('[data-filter-toggle]');
  const filterPanel = $('[data-filter-panel]');
  if (filterToggle && filterPanel) {
    filterToggle.addEventListener('click', () => {
      const open = filterPanel.classList.toggle('is-open');
      filterToggle.setAttribute('aria-expanded', String(open));
    });
    $('[data-filter-close]', filterPanel)?.addEventListener('click', () => filterPanel.classList.remove('is-open'));
  }

  /* ---- Premium commerce layer: drawer quantity, free-ship progress, countdown, gallery, back-to-top ---- */
  const inr = (cents) => `₹${(cents / 100).toLocaleString('en-IN')}`;
  const FREE_SHIP_THRESHOLD = 99900;

  const updateFreeShip = async () => {
    const box = $('[data-free-ship]');
    if (!box) return;
    try {
      const response = await fetch('/cart.js', { headers: { Accept: 'application/json' } });
      if (!response.ok) return;
      const cart = await response.json();
      const text = $('[data-free-ship-text]', box);
      const bar = $('[data-free-ship-bar]', box);
      const remaining = FREE_SHIP_THRESHOLD - cart.total_price;
      if (remaining <= 0) {
        text.textContent = 'You unlocked FREE shipping across India 🎉';
      } else {
        text.textContent = `You are ${inr(remaining)} away from FREE shipping`;
      }
      bar.style.width = `${Math.min(100, Math.round((cart.total_price / FREE_SHIP_THRESHOLD) * 100))}%`;
    } catch (error) { /* static preview or offline: leave neutral */ }
  };

  const bindDrawerQuantity = () => {
    $$('[data-quantity-plus][data-line], [data-quantity-minus][data-line]').forEach((button) => {
      if (button.dataset.bound) return;
      button.dataset.bound = 'true';
      button.addEventListener('click', async () => {
        const line = parseInt(button.dataset.line, 10);
        const counter = $('[data-line-qty]', button.parentElement);
        const current = counter ? parseInt(counter.textContent, 10) || 1 : 1;
        const quantity = button.hasAttribute('data-quantity-plus') ? current + 1 : Math.max(1, current - 1);
        try {
          const response = await fetch('/cart/change.js', {
            method: 'POST',
            headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
            body: JSON.stringify({ line, quantity }),
          });
          if (!response.ok) throw new Error('change failed');
          const cart = await response.json();
          updateCartCount(cart.item_count);
          await refreshDrawer();
          updateFreeShip();
        } catch (error) { console.warn('Quantity update failed', error); }
      });
    });
  };
  bindDrawerQuantity();
  updateFreeShip();

  $$('[data-countdown]').forEach((element) => {
    const hours = parseFloat(element.dataset.countdown) || 48;
    const deadline = Date.now() + hours * 3600 * 1000;
    const pad = (value) => String(value).padStart(2, '0');
    const tick = () => {
      const delta = Math.max(0, deadline - Date.now());
      const h = Math.floor(delta / 3600000);
      const m = Math.floor((delta % 3600000) / 60000);
      const s = Math.floor((delta % 60000) / 1000);
      const hEl = $('[data-count-h]', element);
      const mEl = $('[data-count-m]', element);
      const sEl = $('[data-count-s]', element);
      if (hEl) hEl.textContent = pad(h);
      if (mEl) mEl.textContent = pad(m);
      if (sEl) sEl.textContent = pad(s);
    };
    tick();
    setInterval(tick, 1000);
  });

  $$('.product-gallery__thumb').forEach((thumb) => {
    thumb.addEventListener('click', () => {
      const index = parseInt(thumb.dataset.thumb, 10);
      $$('.product-gallery__item').forEach((item, i) => item.classList.toggle('product-gallery__item--featured', i === index));
      $$('.product-gallery__thumb').forEach((t, i) => {
        t.classList.toggle('is-active', i === index);
        t.setAttribute('aria-current', String(i === index));
      });
    });
  });

  const backToTop = $('[data-back-to-top]');
  if (backToTop) {
    const onScroll = () => backToTop.classList.toggle('is-visible', window.scrollY > 600);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    backToTop.addEventListener('click', () => {
      const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    });
  }
});
