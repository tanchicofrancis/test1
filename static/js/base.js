document.addEventListener("DOMContentLoaded", function () {

    // Function to update the total price display
    function updateTotalPrice(newTotalPrice) {
        const totalPriceElement = document.querySelector("#total-price");
        if (totalPriceElement) {
            // Format the total price as currency (example for PHP Peso, can be changed as needed)
            totalPriceElement.textContent = "₱" + parseFloat(newTotalPrice).toFixed(2);
        }
    }

    // Adding event listeners to all "Add to Cart" buttons
    const addToCartButtons = document.querySelectorAll(".add-to-cart");
    addToCartButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const productId = button.getAttribute("data-id");
            const productName = button.getAttribute("data-name");

            if (!productId) {
                console.error("Product ID is missing.");
                return;
            }

            fetch(`/add_to_cart/${productId}/`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.success) {
                        alert(`${productName} has been added to your cart!`);
                        if (data.total_price) {
                            updateTotalPrice(data.total_price); 
                        }
                    } else {
                        alert(data.message || "There was an issue adding the product to the cart.");
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("An error occurred while adding the product to the cart.");
                });
        });
    });

    // Adding event listeners to all "Remove from Cart" buttons
    const removeFromCartButtons = document.querySelectorAll(".remove-from-cart");
    removeFromCartButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const productId = button.getAttribute("data-id");
            const productName = button.getAttribute("data-name");

            if (!productId) {
                console.error("Product ID is missing.");
                return;
            }

            fetch(`/remove_from_cart/${productId}/`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.success) {
                        alert(`${productName} has been removed from your cart!`);

                        const cartItem = document.querySelector(`#cart-item-${productId}`);
                        if (cartItem) {
                            cartItem.remove();
                        }

                        if (data.new_total_price) {
                            updateTotalPrice(data.new_total_price);
                        }
                    } else {
                        alert(data.message || "There was an issue removing the product from the cart.");
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("An error occurred while removing the product from the cart.");
                });
        });
    });
});
