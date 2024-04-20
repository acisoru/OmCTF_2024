async function SubmitReg() {
    let username = document.getElementById("floatingInput").value
    let password = document.getElementById("floatingPassword").value
    let confirmation = document.getElementById("floatingConfirmPassword").value
    if (confirmation != password) {
        document.getElementById("error").innerHTML = "Passwords do not match"
        return
    }
    
    let response = await fetch(`http://${window.location.host}/api/v1/register`, {
            method: "POST",
            body: JSON.stringify({
              username: username,
              password: password,
            }),
            headers: {
              "Content-type": "application/json; charset=UTF-8"
            }
          });

    if (response.status != 201) {
        document.getElementById("error").innerHTML = (await response.json()).err
        return
    }
    location.replace("./login.html")
}
document.getElementById("registerbutton").addEventListener("click", SubmitReg);