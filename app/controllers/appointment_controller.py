from flask import render_template, request, session, redirect, url_for, flash
from app.services.appointment_service import AppointmentService
from app.models.appointment import Appointment

class AppointmentController:
    """Controller navigating client appointment schedules, status timelines, and queues"""

    @staticmethod
    def list_appointments():
        """Renders client-side scheduler index layout displaying past & active requests"""
        user_id = session.get('user_id')
        appointments = Appointment.find_by_user_id(user_id)
        return render_template('client-page/appointments.html', appointments=appointments)

    @staticmethod
    def book_appointment():
        """POST handler writing a newly scheduled appointment to the system"""
        user_id = session.get('user_id')
        motorcycle_name = request.form.get('motorcycle_name', '').strip()
        plate_number = request.form.get('plate_number', '').strip()
        reason = request.form.get('reason', '').strip()
        appointment_date = request.form.get('appointment_date', '').strip()
        appointment_time = request.form.get('appointment_time', '').strip()

        result = AppointmentService.book_new(
            user_id=user_id,
            motorcycle_name=motorcycle_name,
            plate_number=plate_number,
            reason=reason,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )

        if result['success']:
            flash(result['message'], "success")
        else:
            flash(result['message'], "danger")
            
        return redirect(url_for('appointment.list_appointments'))

    @staticmethod
    def cancel_appointment(appointment_id):
        """POST handler canceling a pending repair slot securely"""
        user_id = session.get('user_id')
        result = AppointmentService.cancel(appointment_id, user_id)

        if result['success']:
            flash(result['message'], "success")
        else:
            flash(result['message'], "danger")
            
        return redirect(url_for('appointment.list_appointments'))