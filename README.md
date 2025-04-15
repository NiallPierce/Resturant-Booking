# Restaurant Finder

Restaurant Finder is a web application that allows users to browse restaurants, check time slots, and make bookings. Designed to simplify the reservation process, this app ensures users can conveniently plan their dining experience.

---

## How to Use

1. Visit the live application [here](https://restaurantbookingp4-3e3fd346ce64.herokuapp.com/).
2. Browse the available restaurants on the homepage.
3. View restaurant details such as location, opening hours, and contact information.
4. Check availability and time slots.
5. Make a booking by selecting a date, time, and specifying the number of guests.

---

## Features

### Existing Features:

1. **Restaurant Listings:**
   - Displays a list of restaurants with their names, addresses, opening hours, and contact details.

    ![Restaurant Listings](screenshots/restaurant_list.png "Listings")

2. **Booking System:**
   - Users can reserve tables by selecting a restaurant, time slot, and specifying the number of guests.
   - Users can provide special requests during booking.

   ![Booking](screenshots/booking.png "Booking")

3. **Menu Display:**
   - Restaurants can showcase their menu items with descriptions and prices.

   ![Menu](screenshots/menu.png "Menu")

4. **User Accounts:**
   - Allow users to create accounts to view and manage their bookings.

   ![Register](screenshots/register.png "Register")
   ![Bookings](screenshots/my_bookings.png "My Bookings")

### Future Features:

1. **Rating and Reviews:**
   - Enable users to rate restaurants and provide reviews after dining.

2. **Enhanced Search and Filters:**
   - Add advanced filters for cuisine, price range, and ratings.

3. **Email Notifications:**
   - Send users confirmation emails and reminders for their bookings.

---

## User Stories

### Authentication Stories
1. **User Registration**
   - As a new user
   - I want to create an account
   - So that I can access the booking system
   - Acceptance Criteria:
     - User can enter username, email, and password
     - System validates email format
     - System enforces password strength requirements
     - User receives confirmation message

2. **User Login**
   - As a registered user
   - I want to log in to my account
   - So that I can manage my bookings
   - Acceptance Criteria:
     - User can enter credentials
     - System validates credentials
     - User is redirected to dashboard after successful login
     - Failed login shows appropriate error message

### Restaurant Browsing Stories
1. **View Restaurant List**
   - As a user
   - I want to see a list of available restaurants
   - So that I can choose where to dine
   - Acceptance Criteria:
     - List shows restaurant names, addresses, and opening hours
     - Each restaurant has a "View Details" button
     - List is responsive and works on all devices

2. **View Restaurant Details**
   - As a user
   - I want to see detailed information about a restaurant
   - So that I can make an informed decision
   - Acceptance Criteria:
     - Shows full restaurant description
     - Displays opening hours and contact information
     - Shows available menu items
     - Includes "Book Now" button

### Booking Management Stories
1. **Create Booking**
   - As a logged-in user
   - I want to make a new booking
   - So that I can reserve a table
   - Acceptance Criteria:
     - User can select date and time
     - User can specify number of guests
     - User can add special requests
     - System validates availability
     - User receives booking confirmation

2. **Edit Booking**
   - As a logged-in user
   - I want to modify my existing booking
   - So that I can update my reservation details
   - Acceptance Criteria:
     - User can change date and time
     - User can update number of guests
     - User can modify special requests
     - System validates new availability
     - User receives update confirmation

3. **Cancel Booking**
   - As a logged-in user
   - I want to cancel my booking
   - So that I can free up the table for others
   - Acceptance Criteria:
     - User can cancel from booking details
     - System shows confirmation dialog
     - User receives cancellation confirmation
     - Table becomes available for new bookings

4. **Delete Booking**
   - As a logged-in user
   - I want to permanently remove my booking
   - So that I can clean up my booking history
   - Acceptance Criteria:
     - User can delete from booking details
     - System shows confirmation dialog
     - Booking is removed from history
     - User receives deletion confirmation

### Contact System Stories
1. **Submit Contact Form**
   - As a user
   - I want to send a message to the restaurant
   - So that I can ask questions or provide feedback
   - Acceptance Criteria:
     - User can enter name, email, and message
     - System validates email format
     - User receives submission confirmation
     - Admin receives notification

2. **View Contact History**
   - As an admin
   - I want to see all contact submissions
   - So that I can respond to user inquiries
   - Acceptance Criteria:
     - List shows all contact submissions
     - Each entry shows sender and timestamp
     - Admin can mark messages as read/unread
     - Admin can delete messages

### Admin Management Stories
1. **Approve/Reject Bookings**
   - As an admin
   - I want to manage booking requests
   - So that I can control restaurant capacity
   - Acceptance Criteria:
     - Admin can view pending bookings
     - Admin can approve or reject bookings
     - User receives status update notification
     - System updates booking status

2. **Manage Restaurant Details**
   - As an admin
   - I want to update restaurant information
   - So that I can keep details current
   - Acceptance Criteria:
     - Admin can edit restaurant details
     - Admin can update opening hours
     - Admin can manage menu items
     - Changes are immediately visible

---

## Data Model
 
 ### Classes:
 
 #### 1. `Restaurant`
 Represents a restaurant in the system, including its essential details such as name, address, operating hours, and contact information.
 
 **Fields:**
 - `name` (CharField): The name of the restaurant.
 - `address` (CharField): The address of the restaurant.
 - `description` (TextField): An optional description of the restaurant.
 - `opening_time` (TimeField): Default set to 09:00 AM.
 - `closing_time` (TimeField): Default set to 10:00 PM.
 - `capacity` (IntegerField): The maximum capacity of the restaurant. Default is 50.
 - `contact_number` (CharField): The restaurant's contact phone number.
 - `email` (EmailField): The restaurant's contact email address.
 
 **Methods:**
 - `__str__`: Returns the name of the restaurant.
 
 ---
 
 #### 2. `TimeSlot`
 Represents available time slots for booking at a restaurant.
 
 **Fields:**
 - `restaurant` (ForeignKey): The associated restaurant.
 - `start_time` (TimeField): The start time of the slot.
 - `end_time` (TimeField): The end time of the slot.
 - `is_available` (BooleanField): Indicates if the time slot is currently available for booking.
 
 **Methods:**
 - `__str__`: Returns the restaurant name and the time range of the slot.
 
 ---
 
 #### 3. `Booking`
 Handles user reservations and associated details, such as the restaurant, table, and time slot.
 
 **Fields:**
 - `user` (ForeignKey): The user making the booking.
 - `restaurant` (ForeignKey): The restaurant for the booking.
 - `table` (ForeignKey): An optional field linking to a specific table.
 - `time_slot` (ForeignKey): An optional field linking to a specific time slot.
 - `date` (DateField): The date of the booking.
 - `time` (TimeField): The specific time of the booking.
 - `number_of_guests` (PositiveIntegerField): The number of guests in the booking.
 - `special_requests` (TextField): Any special requests made by the user. Optional.
 - `status` (CharField): Status of the booking (`pending`, `confirmed`, `cancelled`).
 - `created_at` (DateTimeField): The timestamp when the booking was created.
 - `updated_at` (DateTimeField): The timestamp when the booking was last updated.
 
 **Methods:**
 - `__str__`: Returns a string indicating the user, restaurant, date, and time of the booking.
 
 **Meta:**
 - Orders bookings by the most recent `date` and `time`.
 
 ---
 
 #### 4. `MenuItem`
 Represents a menu item offered by a restaurant.
 
 **Fields:**
 - `name` (CharField): The name of the menu item.
 - `description` (TextField): A description of the menu item.
 - `price` (DecimalField): The price of the menu item.
 - `restaurant` (ForeignKey): The restaurant offering the menu item.
 
 **Methods:**
 - `__str__`: Returns the name and price of the menu item.

## Design

### Wireframes

The application was designed with a focus on user experience and intuitive navigation.

### Design Decisions

1. **User Interface**
   - Clean, minimalist design focusing on content
   - Responsive layout that works on all devices
   - Clear call-to-action buttons
   - Consistent color scheme and typography

2. **User Experience**
   - Intuitive navigation flow
   - Clear feedback for user actions
   - Easy-to-use booking process
   - Quick access to important information

3. **Technical Architecture**
   - Django-based backend for robust data handling
   - PostgreSQL database for reliable data storage
   - Django Admin interface for efficient management
   - RESTful API design for future scalability

4. **Security Considerations**
   - User authentication and authorization
   - Secure form handling
   - Data validation and sanitization
   - CSRF protection

5. **Performance Optimization**
   - Efficient database queries
   - Caching strategies
   - Optimized static file serving
   - Lazy loading of images

### Color Scheme
- Primary: #2C3E50 (Dark Blue)
- Secondary: #E74C3C (Red)
- Accent: #3498DB (Light Blue)
- Background: #F8F9FA (Light Gray)
- Text: #2C3E50 (Dark Blue)

### Typography
- Headings: 'Roboto', sans-serif
- Body: 'Open Sans', sans-serif
- Sizes:
  - H1: 2.5rem
  - H2: 2rem
  - H3: 1.75rem
  - Body: 1rem
  - Small: 0.875rem

  ## Testing

### Automated Testing

#### Unit Tests
The project includes comprehensive unit tests for all models. These tests can be found in `restaurant/tests.py`.

To run the tests:
```bash
python manage.py test
```

##### Model Tests Coverage:

1. **RestaurantModelTest**
   - Tests restaurant creation with all fields
   - Validates field values and data types
   - Coverage: Basic CRUD operations

2. **TimeSlotModelTest**
   - Tests time slot creation and association with restaurant
   - Validates time formatting and availability status
   - Coverage: Basic CRUD operations

3. **BookingModelTest**
   - Tests booking creation with user and restaurant association
   - Validates booking details and status management
   - Coverage: Basic CRUD operations

4. **MenuItemModelTest**
   - Tests menu item creation and restaurant association
   - Validates price formatting and item details
   - Coverage: Basic CRUD operations

### Validation Testing

#### HTML Validation
All HTML templates have been validated using the W3C Markup Validation Service.

| Page | Result | Evidence |
|------|---------|-----------|
| Home | Pass | [Screenshot](screenshots/validation/base.html.png) |
| Booking Form | Pass | [Screenshot](screenshots/validation/book.html.png) |
| Contact | Pass | [Screenshot](screenshots/validation/contact.png) |

#### CSS Validation
CSS has been validated using the W3C CSS Validation Service.

| File | Result | Evidence |
|------|---------|-----------|
| Bootstrap CDN | Pass | External Library |
| Custom CSS | Pass | [Screenshot](screenshots/validation/css.png) |

#### Python Validation (PEP8)
All Python files have been validated using pycodestyle (formerly pep8).

| File | Result |
|------|---------|
| models.py | Pass |
| views.py | Pass |
| forms.py | Pass |
| admin.py | Pass |

#### JavaScript Validation
JavaScript code has been validated using JSHint.

| File | Result | Evidence |
|------|---------|-----------|
| Bootstrap JS | Pass | External Library |


### Manual Testing

#### User Authentication Features

##### Registration
| Test Case | Steps | Expected Result | Actual Result | Pass/Fail |
|-----------|-------|-----------------|---------------|-----------|
| Valid Registration | 1. Click Register<br>2. Fill form with valid data<br>3. Submit | Account created and logged in | As expected | Pass |
| Invalid Email | 1. Click Register<br>2. Enter invalid email<br>3. Submit | Error message shown | As expected | Pass |
| Password Mismatch | 1. Click Register<br>2. Enter different passwords<br>3. Submit | Error message shown | As expected | Pass |

##### Login
| Test Case | Steps | Expected Result | Actual Result | Pass/Fail |
|-----------|-------|-----------------|---------------|-----------|
| Valid Login | 1. Click Login<br>2. Enter valid credentials<br>3. Submit | Successfully logged in | As expected | Pass |
| Invalid Password | 1. Click Login<br>2. Enter wrong password<br>3. Submit | Error message shown | As expected | Pass |

#### Booking Features

##### Create Booking
| Test Case | Steps | Expected Result | Actual Result | Pass/Fail |
|-----------|-------|-----------------|---------------|-----------|
| Valid Booking | 1. Select restaurant<br>2. Choose date/time<br>3. Enter guests<br>4. Submit | Booking created | As expected | Pass |
| Past Date | 1. Select past date<br>2. Submit | Error message shown | As expected | Pass |
| Over Capacity | 1. Enter guests > capacity<br>2. Submit | Error message shown | As expected | Pass |

##### Modify Booking
| Test Case | Steps | Expected Result | Actual Result | Pass/Fail |
|-----------|-------|-----------------|---------------|-----------|
| Change Date | 1. Edit booking<br>2. Select new date<br>3. Submit | Date updated | As expected | Pass |
| Change Guests | 1. Edit booking<br>2. Change guest number<br>3. Submit | Guest number updated | As expected | Pass |

##### Delete Booking
| Test Case | Steps | Expected Result | Actual Result | Pass/Fail |
|-----------|-------|-----------------|---------------|-----------|
| Cancel Booking | 1. View bookings<br>2. Click cancel<br>3. Confirm | Booking cancelled | As expected | Pass |

#### Restaurant Features

##### Restaurant List
| Test Case | Steps | Expected Result | Actual Result | Pass/Fail |
|-----------|-------|-----------------|---------------|-----------|
| View List | 1. Visit homepage | List of restaurants shown | As expected | Pass |
| Restaurant Details | 1. Click restaurant<br>2. View details | Details displayed | As expected | Pass |

##### Menu Items
| Test Case | Steps | Expected Result | Actual Result | Pass/Fail |
|-----------|-------|-----------------|---------------|-----------|
| View Menu | 1. Visit restaurant<br>2. View menu | Menu items shown | As expected | Pass |
| Item Details | 1. Click menu item | Item details shown | As expected | Pass |

#### Responsive Design Testing

##### Mobile View
| Test Case | Steps | Expected Result | Actual Result | Pass/Fail |
|-----------|-------|-----------------|---------------|-----------|
| Navigation | 1. View on mobile<br>2. Click menu | Hamburger menu works | As expected | Pass |
| Booking Form | 1. Complete booking on mobile | Form is usable | As expected | Pass |

##### Tablet View
| Test Case | Steps | Expected Result | Actual Result | Pass/Fail |
|-----------|-------|-----------------|---------------|-----------|
| Layout | 1. View on tablet | Responsive layout | As expected | Pass |
| Images | 1. Check images | Properly scaled | As expected | Pass |

##### Desktop View
| Test Case | Steps | Expected Result | Actual Result | Pass/Fail |
|-----------|-------|-----------------|---------------|-----------|
| Navigation | 1. View on desktop | Full menu shown | As expected | Pass |
| Content | 1. Check layout | Properly formatted | As expected | Pass |

### Bug Tracking

#### Known Bugs
| Bug ID | Description | Status | Resolution |
|--------|-------------|--------|------------|
| BUG-001 | Past dates selectable in date picker | Fixed | Added date validation |
| BUG-002 | Double booking possible for same slot | Fixed | Added booking conflict check |
