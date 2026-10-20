// Небольшое клиентское поведение интерфейса: текущий год в подвале.

const yearElement = document.getElementById("current-year");

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}
