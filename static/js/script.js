document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("#submitRequestForm");
    const submitBtn = document.querySelector("#submitBtn");

    if (form && submitBtn) {

        form.addEventListener("submit", function () {

            if (form.dataset.submitting === "true") {
                return;
            }
            form.dataset.submitting = "true";

            submitBtn.disabled = true;

            submitBtn.textContent = "Submitting...";

        });

    }

});