// Находим элементы
const openModalBtn = document.getElementById("openEditProfileBtn");
const closeModalBtn = document.getElementById("closeEditProfileBtn");
const modal = document.getElementById("editProfileModal");

// Открытие модального окна при нажатии на кнопку "Редактировать профиль"
openModalBtn.addEventListener("click", function() {
    modal.style.display = "block";
});

// Закрытие модального окна при нажатии на кнопку "×"
closeModalBtn.addEventListener("click", function() {
    modal.style.display = "none";
});

// Закрытие модального окна, если кликнуть за его пределами
window.addEventListener("click", function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
});

function setStatus(status) {
    document.getElementById('current_status').value = status; // Отображение статуса в поле
}