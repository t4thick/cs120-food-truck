# Item7 Food Truck - Class Presentation Guide

## 🎯 Presentation Overview

**Duration**: 15-20 minutes  
**Format**: Live demo + slides  
**Audience**: CS120 Class

---

## 📋 Phase 1: Introduction & Project Overview (3-4 minutes)

### Opening Statement
> "Today we're presenting **Item7 Food Truck**, a comprehensive web application that combines customer ordering with staff management. It's built with Flask and demonstrates real-world food service operations."

### Key Points to Cover:

1. **Problem Statement**
   - Food truck needs online ordering system
   - Staff needs management portal
   - Need to track orders, schedules, and inventory

2. **Solution Overview**
   - Customer-facing ordering system
   - Staff management portal
   - Real-time order tracking
   - Time clock system for employees

3. **Technology Stack**
   - **Backend**: Flask (Python)
   - **Storage**: CSV files (simple, no database needed)
   - **Frontend**: HTML, CSS, JavaScript
   - **Payment**: Stripe integration (demo mode)
   - **Maps**: Leaflet.js for delivery addresses

4. **Live Demo Link** (if deployed)
   - Show the live URL: `https://item7-food-truck.onrender.com`
   - Or run locally: `http://localhost:5001`

### Visual Aid:
- Show homepage screenshot
- Show project structure diagram
- Mention: "We'll dive into the features next"

---

## 🎬 Phase 2: Feature Demonstration (6-8 minutes)

### A. Customer Experience (2-3 minutes)

**Demo Flow:**
1. **Homepage**
   - Show featured menu items
   - Highlight "Popular Picks" section
   - Show contact information (location, phone)

2. **Menu Browsing**
   - Navigate to full menu
   - Show category carousel (swipe through items)
   - Demonstrate: "We have 23 pre-populated items across 5 categories"

3. **Shopping Cart**
   - Add items to cart
   - Show quantity editing
   - Remove items
   - "Cart updates in real-time using session storage"

4. **Checkout Process**
   - Show delivery address form
   - **Highlight**: Map integration (auto-location detection)
   - Show payment options (Stripe demo mode + Cash on Delivery)
   - Show tip calculation (10%, 15%, 20%, 25%, custom)
   - Show tax calculation (7.5%)
   - Complete order

**Key Talking Points:**
- "Customers can order online with full delivery address support"
- "We integrated maps like DoorDash for location selection"
- "Payment processing with Stripe, or cash on delivery option"
- "All orders are saved to CSV for staff to process"

---

### B. Staff Portal Features (3-4 minutes)

**Demo Flow:**

1. **Staff Login**
   - Login as staff member
   - Show staff dashboard

2. **Order Management**
   - Navigate to Orders page
   - Show all customer orders
   - **Highlight**: Allergy alerts (yellow/red borders)
   - Demonstrate status updates:
     - "Pending" → "Preparation Done" → "Ready for Delivery"
   - Show "Hand Off to Delivery" button

3. **Menu Management** ⭐ **KEY FEATURE**
   - Navigate to "Manage Menu"
   - Show existing 23 menu items
   - **Demonstrate adding a new item:**
     - Fill form (name, description, price, category)
     - **Upload an image** (show file upload)
     - Add allergens
     - Save to CSV
   - **Demonstrate editing:**
     - Edit existing item
     - Show "Remove current image" option
     - Upload new image
   - **Demonstrate deleting:**
     - Delete an item with confirmation

4. **Time Clock System** ⭐ **KEY FEATURE**
   - Navigate to Schedule/Time Clock
   - Show "Claim a Shift" form
   - **Demonstrate check-in:**
     - Claim shift
     - Check in
     - Show active shift display
   - **Demonstrate break management:**
     - Start break
     - End break
   - **Demonstrate early checkout:**
     - Show "Check Out Early (Emergency)" button
   - **Show shift notes:**
     - Add notes during shift
   - **Show work history:**
     - View past shifts with hours worked
     - Show weekly hours total

5. **Statistics Dashboard** (Quick overview)
   - Show daily/monthly/yearly totals
   - Show top customers
   - Show revenue tracking

**Key Talking Points:**
- "Staff can manage the entire menu - add, edit, delete items with images"
- "Time clock system tracks actual hours worked, including breaks"
- "Order management with allergy alerts for food safety"
- "Real-time statistics for business insights"

---

### C. Advanced Features (1 minute)

**Quick Highlights:**
1. **Deals Management** (Senior Managers)
   - Create promotions
   - Show on homepage

2. **Staff Management** (Admins)
   - Remove staff members
   - Senior manager verification

3. **Order Tracking**
   - Customer order history
   - Status updates visible to customers

---

## 🔧 Phase 3: Technical Implementation (4-5 minutes)

### A. Architecture Overview

**Show on screen:**
```
┌─────────────────┐
│  Flask App      │
│  (app.py)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ FoodTruck Class │
│ (foodtruck.py)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CSV Storage    │
│  (data/*.csv)   │
└─────────────────┘
```

**Explain:**
- "We use CSV files instead of a database for simplicity"
- "All data persists across sessions"
- "Easy to backup and manage"

---

### B. Key Technical Features

1. **CSV-Based Storage**
   - Show file structure: `data/menu.csv`, `data/orders.csv`, etc.
   - Explain: "5 CSV files store all application data"
   - "Menu items migrated from hardcoded to CSV on first run"

