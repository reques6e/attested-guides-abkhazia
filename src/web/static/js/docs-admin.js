function renderAdminDocuments(documents) {
    window.documents = documents;

    const tableBody = document.getElementById('documents-list');
    tableBody.innerHTML = '';

    documents.forEach((doc) => {
        const row = document.createElement('tr');
        row.classList.add('user-row');

        // Колонка с иконкой
        const iconCell = document.createElement('td');
        iconCell.classList.add('number');
        const icon = document.createElement('img');
        icon.classList.add('file-icon');
        icon.src = getIconSrc(doc.file_type);
        iconCell.appendChild(icon);

        // Колонка с названием документа
        const nameCell = document.createElement('td');
        nameCell.textContent = doc.name;

        // Колонка с ссылкой на файл
        const linkCell = document.createElement('td');
        const link = document.createElement('a');
        link.href = doc.url;
        link.textContent = 'Перейти';
        linkCell.appendChild(link);

        // Колонка с редактированием
        const fileEdit = document.createElement('td');
        const file = document.createElement('a');
        file.href = '#';
        file.textContent = 'Изменить';
        file.setAttribute('data-id', doc.id);
        file.classList.add('edit-document');
        fileEdit.appendChild(file);

        row.appendChild(iconCell);
        row.appendChild(nameCell);
        row.appendChild(linkCell);
        row.appendChild(fileEdit);

        tableBody.appendChild(row);
    });

    // Добавляем обработчик клика на кнопки "Изменить"
    document.querySelectorAll('.edit-document').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const docId = event.target.getAttribute('data-id');
            openEditModal(docId);
        });
    });
}

// Функция открытия модального окна с данными документа
function openEditModal(docId) {
    const modal = document.getElementById('edit-modal');
    const modalTitle = document.getElementById('modal-title');
    const docNameInput = document.getElementById('document-name');
    const docUrlInput = document.getElementById('document-url');
    const docTypeSelect = document.getElementById('document-type');
    const saveButton = document.getElementById('save-changes');

    // Находим документ в массиве documents (нужно передать его в функцию или сделать глобальным)
    const documentToEdit = documents.find(doc => doc.id == docId);
    
    if (documentToEdit) {
        modalTitle.textContent = `Редактирование документа #${docId}`;
        docNameInput.value = documentToEdit.name;
        docUrlInput.value = documentToEdit.url;
        docTypeSelect.value = documentToEdit.file_type;
        
        saveButton.setAttribute('data-id', docId);
        modal.style.display = 'block';
    } else {
        console.error('Документ не найден');
    }
}

// Закрытие модального окна
document.getElementById('close-modal').addEventListener('click', () => {
    document.getElementById('edit-modal').style.display = 'none';
});



async function fetchDocuments() {
    const loader = document.getElementById('loader');
    loader.classList.remove('hidden');

    try {
        const response = await fetch("http://0.0.0.0:5008/v1/docs/");
        if (!response.ok) {
            throw new Error(`Ошибка: ${response.status}`);
        }
        const data = await response.json();
        loader.classList.add('hidden');

        return data.data;
    } catch (error) {
        console.error("Ошибка при получении документов:", error);
        return [];
    }
}


function getIconSrc(fileType) {
    switch (fileType) {
        case 'doc':
            return "/static/img/files/doc.png";  // Иконка для doc
        case 'pdf':
            return "/static/img/files/pdf.png";  // Иконка для pdf
        case 'xlsx':
            return "/static/img/files/xls.png";  // Иконка для xlsx
        default:
            return "/static/img/files/doc.png";  
    }
}

// Запуск функции загрузки документов и рендеринга
document.addEventListener('DOMContentLoaded', async () => {
    const documents = await fetchDocuments();  
    renderAdminDocuments(documents);  
});

document.getElementById('save-changes').addEventListener('click', async () => {
    const docId = document.getElementById('save-changes').getAttribute('data-id');
    const name = document.getElementById('document-name').value;
    const url = document.getElementById('document-url').value;
    const file_type = document.getElementById('document-type').value;

    // Собираем данные для отправки
    const data = {
        id: docId,
        name: name,
        url: url,
        file_type: file_type
    };

    try {
        const authHash = localStorage.getItem('auth_hash');
    
        const response = await fetch('http://0.0.0.0:5008/v1/gids/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authHash}`  
            },
            body: JSON.stringify(data)
        });
        console.log(response)
        // if (!response.ok) {
        //     throw new Error(`Ошибка HTTP: ${response.status}`);
        // }

        // Закрываем модальное окно после успешного сохранения
        document.getElementById('edit-modal').style.display = 'none';
        
        // Обновляем список документов
        const updatedDocuments = await fetchDocuments();
        renderAdminDocuments(updatedDocuments);
        
        console.log('Данные успешно сохранены:', data);
        
    } catch (error) {
        console.error('Ошибка при сохранении:', error);
        alert('Произошла ошибка при сохранении данных');
    }
});