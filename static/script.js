function hide_card(card)
{
    card.style.display = 'none';
}


// document.addEventListener("DOMContentLoaded", function() {
	
// 	// Have each checkbox remove the corresponding cards
// 	document.querySelectorAll("input[type='checkbox']").forEach(function(box) {
// 		console.log(box.name, box.checked);
// 	});
// });

document.addEventListener('change', function(e) {
	const brand = e.target.name;
	card_select(brand);
});

function card_select(brand) {
	document.querySelectorAll('.product-card').forEach(function(card) {
		if (card.dataset.brand == brand) {

			if (card.style.display !== 'none') {
				card.style.display = 'none';
			}
			else if (card.style.display == 'none') {
				card.style.display = 'block';
			}
		}
	});
};


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