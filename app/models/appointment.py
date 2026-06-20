from app.database import Database

class Appointment:
    """Model mapping database operations on 'appointments' table"""

    @staticmethod
    def create(user_id: int, motorcycle_name: str, plate_number: str, reason: str, appointment_date: str, appointment_time: str):
        """Inserts a new client booking record into the database"""
        query = """
            INSERT INTO appointments (user_id, motorcycle_name, plate_number, reason, appointment_date, appointment_time, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
        """
        params = (user_id, motorcycle_name, plate_number, reason, appointment_date, appointment_time)
        return Database.execute_query(query, params, commit=True)

    @staticmethod
    def find_by_user_id(user_id: int):
        """Fetches all appointments booked by a specific client, ordered chronologically"""
        query = """
            SELECT a.*, u.first_name AS mechanic_first, u.last_name AS mechanic_last 
            FROM appointments a
            LEFT JOIN users u ON a.mechanic_id = u.id
            WHERE a.user_id = %s
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """
        return Database.execute_query(query, (user_id,))

    @staticmethod
    def find_by_id(appointment_id: int):
        """Finds details of a single appointment record by its reference ID"""
        query = "SELECT * FROM appointments WHERE id = %s"
        results = Database.execute_query(query, (appointment_id,))
        return results[0] if results else None

    @staticmethod
    def cancel_appointment(appointment_id: int, user_id: int):
        """Permits clients to cancel their pending appointments securely"""
        query = "UPDATE appointments SET status = 'Cancelled' WHERE id = %s AND user_id = %s AND status = 'Pending'"
        return Database.execute_query(query, (appointment_id, user_id), commit=True)