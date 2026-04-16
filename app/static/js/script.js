// Auto-hide flash notification toasts shortly after they appear.
setTimeout(() => {
    document.querySelectorAll(".notice-toast").forEach((el) => {
        el.classList.add("is-hiding");
        setTimeout(() => el.remove(), 250);
    });
}, 3000);
