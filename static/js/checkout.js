    if (user != 'AnonymousUser'){
		 	document.getElementById('user-info').innerHTML = ''
    }

    var total = parseFloat(document.getElementById('total').textContent.split('$')[1]);



    var form = document.getElementById('form')
    form.addEventListener('submit', function(e){
	    	e.preventDefault();
	    	document.getElementById('form-button').classList.add("hidden");
	    	document.getElementById('payment-info').classList.remove("hidden");
    })

	/*
    document.getElementById('make-payment').addEventListener('click', function(e){
    	if (total != '' || total != undefined || total!= 0){
			submitFormData();
		}
    })*/

    function submitFormData(){
  	    //console.log('Payment button clicked');

  	    var userFormData = {
				'name':null,
				'email':null,
				'total':total,
			}

		var shippingInfo = {
				'address':null,
				'city':null,
				'state':null,
				'zipcode':null,
			}

		shippingInfo.address = form.address.value;
  	    shippingInfo.city = form.city.value;
  	    shippingInfo.state = form.state.value;
  	    shippingInfo.zipcode = form.zipcode.value;


	    	if (user == 'AnonymousUser'){
	    		userFormData.name = form.name.value;
	    		userFormData.email = form.email.value;
	    	}

	    	//console.log('Shipping Info:', shippingInfo);
	    	//console.log('User Info:', userFormData);

	    	var url = "/process-order/"
	    	fetch(url, {
	    		method:'POST',
	    		headers:{
	    			'Content-Type':'application/json',
	    			'X-CSRFToken':csrftoken,
	    		},
	    		body:JSON.stringify({'form':userFormData, 'shipping':shippingInfo}),
	    	})
	    	.then((response) => response.json())
	    	.then((data) => {
				  console.log('Success:', data);
				  alert('Transaction completed');
				  // clear cart cookie if transaction is success
				  cart = {}
				  document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
				  window.location.href = "/";
				})
    }