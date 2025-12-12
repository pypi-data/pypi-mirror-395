// ============ ТЁМНАЯ / СВЕТЛАЯ ТЕМА ============
const body = document.body;
const toggle = document.getElementById("themeToggle");

if (localStorage.getItem("theme") === "dark") {
    body.classList.add("dark");
}

toggle.addEventListener("click", () => {
    body.classList.toggle("dark");
    localStorage.setItem("theme", body.classList.contains("dark") ? "dark" : "light");
});

// ============ COLLAPSIBLE PANELS ============
document.querySelectorAll(".collapsible").forEach(h => {
    h.addEventListener("click", () => {
        const content = h.nextElementSibling;
        h.classList.toggle("active");
        content.classList.toggle("open");
    });
});

// ============ КНОПКА «РЕФАКТОРИНГ» ============
document.getElementById("refactorBtn").addEventListener("click", () => {
    alert("Рефакторинг не реализован.\n\nНо проект явно намекает.");
});

// ============ ПОИСК В ОТЧЁТЕ ============
const searchInput = document.getElementById("searchInput");
const reportBlock = document.getElementById("reportBlock");
const originalText = reportBlock.textContent;

searchInput.addEventListener("input", () => {
    const q = searchInput.value.trim();
    if (!q) {
        reportBlock.textContent = originalText;
        return;
    }
    const regex = new RegExp(q, "gi");
    reportBlock.innerHTML = originalText.replace(regex, m => `<span class="highlight">${m}</span>`);
});

// ============ Chart.js: строки по расширениям ============
if (window.PROJECT_METRICS && window.PROJECT_METRICS.ext_lines) {
    const ctx = document.getElementById("extChart");
    if (ctx && window.Chart) {
        const labels = Object.keys(window.PROJECT_METRICS.ext_lines);
        const data = Object.values(window.PROJECT_METRICS.ext_lines);

        new Chart(ctx, {
            type: "bar",
            data: {
                labels,
                datasets: [{
                    label: "Строк кода по расширениям",
                    data
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: false
                    }
                },
                scales: {
                    x: { ticks: { color: getComputedStyle(document.body).color } },
                    y: { ticks: { color: getComputedStyle(document.body).color } }
                }
            }
        });
    }
}
