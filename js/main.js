/**
 * JUBAYER AI STUDIO — MAIN INTERACTIVE SCRIPT
 * Features: Filter tabs, Messenger widget toggle, live clock, copy toast, smooth scroll
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Lucide Icons
    if (window.lucide) {
        lucide.createIcons();
    }

    // 2. High-Tech System Clock (UTC+6 Dhaka)
    function updateTechClock() {
        const clockEl = document.getElementById('tech-clock');
        if (clockEl) {
            const now = new Date();
            const timeStr = now.toLocaleTimeString('en-US', {
                timeZone: 'Asia/Dhaka',
                hour12: false,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            clockEl.textContent = `${timeStr} (BST / UTC+6)`;
        }
    }
    updateTechClock();
    setInterval(updateTechClock, 1000);

    // 3. Project Filter Tabs
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active button state
            filterBtns.forEach(b => {
                b.classList.remove('bg-cyan-500/20', 'text-cyan-400', 'border-cyan-400');
                b.classList.add('bg-white/5', 'text-slate-300', 'border-white/10');
            });
            btn.classList.add('bg-cyan-500/20', 'text-cyan-400', 'border-cyan-400');
            btn.classList.remove('bg-white/5', 'text-slate-300', 'border-white/10');

            const category = btn.getAttribute('data-filter');

            projectCards.forEach(card => {
                const cardCat = card.getAttribute('data-category');
                if (category === 'all' || cardCat.includes(category)) {
                    card.classList.remove('hidden');
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 50);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(15px)';
                    setTimeout(() => {
                        card.classList.add('hidden');
                    }, 250);
                }
            });
        });
    });

    // 4. Floating Messenger Chat Widget
    const messengerFab = document.getElementById('messenger-fab');
    const messengerModal = document.getElementById('messenger-modal');
    const messengerClose = document.getElementById('messenger-close');

    if (messengerFab && messengerModal && messengerClose) {
        messengerFab.addEventListener('click', () => {
            messengerModal.classList.toggle('hidden');
            if (!messengerModal.classList.contains('hidden')) {
                // Focus message input or button
                const btn = messengerModal.querySelector('a');
                if (btn) btn.focus();
            }
        });

        messengerClose.addEventListener('click', () => {
            messengerModal.classList.add('hidden');
        });
    }

    // 5. Toast Notification System
    window.showToast = function(message) {
        const toast = document.getElementById('toast-notification');
        const toastMsg = document.getElementById('toast-message');
        if (toast && toastMsg) {
            toastMsg.textContent = message;
            toast.classList.remove('translate-y-20', 'opacity-0');
            toast.classList.add('translate-y-0', 'opacity-100');
            setTimeout(() => {
                toast.classList.remove('translate-y-0', 'opacity-100');
                toast.classList.add('translate-y-20', 'opacity-0');
            }, 3000);
        }
    };

    // 6. Copy to Clipboard handler
    const copyBtns = document.querySelectorAll('.copy-trigger');
    copyBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const textToCopy = btn.getAttribute('data-copy');
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    window.showToast(`Copied to clipboard: ${textToCopy}`);
                }).catch(err => {
                    console.error('Copy failed:', err);
                });
            }
        });
    });

    // 7. Mobile Navigation Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        // Close on link click
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });
    }

    // 8. Order / Checkout Modal
    const orderModal = document.getElementById('order-modal');
    const orderClose = document.getElementById('order-close');
    const modalProductName = document.getElementById('modal-product-name');
    const modalProductPrice = document.getElementById('modal-product-price');
    const modalWhatsAppLink = document.getElementById('modal-whatsapp-link');
    const orderTriggerBtns = document.querySelectorAll('.order-trigger-btn');

    if (orderModal) {
        orderTriggerBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const product = btn.getAttribute('data-product') || 'AI Product / Service';
                const price = btn.getAttribute('data-price') || 'Contact for Price';

                if (modalProductName) modalProductName.textContent = product;
                if (modalProductPrice) modalProductPrice.textContent = price;

                if (modalWhatsAppLink) {
                    const waText = encodeURIComponent(`Hello Jubayer, I want to order "${product}" (${price}) from Jubayer AI Studio.`);
                    modalWhatsAppLink.href = `https://wa.me/8801354840991?text=${waText}`;
                }

                orderModal.classList.remove('hidden');
            });
        });

        if (orderClose) {
            orderClose.addEventListener('click', () => {
                orderModal.classList.add('hidden');
            });
        }

        orderModal.addEventListener('click', (e) => {
            if (e.target === orderModal) {
                orderModal.classList.add('hidden');
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !orderModal.classList.contains('hidden')) {
                orderModal.classList.add('hidden');
            }
        });
    }
});

