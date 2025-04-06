let users = [];
let currentPage = 1;
const usersPerPage = 10;

async function loadUsers() {
    try {
        const response = await fetch("http://0.0.0.0:5008/v1/gids/all/");
        if (!response.ok) {
            throw new Error(`Ошибка: ${response.status}`);
        }
        const data = await response.json();
        users = data;
    } catch (error) {
        console.error("Ошибка при получении документов:", error);
        return [];
    }

    renderTable();
}
function renderTable() {
    const tableBody = document.getElementById("tableBody");
    tableBody.innerHTML = "";

    const startIndex = (currentPage - 1) * usersPerPage;
    const endIndex = startIndex + usersPerPage;
    const visibleUsers = users.slice(startIndex, endIndex);

    visibleUsers.forEach((user, index) => {
        const row = document.createElement("tr");
        row.className = "user-row";
        row.onclick = () => goToProfile(`user/${user.id}`);
        row.innerHTML = `
            <td class="number">${startIndex + index + 1}</td>
            <td>${user.name}</td>
            <td class="id">${user.id}</td>
            <td>+${user.phone}</td>
        `;
        tableBody.appendChild(row);
    });

    updatePagination();
}

function updatePagination() {
    const totalPages = Math.ceil(users.length / usersPerPage);
    document.getElementById("pageInfo").innerText = `Страница ${currentPage} из ${totalPages}`;

    document.getElementById("prevBtn").disabled = currentPage === 1;
    document.getElementById("nextBtn").disabled = currentPage === totalPages;
}

function nextPage() {
    if (currentPage < Math.ceil(users.length / usersPerPage)) {
        currentPage++;
        renderTable();
    }
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        renderTable();
    }
}

function goToProfile(url) {
    window.location.href = url;
}

function filterTable() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    users = users.filter(user => 
        user.name.toLowerCase().includes(input) ||
        user.id.toLowerCase().includes(input) ||
        user.phone.includes(input)
    );
    currentPage = 1;
    renderTable();
}

loadUsers();