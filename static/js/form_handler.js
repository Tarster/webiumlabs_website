document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    if (!form) return;

    // Create a beautiful, premium glassmorphism modal element and append it to body
    const modalContainer = document.createElement("div");
    modalContainer.id = "custom-contact-modal";
    modalContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(10, 10, 10, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        z-index: 99999;
        font-family: 'Outfit', 'Inter', sans-serif;
    `;
    
    const modalContent = document.createElement("div");
    modalContent.style.cssText = `
        background: linear-gradient(135deg, rgba(25, 25, 25, 0.9) 0%, rgba(15, 15, 15, 0.95) 100%);
        border: 1px solid rgba(228, 111, 3, 0.3);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 40px rgba(228, 111, 3, 0.15);
        border-radius: 16px;
        padding: 40px;
        max-width: 480px;
        width: 90%;
        text-align: center;
        transform: scale(0.9);
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        color: #ffffff;
    `;
    
    modalContainer.appendChild(modalContent);
    document.body.appendChild(modalContainer);

    function showModal(title, message, isSuccess = true) {
        const iconHtml = isSuccess 
            ? `<div style="width: 72px; height: 72px; background: rgba(228, 111, 3, 0.1); border: 2px solid rgb(228, 111, 3); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 24px; box-shadow: 0 0 20px rgba(228, 111, 3, 0.3);">
                <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="rgb(228, 111, 3)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
               </div>`
            : `<div style="width: 72px; height: 72px; background: rgba(239, 68, 68, 0.1); border: 2px solid rgb(239, 68, 68); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 24px; box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);">
                <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="rgb(239, 68, 68)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
               </div>`;

        const buttonColor = isSuccess ? 'linear-gradient(90deg, rgb(228, 111, 3) 0%, rgb(255, 177, 104) 100%)' : 'rgb(239, 68, 68)';
        const buttonHoverColor = isSuccess ? 'rgba(228, 111, 3, 0.8)' : 'rgba(239, 68, 68, 0.8)';

        modalContent.innerHTML = `
            ${iconHtml}
            <h2 style="font-size: 26px; font-weight: 700; margin-bottom: 12px; background: ${isSuccess ? 'linear-gradient(90deg, #ff9f43, #ff5252)' : 'none'}; -webkit-background-clip: ${isSuccess ? 'text' : 'none'}; -webkit-text-fill-color: ${isSuccess ? 'transparent' : 'white'}; color: ${isSuccess ? 'none' : '#ef4444'}">${title}</h2>
            <p style="font-size: 16px; color: rgba(255, 255, 255, 0.7); line-height: 1.6; margin-bottom: 30px;">${message}</p>
            <button id="modal-close-btn" style="
                background: ${buttonColor};
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px 32px;
                font-size: 15px;
                font-weight: 600;
                cursor: pointer;
                outline: none;
                transition: transform 0.2s, opacity 0.2s;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            ">Dismiss</button>
        `;

        modalContainer.style.opacity = "1";
        modalContainer.style.pointerEvents = "auto";
        modalContent.style.transform = "scale(1)";

        const closeBtn = document.getElementById("modal-close-btn");
        closeBtn.addEventListener("click", closeModal);
        
        closeBtn.addEventListener("mouseenter", () => {
            closeBtn.style.transform = "scale(1.03)";
            closeBtn.style.opacity = "0.95";
        });
        closeBtn.addEventListener("mouseleave", () => {
            closeBtn.style.transform = "scale(1)";
            closeBtn.style.opacity = "1";
        });
    }

    function closeModal() {
        modalContainer.style.opacity = "0";
        modalContainer.style.pointerEvents = "none";
        modalContent.style.transform = "scale(0.9)";
    }

    // Close modal on container click (outside modal content)
    modalContainer.addEventListener("click", function(e) {
        if (e.target === modalContainer) {
            closeModal();
        }
    });

    // Helper to get CSRF cookie value
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

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        e.stopPropagation();

        // Locate submit button
        const submitBtn = form.querySelector("button[type='submit']") || form.querySelector("button");
        const originalBtnText = submitBtn ? submitBtn.innerHTML : "Submit";

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <span style="display: inline-flex; align-items: center;">
                    <svg class="spinner" viewBox="0 0 50 50" style="width: 20px; height: 20px; animation: rotate 2s linear infinite; margin-right: 8px;">
                        <circle class="path" cx="25" cy="25" r="20" fill="none" stroke="currentColor" stroke-width="5" style="stroke-linecap: round; animation: dash 1.5s ease-in-out infinite;"></circle>
                    </svg>
                    Sending...
                </span>
            `;
            
            // Add style for animations if not already present
            if (!document.getElementById("spinner-styles")) {
                const styles = document.createElement("style");
                styles.id = "spinner-styles";
                styles.innerHTML = `
                    @keyframes rotate { 100% { transform: rotate(360deg); } }
                    @keyframes dash {
                        0% { stroke-dasharray: 1, 150; stroke-dashoffset: 0; }
                        50% { stroke-dasharray: 90, 150; stroke-dashoffset: -35; }
                        100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124; }
                    }
                `;
                document.head.appendChild(styles);
            }
        }

        // Gather all fields, matching the actual names of elements in contact.html
        const nameInput = form.querySelector("[name='Name']") || form.querySelector("[name='name']");
        const emailInput = form.querySelector("[name='Email']") || form.querySelector("[name='email']");
        const companyInput = form.querySelector("[name='Company']") || form.querySelector("[name='company']");
        const serviceSelect = form.querySelector("[name='Service']") || form.querySelector("[name='service']");
        const budgetSelect = form.querySelector("[name='Budget']") || form.querySelector("[name='budget']");
        
        // Textarea might have name="message" (after replace) or name="Name" (duplicate in original)
        // Find by tag name 'textarea' to be 100% sure
        const messageTextarea = form.querySelector("textarea");

        const payload = {
            name: nameInput ? nameInput.value : "",
            email: emailInput ? emailInput.value : "",
            company: companyInput ? companyInput.value : "",
            service: serviceSelect ? serviceSelect.value : "",
            budget: budgetSelect ? budgetSelect.value : "",
            message: messageTextarea ? messageTextarea.value : ""
        };

        const csrfToken = getCookie("csrftoken");

        fetch("/contact/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(payload)
        })
        .then(async response => {
            const data = await response.json();
            if (response.ok) {
                showModal("Message Sent!", data.message, true);
                form.reset();
            } else {
                // If there are specific field errors, format them beautifully
                let errorMsg = "";
                if (data.errors) {
                    errorMsg = Object.values(data.errors).join("<br>");
                } else {
                    errorMsg = data.error || "Please verify your inputs and try again.";
                }
                showModal("Validation Error", errorMsg, false);
            }
        })
        .catch(error => {
            console.error("Submission error:", error);
            showModal("Connection Failed", "Unable to send your request. Please check your network and try again.", false);
        })
        .finally(() => {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        });
    });
});
