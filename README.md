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

// ... rest of the existing README content ...
