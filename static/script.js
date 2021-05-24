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
				card.style.display = 'flex';
			}
		}
	});
};

// check for any checkbox tick or un-tick, and hide/unhide the corresponding
// product card
document.addEventListener('change', function(e) {
	if (e.target.name == 'Select-All') {
		// check/uncheck all other boxes to match the state of 'Select-All'
		const checkboxes = document.querySelectorAll('input[class="brand"]');
	    for (const checkbox of checkboxes) {
	        if (checkbox.checked != e.target.checked) {
	        	checkbox.click();
	        }
	        checkbox.checked = e.target.checked;
	    }
	}
	
	else {
		const brand = e.target.name;
		card_select(e.target, brand);
	}

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