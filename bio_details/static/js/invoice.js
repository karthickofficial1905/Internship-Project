// Manual test function - call this in console to test updates
function testUpdateTotals() {
    console.log('Testing manual update...');
    updateTotals({
        subtotal: '1000.00',
        total_tax: '180.00',
        total_discount: '50.00',
        total_amount: '1130.00'
    });
}

// Test function to verify elements exist
function testTotalElements() {
    console.log('=== Testing Total Elements ===');
    console.log('total-tax:', document.getElementById('total-tax'));
    console.log('total-discount:', document.getElementById('total-discount'));
    console.log('total-amount:', document.getElementById('total-amount'));
    console.log('summary-subtotal:', document.getElementById('summary-subtotal'));
    console.log('summary-tax:', document.getElementById('summary-tax'));
    console.log('summary-discount:', document.getElementById('summary-discount'));
    console.log('summary-total:', document.getElementById('summary-total'));
    console.log('=== End Test ===');
}

// Call test function when page loads
document.addEventListener('DOMContentLoaded', function() {
    testTotalElements();
    
    const productSelect = document.getElementById('product-select');
    const quantityInput = document.getElementById('quantity');
    const priceDisplay = document.getElementById('price-display');
    const taxInput = document.getElementById('tax-input');
    const discountInput = document.getElementById('discount-input');
    const productTotalDisplay = document.getElementById('product-total-display');
    const productForm = document.getElementById('product-form');
    const submitBtn = document.getElementById('submit-btn');

    // Calculate product total when inputs change
    function calculateProductTotal() {
        const selectedOption = productSelect.options[productSelect.selectedIndex];
        const currencySymbol = selectedOption.dataset.currency || '?';
        
        if (!selectedOption.value) {
            priceDisplay.value = currencySymbol + '0';
            productTotalDisplay.value = currencySymbol + '0';
            return;
        }

        const price = parseFloat(selectedOption.dataset.price) || 0;
        const quantity = parseInt(quantityInput.value) || 1;
        const taxRate = parseFloat(selectedOption.dataset.tax) || 18;
        const discountRate = parseFloat(selectedOption.dataset.discount) || 0;
        const stock = parseInt(selectedOption.dataset.stock) || 0;

        // Update tax and discount inputs with product values
        taxInput.value = taxRate + '%';
        discountInput.value = discountRate + '%';

        // Validate quantity against stock
        if (quantity > stock) {
            quantityInput.value = stock;
            showToast('Quantity adjusted to available stock: ' + stock, 'warning');
            return;
        }

        priceDisplay.value = currencySymbol + price.toFixed(2);

        const subtotal = price * quantity;
        const taxAmount = (subtotal * taxRate) / 100;
        const discountAmount = (subtotal * discountRate) / 100;
        const total = subtotal + taxAmount - discountAmount;

        productTotalDisplay.value = currencySymbol + total.toFixed(2);
    }

    // Update form when product is selected
    productSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        if (selectedOption.value) {
            const stock = parseInt(selectedOption.dataset.stock) || 0;
            
            // Set max quantity to available stock
            quantityInput.max = stock;
            
            // Show stock info
            showStockInfo(stock);
        } else {
            quantityInput.removeAttribute('max');
            hideStockInfo();
        }
        calculateProductTotal();
    });

    // Add stock validation to quantity input
    quantityInput.addEventListener('input', function() {
        const selectedOption = productSelect.options[productSelect.selectedIndex];
        if (selectedOption.value) {
            const stock = parseInt(selectedOption.dataset.stock) || 0;
            const quantity = parseInt(this.value) || 1;
            
            if (quantity > stock) {
                this.value = stock;
                showToast(`Maximum available quantity is ${stock}`, 'warning');
            }
        }
        calculateProductTotal();
    });

    // Recalculate when quantity, tax, or discount changes
    taxInput.addEventListener('input', calculateProductTotal);
    discountInput.addEventListener('input', calculateProductTotal);

    // Show/hide stock information
    function showStockInfo(stock) {
        let stockInfo = document.querySelector('.stock-info');
        if (!stockInfo) {
            stockInfo = document.createElement('div');
            stockInfo.className = 'stock-info';
            productSelect.parentNode.appendChild(stockInfo);
        }
        
        if (stock === 0) {
            stockInfo.textContent = 'Out of Stock';
            stockInfo.className = 'stock-info out-of-stock';
        } else if (stock <= 5) {
            stockInfo.textContent = `Low Stock: ${stock} remaining`;
            stockInfo.className = 'stock-info low-stock';
        } else {
            stockInfo.textContent = `In Stock: ${stock} available`;
            stockInfo.className = 'stock-info in-stock';
        }
    }
    
    function hideStockInfo() {
        const stockInfo = document.querySelector('.stock-info');
        if (stockInfo) {
            stockInfo.remove();
        }
    }

    // Handle form submission
    productForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const selectedOption = productSelect.options[productSelect.selectedIndex];
        if (!selectedOption.value) {
            showToast('Please select a product', 'warning');
            return;
        }
        
        const stock = parseInt(selectedOption.dataset.stock) || 0;
        const quantity = parseInt(quantityInput.value) || 1;
        
        if (stock === 0) {
            showToast('Selected product is out of stock', 'error');
            return;
        }
        
        if (quantity > stock) {
            showToast(`Only ${stock} units available`, 'error');
            return;
        }
        
        const formData = new FormData(this);
        
        // Remove % symbol from tax and discount before sending
        const taxValue = taxInput.value.replace('%', '');
        const discountValue = discountInput.value.replace('%', '');
        formData.set('tax_rate', taxValue);
        formData.set('discount_rate', discountValue);
        
        const submitButton = this.querySelector('button[type="submit"]');
        
        // Disable submit button
        submitButton.disabled = true;
        submitButton.textContent = 'Adding...';
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Add new row to table
                addRowToTable(data.item);
                
                // Update totals
                updateTotals(data);
                
                // Reset form properly
                productSelect.selectedIndex = 0;
                quantityInput.value = 1;
                const currencySymbol = data.currency_symbol || '?';
                priceDisplay.value = currencySymbol + '0';
                productTotalDisplay.value = currencySymbol + '0';
                taxInput.value = '18%';
                discountInput.value = '5%';
                
                // Hide stock info
                hideStockInfo();
                
                // Remove added product from dropdown
                const selectedOption = productSelect.options[productSelect.selectedIndex];
                selectedOption.remove();
                
                showToast('Product added successfully!', 'success');
            } else {
                showToast(data.error || 'Failed to add product', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred while adding the product', 'error');
        })
        .finally(() => {
            // Re-enable submit button
            submitButton.disabled = false;
            submitButton.textContent = '+ Add Product';
        });
    });

    // Add new row to table
    function addRowToTable(item) {
        const tableBody = document.getElementById('amount-table-body');
        const totalRow = tableBody.querySelector('.total-row');
        const rowCount = tableBody.querySelectorAll('tr:not(.total-row)').length + 1;
        const currencySymbol = item.currency_symbol || '?';
        
        const newRow = document.createElement('tr');
        newRow.setAttribute('data-item-id', item.id);
        newRow.setAttribute('id', `row-${item.id}`);
        newRow.innerHTML = `
            <td class="text-center">${rowCount}</td>
            <td class="text-left">${item.product_name}</td>
            <td class="text-right">${currencySymbol}${parseFloat(item.unit_price).toFixed(2)}</td>
            <td class="text-center qty-cell" data-original-qty="${item.qty}" data-product-name="${item.product_name}">
                <span class="qty-display">${item.qty}</span>
                <input type="number" class="qty-input" value="${item.qty}" min="1" style="display:none; width:60px; text-align:center;">
                <small class="stock-info" style="display:none; color:#666; font-size:11px;"></small>
            </td>
            <td class="text-right">${currencySymbol}${parseFloat(item.tax).toFixed(2)}</td>
            <td class="text-right">${currencySymbol}${parseFloat(item.discount).toFixed(2)}</td>
            <td class="text-right item-total">${currencySymbol}${parseFloat(item.total).toFixed(2)}</td>
            <td class="text-center action-cell">
                <div class="action-buttons">
                    <button onclick="editItem(${item.id})" class="edit-btn" type="button" title="Edit Quantity" style="padding: 8px; margin: 2px;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="m18.5 2.5 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                    </button>
                    <button onclick="saveItem(${item.id})" class="save-btn" type="button" style="display:none; padding: 8px; margin: 2px;" title="Save Changes">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="20,6 9,17 4,12"></polyline>
                        </svg>
                    </button>
                    <button onclick="cancelEdit(${item.id})" class="cancel-btn" type="button" style="display:none; padding: 8px; margin: 2px;" title="Cancel Edit">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                    <button onclick="removeItem(${item.id})" class="remove-btn" type="button" title="Remove Item" style="padding: 8px; margin: 2px;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3,6 5,6 21,6"></polyline>
                            <path d="m19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"></path>
                            <line x1="10" y1="11" x2="10" y2="17"></line>
                            <line x1="14" y1="11" x2="14" y2="17"></line>
                        </svg>
                    </button>
                </div>
            </td>
        `;
        
        tableBody.insertBefore(newRow, totalRow);
        
        // Remove the "No items added yet" row if it exists
        const noItemsRow = document.getElementById('no-items-row');
        if (noItemsRow) {
            noItemsRow.remove();
        }
    }

    // Submit order
    if (submitBtn) {
        submitBtn.addEventListener('click', function() {
            const tableBody = document.getElementById('amount-table-body');
            const itemRows = tableBody.querySelectorAll('tr:not(.total-row)');
            
            if (itemRows.length === 0) {
                showToast('Please add at least one product to place the order', 'warning');
                return;
            }
            
            showOrderModal();
        });
    }

});

