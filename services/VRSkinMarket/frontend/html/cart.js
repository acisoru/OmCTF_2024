async function getResponse(){
    let response = await fetch(`http://${window.location.host}/api/v1/cart`)
    if (response.status == 401) {
      location.replace("./login.html")
      return
    }
    if (response.status != 200) {
      alert((await response.json()).err)
      return
    }
    let content = await response.json()    
    let products = document.getElementById('cartitems')
    let key;
    let goods = content.goods
    for (key in goods){
        products.insertAdjacentHTML('beforeend', `
        <div class="card mb-3" id="cartitems">
        <div class="card-body">
        <div class="d-flex justify-content-between">
          <div class="d-flex flex-row align-items-center">
            <div>
              <img
                src="${goods[key].picture}"
                class="img-fluid rounded-3" alt="Shopping item" style="width: 65px;">
            </div>
            <div class="ms-3">
              <h5>${goods[key].name}</h5>
              <p class="small mb-0">${goods[key].description}</p>
            </div>
          </div>
          <div class="d-flex flex-row align-items-center">
            <div style="width: 80px;">
              <h5 class="mb-0">${goods[key].price} Ð</h5>
            </div>
            <button type="button" class="btn btn-secondary" id="deletebutton${goods[key].ID}">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16" id="trashicon${goods[key].ID}">
              <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
      </div>`)
      document.getElementById(`deletebutton${goods[key].ID}`).addEventListener("click", DeleteFromCart);
      document.getElementById(`deletebutton${goods[key].ID}`).merch_id = goods[key].ID
      document.getElementById(`trashicon${goods[key].ID}`).merch_id = goods[key].ID

    }
    let result = document.getElementById('result')
    result.insertAdjacentHTML('beforeend', `
    <div class="d-flex justify-content-between mb-4">
        <h5 class="text-uppercase">items: </h5>
        <h5>${content.total_quantity}</h5>
    </div> 
    <hr class="my-4">

    <div class="d-flex justify-content-between mb-5">
        <h5 class="text-uppercase">Total price: </h5>
        <h5>${content.price} Ð</h5>
    </div>`)
    document.getElementById("makeorderbutton").addEventListener("click", createOrder);
    document.getElementById("makeorderbutton").cart_id = content.ID

  }


async function createOrder(){
  let response = await fetch(`http://${window.location.host}/api/v1/order`, {
          method: "POST",
          body: JSON.stringify({
            status: "created",
            cart_id: document.getElementById("makeorderbutton").cart_id,
          }),
          headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
        });
    if (response.status != 201) {
      alert((await response.json()).err)
    } else {
        content = await response.json()
        location.replace(`./order_created.html?id=${content.ID}`)
    }
}

async function DeleteFromCart(event){
  let response = await fetch(`http://${window.location.host}/api/v1/cart?id=${event.target.merch_id}`, {
          method: "DELETE"
        });
  if (response.status != 200) {
    alert((await response.json()).err)
  } else {
      location.replace(`./cart.html`)
  }
}
getResponse()