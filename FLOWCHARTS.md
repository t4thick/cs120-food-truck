# Item7 Food Truck - System Flowcharts

This document contains visual flowcharts for understanding the system architecture and user flows.

## 📊 Table of Contents
1. [System Architecture Flow](#system-architecture-flow)
2. [Customer Ordering Flow](#customer-ordering-flow)
3. [Staff Portal Flow](#staff-portal-flow)
4. [Time Clock System Flow](#time-clock-system-flow)
5. [Menu Management Flow](#menu-management-flow)
6. [Order Processing Flow](#order-processing-flow)
7. [Authentication Flow](#authentication-flow)

---

## 🏗️ System Architecture Flow

```mermaid
graph TB
    A[User Browser] -->|HTTP Request| B[Flask App]
    B --> C{Route Handler}
    C -->|Public| D[Public Routes]
    C -->|Staff| E[Staff Routes]
    C -->|API| F[API Routes]
    
    D --> G[FoodTruck Class]
    E --> G
    F --> G
    
    G --> H[CSV Operations]
    H --> I[data/users.csv]
    H --> J[data/menu.csv]
    H --> K[data/orders.csv]
    H --> L[data/shifts.csv]
    H --> M[data/deals.csv]
    
    G -->|Return Data| C
    C -->|Render Template| N[Jinja2 Templates]
    N -->|HTML Response| A
```

---

## 🛒 Customer Ordering Flow

```mermaid
flowchart TD
    Start([Customer Visits Site]) --> Home[Homepage]
    Home --> Browse[Browse Menu]
    Browse --> Add{Add to Cart?}
    Add -->|Yes| Cart[View Cart]
    Add -->|No| Browse
    Cart --> Continue{Continue Shopping?}
    Continue -->|Yes| Browse
    Continue -->|No| Checkout[Go to Checkout]
    
    Checkout --> Login{Logged In?}
    Login -->|No| Signup[Sign Up / Login]
    Login -->|Yes| Delivery[Enter Delivery Info]
    Signup --> Delivery
    
    Delivery --> Map[Select Location on Map]
    Map --> Payment{Payment Method?}
    Payment -->|Stripe| Card[Enter Card Details]
    Payment -->|Cash| Confirm[Confirm Order]
    
    Card --> Process[Process Payment]
    Process --> Success{Success?}
    Success -->|Yes| Confirm
    Success -->|No| Error[Show Error]
    Error --> Card
    
    Confirm --> Save[Save Order to CSV]
    Save --> Email[Send Confirmation]
    Email --> Done([Order Complete])
```

---

## 👨‍💼 Staff Portal Flow

```mermaid
flowchart TD
    Start([Staff Login]) --> Auth{Authenticated?}
    Auth -->|No| Error[Show Error]
    Error --> Start
    Auth -->|Yes| Dashboard[Staff Dashboard]
    
    Dashboard --> Menu{Select Action}
    Menu -->|Orders| Orders[View Orders]
    Menu -->|Statistics| Stats[View Statistics]
    Menu -->|Manage Menu| MenuMgmt[Menu Management]
    Menu -->|Schedule| Schedule[Time Clock]
    Menu -->|Deals| Deals[Deals Management]
    Menu -->|Staff| StaffMgmt[Staff Management]
    
    Orders --> UpdateStatus[Update Order Status]
    UpdateStatus --> Pending[Pending]
    Pending --> Prep[Preparation Done]
    Prep --> Ready[Ready for Delivery]
    
    Stats --> Reports[View Reports]
    Reports --> Daily[Daily Stats]
    Reports --> Monthly[Monthly Stats]
    Reports --> Yearly[Yearly Stats]
    
    MenuMgmt --> MenuAction{Action?}
    MenuAction -->|Add| AddItem[Add Menu Item]
    MenuAction -->|Edit| EditItem[Edit Menu Item]
    MenuAction -->|Delete| DeleteItem[Delete Menu Item]
    
    AddItem --> UploadImg[Upload Image]
    UploadImg --> SaveMenu[Save to CSV]
    EditItem --> UpdateImg{Update Image?}
    UpdateImg -->|Yes| RemoveImg[Remove Old Image]
    UpdateImg -->|No| KeepImg[Keep Current]
    RemoveImg --> UploadImg
    KeepImg --> SaveMenu
    DeleteItem --> RemoveFromCSV[Remove from CSV]
    
    Schedule --> ShiftAction{Shift Action?}
    ShiftAction -->|Claim| Claim[Claim Shift]
    ShiftAction -->|Check In| CheckIn[Check In]
    ShiftAction -->|Break| Break[Start/End Break]
    ShiftAction -->|Check Out| CheckOut[Check Out]
    ShiftAction -->|Early| Early[Early Checkout]
    ShiftAction -->|Notes| Notes[Add Shift Notes]
    
    Claim --> Schedule
    CheckIn --> Working[Working]
    Working --> Break
    Working --> CheckOut
    Break --> Working
    Working --> Early
    CheckOut --> Record[Record Hours]
    Early --> Record
    Notes --> SaveNotes[Save Notes]
```

---

## ⏰ Time Clock System Flow

```mermaid
stateDiagram-v2
    [*] --> Scheduled: Staff Claims Shift
    
    Scheduled --> CheckedIn: Check In Button
    CheckedIn --> OnBreak: Start Break Button
    OnBreak --> CheckedIn: End Break Button
    
    CheckedIn --> Completed: Check Out Button
    CheckedIn --> Completed: Early Checkout Button
    OnBreak --> Completed: Early Checkout Button
    
    Completed --> [*]: Hours Calculated & Saved
    
    note right of CheckedIn
        Can add shift notes
        Can take breaks
        Can check out early
    end note
    
    note right of OnBreak
        Can end break
        Can check out early
    end note
```

### Time Clock State Transitions

```
┌──────────┐
│ Scheduled│ ← Staff claims a shift
└────┬─────┘
     │ Check In
     ▼
┌──────────┐
│Checked In│ ← Working on shift
└────┬─────┘
     │ Start Break
     ▼
┌──────────┐
│ On Break │ ← Taking a break
└────┬─────┘
     │ End Break
     ▼
┌──────────┐
│Checked In│ ← Back to work
└────┬─────┘
     │ Check Out
     ▼
┌──────────┐
│Completed │ ← Shift finished
└──────────┘
```

---

## 🍽️ Menu Management Flow

```mermaid
flowchart LR
    A[Staff Portal] --> B[Manage Menu]
    B --> C{Action}
    
    C -->|Add New| D[Fill Form]
    C -->|Edit| E[Select Item]
    C -->|Delete| F[Confirm Delete]
    
    D --> G[Upload Image?]
    G -->|Yes| H[Save Image File]
    G -->|No| I[Use Default]
    H --> J[Save to menu.csv]
    I --> J
    
    E --> K[Load Current Data]
    K --> L[Update Form]
    L --> M{Change Image?}
    M -->|Yes| N{Remove Old?}
    M -->|No| O[Keep Current]
    N -->|Yes| P[Delete Old File]
    N -->|No| Q[Keep Old]
    P --> H
    Q --> H
    O --> R[Update CSV]
    H --> R
    
    F --> S[Remove from CSV]
    J --> T[Menu Updated]
    R --> T
    S --> T
    T --> U[Display on Site]
```

---

## 📦 Order Processing Flow

```mermaid
sequenceDiagram
    participant C as Customer
    participant W as Web App
    participant CSV as CSV Storage
    participant S as Staff Portal
    participant P as Payment (Stripe/Cash)
    
    C->>W: Add Items to Cart
    W->>W: Store in Session
    C->>W: Proceed to Checkout
    W->>C: Show Checkout Form
    C->>W: Enter Delivery Info
    C->>W: Select Payment Method
    C->>W: Add Tip & Confirm
    
    alt Stripe Payment
        C->>P: Submit Card Details
        P->>W: Payment Success
    else Cash on Delivery
        W->>W: Mark as Cash
    end
    
    W->>CSV: Save Order to orders.csv
    CSV->>S: New Order Available
    S->>S: Display in Orders Page
    S->>S: Update Status
    S->>CSV: Update Order Status
    W->>C: Show Confirmation
```

---

## 🔐 Authentication Flow

```mermaid
flowchart TD
    Start([User Visits Site]) --> Check{Logged In?}
    Check -->|Yes| Role{What Role?}
    Check -->|No| Public[Public Access]
    
    Role -->|Customer| Customer[Customer Access]
    Role -->|Staff| Staff[Staff Access]
    Role -->|Admin| Admin[Admin Access]
    
    Public --> Login[Login Page]
    Public --> Signup[Signup Page]
    
    Login --> Validate{Valid Credentials?}
    Validate -->|Yes| SetSession[Set Session]
    Validate -->|No| Error[Show Error]
    Error --> Login
    
    Signup --> StaffCode{Registering as Staff?}
    StaffCode -->|Yes| EnterCode[Enter Staff Code]
    StaffCode -->|No| CreateAccount[Create Account]
    EnterCode --> ValidateCode{Code Valid?}
    ValidateCode -->|Yes| CreateAccount
    ValidateCode -->|No| CodeError[Show Error]
    CodeError --> EnterCode
    
    CreateAccount --> HashPassword[Hash Password]
    HashPassword --> SaveUser[Save to users.csv]
    SaveUser --> SetSession
    
    SetSession --> Role
    
    Customer --> CustomerPages[Menu, Cart, Checkout]
    Staff --> StaffPages[+ Staff Portal]
    Admin --> AdminPages[+ Admin Tools]
```

---

## 🔄 Data Flow Diagram

```mermaid
graph TB
    subgraph "Frontend"
        A[User Interface]
        B[Forms]
        C[Display]
    end
    
    subgraph "Backend"
        D[Flask Routes]
        E[FoodTruck Class]
        F[Business Logic]
    end
    
    subgraph "Storage"
        G[CSV Files]
        H[Image Files]
        I[Session Data]
    end
    
    A --> B
    B --> D
    D --> E
    E --> F
    F --> G
    F --> H
    E --> I
    G --> E
    E --> D
    D --> C
    C --> A
```

---

## 📊 Order Status Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Pending: Customer Places Order
    Pending --> PreparationDone: Staff: Preparation Done
    PreparationDone --> ReadyForDelivery: Staff: Hand Off to Delivery
    ReadyForDelivery --> [*]: Order Completed
    
    note right of Pending
        Customer can view order
        Staff sees in orders list
    end note
    
    note right of PreparationDone
        Food is ready
        Waiting for delivery
    end note
    
    note right of ReadyForDelivery
        Ready to be delivered
        Final status
    end note
```

---

## 🎯 Feature Interaction Map

```mermaid
graph LR
    A[Homepage] --> B[Menu]
    B --> C[Cart]
    C --> D[Checkout]
    D --> E[Orders]
    
    F[Staff Login] --> G[Dashboard]
    G --> H[Orders Management]
    G --> I[Statistics]
    G --> J[Menu Management]
    G --> K[Time Clock]
    G --> L[Deals]
    
    H --> M[Update Status]
    J --> N[Add/Edit/Delete Items]
    K --> O[Check In/Out]
    L --> P[Create Deals]
    
    E --> Q[CSV Storage]
    M --> Q
    N --> Q
    O --> Q
    P --> Q
```

---

## 📝 Notes

- All flowcharts use **Mermaid** syntax, which is supported by GitHub
- These diagrams can be viewed directly on GitHub or using Mermaid-compatible viewers
- Flowcharts represent the current system implementation as of November 2024

---

**Last Updated**: November 2024
**Version**: 2.0

