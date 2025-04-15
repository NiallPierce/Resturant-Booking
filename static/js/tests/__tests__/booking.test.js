const BookingForm = require('../../booking.js');

describe('BookingForm', () => {
    let form;
    let bookingForm;

    beforeEach(() => {
        // Create a form element
        form = document.createElement('form');
        form.id = 'booking-form';
        document.body.appendChild(form);

        // Add required input fields
        const dateInput = document.createElement('input');
        dateInput.id = 'id_date';
        form.appendChild(dateInput);

        const timeInput = document.createElement('input');
        timeInput.id = 'id_time';
        form.appendChild(timeInput);

        const guestsInput = document.createElement('input');
        guestsInput.id = 'id_number_of_guests';
        form.appendChild(guestsInput);

        bookingForm = new BookingForm('booking-form');
    });

    afterEach(() => {
        document.body.removeChild(form);
    });

    test('validates empty form', () => {
        expect(bookingForm.validateForm()).toBe(false);
    });

    test('validates guest count', () => {
        const guestsInput = form.querySelector('#id_number_of_guests');
        guestsInput.value = '0';
        expect(bookingForm.validateForm()).toBe(false);

        guestsInput.value = '21';
        expect(bookingForm.validateForm()).toBe(false);

        guestsInput.value = '5';
        form.querySelector('#id_date').value = '2024-01-01';
        form.querySelector('#id_time').value = '12:00';
        expect(bookingForm.validateForm()).toBe(true);
    });

    test('clears errors', () => {
        const dateInput = form.querySelector('#id_date');
        bookingForm.showError(dateInput, 'Test error');
        expect(dateInput.classList.contains('is-invalid')).toBe(true);

        bookingForm.clearErrors();
        expect(dateInput.classList.contains('is-invalid')).toBe(false);
    });

    test('prevents form submission when invalid', () => {
        const event = { preventDefault: jest.fn() };
        bookingForm.handleSubmit(event);
        expect(event.preventDefault).toHaveBeenCalled();
    });

    test('allows form submission when valid', () => {
        form.querySelector('#id_date').value = '2024-01-01';
        form.querySelector('#id_time').value = '12:00';
        form.querySelector('#id_number_of_guests').value = '5';

        const event = { preventDefault: jest.fn() };
        bookingForm.handleSubmit(event);
        expect(event.preventDefault).not.toHaveBeenCalled();
    });

    test('shows error messages correctly', () => {
        const dateInput = form.querySelector('#id_date');
        bookingForm.showError(dateInput, 'Test error message');
        
        expect(dateInput.classList.contains('is-invalid')).toBe(true);
        const errorDiv = dateInput.nextElementSibling;
        expect(errorDiv).not.toBeNull();
        expect(errorDiv.classList.contains('invalid-feedback')).toBe(true);
        expect(errorDiv.textContent).toBe('Test error message');
    });

    test('handles missing form elements gracefully', () => {
        // Test with null form
        const nullForm = new BookingForm('non-existent-form');
        expect(() => {
            nullForm.validateForm();
            nullForm.clearErrors();
            nullForm.showError(null, 'test');
        }).not.toThrow();

        // Test with missing input elements
        const emptyForm = document.createElement('form');
        emptyForm.id = 'empty-form';
        document.body.appendChild(emptyForm);
        const emptyBookingForm = new BookingForm('empty-form');
        
        expect(() => {
            emptyBookingForm.validateForm();
            emptyBookingForm.clearErrors();
            emptyBookingForm.showError(null, 'test');
        }).not.toThrow();
        
        document.body.removeChild(emptyForm);
    });
});