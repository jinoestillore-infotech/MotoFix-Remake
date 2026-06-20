from flask import Blueprint
from app.controllers.appointment_controller import AppointmentController
from app.classes.Authentication import Authentication

appointment_bp = Blueprint('appointment', __name__)

# Restrict entire appointments blueprint exclusively to Clients
@appointment_bp.before_request
@Authentication.role_required('Client')
def restrict_to_clients():
    pass

@appointment_bp.route('/', methods=['GET'])
def list_appointments():
    """Renders appointments index dashboard"""
    return AppointmentController.list_appointments()

@appointment_bp.route('/book', methods=['POST'])
def book():
    """Form endpoint processing new booking submissions"""
    return AppointmentController.book_appointment()

@appointment_bp.route('/cancel/<int:appointment_id>', methods=['POST'])
def cancel(appointment_id):
    """Secure client cancellation endpoint"""
    return AppointmentController.cancel_appointment(appointment_id)

@appointment_bp.route('/count', methods=['GET'])
def count():
    """AJAX API endpoint returning live approved or cancelled appointment badge counts"""
    return AppointmentController.get_badge_count_api()