// Update totals in the table and summary - moved outside DOMContentLoaded
function updateTotals(data) {
    console.log('=== updateTotals called ===');
    console.log('Data received:', data);
    
    // Use currency symbol from server response, fallback to data.currency_symbol, then to ₹
    const currencySymbol = data.currency_symbol || '₹';
    console.log('Using currency symbol:', currencySymbol);
    
    // Update subtotal in table
    const subtotalAmountCell = document.getElementById('subtotal-amount');
    console.log('Subtotal amount cell found:', subtotalAmountCell);
    if (subtotalAmountCell) {
        const newSubtotalValue = currencySymbol + parseFloat(data.subtotal || 0).toFixed(2);
        console.log('Setting subtotal amount to:', newSubtotalValue);
        subtotalAmountCell.textContent = newSubtotalValue;
        // Add visual feedback
        subtotalAmountCell.style.backgroundColor = '#fff3cd';
        subtotalAmountCell.style.transition = 'background-color 0.5s';
        setTimeout(() => {
            subtotalAmountCell.style.backgroundColor = '';
        }, 1000);
    }
    
    // Update table totals using specific IDs
    const totalTaxCell = document.getElementById('total-tax');
    console.log('Total tax cell found:', totalTaxCell);
    if (totalTaxCell) {
        const newTaxValue = currencySymbol + parseFloat(data.total_tax || 0).toFixed(2);
        console.log('Setting total tax to:', newTaxValue);
        totalTaxCell.textContent = newTaxValue;
        // Add visual feedback
        totalTaxCell.style.backgroundColor = '#d4edda';
        totalTaxCell.style.transition = 'background-color 0.5s';
        setTimeout(() => {
            totalTaxCell.style.backgroundColor = '';
        }, 1000);
    }
    
    const totalDiscountCell = document.getElementById('total-discount');
    console.log('Total discount cell found:', totalDiscountCell);
    if (totalDiscountCell) {
        const newDiscountValue = currencySymbol + parseFloat(data.total_discount || 0).toFixed(2);
        console.log('Setting total discount to:', newDiscountValue);
        totalDiscountCell.textContent = newDiscountValue;
        // Add visual feedback
        totalDiscountCell.style.backgroundColor = '#f8d7da';
        totalDiscountCell.style.transition = 'background-color 0.5s';
        setTimeout(() => {
            totalDiscountCell.style.backgroundColor = '';
        }, 1000);
    }
    
    const totalAmountCell = document.getElementById('total-amount');
    console.log('Total amount cell found:', totalAmountCell);
    if (totalAmountCell) {
        const newAmountValue = currencySymbol + parseFloat(data.total_amount || 0).toFixed(2);
        console.log('Setting total amount to:', newAmountValue);
        totalAmountCell.textContent = newAmountValue;
        // Add visual feedback
        totalAmountCell.style.backgroundColor = '#cce7ff';
        totalAmountCell.style.transition = 'background-color 0.5s';
        setTimeout(() => {
            totalAmountCell.style.backgroundColor = '';
        }, 1000);
    }

    // Update summary section using specific IDs
    const summarySubtotal = document.getElementById('summary-subtotal');
    console.log('Summary subtotal cell found:', summarySubtotal);
    if (summarySubtotal) {
        const newSubtotalValue = currencySymbol + parseFloat(data.subtotal || 0).toFixed(2);
        console.log('Setting summary subtotal to:', newSubtotalValue);
        summarySubtotal.textContent = newSubtotalValue;
        // Add visual feedback
        summarySubtotal.style.backgroundColor = '#fff3cd';
        summarySubtotal.style.transition = 'background-color 0.5s';
        setTimeout(() => {
            summarySubtotal.style.backgroundColor = '';
        }, 1000);
    }
    
    const summaryTax = document.getElementById('summary-tax');
    console.log('Summary tax cell found:', summaryTax);
    if (summaryTax) {
        const newSummaryTaxValue = currencySymbol + parseFloat(data.total_tax || 0).toFixed(2);
        console.log('Setting summary tax to:', newSummaryTaxValue);
        summaryTax.textContent = newSummaryTaxValue;
        // Add visual feedback
        summaryTax.style.backgroundColor = '#d4edda';
        summaryTax.style.transition = 'background-color 0.5s';
        setTimeout(() => {
            summaryTax.style.backgroundColor = '';
        }, 1000);
    }
    
    const summaryDiscount = document.getElementById('summary-discount');
    console.log('Summary discount cell found:', summaryDiscount);
    if (summaryDiscount) {
        const newSummaryDiscountValue = currencySymbol + parseFloat(data.total_discount || 0).toFixed(2);
        console.log('Setting summary discount to:', newSummaryDiscountValue);
        summaryDiscount.textContent = newSummaryDiscountValue;
        // Add visual feedback
        summaryDiscount.style.backgroundColor = '#f8d7da';
        summaryDiscount.style.transition = 'background-color 0.5s';
        setTimeout(() => {
            summaryDiscount.style.backgroundColor = '';
        }, 1000);
    }
    
    const summaryTotal = document.getElementById('summary-total');
    console.log('Summary total cell found:', summaryTotal);
    if (summaryTotal) {
        const newSummaryTotalValue = '<strong>' + currencySymbol + parseFloat(data.total_amount || 0).toFixed(2) + '</strong>';
        console.log('Setting summary total to:', newSummaryTotalValue);
        summaryTotal.innerHTML = newSummaryTotalValue;
        // Add visual feedback
        summaryTotal.style.backgroundColor = '#cce7ff';
        summaryTotal.style.transition = 'background-color 0.5s';
        setTimeout(() => {
            summaryTotal.style.backgroundColor = '';
        }, 1000);
    }
    
    console.log('=== updateTotals completed ===');
}

