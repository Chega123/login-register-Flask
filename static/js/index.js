window.onload = function(){
    const form = document.getElementById("form-login")

    form.addEventListener("submit", (ev)=>{
        ev.preventDefault()
        data = {
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        }
        fetch("/index",{
            method:"POST",
            body:JSON.stringify(data),
            headers:{
                'Content-Type':'application/json'
            }
        })
            .then(response => response.json())
            .then(data=>{
                if(data.status == 200){
                    console.log(data)
                    window.location.href = "/dashboard"
                }
                else{
                    alert(data.message)
                }
            })
    })
}