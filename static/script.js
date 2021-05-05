function hide_card(card)
{
    card.style.display = 'none';
}

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