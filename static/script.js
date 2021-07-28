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
	// If the 'Select All' box has been checked:
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

	// Otherwise a brand box has been checked:
	else {
		const brand = e.target.name;
		card_select(e.target, brand);
	}

});