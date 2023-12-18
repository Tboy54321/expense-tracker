const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item=> {
	const li = item.parentElement;

	item.addEventListener('click', function () {
		allSideMenu.forEach(i=> {
			i.parentElement.classList.remove('active');
		})
		li.classList.add('active');
	})
});

const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
})

const switchMode = document.getElementById('switch-mode');

switchMode.addEventListener('change', function () {
	if(this.checked) {
		document.body.classList.add('dark');
	} else {
		document.body.classList.remove('dark');
	}
})

let popup = document.getElementById("popup-container");
    let body = document.body;
    function openpopup() {
        popup.classList.add("open-popup");
        body.classList.add("open-popup");
    }
    function closepopup() {
        popup.classList.remove("open-popup");
        body.classList.remove("open-popup");
    }

function addExpense() {
    const form = $('#expenseForm');
    const formData = form.serialize();

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: formData,
        success: function (data) {
            // Update the table dynamically with the new expense
            const newRow = `
                <tr>
                    <td>${data.date}</td>
                    <td>${data.category}</td>
                    <td>$${data.amount}</td>
                    <td>${data.status}</td>
                </tr>
            `;

            $('table tbody').append(newRow);

            // Clear the form fields
            form[0].reset();
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}