// Manual test function - call this in console to test updates
function testUpdateTotals() {
    console.log('Testing manual update...');
    updateTotals({
        subtotal: '1000.00',
        total_tax: '180.00',
        total_discount: '50.00',
        total_amount: '1130.00'
    });
}

// Submit order function
function submitOrder() {
    const tableBody = document.getElementById('amount-table-body');
    const itemRows = tableBody.querySelectorAll('tr:not(.total-row)');
    
    if (itemRows.length === 0) {
        showToast('Please add at least one product to place the order', 'warning');
        return;
    }
    
    const orderId = document.querySelector('[name="order_id"]').value;
    
    const formData = new FormData();
    formData.append('order_id', orderId);
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
    
    fetch('/place-order/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showOrderModal();
        } else {
            showToast(data.message || 'Failed to place order', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred while placing the order', 'error');
    });
}

// Remove item function
function removeItem(itemId) {
    // Get the item name from the table row
    const row = document.querySelector(`button[onclick="removeItem(${itemId})"]`)?.closest('tr');
    const itemName = row ? row.cells[1].textContent.trim() : 'Item';
    
    showRemoveModal(itemId, itemName);
}

let itemToRemove = null;
let itemNameToRemove = null;

function showRemoveModal(itemId, itemName) {
    itemToRemove = itemId;
    itemNameToRemove = itemName;
    
    // Update modal text to show item name
    const modalText = document.querySelector('#removeModal p');
    if (modalText) {
        modalText.textContent = `Are you sure you want to remove "${itemName}" from the invoice?`;
    }
    
    document.getElementById('removeModal').style.display = 'block';
}

