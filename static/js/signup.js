window.onload = function(){
	const form = document.getElementById("form-signup")

	form.addEventListener("submit", (ev)=>{
		ev.preventDefault();
		data = {
			name: document.getElementById("name").value,
			lastname: document.getElementById("lastname").value,
			email: document.getElementById("email").value,
			password: document.getElementById("password").value,
			phonenumber: document.getElementById("phonenumber").value
		}	

		fetch("/signup",{
			method:"POST",
			body:JSON.stringify(data),
			headers:{
				"Content-Type":"application/json"
			}
		})
		.then(response => response.json())
			.then(data => {
				if(data.status == 200){
					document.getElementById("name").value=""
					document.getElementById("lastname").value=""
					document.getElementById("email").value=""
					document.getElementById("password").value=""
					document.getElementById("phonenumber").value=""
					window.location.href = "/index"
				}
				alert(data.message)
			})
	})
}