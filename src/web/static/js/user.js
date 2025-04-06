// Имитация базы данных экскурсоводов
const guidesDatabase = {
    "U191KK": {
        id: "U191KK",
        fullName: "Абанос Астамур Русланович",
        photoProfile: "https://img.freepik.com/free-photo/close-up-shot-serious-looking-handsome-adult-european-man-with-red-hair-beard-staring-with-focused-determined-expression-standing-strict-pose-gray-wall_176420-27574.jpg?t=st=1743933775~exp=1743937375~hmac=962096c06812fd48366a04e537080bd062975393b7bbb4e4ffa8a6d8f81c2b19&w=996",
        category: "Первая категория",
        license: {
            number: "№ 8368 от 03.10.2022 г.",
            issuingAuthority: "Министерство туризма Республики Абхазия",
            issueDate: "05.10.2022",
            status: "Отозвана"
        },
        tags: ["Исторические экскурсии", "Природные маршруты"],
        contacts: {
            phone: "7940-997-09-79",
            email: "",
            address: ""
        },
        routes: [
            {
                id: 1,
                name: "Основной маршрут",
                groupNumber: "№ в группе: 1",
                points: [
                    "пос. Гячрыпш",
                    "г. Гагра",
                    "г. Пицунда",
                    "оз. Рица",
                    "г. Н. Афон",
                    "пос. Гячрыпш"
                ]
            }
        ],
        additionalInfo: {
            inn: "123456789012",
            examType: "Очный (теория + практика)",
            entityType: "Физическое лицо"
        },
        history: [
            { date: "12.07.2023", action: "Добавлен в реестр" },
            { date: "15.08.2023", action: "Номер телефона обновлён" },
            { date: "20.09.2023", action: "ФИО было обновлено" },
            { date: "01.10.2023", action: "Добавлен новый маршрут" }
        ]
    }
};

// Функция для получения данных экскурсовода
function getGuideById(guideId) {
    return new Promise(async (resolve, reject) => {
        try {
            const response = await fetch(`http://0.0.0.0:5008/v1/gids/?id=${guideId}`);
            if (!response.ok) {
                throw new Error(`Ошибка: ${response.status}`);
            }

            const data = await response.json();
            console.log(data)
            if (data) {
                const processedGuide = processEmptyFields(data);
                resolve(processedGuide);
            } else {
                reject(new Error("Экскурсовод с указанным ID не найден"));
            }
        } catch (error) {
            console.error("Ошибка при получении данных экскурсовода:", error);
            reject(error);
        }
    });
}

// Функция для обработки пустых полей
function processEmptyFields(data) {
    const processed = JSON.parse(JSON.stringify(data));
    function process(obj) {
        for (const key in obj) {
            if (obj[key] === null || obj[key] === undefined || obj[key] === "") {
                obj[key] = "Нет данных";
            } else if (typeof obj[key] === "object") {
                process(obj[key]);
            }
        }
    }
    process(processed);
    return processed;
}

