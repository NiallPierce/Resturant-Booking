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
- `description` (TextField): A brief description of the dish.
- `price` (DecimalField): The price of the menu item.
- `restaurant` (ForeignKey): The associated restaurant offering this menu item.

**Methods:**
- `__str__`: Returns the name and price of the menu item.

---

