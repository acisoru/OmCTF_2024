const searchString = new URLSearchParams(window.location.search);

const merch_id = searchString.get('id');

async function getResponse(){
  let response = await fetch(`http://${window.location.host}/api/v1/my_merchandise?id=${merch_id}`)
  if (response.status == 401) {
    location.replace("./login.html")
    return
  }
  if (response.status != 200) {
    alert((await response.json()).err)
    return
  }
  let content = await response.json()
  let list = document.getElementById('merchandise')
  list.innerHTML +=`
  <img src="${content.picture}"
    class="card-img-top" />
  <div class="card-body">
    <div class="text-center">
      <h5 class="card-title">${content.name}</h5>
      <p class="text-muted mb-4">${content.description}</p>
    </div>
    <div>
      <div class="d-flex justify-content-between">
        <span>Seller</span><span>${content.seller}</span>
      </div>
      <div class="d-flex justify-content-between">
        <span>NFTToken</span><span>${content.NFTToken}</span>
      </div>
      <div class="d-flex justify-content-between">
        <span>Status</span><span>${content.status}</span>
      </div>
    </div>
    <div class="d-flex justify-content-between total font-weight-bold mt-4">
      <span>Price</span><span>${content.price} Ð</span>
    </div>
  </div>`
  document.getElementById("buybutton").addEventListener("click", AddToCart);
}

async function AddToCart(event) {
  let response = await fetch(`http://${window.location.host}/api/v1/cart?id=${merch_id}`, {
    method: "PUT",
  });
  if (response.status != 200) {
    alert((await response.json()).err)
    return
  }
event.target.innerHTML="In cart"
}
getResponse()