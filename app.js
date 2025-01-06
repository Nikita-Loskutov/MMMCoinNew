document.addEventListener('DOMContentLoaded', () => {
    const hamster = document.getElementById('hamster');
    const scoreElement = document.getElementById('score');
    const progressBar = document.querySelector('.level-progress');
    let score = parseInt(scoreElement.innerText);

    function updateProgressBar() {
        const percentage = (score / 5000) * 100;
        progressBar.style.width = `${Math.min(percentage, 100)}%`;
    }

    hamster.addEventListener('click', (event) => {
        const rect = hamster.getBoundingClientRect();
        const offfsetX = event.clientX - rect.left - rect.width / 2;
        const offfsetY = event.clientY - rect.top - rect.height / 2;
        const DEG = 40;
        const tiltX = (offfsetY / rect.height) * DEG;
        const tiltY = (offfsetX / rect.width) * -DEG;

        hamster.style.setProperty('--tiltX', `${tiltX}deg`);
        hamster.style.setProperty('--tiltY', `${tiltY}deg`);

        setTimeout(() => {
            hamster.style.setProperty('--tiltX', `0deg`);
            hamster.style.setProperty('--tiltY', `0deg`);
        }, 300);

        // Увеличиваем счёт
        score += 1;
        scoreElement.innerText = score;

        // Обновляем прогресс-бар
        updateProgressBar();

        // Создаём элемент для взлетающей цифры +1
        const plusOne = document.createElement('div');
        plusOne.className = 'floating-plus-one';
        plusOne.innerText = '+1';

        // Получаем позицию клика и устанавливаем координаты для элемента
        plusOne.style.left = `${event.clientX}px`;
        plusOne.style.top = `${event.clientY}px`;

        document.body.appendChild(plusOne);

        // Удаляем элемент после завершения анимации
        setTimeout(() => {
            document.body.removeChild(plusOne);
        }, 1000);
    });

    // Инициализируем прогресс-бар при загрузке
    updateProgressBar();


});