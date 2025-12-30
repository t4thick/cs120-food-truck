# Special Features Documentation

## Two Easy-to-Explain Features for Group Presentation

---

## 🧾 Feature 1: Automatic Sales Tax Calculation System

### What It Does
The food truck app automatically calculates and adds **7.5% sales tax** to every customer order. This is a legal requirement for prepared food in most US states.

### How It Works (Simple Explanation)
1. Customer adds items to their cart (e.g., Burger $8.99, Fries $3.99)
2. The system calculates the **subtotal** (items added together)
3. The system automatically calculates **7.5% tax** on the subtotal
4. The **final total** = subtotal + tax

### Example Calculation
```
Customer Order:
- Classic Burger:     $8.99
- Loaded Fries:       $4.99
- Soft Drink:         $2.49
─────────────────────────────
Subtotal:            $16.47
Tax (7.5%):           $1.24
─────────────────────────────
TOTAL:               $17.71
```

### Where to See This in the Code

**File: `app.py` (Line 59-60)**
```python
# Tax rate for prepared food (7.5% is a common rate in many US states)
TAX_RATE = float(os.environ.get("TAX_RATE", "0.075"))  # 7.5% default
```

**File: `app.py` (Lines 1120-1123)** - Cart page calculation:
```python
subtotal = sum(float(item.get("price", 0)) * int(item.get("qty", 0)) for item in cart.values())
tax_amount = subtotal * TAX_RATE
total = subtotal + tax_amount
```

**File: `templates/checkout.html` (Lines 27-29)** - Display to customer:
```html
<div class="total-line">
    <span>Tax (7.5%):</span>
    <span>${{ "%.2f"|format(tax_amount) }}</span>
</div>
```

### Why This Feature is Important
- **Legal Compliance**: Businesses must charge sales tax on prepared food
- **Transparency**: Customers see exactly how much tax they're paying
- **Automatic**: Staff don't have to manually calculate tax - no math errors
- **Configurable**: The tax rate can be changed via environment variable if needed

### How to Demonstrate to Teacher
1. Go to the **Menu** page
2. Add a few items to the cart
3. Go to **Cart** page - you'll see the tax automatically calculated
4. Proceed to **Checkout** - the breakdown shows Subtotal, Tax, and Total separately

---

## 💰 Feature 2: Customer Tipping System

### What It Does
The checkout page allows customers to add a **tip** for the food truck staff. They can choose from preset percentages (10%, 15%, 20%, 25%) or enter a custom tip amount.

### How It Works (Simple Explanation)
1. Customer goes to checkout
2. They see tip buttons: **No Tip, 10%, 15%, 20%, 25%**
3. Each button shows the actual dollar amount (e.g., "15% ($2.47)")
4. Customer can also type a **custom amount** if they want
5. The tip is added to the final total
6. The tip is calculated based on the **subtotal** (before tax)

### Example
```
Order Subtotal:      $16.47
Tax (7.5%):           $1.24
─────────────────────────────
Before Tip:          $17.71

Customer selects 15% tip:
Tip (15%):            $2.47
─────────────────────────────
FINAL TOTAL:         $20.18
```

### Where to See This in the Code

**File: `templates/checkout.html` (Lines 43-57)** - Tip selection UI:
```html
<div class="checkout-section">
    <h2>Add Tip (Optional)</h2>
    <div class="tip-options">
        <button type="button" class="tip-btn" data-tip="0">No Tip</button>
        <button type="button" class="tip-btn" data-tip="10">10% (${{ "%.2f"|format(subtotal * 0.10) }})</button>
        <button type="button" class="tip-btn" data-tip="15">15% (${{ "%.2f"|format(subtotal * 0.15) }})</button>
        <button type="button" class="tip-btn" data-tip="20">20% (${{ "%.2f"|format(subtotal * 0.20) }})</button>
        <button type="button" class="tip-btn" data-tip="25">25% (${{ "%.2f"|format(subtotal * 0.25) }})</button>
    </div>
    <div class="custom-tip">
        <label for="custom_tip">Custom Amount:</label>
        <input type="number" id="custom_tip" step="0.01" min="0" placeholder="0.00">
    </div>
</div>
```

**File: `templates/checkout.html` (Lines 827-860)** - JavaScript calculation:
```javascript
function updateTip() {
    let tipValue = 0;
    if (customTipAmount > 0) {
        tipValue = customTipAmount;
    } else if (selectedTipPercentage > 0) {
        // Tip is calculated on subtotal (before tax)
        tipValue = subtotal * (selectedTipPercentage / 100);
    }
    
    // Final total = subtotal + tax + tip
    const finalTotal = baseTotal + tipValue;
    
    // Update the display
    document.getElementById('tip-amount').textContent = '$' + tipValue.toFixed(2);
    document.getElementById('final-total').textContent = '$' + finalTotal.toFixed(2);
}
```

**File: `app.py` (Lines 1286-1295)** - Processing tip on form submission:
```python
# Get tip amount
try:
    tip_amount = float(request.form.get("tip_amount", "0") or "0")
    tip_percentage = float(request.form.get("tip_percentage", "0") or "0")
except (ValueError, TypeError):
    tip_amount = 0.0
    tip_percentage = 0.0

# Calculate final total with tip
final_total = total + tip_amount
```

### Why This Feature is Important
- **Customer Appreciation**: Lets customers show appreciation for good service
- **Staff Motivation**: Tips encourage staff to provide great service
- **Flexibility**: Preset buttons make it easy, custom amount gives freedom
- **Industry Standard**: Most food delivery apps have tipping features
- **Real-time Updates**: The total updates instantly when selecting a tip

### How to Demonstrate to Teacher
1. Add items to cart and go to **Checkout**
2. Look at the **"Add Tip (Optional)"** section
3. Click different tip buttons - watch the total update in real-time
4. Try entering a custom tip amount
5. Show that "No Tip" is also an option
6. Complete an order and show how the tip appears in the order summary

---

## Quick Reference for Presentation

| Feature | Location in App | Key Files |
|---------|-----------------|-----------|
| Tax Calculation | Cart & Checkout pages | `app.py` (lines 59-60, 1120-1123), `checkout.html` (lines 27-29) |
| Tipping System | Checkout page | `checkout.html` (lines 43-57, 827-860), `app.py` (lines 1286-1295) |

## Talking Points for Teacher

### For Tax Feature:
- "Our app automatically calculates 7.5% sales tax on all orders"
- "This ensures legal compliance with tax laws"
- "The customer sees the breakdown: subtotal, tax, and total"
- "The tax rate is configurable if it needs to change"

### For Tipping Feature:
- "We implemented a tipping system similar to DoorDash or Uber Eats"
- "Customers can choose preset percentages or enter a custom amount"
- "The tip is calculated on the subtotal before tax"
- "The total updates in real-time when they select a tip"
- "It's optional - they can also choose 'No Tip'"

---

**Pro Tip**: When demonstrating, have a few items already in the cart so you can quickly show both features working together on the checkout page!

