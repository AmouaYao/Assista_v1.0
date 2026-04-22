const WHATSAPP_NUMBER = "2250700763085";
      const CURRENCY = "FCFA";

      // Base de données des articles (fournie par Django dans le template)

      let cart = {};
      let tableNum = "";

      function fmt(n) {
        return n.toLocaleString("fr-FR") + " " + CURRENCY;
      }

      function getItem(id) {
        return itemsDB[id];
      }

      function renderCtrl(id, qty) {
        if (qty === 0)
          return `<button class="qty-btn add" onclick="addItem(${id})">+</button>`;
        return `<button class="qty-btn" onclick="removeItem(${id})">−</button><span class="qty-display">${qty}</span><button class="qty-btn add" onclick="addItem(${id})">+</button>`;
      }

      function updateItemControls(id) {
        const ctrlDiv = document.getElementById("ctrl-" + id);
        if (ctrlDiv) ctrlDiv.innerHTML = renderCtrl(id, cart[id] || 0);
      }

      function addItem(id) {
        cart[id] = (cart[id] || 0) + 1;
        updateItemControls(id);
        updateCartBar();
      }

      function removeItem(id) {
        cart[id] = Math.max(0, (cart[id] || 0) - 1);
        if (cart[id] === 0) delete cart[id];
        updateItemControls(id);
        updateCartBar();
      }

      function cartTotal() {
        return Object.entries(cart).reduce(
          (s, [id, q]) => s + getItem(parseInt(id)).price * q,
          0
        );
      }

      function cartItemCount() {
        return Object.values(cart).reduce((s, q) => s + q, 0);
      }

      function updateCartBar() {
        const cnt = cartItemCount(),
          subtotal = cartTotal();
        const pourboireParArticle = fraisApplicationActives ? montantFraisApplication : 0;
        const pourboireTotal = fraisApplicationActives ? cnt * pourboireParArticle : 0;
        const totalAvecPourboire = subtotal + pourboireTotal;
        const bar = document.getElementById("cartBar");
        document.getElementById("cartCount").textContent = cnt;
        document.getElementById("cartTotalBar").textContent = fmt(totalAvecPourboire);
        if (cnt > 0) bar.classList.add("visible");
        else bar.classList.remove("visible");
      }

      function openCart() {
        renderCartItems();
        document.getElementById("cartSheet").classList.add("open");
        document.body.style.overflow = "hidden";
      }

      function closeCart() {
        document.getElementById("cartSheet").classList.remove("open");
        document.body.style.overflow = "";
      }

      function renderCartItems() {
        const container = document.getElementById("cartItems");
        const summary = document.getElementById("cartSummary");
        container.innerHTML = "";
        const ids = Object.keys(cart);
        if (!ids.length) {
          container.innerHTML = `<div class="empty-cart"><div class="empty-icon">🌿</div><div class="empty-text">Votre panier est vide</div></div>`;
          summary.style.display = "none";
          return;
        }
        ids.forEach((id) => {
          const item = getItem(parseInt(id)),
            qty = cart[id];
          const div = document.createElement("div");
          div.className = "cart-item";
          const itemImage = item.image ? `<img src="${item.image}" alt="${item.name}">` : item.emoji;
          div.innerHTML = `
      <div class="cart-item-emoji">${itemImage}</div>
      <div class="cart-item-info">
        <div class="cart-item-name">${item.name}</div>
        <div class="cart-item-unit">${item.price.toLocaleString(
          "fr-FR"
        )} ${CURRENCY} / unité</div>
      </div>
      <div class="cart-item-right">
        <div class="cart-item-total">${(item.price * qty).toLocaleString(
          "fr-FR"
        )} F</div>
        <div class="cart-item-controls">
          <button class="cqty-btn" onclick="removeItemCart(${id})">−</button>
          <span class="cqty-display">${qty}</span>
          <button class="cqty-btn add" onclick="addItemCart(${id})">+</button>
        </div>
      </div>`;
          container.appendChild(div);
        });
        summary.style.display = "block";
        const subtotal = cartTotal();
        const itemCount = cartItemCount();
        const pourboireParArticle = fraisApplicationActives ? montantFraisApplication : 0;
        const pourboireTotal = fraisApplicationActives ? itemCount * pourboireParArticle : 0;
        const totalAvecPourboire = subtotal + pourboireTotal;
        
        document.getElementById("cartSubTotal").textContent = fmt(subtotal);
        
        // Mettre à jour le pourboire et le total final
        let summaryHtml = summary.innerHTML;
        if (!summaryHtml.includes('cartPourboire')) {
            summaryHtml += `
                <div class="summary-row" id="cartPourboire">
                    <span>Frais d'application (${itemCount} article${itemCount > 1 ? 's' : ''})</span>
                    <span class="summary-val">${fmt(pourboireTotal)}</span>
                </div>
                <div class="summary-row" style="font-weight: 600; border-top: 1px solid var(--cream-dark); padding-top: 8px; margin-top: 8px;">
                    <span>Total à payer</span>
                    <span class="summary-val">${fmt(totalAvecPourboire)}</span>
                </div>
            `;
            summary.innerHTML = summaryHtml;
        } else {
            // Mettre à jour les valeurs existantes
            const pourboireElement = summary.querySelector('#cartPourboire .summary-val');
            const totalElement = summary.querySelector('.summary-row:last-child .summary-val');
            if (pourboireElement) {
                pourboireElement.textContent = fmt(pourboireTotal);
                const pourboireLabel = summary.querySelector('#cartPourboire span:first-child');
                pourboireLabel.textContent = `Frais d'application (${itemCount} article${itemCount > 1 ? 's' : ''})`;
            }
            if (totalElement) {
                totalElement.textContent = fmt(totalAvecPourboire);
            }
        }
      }

      function addItemCart(id) {
        addItem(parseInt(id));
        renderCartItems();
      }
      function removeItemCart(id) {
        removeItem(parseInt(id));
        renderCartItems();
        if (!cartItemCount()) closeCart();
      }

      function openPayment() {
        if (!cartItemCount()) return;
        closeCart();
        renderOrderRecap();
        document.getElementById("phoneInput").value = "";
        document.getElementById("sendBtn").classList.add("disabled");
        document.getElementById("paySheet").classList.add("open");
        document.body.style.overflow = "hidden";
      }

      function closePayment() {
        document.getElementById("paySheet").classList.remove("open");
        document.body.style.overflow = "";
      }

      function renderOrderRecap() {
        const total = cartTotal();
        const itemCount = cartItemCount();
        const pourboireParArticle = fraisApplicationActives ? montantFraisApplication : 0;
        const pourboireTotal = fraisApplicationActives ? itemCount * pourboireParArticle : 0;
        const totalAvecPourboire = total + pourboireTotal;
        
        let html = `<div class="recap-title">Récapitulatif · Table ${tableNum}</div>`;
        Object.entries(cart).forEach(([id, qty]) => {
          const item = getItem(parseInt(id));
          html += `<div class="recap-item"><span>${qty}× ${
            item.name
          }</span><span>${(item.price * qty).toLocaleString(
            "fr-FR"
          )} F</span></div>`;
        });
        html += `<div class="recap-subtotal"><span>Sous-total</span><span class="recap-amount">${fmt(
          total
        )}</span></div>`;
        html += `<div class="recap-item" style="border-top: 1px solid var(--cream-dark); padding-top: 12px; margin-top: 8px;">
          <span>Frais d'application (${itemCount} article${itemCount > 1 ? 's' : ''})</span>
          <span>${fmt(pourboireTotal)}</span>
        </div>`;
        html += `<div class="recap-subtotal" style="font-weight: 600; font-size: 20px;">
          <span>Total à payer</span>
          <span class="recap-amount">${fmt(totalAvecPourboire)}</span>
        </div>`;
        
        // Ajouter le bouton de paiement Wave
        const wavePaymentUrl = `https://pay.wave.com/m/M_ci_-5o8YqgPD6iB/c/ci/?amount=${totalAvecPourboire}`;
        
        document.getElementById("orderRecap").innerHTML = html;
      }

      document
        .getElementById("phoneInput")
        .addEventListener("input", function () {
          const v = this.value.trim();
          const btn = document.getElementById("sendBtn");
          const phoneRegex = /^[0-9]{8,}$/;
          if (phoneRegex.test(v)) btn.classList.remove("disabled");
          else btn.classList.add("disabled");
        });

      async function sendOrder() {
        const phone = document.getElementById("phoneInput").value.trim();
        const phoneRegex = /^[0-9]{8,}$/;
        if (!phoneRegex.test(phone)) return;

        const notes = document.getElementById("cartNotes").value.trim();
        const total = cartTotal();

        // Préparer les données pour l'API
        const orderData = {
          table: tableNum,
          client_telephone: phone,
          total: total,
          notes: notes,
          items: Object.entries(cart).map(([id, qty]) => ({
            id: parseInt(id),
            quantite: qty
          }))
        };

        try {
          // Sauvegarder la commande dans la base de données
          const response = await fetch('/api/sauvegarder-commande/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(orderData)
          });

          const result = await response.json();
          
          if (result.success) {
            // Préparer le message WhatsApp
            let lines = [];
            lines.push("NOUVELLE COMMANDE - E-Menus");
            lines.push(`Référence : ${result.reference}`);
            lines.push(`Session : ${result.session}`);
            lines.push("Table : " + tableNum);
            lines.push("----------------------------------------");

            Object.entries(cart).forEach(([id, qty]) => {
              const it = getItem(parseInt(id));
              const itemTotal = (it.price * qty).toLocaleString("fr-FR");
              lines.push(qty + " x " + it.name + " : " + itemTotal + " FCFA");
            });

            lines.push("----------------------------------------");
            lines.push("Sous-total : " + total.toLocaleString("fr-FR") + " FCFA");
            lines.push("Frais d'application : " + result.pourboire.toLocaleString("fr-FR") + " FCFA");
            lines.push("Total à payer : " + result.total_avec_pourboire.toLocaleString("fr-FR") + " FCFA");
            lines.push("----------------------------------------");
            lines.push("numero de paiement wave : " + phone);

            if (notes) {
              lines.push("----------------------------------------");
              lines.push("Remarques : " + notes);
            }

            lines.push("----------------------------------------");
            lines.push("Merci de verifier le paiement dans votre tableau de bord Wave.");

            const message = lines.join("\n");
            const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
            window.open(url, "_blank");
            closePayment();
            document.getElementById("successScreen").classList.add("open");
          } else {
            alert('Erreur lors de la sauvegarde: ' + result.error);
          }
        } catch (error) {
          console.error('Erreur:', error);
          alert('Erreur lors de l\'envoi de la commande');
        }
      }

      function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }

      function resetApp() {
        cart = {};
        document.getElementById("successScreen").classList.remove("open");
        document.getElementById("cartNotes").value = "";
        // Réinitialiser tous les contrôles
        for (let i = 1; i <= 16; i++) {
          updateItemControls(i);
        }
        updateCartBar();
      }

      function initTable() {
        const p = new URLSearchParams(window.location.search);
        const t = p.get("table");
        if (t && t.trim()) {
          tableNum = t.trim();
          document.getElementById("tableSel").style.display = "none";
          updateTableBadge();
          initNavigation();
        }
      }

      function setTable() {
        const v = document.getElementById("tsInput").value.trim();
        if (!v) {
          document.getElementById("tsInput").focus();
          return;
        }
        tableNum = v;
        
        // Transition smooth du sélecteur de table
        const tableSelector = document.getElementById("tableSel");
        tableSelector.style.opacity = "0";
        tableSelector.style.transform = "scale(0.95)";
        
        setTimeout(() => {
          tableSelector.style.display = "none";
          updateTableBadge();
          initNavigation();
        }, 300);
      }

      function updateTableBadge() {
        document.getElementById("tableBadge").textContent = "Table " + tableNum;
        document.getElementById("payTableNum").textContent = tableNum;
      }

      function initNavigation() {
        // Afficher la première section
        document.getElementById("sec-boissons").classList.remove("hidden-cat");

        // Gestion des clics sur les boutons de catégorie
        const catBtns = document.querySelectorAll(".cat-btn");
        const sections = {
          boissons: document.getElementById("sec-boissons"),
          snacks: document.getElementById("sec-snacks"),
          plats: document.getElementById("sec-plats"),
          desserts: document.getElementById("sec-desserts"),
        };

        catBtns.forEach((btn) => {
          btn.addEventListener("click", () => {
            catBtns.forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");

            const cat = btn.getAttribute("data-cat");
            Object.values(sections).forEach((section) => {
              if (section) section.classList.add("hidden-cat");
            });
            if (sections[cat]) sections[cat].classList.remove("hidden-cat");
          });
        });
      }

      initTable();