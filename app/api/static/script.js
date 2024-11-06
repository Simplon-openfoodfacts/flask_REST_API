// static/script.js

document.addEventListener("DOMContentLoaded", function () {
    const btnGoogle = document.getElementById("btn-google");
    const btnEmail = document.getElementById("btn-email");
    const btnGuest = document.getElementById("btn-guest");

    function showNavbar() {
        const navbar = document.querySelector(".navbar");
        if (navbar) {
            navbar.style.display = "flex";
        }
    }

    if (btnGoogle) btnGoogle.addEventListener("click", showNavbar);
    if (btnEmail) btnEmail.addEventListener("click", showNavbar);
    if (btnGuest) btnGuest.addEventListener("click", showNavbar);

    const nutritionalValuesMax = {
        "energy": 600,
        "saturated_fat": 10,
        "carbohydrates": 50,
        "sugars": 22.5,
        "fiber": 35,
        "proteins": 20,
        "salt": 3
    };

    window.validateInput = function (field) {
        const inputField = document.getElementById(field);
        const value = parseFloat(inputField.value);
        const max = nutritionalValuesMax[field];
        const icon = document.getElementById(`icon-${field}`);

        if (isNaN(value) || value < 0) {
            inputField.value = ""; // Réinitialiser si entrée non valide
            icon.innerHTML = ""; // Pas d'icône
            return;
        }

        if (value === 0) {
            icon.innerHTML = "❌";
            icon.style.color = "red";
        } else if (max !== "N/A" && value <= max) {
            icon.innerHTML = "✔️";
            icon.style.color = "green";
        } else if (max !== "N/A" && value > max) {
            icon.innerHTML = "❌";
            icon.style.color = "red";
        } else {
            icon.innerHTML = "";
        }

        validateForm();
    };

    function validateForm() {
        const fields = ["energy", "saturated_fat", "carbohydrates", "sugars", "fiber", "proteins", "salt"];
        const invalidFields = [];
        let allZero = true;

        fields.forEach(field => {
            const value = parseFloat(document.getElementById(field).value) || 0;
            const max = nutritionalValuesMax[field];
            const icon = document.getElementById(`icon-${field}`);
            
            if (max !== "N/A" && value > max) {
                invalidFields.push(field);
            }
            if (value !== 0) {
                allZero = false;
            }
        });

        const submitButton = document.querySelector(".calculate-button");
        const errorMessage = document.getElementById("error-message");

        if (allZero) {
            submitButton.disabled = true;
            errorMessage.textContent = "Les valeurs nutritionnelles d'un produit ne peuvent pas être toutes à zéro.";
            errorMessage.style.color = "red";
        } else if (invalidFields.length > 0) {
            submitButton.disabled = true;
            errorMessage.textContent = `Les valeurs suivantes sont incorrectes : ${invalidFields.join(", ")}`;
            errorMessage.style.color = "red";
        } else {
            submitButton.disabled = false;
            errorMessage.textContent = "";
        }
    }

    // Fonction de réinitialisation
    document.getElementById("reset-button").addEventListener("click", function () {
        const fields = ["energy", "saturated_fat", "carbohydrates", "sugars", "fiber", "proteins", "salt"];
        fields.forEach(field => {
            document.getElementById(field).value = "";
            document.getElementById(`icon-${field}`).innerHTML = "";
        });
        document.getElementById("error-message").textContent = "";
        document.querySelector(".result-grade").innerHTML = ""; // Réinitialiser le grade affiché
        document.querySelector(".calculate-button").disabled = true;
    });
});
