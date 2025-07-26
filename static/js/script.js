// =================== Tab Functionality ===================
document.addEventListener('DOMContentLoaded', function () {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    if (tabBtns.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                const tabId = this.getAttribute('data-tab');

                tabBtns.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));

                this.classList.add('active');
                document.getElementById(tabId).classList.add('active');
            });
        });
    }

    // =================== Flash Message Auto-Close ===================
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });

    // =================== Seat Selection Logic with Limit ===================
    const seats = document.querySelectorAll('.seat:not(.sold)');
    const selectedSeatsInput = document.getElementById('selectedSeats');
    const peopleInput = document.getElementById('people');
    let selectedSeats = [];

    seats.forEach(seat => {
        seat.addEventListener('click', () => {
            const maxSeats = parseInt(peopleInput.value);
            const seatNumber = seat.getAttribute('data-seat');

            if (seat.classList.contains('selected')) {
                seat.classList.remove('selected');
                selectedSeats = selectedSeats.filter(s => s !== seatNumber);
            } else {
                if (selectedSeats.length < maxSeats) {
                    seat.classList.add('selected');
                    selectedSeats.push(seatNumber);
                } else {
                    alert(`You can select only ${maxSeats} seats.`);
                }
            }

            selectedSeatsInput.value = selectedSeats.join(',');
            console.log('Selected Seats:', selectedSeatsInput.value);
        });
    });
});

// =================== UPI QR Code Toggle ===================
function toggleQRCode() {
    const payment_method = document.getElementById('payment').value;
    const qrImage = document.getElementById('qrImg');

    if (payment_method === 'UPI') {
        qrImage.style.display = 'block';
    } else {
        qrImage.style.display = 'none';
    }
}

// =================== Show Seat Section ===================
function showSeatSelection() {
    const peopleInput = document.getElementById('people').value;
    const seatSection = document.getElementById('seatSection');

    if (peopleInput > 0) {
        seatSection.style.display = 'block';
    } else {
        seatSection.style.display = 'none';
    }
}
function checkPeopleLimit() {
    const peopleInput = document.getElementById('people');
    if (peopleInput.value > 250) {
        alert("You cannot select more than 250 people!");
        peopleInput.value = 250;
    }
}
