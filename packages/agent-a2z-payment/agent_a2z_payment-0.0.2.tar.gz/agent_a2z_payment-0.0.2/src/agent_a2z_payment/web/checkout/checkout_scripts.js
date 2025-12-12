<script src="https://js.stripe.com/v3/" async></script>
<script>
            // Simple logic to switch tabs
            function selectMethod(method) {{
                // Reset styles
                document.querySelectorAll('.pm-option').forEach(el => {{
                    el.style.border = '1px solid #ddd';
                    el.style.background = 'white';
                }});
                document.querySelectorAll('.pm-action').forEach(el => el.style.display = 'none');

                // Activate selected
                const selectedOpt = document.getElementById('opt-' + method);
                if (selectedOpt) {{
                    selectedOpt.style.border = '2px solid #007bff';
                    selectedOpt.style.background = '#f0f7ff';
                }}

                const actionDiv = document.getElementById('action-' + method);
                if (actionDiv) actionDiv.style.display = 'block';
            }}

            // Initialize Stripe (Mock logic for demo)
            (function() {{
                if (typeof Stripe !== 'undefined') {{
                    const stripe = Stripe("{publishable_key}");
                    const elements = stripe.elements();
                    const card = elements.create("card");
                    card.mount("#card-element");

                    document.querySelector("#pay-btn").onclick = async () => {{
                        const res = await stripe.confirmCardPayment(
                            "{client_secret}",
                            {{
                                payment_method: {{ card: card }}
                            }}
                        );

                        if (res.error) {{
                            alert(res.error.message);
                        }} else {{
                            alert("Payment processing... you will continue after confirmation.");
                        }}
                    }}
                }}
            }})();
</script>
