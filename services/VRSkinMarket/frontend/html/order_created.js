const searchString = new URLSearchParams(window.location.search);

const order_id = searchString.get('id');

document.getElementById("order_button").addEventListener("click", find_order);

async function find_order() {
    location.replace(`./order.html?id=${order_id}`)
}