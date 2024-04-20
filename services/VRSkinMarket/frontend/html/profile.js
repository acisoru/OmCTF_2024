async function getProfile(){
    let response = await fetch(`http://${window.location.host}/api/v1/profile`)
    if (response.status == 401) {
      location.replace("./login.html")
      return
    }
    if (response.status != 200) {
      alert((await response.json()).err)
      return
    }
    let content = await response.json()
    // content = content.splice(0,10)
    
    let list = document.getElementById('user')


    list.innerHTML +=`
    <div class="col-lg-4">
    <div class="card mb-4">
      <div class="card-body text-center">
        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3.webp" alt="avatar"
          class="rounded-circle img-fluid" style="width: 150px;">
        <h5 class="my-3">${content.username}</h5>
        <p class="text-muted mb-1">${content.status}</p>
        <div class="d-flex justify-content-center mb-2">
          <button type="button" class="btn btn-primary" id="logoutbutton">Logout</button>
        </div>
      </div>
    </div>
  </div>
  <div class="col-lg-8">
    <div class="card mb-4">
      <div class="card-body">
        <div class="row">
        </div>
        <div class="row">
          <div class="col-sm-3">
            <p class="mb-0">DogeCoin available</p>
          </div>
          <div class="col-sm-9">
            <p class="text-muted mb-0">${content.cash} Ð</p>
          </div>
        </div>
        <hr>
        <div class="row">
          <div class="col-sm-3">
            <p class="mb-0">Wallet key</p>
          </div>
          <div class="col-sm-9">
            <p class="text-muted mb-0">${content.flag}</p>
          </div>
        </div>
      </div>
    </div>             
  </div>`

  document.getElementById("logoutbutton").addEventListener("click", Logout);

  let orders = document.getElementById('orders')
  let order;
  
  for (order in content.orders){
  orders.innerHTML +=`<li class="list-group-item d-flex justify-content-between align-items-start">
  <div class="ms-2 me-auto">
  <div class="fw-bold"><a href="order.html?id=${content.orders[order].ID}" class="link">${content.orders[order].ID}</a></div>
  ${content.orders[order].status}
  </div>
  <span class="badge text-bg-primary rounded-pill">${content.orders[order].status}</span></li>`
  }

  let skins = document.getElementById('skins')
  let skin;
  for (skin in content.merchandise){
    skins.innerHTML +=`<li class="list-group-item d-flex justify-content-between align-items-start">
    <div class="ms-2 me-auto">
    <div class="fw-bold"><a href="my_merch.html?id=${content.merchandise[skin].ID}" class="link">${content.merchandise[skin].name}</a></div>
    ${content.merchandise[skin].description}
  </div>
  <span class="badge text-bg-primary rounded-pill">${content.merchandise[skin].status}</span></li>`
  }
}

async function Logout() {
  let response = await fetch(`http://${window.location.host}/api/v1/logout`)
  if (response.status != 200) {
    alert(response.json())
    return
  }
  location.replace("./login.html")

}
getProfile()





