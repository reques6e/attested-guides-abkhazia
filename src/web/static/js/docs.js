async function fetchDocuments() {
    try {
        const response = await fetch("http://0.0.0.0:5008/v1/docs/");
        if (!response.ok) {
            throw new Error(`Ошибка: ${response.status}`);
        }
        const data = await response.json();
        return data.data;
    } catch (error) {
        console.error("Ошибка при получении документов:", error);
        return [];
    }
}


function renderDocuments(documents) {
    const tableBody = document.getElementById('documents-list');
    tableBody.innerHTML = '';  // чистим таблицу

    documents.forEach((doc, index) => {
        const row = document.createElement('tr');
        row.classList.add('user-row');

        // Колонка с иконкой
        const iconCell = document.createElement('td');
        iconCell.classList.add('number');
        const icon = document.createElement('img');
        icon.classList.add('file-icon');
        icon.src = getIconSrc(doc.type);  
        iconCell.appendChild(icon);

        // Колонка с названием документа
        const nameCell = document.createElement('td');
        nameCell.textContent = doc.name;

        // Колонка с ссылкой на файл
        const linkCell = document.createElement('td');
        const link = document.createElement('a');
        link.href = doc.file;
        link.textContent = 'Перейти';
        linkCell.appendChild(link);

        row.appendChild(iconCell);
        row.appendChild(nameCell);
        row.appendChild(linkCell);

        tableBody.appendChild(row);
    });
}

function getIconSrc(fileType) {
    switch (fileType) {
        case 'doc':
            return "static/img/files/doc.png";  // Иконка для doc
        case 'pdf':
            return "static/img/files/pdf.png";  // Иконка для pdf
        case 'xlsx':
            return "static/img/files/xls.png";  // Иконка для xlsx
        default:
            return "static/img/files/doc.png";  // Иконка по умолчанию
    }
}

// Запуск функции загрузки документов и рендеринга
document.addEventListener('DOMContentLoaded', async () => {
    const documents = await fetchDocuments();  // Получение данных из API
    renderDocuments(documents);  // Отображение данных в таблице
});