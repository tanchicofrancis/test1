// Initialize the cart from localStorage or set to an empty array
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Add event listeners to all "Add to Cart" buttons
document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', (event) => {
        const id = event.target.getAttribute('data-id');
        const name = event.target.getAttribute('data-name');
        const price = event.target.getAttribute('data-price');

        // Check if the product is already in the cart
        const existingItem = cart.find(item => item.id === id);
        if (existingItem) {
            existingItem.quantity += 1; // Increase quantity
        } else {
            // Add new product to the cart
            cart.push({ id, name, price, quantity: 1 });
        }

        // Save the updated cart back to localStorage
        localStorage.setItem('cart', JSON.stringify(cart));

        // Provide feedback to the user
        alert(`${name} has been added to your cart!`);
    });
});

// Function to retrieve and display the cart contents
function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}