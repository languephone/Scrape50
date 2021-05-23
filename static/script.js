function hide_card(card) {
	card.style.display = 'none';
}

function card_select(target, brand) {
	// Have each brand checkbox remove the corresponding product cards
	document.querySelectorAll('.product-card').forEach(function(card) {
		if (card.dataset.brand == brand) {

			if (target.checked == false) {
				card.style.display = 'none';
			}
			else if (target.checked == true) {
				card.style.display = 'block';
			}
		}
	});
};

document.addEventListener('change', function(e) {
	const brand = e.target.name;
	card_select(e.target, brand);
});

document.addEventListener('DOMContentLoaded', function() {
	document.querySelector('input[name="Select-All"]').onclick = function() {
		const checkboxes = document.querySelectorAll('input[class="brand"]');
	    for (const checkbox of checkboxes) {
	        if (checkbox.checked != this.checked) {
	        	checkbox.click();
	        };
	        checkbox.checked = this.checked;
	    }
	};
});

// let input = document.querySelector('input');
// input.addEventListener('keyup', function() {
//     $.get('/search?q=' + input.value, function(brands) {
//         let html = '';
//         for (let item in brands)
//         {
//             let brand = brands[item].brand;
//             let scrapedate = brands[item].scrapedate;
//             let site = brands[item].site;
//             html += '<tr>'
//                 + '<td>' + brand + '</td>'
//                 + '<td>' + scrapedate + '</td>'
//                 + '<td>' + site + '</td>'
//                 + '</tr>'
//         }
//         document.querySelector('tbody').innerHTML = html;
//     });
// });