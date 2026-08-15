from database import SessionLocal, engine, Base
from models import Prototype

if __name__ == "__main__":
    print("Starting database creation...")
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        proto_1 = Prototype(
            model_name="Canus-V1",
            engine_type="V8 Hybrid",
            horsepower=850,
            weight=1250.32
        )

    proto_2 = Prototype(
        model_name="Canus-Aereo",
        engine_type="Electric",
        horsepower=800,
        weight=1460.23
    )

    if db.query(Prototype).first() is None:
        db.add_all([proto_1, proto_2])
        db.commit()
        print("New prototypes added to the database successfully...\n")
    else:
        print("The database already contains records. Insertion is being omitted to avoid duplicates.\n")

        print("--- Current database ---")
        all_prototypes = db.query(Prototype).all()

        for p in all_prototypes:
            power_to_weight_ratio = p.horsepower / p.weight

            print(
                f"[{p.id}] Model: {p.model_name} | Engine: {p.engine_type} | {p.horsepower} HP")
            print(
                f"     -> Power-to-weight ratio: {round(power_to_weight_ratio, 2)} HP/KG")

print("\nSession closed...")