// Функция для обновления интерфейса
function updateUI(guide) {
    const isLicenseRevoked = guide.license.status === "Отозвана";

    // Уведомление об отозванной лицензии
    if (isLicenseRevoked) {
        const warningBanner = document.createElement('div');
        warningBanner.className = 'license-warning';
        warningBanner.innerHTML = `
            <div class="license-warning-content">
                <strong>Внимание!</strong> Лицензия данного экскурсовода была отозвана.
                Проведение экскурсий запрещено.
            </div>
        `;
        document.querySelector('.container').insertBefore(warningBanner, document.querySelector('.profile-card'));
    }

    // 1. Обновляем основную информацию
    safeSetText('.profile-title', guide.fullName);
    safeSetText('.profile-subtitle', `ID: ${guide.id} | Экскурсовод ${guide.category.toLowerCase()}`);

    // 2. Обновляем аватар
    const avatar = document.querySelector('.profile-avatar');
    if (avatar) {
        if (guide.photoProfile) {
            // Если есть URL фото, используем его
            avatar.src = guide.photoProfile;
            avatar.alt = `Фото ${guide.fullName}`;
            avatar.style.display = 'block';
            const initialsElement = document.querySelector('.profile-avatar-initials');
            if (initialsElement) {
                initialsElement.style.display = 'none';
            }
        } else {
            // Если фото нет, показываем инициалы
            const names = guide.fullName.split(' ');
            const initials = (names[0][0] || '') + (names[1] ? names[1][0] : '');
            const initialsElement = document.querySelector('.profile-avatar-initials');
            if (initialsElement) {
                initialsElement.textContent = initials;
                initialsElement.style.display = 'flex';
            }
            avatar.style.display = 'none';
        }
    }

    // 3. Обновляем контакты и основную информацию
    const infoGrid = document.querySelector('.info-grid');
    if (infoGrid) {
        const infoValues = infoGrid.querySelectorAll('.info-value');
        if (infoValues.length >= 4) {
            infoValues[0].textContent = guide.contacts.phone || 'Нет данных';
            infoValues[1].textContent = guide.category || 'Нет данных';
            infoValues[2].textContent = guide.license.issuingAuthority || 'Нет данных';
            infoValues[3].textContent = guide.license.number || 'Нет данных';
        }
    }

    // 4. Обновляем маршруты
    const routesContainer = document.querySelector('.profile-card h3').parentNode;
    if (routesContainer && guide.routes && guide.routes.length > 0) {
        // Очищаем существующие маршруты (кроме заголовка)
        while (routesContainer.children.length > 1) {
            routesContainer.removeChild(routesContainer.lastChild);
        }

        // Добавляем каждый маршрут
        guide.routes.forEach(route => {
            const routeCard = document.createElement('div');
            routeCard.className = 'route-card';
            
            const routeTitle = document.createElement('div');
            routeTitle.className = 'route-title';
            routeTitle.innerHTML = `
                ${route.name || 'Маршрут'}
                <span class="route-number">${route.groupNumber || '№ в группе: N/A'}</span>
            `;
            
            const routePoints = document.createElement('div');
            routePoints.className = 'route-points';
            
            if (route.points && route.points.length > 0) {
                route.points.forEach((point, index) => {
                    const pointElement = document.createElement('span');
                    pointElement.className = 'route-point';
                    pointElement.textContent = point;
                    routePoints.appendChild(pointElement);

                    if (index < route.points.length - 1) {
                        const arrow = document.createElement('span');
                        // arrow.className = 'route-arrow';
                        // arrow.innerHTML = ' &rarr; ';
                        routePoints.appendChild(arrow);
                    }
                });
            } else {
                routePoints.innerHTML = '<span class="route-point">Нет данных о маршруте</span>';
            }
            
            routeCard.appendChild(routeTitle);
            routeCard.appendChild(routePoints);
            routesContainer.appendChild(routeCard);
        });
    }
    // 5. Обновляем дополнительные данные
    const profileCards = document.querySelectorAll('.profile-card');
    if (profileCards.length >= 3) {
        const additionalInfoValues = profileCards[2].querySelectorAll('.info-value');
        if (additionalInfoValues.length >= 4) {
            additionalInfoValues[0].textContent = guide.additionalInfo.inn || 'Нет данных';
            additionalInfoValues[1].textContent = guide.additionalInfo.examType || 'Нет данных';
            additionalInfoValues[2].textContent = guide.additionalInfo.entityType || 'Нет данных';
            additionalInfoValues[3].textContent = guide.license.issueDate || 'Нет данных';
        }
    }

    // 6. Обновляем историю изменений
    const historyContainer = document.getElementById('history-container');
    if (historyContainer && guide.history) {
        historyContainer.innerHTML = '';
        guide.history.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = 'info-item';

            const label = document.createElement('span');
            label.className = 'info-label';
            label.textContent = item.date;

            const value = document.createElement('div');
            value.className = 'info-value';
            value.textContent = item.action;

            itemElement.appendChild(label);
            itemElement.appendChild(value);
            historyContainer.appendChild(itemElement);
        });
    }

    // 7. Обновляем бейджи
    const badgesContainer = document.getElementById('badges-container');
    if (badgesContainer) {
        badgesContainer.innerHTML = '';

        if (guide.license && guide.license.status) {
            const licenseBadge = document.createElement('span');
            licenseBadge.className = isLicenseRevoked ? 'badge badge-revoked' : 'badge';
            licenseBadge.textContent = guide.license.status;
            badgesContainer.appendChild(licenseBadge);
        }

        if (guide.tags) {
            guide.tags.forEach(tag => {
                const badge = document.createElement('span');
                badge.className = 'badge';
                badge.textContent = tag;
                badgesContainer.appendChild(badge);
            });
        }
    }
}

function safeSetText(selector, text) {
    const element = document.querySelector(selector);
    if (element) {
        element.textContent = text || 'Нет данных';
    }
}

// Загрузка данных
document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loader');
    loader.classList.remove('hidden');

    const userInfoElement = document.getElementById('user-info');
    const guideId = userInfoElement ? userInfoElement.getAttribute('data-user-id') : null;

    getGuideById(guideId)
        .then(guide => {
            updateUI(guide);
        })
        .catch(error => {
            console.error("Ошибка:", error.message);
        })
        .finally(() => {
            loader.classList.add('hidden');
        });
});