2. **Image Upload System**
   - Show `static/images/menu/` directory
   - Explain: "Uploaded images stored with timestamped filenames"
   - "Can remove and replace images"

3. **Session Management**
   - Explain: "Cart stored in Flask sessions"
   - "User authentication via sessions"
   - "Role-based access control"

4. **RESTful API Endpoints**
   - Show: `/api/menu`, `/api/cart`, `/api/staff/shifts`
   - "JSON endpoints for dynamic updates"

5. **Error Handling**
   - "Comprehensive try-catch blocks"
   - "User-friendly error messages"
   - "Logging for debugging"

---

### C. Code Highlights (Show snippets)

1. **Menu Management Function**
   ```python
   def add_menu_item(self, name, description, price, category, vegan, image, allergens):
       # Generate unique ID
       # Save to CSV
       # Reload menu
   ```

2. **Time Clock Logic**
   ```python
   def update_shift_status(self, shift_id, status, check_in_time, check_out_time):
       # Calculate hours worked
       # Subtract break time
       # Update CSV
   ```

3. **Order Processing**
   ```python
   # Process payment (Stripe or cash)
   # Calculate tax and tip
   # Save to orders.csv
   # Update status
   ```

---

### D. Challenges & Solutions

1. **Challenge**: Menu items were hardcoded
   - **Solution**: Migrated to CSV with auto-migration on first run

2. **Challenge**: Image uploads needed file management
   - **Solution**: Timestamped filenames, organized in `menu/` folder

3. **Challenge**: Time tracking accuracy
   - **Solution**: Break time subtraction, early checkout handling

4. **Challenge**: Homepage menu not showing
   - **Solution**: Explicit menu loading in route handler

---

## 🎓 Phase 4: Q&A & Wrap-up (2-3 minutes)

### Summary Points

1. **What We Built**
   - Full-stack web application
   - Customer ordering system
   - Staff management portal
   - Real-time order tracking
   - Time clock system

2. **Key Achievements**
   - ✅ 23 pre-populated menu items
   - ✅ Image upload functionality
   - ✅ Time clock with break tracking
   - ✅ Order management with allergy alerts
   - ✅ Statistics dashboard
   - ✅ Payment integration (Stripe + Cash)

3. **Technical Highlights**
   - CSV-based storage (no database)
   - RESTful API endpoints
   - Role-based access control
   - Responsive design
   - Error handling throughout

---

### Potential Questions & Answers

**Q: Why CSV instead of a database?**  
A: "For this course project, CSV files are simpler to manage and demonstrate file I/O concepts. In production, we'd use a database."

**Q: How do you handle concurrent orders?**  
A: "CSV files are locked during writes. For production, we'd use a database with proper transaction handling."

**Q: Can customers track their orders?**  
A: "Yes, customers can view their order history. Staff can update order status in real-time."

**Q: How does the time clock calculate hours?**  
A: "It calculates total time from check-in to check-out, then subtracts break duration. All stored in shifts.csv."

**Q: What about security?**  
A: "We use password hashing (pbkdf2:sha256), session management, role-based access, and input sanitization."

**Q: Can you deploy this?**  
A: "Yes, it's deployed on Render.com. The live URL is [if available]."

---

### Closing Statement

> "Item7 Food Truck demonstrates a complete food service management system with both customer and staff interfaces. We've implemented real-world features like menu management, time tracking, and order processing. The application is fully functional and ready for deployment. Thank you!"

---

## 📊 Presentation Checklist

### Before Presentation:
- [ ] Test all features work
- [ ] Have demo data ready (menu items, test orders)
- [ ] Prepare screenshots/recordings as backup
- [ ] Test internet connection (if using live demo)
- [ ] Have code snippets ready to show
- [ ] Prepare answers for common questions

### During Presentation:
- [ ] Start with clear introduction
- [ ] Show live demo (don't just talk)
- [ ] Highlight key features (menu management, time clock)
- [ ] Explain technical decisions
- [ ] Keep to time limit
- [ ] Engage with audience

### Visual Aids:
- [ ] Project architecture diagram
- [ ] Screenshots of key features
- [ ] Code snippets (if showing code)
- [ ] Flowchart diagrams (optional)

---

## 🎯 Key Messages to Emphasize

1. **Real-World Application**: "This isn't just a demo - it's a functional system"
2. **Complete Solution**: "We built both customer and staff sides"
3. **Production-Ready Features**: "Image uploads, payment processing, time tracking"
4. **Clean Code**: "Well-organized, documented, error-handled"
5. **Scalable Design**: "Easy to extend with more features"

---

## ⏱️ Time Breakdown

| Phase | Duration | Focus |
|-------|----------|-------|
| Phase 1: Introduction | 3-4 min | Overview, tech stack |
| Phase 2: Demo | 6-8 min | Live feature demonstration |
| Phase 3: Technical | 4-5 min | Architecture, code, challenges |
| Phase 4: Q&A | 2-3 min | Summary, questions |
| **Total** | **15-20 min** | |

---

## 💡 Pro Tips

1. **Practice the demo** - Know exactly what to click
2. **Have backup screenshots** - In case demo fails
3. **Show enthusiasm** - This is a cool project!
4. **Explain the "why"** - Not just what, but why you made decisions
5. **Be ready for questions** - Know your code well
6. **Highlight unique features** - Menu management, time clock, image uploads

---

**Good luck with your presentation! 🚀**

