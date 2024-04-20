const searchString = new URLSearchParams(window.location.search);
const order_id = searchString.get('id');

async function getResponse(){
    let response = await fetch(`http://${window.location.host}/api/v1/order?id=${order_id}`)
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
    let goods = content.cart.goods
    for (key in goods){
        products.innerHTML +=`
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
          </div>
        </div>
      </div>
      </div>`
    }
    let result = document.getElementById('result')
    result.innerHTML +=`
    <div class="d-flex justify-content-between mb-4">
        <h5 class="text-uppercase">items: </h5>
        <h5>${content.cart.total_quantity}</h5>
    </div> 
    <hr class="my-4">

    <div class="d-flex justify-content-between mb-5">
        <h5 class="text-uppercase">Total price:</h5>
        <h5>${content.cart.price} Ð</h5>
    </div>
    <hr class="my-4">
    <div class="d-flex justify-content-between mb-4">
    <h5 class="text-uppercase">status: ${content.status}</h5>
    </div>`
    btn =  document.getElementById("buybutton")
    if (content.status == "paid") {
      btn.disabled = true;
    } else {
      btn.addEventListener("click", BuyOrder);
      btn.order_id = content.ID
      btn.price = content.cart.price
    }
}


async function BuyOrder(){
  btn = document.getElementById("buybutton")
  let response = await fetch(`http://${window.location.host}/api/v1/buy`, {
          method: "POST",
          body: JSON.stringify({
            ID: btn.order_id,
            cart:{ price: btn.price}
          }),
          headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
        });
    if (response.status != 200) {
      alert((await response.json()).err)
    } else {
        location.replace("./order_paid.html")
    }
}
getResponse()