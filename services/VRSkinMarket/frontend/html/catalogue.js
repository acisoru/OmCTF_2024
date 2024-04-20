const searchString = new URLSearchParams(window.location.search);
pageId = Number(searchString.get('PageId'));

if (pageId == null){
  pageId = 1;
}

async function getResponse(){
  let response = await fetch(`http://${window.location.host}/api/v1/catalogue`, {
    method: "POST",
    body: JSON.stringify({
      limit: 12,
      page: pageId,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  });
  if (response.status == 401) {
      location.replace("./login.html")
      return
  }
  let content = await response.json()
  let list = document.getElementById('posts')
  let key;
  let skins = content.rows 
  for (key in skins){
    if (!skins[key].picture) {
      skins[key].picture = "https://avatars.mds.yandex.net/get-shedevrum/12369909/913c5d69bd5211eebd93fe19746b188b/orig"
    }
    list.insertAdjacentHTML('beforeend', ` <div class="col">
    <div class="card shadow-sm">
      <img src = "${skins[key].picture}">
      <div class="card-body">
      <p class="card-text"><b>${skins[key].name}</b></p>
      <small class="card-text">${skins[key].seller}</small>
        <p class="card-text">${skins[key].description}</p>
        <div class="d-flex justify-content-between align-items-center">
          <div class="btn-group">
          <a href="product.html?id=${skins[key].ID}"
            <button type="button" class="btn btn-sm btn-outline-secondary">View</button>
            </a>
            <button type="button" class="btn btn-sm btn-outline-secondary" id="buy${skins[key].ID}button">Buy</button>
          </div>
          <small class="text-body-secondary">${skins[key].price} Ð</small>
        </div>
      </div>
    </div>
  </div>`)
  let btn = document.getElementById(`buy${skins[key].ID}button`)
  btn.store_id = skins[key].ID
  btn.addEventListener("click", AddToCart);
  document.getElementById("Next").total_pages = content.total_pages
  }
}
async function AddToCart(event) {
  let response = await fetch(`http://${window.location.host}/api/v1/cart?id=${event.target.store_id}`, {
    method: "PUT",
  });
  if (response.status != 200) {
    alert((await response.json()).err)
    return
  }

event.target.innerHTML="In cart"
}

getResponse()


//pagination

document.getElementById("Previous").addEventListener("click", find_page_Previous);
document.getElementById("Next").addEventListener("click", find_page_Next);

async function find_page_Previous() {
    if (pageId > 1){
      pageId = pageId - 1;
      location.replace(`catalogue.html?PageId=${pageId}`)
    }
}

async function find_page_Next() {
  if (pageId < document.getElementById("Next").total_pages){
    pageId = pageId + 1;
    location.replace(`catalogue.html?PageId=${pageId}`)
  }
}