class BookingForm {
    constructor(formId) {
        this.form = document.getElementById(formId);
        if (this.form) {
            this.form.addEventListener('submit', this.handleSubmit.bind(this));
        }
    }

    validateForm() {
        if (!this.form) return false;
        
        const date = this.form.querySelector('#id_date');
        const time = this.form.querySelector('#id_time');
        const guests = this.form.querySelector('#id_number_of_guests');
        
        if (!date || !time || !guests) return false;

        let isValid = true;
        this.clearErrors();

        // Validate date
        if (!date.value) {
            this.showError(date, 'Please select a date');
            isValid = false;
        }

        // Validate time
        if (!time.value) {
            this.showError(time, 'Please select a time');
            isValid = false;
        }

        // Validate number of guests
        const numGuests = parseInt(guests.value);
        if (!numGuests || numGuests < 1 || numGuests > 20) {
            this.showError(guests, 'Please enter a number between 1 and 20');
            isValid = false;
        }

        return isValid;
    }

    clearErrors() {
        if (!this.form) return;
        
        const inputs = this.form.querySelectorAll('input');
        inputs.forEach(input => {
            input.classList.remove('is-invalid');
            const errorDiv = input.nextElementSibling;
            if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
                errorDiv.remove();
            }
        });
    }

    showError(input, message) {
        if (!input) return;
        
        input.classList.add('is-invalid');
        const errorDiv = document.createElement('div');
        errorDiv.classList.add('invalid-feedback');
        errorDiv.textContent = message;
        input.parentNode.appendChild(errorDiv);
    }

    handleSubmit(event) {
        if (!this.form) return;
        
        if (!this.validateForm()) {
            event.preventDefault();
        }
    }
}

module.exports = BookingForm;