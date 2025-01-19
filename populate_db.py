import random
from datetime import datetime, timedelta
from flask_app import create_app  # Import the create_app function to initialize the app
from main.database import db, Patients, Prescriptions  # Import db and models from database.py


def random_date(start, end):
    """Generate a random datetime between two datetime objects."""
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))


def populate_database():
    # Sample data
    patient_names = ["Alice Smith", "Bob Johnson", "Catherine Lee", "David Brown", "Emma Wilson",
                     "Frank Harris", "Grace Young", "Henry Clark", "Ivy Hall", "Jack Adams"]
    medications = ["Ibuprofen", "Amoxicillin", "Paracetamol", "Metformin", "Omeprazole"]

    # Generate and insert patients
    for i, name in enumerate(patient_names, start=1):
        patient = Patients(
            name=name,
            cpf=f"{random.randint(10000000000, 99999999999)}",
            birth_date=random_date(datetime(1970, 1, 1), datetime(2010, 12, 12)).date(),
            phone=f"+1-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            street=f"Street {i}",
            number=f"{random.randint(1, 999)}",
            additional_info=f"Apt {random.randint(1, 50)}" if random.random() > 0.5 else None,
            country="Country X",
            state=f"State {random.choice(['A', 'B', 'C'])}",
            city=f"City {random.randint(1, 5)}",
            medical_history="No significant history." if random.random() > 0.3 else "Has allergies."
        )
        db.session.add(patient)
        db.session.commit()

        # Generate and insert prescriptions for the patient
        for _ in range(random.randint(0, 5)):
            prescription = Prescriptions(
                patient_id=patient.id,
                medication=random.choice(medications),
                dosage=f"{random.randint(1, 3)} tablets per day",
                date_prescribed=random_date(datetime(2023, 1, 1), datetime(2024, 1, 1))
            )
            db.session.add(prescription)

    db.session.commit()


if __name__ == "__main__":
    # Initialize Flask app and database
    app = create_app()
    with app.app_context():  # Ensure the Flask application context is active
        populate_database()
        print("Database populated successfully.")
