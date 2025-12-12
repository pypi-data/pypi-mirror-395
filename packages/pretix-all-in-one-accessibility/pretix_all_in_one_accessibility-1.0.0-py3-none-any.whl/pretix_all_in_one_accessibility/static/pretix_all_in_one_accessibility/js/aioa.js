document.addEventListener("DOMContentLoaded", function () {
    // ===============================
    // FIELD TOGGLE LOGIC
    // ===============================
    function toggleFields() {
        const enablePosition = document.getElementById("id_enable_widget_icon_position");
        const enableCustomSize = document.getElementById("id_enable_icon_custom_size");

        const rightPx = document.getElementById("id_to_the_right_px");
        const rightDir = document.getElementById("id_to_the_right");
        const bottomPx = document.getElementById("id_to_the_bottom_px");
        const bottomDir = document.getElementById("id_to_the_bottom");
        const placeField = document.getElementById("id_aioa_place");

        const sizeValueField = document.getElementById("id_aioa_size_value");
        const sizeSelectField = document.querySelector(".aioa-icon-size-select-wrapper");

        // Toggle position fields
        if (enablePosition && enablePosition.checked) {
            rightPx?.parentElement && (rightPx.parentElement.style.display = "");
            rightDir?.parentElement && (rightDir.parentElement.style.display = "");
            bottomPx?.parentElement && (bottomPx.parentElement.style.display = "");
            bottomDir?.parentElement && (bottomDir.parentElement.style.display = "");
            placeField?.parentElement && (placeField.parentElement.style.display = "none");
        } else {
            rightPx?.parentElement && (rightPx.parentElement.style.display = "none");
            rightDir?.parentElement && (rightDir.parentElement.style.display = "none");
            bottomPx?.parentElement && (bottomPx.parentElement.style.display = "none");
            bottomDir?.parentElement && (bottomDir.parentElement.style.display = "none");
            placeField?.parentElement && (placeField.parentElement.style.display = "");

            // Reset values immediately
            if (rightPx) rightPx.value = 0;
            if (bottomPx) bottomPx.value = 0;
            if (rightDir) rightDir.value = "to_the_left";
            if (bottomDir) bottomDir.value = "to_the_bottom";
        }

        // Toggle icon size fields
        if (enableCustomSize && enableCustomSize.checked) {
            sizeValueField?.parentElement && (sizeValueField.parentElement.style.display = "");
            sizeSelectField && (sizeSelectField.style.display = "none");
        } else {
            sizeValueField?.parentElement && (sizeValueField.parentElement.style.display = "none");
            sizeSelectField && (sizeSelectField.style.display = "");

            // Reset value immediately
            if (sizeValueField) sizeValueField.value = 50;
        }
    }

    toggleFields();

    document.getElementById("id_enable_widget_icon_position")?.addEventListener("change", toggleFields);
    document.getElementById("id_enable_icon_custom_size")?.addEventListener("change", toggleFields);

    // ===============================
    // ICON TYPE SELECTION SYNC
    // ===============================
    const iconTypeRadios = document.querySelectorAll('input[name="aioa_icon_type"]');

    function updateIconPreviews(selectedUrl) {
        document.querySelectorAll(".aioa-icon-img-size").forEach(img => {
            const size = img.closest(".aioa-icon-option")?.dataset.size;
            if (size) {
                img.src = selectedUrl;
                img.style.width = size + "px";
                img.style.height = size + "px";
            }
        });
    }

    iconTypeRadios.forEach(radio => {
        radio.addEventListener("change", () => {
            document.querySelectorAll(".aioa-icon-select-wrapper .aioa-icon-option")
                .forEach(el => el.classList.remove("selected"));

            if (radio.checked) {
                const option = radio.closest(".aioa-icon-option");
                option && option.classList.add("selected");

                const img = option.querySelector("img");
                img && updateIconPreviews(img.src);
            }
        });
    });

    // initial highlight
    document.querySelectorAll('input[name="aioa_icon_type"]:checked').forEach(r => {
        const option = r.closest(".aioa-icon-option");
        option && option.classList.add("selected");
        const img = option.querySelector("img");
        img && updateIconPreviews(img.src);
    });

    // ===============================
    // ICON SIZE SELECTION
    // ===============================
    const iconSizeRadios = document.querySelectorAll('input[name="aioa_icon_size"]');

    iconSizeRadios.forEach(radio => {
        radio.addEventListener("change", () => {
            document.querySelectorAll(".aioa-icon-size-select-wrapper .aioa-icon-option")
                .forEach(el => el.classList.remove("selected"));

            radio.checked && radio.closest(".aioa-icon-option")?.classList.add("selected");
        });
    });

    // initial highlight
    document.querySelectorAll('input[name="aioa_icon_size"]:checked').forEach(r => {
        r.closest(".aioa-icon-option")?.classList.add("selected");
    });
});
