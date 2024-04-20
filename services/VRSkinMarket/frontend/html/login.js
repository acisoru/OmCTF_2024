async function SubmitLogin() {
  let username = document.getElementById("floatingInput").value
  let password = document.getElementById("floatingPassword").value
  fetch(`http://${window.location.host}/api/v1/login`, {
          method: "POST",
          body: JSON.stringify({
            username: username,
            password: password,
          }),
          headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
        }).then((response) => {
          if (response.status != 200) {
            document.getElementById("error").innerHTML = "Wrong username or password"
          } else {
              location.replace("./catalogue.html")
          }
        });
  }
  document.getElementById("signinbutton").addEventListener("click", SubmitLogin);