function closeRemoveModal() {
    document.getElementById('removeModal').style.display = 'none';
    itemToRemove = null;
    itemNameToRemove = null;
}

function confirmRemove() {
    if (!itemToRemove) {
        console.log('No item to remove');
        return;
    }
    
    console.log('Removing item:', itemToRemove, 'Name:', itemNameToRemove);
    
    // Show loading state
    const removeModal = document.getElementById('removeModal');
    const confirmButton = removeModal.querySelector('button[onclick="confirmRemove()"]');
    const originalText = confirmButton.textContent;
    confirmButton.textContent = 'Removing...';
    confirmButton.disabled = true;
    
    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log('CSRF Token:', csrfToken);
    
    fetch(`/remove-invoice-item/${itemToRemove}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: ''
    })
    .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Remove response:', data);
        
        if (data.success) {
            if (data.redirect) {
                showToast(`${itemNameToRemove} removed successfully! ${data.message}`, 'success');
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 1000);
                return;
            }
            
            // Remove row from table
            const row = document.querySelector(`button[onclick="removeItem(${itemToRemove})"]`)?.closest('tr');
            if (row) {
                row.remove();
                updateRowNumbers();
                
                // Update totals immediately with server data
                console.log('Updating totals with server data:', data);
                
                // Update table totals
                const currencySymbol = data.currency_symbol || '?';
                const subtotalAmountCell = document.getElementById('subtotal-amount');
                const totalTaxCell = document.getElementById('total-tax');
                const totalDiscountCell = document.getElementById('total-discount');
                const totalAmountCell = document.getElementById('total-amount');
                
                if (subtotalAmountCell) subtotalAmountCell.textContent = currencySymbol + parseFloat(data.subtotal || 0).toFixed(2);
                if (totalTaxCell) totalTaxCell.textContent = currencySymbol + parseFloat(data.total_tax || 0).toFixed(2);
                if (totalDiscountCell) totalDiscountCell.textContent = currencySymbol + parseFloat(data.total_discount || 0).toFixed(2);
                if (totalAmountCell) totalAmountCell.textContent = currencySymbol + parseFloat(data.total_amount || 0).toFixed(2);
                
                // Update summary section
                const summarySubtotal = document.getElementById('summary-subtotal');
                const summaryTax = document.getElementById('summary-tax');
                const summaryDiscount = document.getElementById('summary-discount');
                const summaryTotal = document.getElementById('summary-total');
                
                if (summarySubtotal) summarySubtotal.textContent = currencySymbol + parseFloat(data.subtotal || 0).toFixed(2);
                if (summaryTax) summaryTax.textContent = currencySymbol + parseFloat(data.total_tax || 0).toFixed(2);
                if (summaryDiscount) summaryDiscount.textContent = currencySymbol + parseFloat(data.total_discount || 0).toFixed(2);
                if (summaryTotal) summaryTotal.innerHTML = '<strong>' + currencySymbol + parseFloat(data.total_amount || 0).toFixed(2) + '</strong>';
                
                // Visual feedback
                [subtotalAmountCell, totalTaxCell, totalDiscountCell, totalAmountCell].forEach(cell => {
                    if (cell) {
                        cell.style.backgroundColor = '#d4edda';
                        cell.style.transition = 'background-color 0.5s';
                        setTimeout(() => {
                            cell.style.backgroundColor = '';
                        }, 1000);
                    }
                });
                
                showToast(`${itemNameToRemove} removed successfully!`, 'success');
            } else {
                console.error('Could not find row to remove');
                showToast(`${itemNameToRemove} removed successfully! Refreshing page...`, 'success');
                setTimeout(() => location.reload(), 1000);
            }
        } else {
            showToast(`Failed to remove ${itemNameToRemove}: ${data.message || 'Unknown error'}`, 'error');
        }
    })
    .catch(error => {
        console.error('Remove error:', error);
        showToast(`Error removing ${itemNameToRemove}`, 'error');
    })
    .finally(() => {
        // Reset button state
        confirmButton.textContent = originalText;
        confirmButton.disabled = false;
        closeRemoveModal();
    });
}

function updateRowNumbers() {
    const tableBody = document.getElementById('amount-table-body');
    const rows = tableBody.querySelectorAll('tr:not(.total-row)');
    rows.forEach((row, index) => {
        row.cells[0].textContent = index + 1;
    });
}

function addProductBackToDropdown(productName) {
    // This would require additional data about the product
    // For now, we'll just reload the page to refresh the dropdown
    // In a more sophisticated implementation, you'd store product data
}

// Cancel order function
function cancelOrder() {
    if (confirm('Are you sure you want to cancel this order? All items will be removed.')) {
        const orderId = document.querySelector('[name="order_id"]')?.value;
        
        if (orderId) {
            const formData = new FormData();
            formData.append('order_id', orderId);
            formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
            
            fetch('/cancel-order/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message, 'success');
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 1000);
                } else {
                    showToast(data.message || 'Failed to cancel order', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('An error occurred while cancelling the order', 'error');
            });
        } else {
            window.location.href = '/cart/';
        }
    }
}

// Show order confirmation modal
function showOrderModal() {
    document.getElementById('orderModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('orderModal').style.display = 'none';
    // Redirect to orders page or dashboard
    window.location.href = '/dashboard/';
}

// Show cancel order modal
function showCancelModal() {
    document.getElementById('cancelModal').style.display = 'block';
}

function closeCancelModal() {
    document.getElementById('cancelModal').style.display = 'none';
}

function confirmCancel() {
    const orderId = document.querySelector('[name="order_id"]')?.value;
    
    if (orderId) {
        const formData = new FormData();
        formData.append('order_id', orderId);
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
        
        fetch('/cancel-order/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                closeCancelModal();
                showCancelledModal();
            } else {
                showToast(data.message || 'Failed to cancel order', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred while cancelling the order', 'error');
        });
    } else {
        closeCancelModal();
        window.location.href = '/cart/';
    }
}

// Show cancelled order modal
function showCancelledModal() {
    document.getElementById('orderCancelledModal').style.display = 'block';
}

function closeCancelledModal() {
    document.getElementById('orderCancelledModal').style.display = 'none';
    // Redirect to dashboard or orders page
    window.location.href = '/dashboard/';
}

// Toast notification system
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    toast.innerHTML = `
        <span>${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
        <div class="toast-timer"></div>
    `;
    
    container.appendChild(toast);
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 3000);
}

// Edit item function - shows form when edit button is clicked
function editItem(itemId) {
    // Show the edit form (don't hide add product form)
    showEditForm(itemId);
}

// Show edit form
function showEditForm(itemId) {
    // Get current item data from the table row
    const row = document.getElementById(`row-${itemId}`);
    if (!row) return;
    
    const productName = row.cells[1].textContent.trim();
    const currentQty = row.querySelector('.qty-display').textContent.trim();
    
    // Get current currency symbol from the table or page elements
    let currencySymbol = '₹'; // Default to rupee
    
    // Try to get currency symbol from various page elements
    const priceCell = row.cells[2]?.textContent;
    if (priceCell) {
        const match = priceCell.match(/[^\d\s.,]+/);
        if (match) currencySymbol = match[0];
    }
    
    // Fallback: try to get from summary total
    if (currencySymbol === '₹') {
        const summaryTotal = document.querySelector('#summary-total')?.textContent;
        if (summaryTotal) {
            const match = summaryTotal.match(/[^\d\s.,]+/);
            if (match) currencySymbol = match[0];
        }
    }
    
    // Fallback: try to get from any price display on page
    if (currencySymbol === '₹') {
        const priceDisplay = document.querySelector('#price-display')?.value;
        if (priceDisplay) {
            const match = priceDisplay.match(/[^\d\s.,]+/);
            if (match) currencySymbol = match[0];
        }
    }
    
    console.log('Using currency symbol:', currencySymbol);
    
    // Remove any existing edit form first
    const existingEditForm = document.getElementById('edit-form-container');
    if (existingEditForm) {
        existingEditForm.remove();
    }
    
    // Get all available products from the original select dropdown
    const originalSelect = document.getElementById('product-select');
    let productOptions = '<option value="">Choose product...</option>';
    
    // Add current product as selected option
    productOptions += `<option value="current" selected>${productName}</option>`;
    
    // Add all available products to edit form dropdown
    for (let i = 0; i < originalSelect.options.length; i++) {
        const option = originalSelect.options[i];
        if (option.value && option.textContent.trim() !== productName) {
            productOptions += `
                <option value="${option.value}" 
                        data-price="${option.dataset.price}"
                        data-tax="${option.dataset.tax}"
                        data-discount="${option.dataset.discount}"
                        data-stock="${option.dataset.stock}">
                    ${option.textContent}
                </option>`;
        }
    }
    
    // Create edit form HTML - exactly like the add product form
    const editFormHTML = `
    <h2>Edit Item</h2>
        <form id="edit-product-form" method="POST" action="/update-invoice-item-qty/${itemId}/" class="product-form">
            <input type="hidden" name="csrfmiddlewaretoken" value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">
            <div class="form-grid">
                <div class="form-field">
                    <label>Product Name</label>
                    <select name="product_id" id="edit-product-select" >
                        ${productOptions}
                    </select>
                </div>
                <div class="form-field">
                    <label>Qty</label>
                    <input type="number" name="quantity" id="edit-quantity" value="${currentQty}" min="1" required>
                    <small class="stock-info">Current stock will be displayed</small>
                </div>
                <div class="form-field">
                    <label>Price</label>
                    <input type="text" id="edit-price-display" value="${currencySymbol}0" readonly>
                </div>
                <div class="form-field">
                    <label>Tax (%)</label>
                    <input type="text" id="edit-tax-input" name="tax_rate" value="18%" readonly>
                </div>
                <div class="form-field">
                    <label>Discount (%)</label>
                    <input type="text" id="edit-discount-input" name="discount_rate" value="5%" readonly>
                </div>
                <div class="form-field product-total-field">
                    <label>Product Total</label>
                    <input type="text" id="edit-product-total-display" value="${currencySymbol}0" readonly>
                </div>
            </div>
            <div class="form-footer">
                <button type="submit" class="add-btn">Update Product</button>
                <button type="button" class="cancel-btn" onclick="cancelEdit()">Cancel</button>
            </div>
        </form>
    `;
    
    // Create container for edit form
    const editFormContainer = document.createElement('div');
    editFormContainer.id = 'edit-form-container';
    editFormContainer.innerHTML = editFormHTML;
    
    // Insert edit form after the original add product form
    const addForm = document.getElementById('product-form');
    const separator = addForm.nextElementSibling; // The separator div
    separator.parentNode.insertBefore(editFormContainer, separator.nextSibling);
    
    // Set up form functionality with currency symbol
    setupEditForm(itemId, row, currencySymbol);
    
    // Scroll to edit form
    editFormContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Setup edit form functionality
function setupEditForm(itemId, row, currencySymbol = '₹') {
    const editForm = document.getElementById('edit-product-form');
    const productSelect = document.getElementById('edit-product-select');
    const quantityInput = document.getElementById('edit-quantity');
    const priceDisplay = document.getElementById('edit-price-display');
    const taxInput = document.getElementById('edit-tax-input');
    const discountInput = document.getElementById('edit-discount-input');
    const productTotalDisplay = document.getElementById('edit-product-total-display');
    
    // Get current values from the row
    const unitPrice = parseFloat(row.cells[2].textContent.replace('?', '')) || 0;
    const taxAmount = parseFloat(row.cells[4].textContent.replace('?', '')) || 0;
    const discountAmount = parseFloat(row.cells[5].textContent.replace('?', '')) || 0;
    const currentQty = parseInt(quantityInput.value) || 1;
    const currentProductName = row.cells[1].textContent.trim();
    
    // Get current product stock from the original dropdown
    const originalSelect = document.getElementById('product-select');
    let currentProductStock = null;
    for (let i = 0; i < originalSelect.options.length; i++) {
        const option = originalSelect.options[i];
        if (option.textContent.trim() === currentProductName) {
            currentProductStock = parseInt(option.dataset.stock) || 0;
            break;
        }
    }
    
    // Calculate tax and discount rates from current values
    const subtotal = unitPrice * currentQty;
    const taxRate = subtotal > 0 ? (taxAmount / subtotal) * 100 : 18;
    const discountRate = subtotal > 0 ? (discountAmount / subtotal) * 100 : 5;
    
    // Set initial values
    priceDisplay.value = currencySymbol + unitPrice.toFixed(2);
    taxInput.value = taxRate.toFixed(0) + '%';
    discountInput.value = discountRate.toFixed(0) + '%';
    
    // Set initial stock info for current product
    updateEditStockInfo(currentProductStock);
    
    // Calculate initial total
    calculateEditProductTotal();
    
    // Add event listeners for product selection change
    productSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        if (selectedOption.value && selectedOption.value !== 'current') {
            // Update with new product data
            const newPrice = parseFloat(selectedOption.dataset.price) || 0;
            const newTax = parseFloat(selectedOption.dataset.tax) || 18;
            const newDiscount = parseFloat(selectedOption.dataset.discount) || 0;
            const newStock = parseInt(selectedOption.dataset.stock) || 0;
            
            priceDisplay.value = currencySymbol + newPrice.toFixed(2);
            taxInput.value = newTax + '%';
            discountInput.value = newDiscount + '%';
            
            // Set max quantity and show stock info
            quantityInput.max = newStock;
            updateEditStockInfo(newStock);
        } else if (selectedOption.value === 'current') {
            // Reset to original values
            priceDisplay.value = currencySymbol + unitPrice.toFixed(2);
            taxInput.value = taxRate.toFixed(0) + '%';
            discountInput.value = discountRate.toFixed(0) + '%';
            quantityInput.removeAttribute('max');
            updateEditStockInfo(currentProductStock);
        }
        calculateEditProductTotal();
    });
    
    // Add stock validation to quantity input
    quantityInput.addEventListener('input', function() {
        const selectedOption = productSelect.options[productSelect.selectedIndex];
        const quantity = parseInt(this.value) || 1;
        
        if (selectedOption.value && selectedOption.value !== 'current') {
            // Validation for new product selection
            const stock = parseInt(selectedOption.dataset.stock) || 0;
            
            if (quantity > stock) {
                this.value = stock;
                showToast(`Maximum available quantity is ${stock}`, 'warning');
            }
        } else {
            // Validation for current product - add back the original quantity to available stock
            if (currentProductStock !== null) {
                const originalQty = parseInt(row.querySelector('.qty-display').textContent) || 0;
                const availableStock = currentProductStock + originalQty; // Add back original quantity
                
                if (quantity > availableStock) {
                    this.value = availableStock;
                    showToast(`Maximum available quantity for ${currentProductName} is ${availableStock} (including current ${originalQty})`, 'warning');
                }
            }
        }
        calculateEditProductTotal();
    });
    
    // Function to update stock info in edit form
    function updateEditStockInfo(stock) {
        const stockInfo = editForm.querySelector('.stock-info');
        if (stockInfo) {
            if (stock === null) {
                stockInfo.textContent = 'Stock information not available';
                stockInfo.className = 'stock-info';
            } else {
                // For current product, add back the original quantity
                const selectedOption = productSelect.options[productSelect.selectedIndex];
                let displayStock = stock;
                
                if (!selectedOption.value || selectedOption.value === 'current') {
                    const originalQty = parseInt(row.querySelector('.qty-display').textContent) || 0;
                    displayStock = stock + originalQty; // Add back original quantity
                }
                
                if (displayStock === 0) {
                    stockInfo.textContent = 'Out of Stock';
                    stockInfo.className = 'stock-info out-of-stock';
                } else if (displayStock <= 5) {
                    stockInfo.textContent = `Low Stock: ${displayStock} available`;
                    stockInfo.className = 'stock-info low-stock';
                } else {
                    stockInfo.textContent = `Available Stock: ${displayStock} units`;
                    stockInfo.className = 'stock-info in-stock';
                }
            }
        }
    }
    
    // Add event listeners
    quantityInput.addEventListener('input', calculateEditProductTotal);
    
    // Calculate product total for edit form
    function calculateEditProductTotal() {
        const selectedOption = productSelect.options[productSelect.selectedIndex];
        let price = unitPrice;
        
        // Use selected product price if different product is selected
        if (selectedOption.value && selectedOption.value !== 'current') {
            price = parseFloat(selectedOption.dataset.price) || 0;
        }
        
        const quantity = parseInt(quantityInput.value) || 1;
        const taxRate = parseFloat(taxInput.value.replace('%', '')) || 0;
        const discountRate = parseFloat(discountInput.value.replace('%', '')) || 0;
        
        const subtotal = price * quantity;
        const taxAmount = (subtotal * taxRate) / 100;
        const discountAmount = (subtotal * discountRate) / 100;
        const total = subtotal + taxAmount - discountAmount;
        
        productTotalDisplay.value = currencySymbol + total.toFixed(2);
    }
    
    // Handle form submission
    editForm.addEventListener('submit', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Validate stock before submission
        const selectedOption = productSelect.options[productSelect.selectedIndex];
        const quantity = parseInt(quantityInput.value) || 1;
        
        if (selectedOption.value && selectedOption.value !== 'current') {
            const stock = parseInt(selectedOption.dataset.stock) || 0;
            if (stock === 0) {
                showToast('Selected product is out of stock', 'error');
                return;
            }
            if (quantity > stock) {
                showToast(`Only ${stock} units available`, 'error');
                return;
            }
        }
        
        const formData = new FormData(this);
        const submitButton = this.querySelector('button[type="submit"]');
        
        // Check if product was changed
        console.log('Selected option:', selectedOption.value, selectedOption.textContent);
        
        if (selectedOption.value && selectedOption.value !== 'current' && selectedOption.value !== '') {
            // Product was changed to a new product
            formData.set('product_id', selectedOption.value);
            formData.set('product_changed', 'true');
            formData.set('new_product_name', selectedOption.textContent.trim());
            console.log('Product changed to:', selectedOption.value, selectedOption.textContent.trim());
        } else {
            // Keep original product, just update quantity
            formData.delete('product_id'); // Don't send product_id to keep original
            formData.set('product_changed', 'false');
            console.log('Product not changed, only updating quantity');
        }
        
        // Remove % symbol from tax and discount before sending
        const taxValue = taxInput.value.replace('%', '');
        const discountValue = discountInput.value.replace('%', '');
        formData.set('tax_rate', taxValue);
        formData.set('discount_rate', discountValue);
        
        // Disable submit button
        submitButton.disabled = true;
        submitButton.textContent = 'Updating...';
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            console.log('Edit form response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Edit form response data:', data);
            if (data.success) {
                // Update the table row with new product info
                const qtyCell = row.querySelector('.qty-cell');
                const qtyDisplay = qtyCell.querySelector('.qty-display');
                qtyDisplay.textContent = formData.get('quantity');
                qtyCell.dataset.originalQty = formData.get('quantity');
                
                // Update product name if changed
                if (selectedOption.value && selectedOption.value !== 'current' && selectedOption.value !== '') {
                    row.cells[1].textContent = selectedOption.textContent.trim();
                    qtyCell.dataset.productName = selectedOption.textContent.trim();
                    console.log('Updated product name to:', selectedOption.textContent.trim());
                    
                    // Force a visual update to confirm change
                    row.cells[1].style.backgroundColor = '#d4edda';
                    setTimeout(() => {
                        row.cells[1].style.backgroundColor = '';
                    }, 2000);
                    
                    // Also update the row's data-item-id if server provides new item data
                    if (data.new_item_id) {
                        row.setAttribute('data-item-id', data.new_item_id);
                        row.setAttribute('id', `row-${data.new_item_id}`);
                        console.log('Updated row ID to:', data.new_item_id);
                    }
                }
                
                // Update price
                const serverCurrencySymbol = data.currency_symbol || currencySymbol;
                if (data.item_unit_price) {
                    row.cells[2].textContent = serverCurrencySymbol + parseFloat(data.item_unit_price).toFixed(2);
                } else {
                    // Use the price from the form if server doesn't return it
                    const currentPrice = parseFloat(priceDisplay.value.replace(/[^\d.]/g, '')) || 0;
                    row.cells[2].textContent = serverCurrencySymbol + currentPrice.toFixed(2);
                }
                
                // Update other cells if data is provided
                if (data.item_tax_amount) {
                    row.cells[4].textContent = serverCurrencySymbol + parseFloat(data.item_tax_amount).toFixed(2);
                }
                if (data.item_discount) {
                    row.cells[5].textContent = serverCurrencySymbol + parseFloat(data.item_discount).toFixed(2);
                }
                if (data.item_total) {
                    row.cells[6].textContent = serverCurrencySymbol + parseFloat(data.item_total).toFixed(2);
                }
                
                // Update overall totals only if provided
                if (data.subtotal && data.total_tax && data.total_discount && data.total_amount) {
                    updateTotals({
                        subtotal: data.subtotal,
                        total_tax: data.total_tax,
                        total_discount: data.total_discount,
                        total_amount: data.total_amount,
                        currency_symbol: serverCurrencySymbol
                    });
                }
                
                // Remove edit form
                cancelEdit();
                
                showToast('Product updated successfully! Changes saved to database.', 'success');
                
                // Log success for debugging
                console.log('Product update completed successfully');
                console.log('Database should now contain the new product');
            } else {
                console.error('Server returned error:', data.error);
                showToast(data.error || 'Failed to update product', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred while updating the product', 'error');
        })
        .finally(() => {
            // Re-enable submit button
            submitButton.disabled = false;
            submitButton.textContent = 'Update Product';
        });
    });
}

// Cancel edit function
function cancelEdit() {
    // Remove edit form
    const editFormContainer = document.getElementById('edit-form-container');
    if (editFormContainer) {
        editFormContainer.remove();
    }
}

// Close modals when clicking outside
window.addEventListener('click', function(event) {
    const orderModal = document.getElementById('orderModal');
    const removeModal = document.getElementById('removeModal');
    const cancelModal = document.getElementById('cancelModal');
    const cancelledModal = document.getElementById('orderCancelledModal');
    
    if (event.target === orderModal) {
        orderModal.style.display = 'none';
    }
    
    if (event.target === removeModal) {
        closeRemoveModal();
    }
    
    if (event.target === cancelModal) {
        closeCancelModal();
    }
    
    if (event.target === cancelledModal) {
        closeCancelledModal();
    }
});



 document.addEventListener('DOMContentLoaded', function() {

        const invoice = document.querySelector('.invoice-container');
        const menuBar2 = document.querySelector('.menu-bar2');
        const svg1 = document.querySelector('.svg1');
        const svg3 = document.querySelector('.svg3');

        svg1.addEventListener('click', () => {
            menuBar2.classList.remove('active');
            invoice.classList.remove('shifted');
        });

        svg3.addEventListener('click', () => {
            menuBar2.classList.add('active');
            invoice.classList.add('shifted');
        });

    });