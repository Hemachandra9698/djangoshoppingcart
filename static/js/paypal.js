
var total = parseFloat(document.getElementById('total').textContent.split('$')[1]);

paypal.Buttons({
            style: {
             color:  'blue',
             shape:  'rect',
            },

            // Set up the transaction
            createOrder: function(data, actions) {
                return actions.order.create({
                    purchase_units: [{
                        amount: {
                            value: parseFloat(total).toFixed(2)
                        }
                    }]
                });
            },

            // Finalize the transaction
            onApprove: function(data, actions) {
                return actions.order.capture().then(function(details) {
                    // Show a success message to the buyer
                    submitFormData();
                    alert('Transaction completed by ' + details.payer.name.given_name + '!');
                });
            }

        }).render('#paypal-button-container');