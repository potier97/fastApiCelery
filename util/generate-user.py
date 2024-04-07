from faker import Faker
import bcrypt
import os

fake = Faker()

# Generar inserción de datos para 50 usuarios
insert_query = "INSERT INTO public.users (username, email, hashed_password) VALUES\n"
email_set = set()
username_set = set()

#SE GENERAN 200 USUARIOS
for _ in range(200):
    username = fake.unique.first_name()
    while username in username_set:
        username = fake.unique.first_name()
    username_set.add(username)

    email = fake.unique.email()
    # Generar un correo electrónico único
    while email in email_set:
        email = fake.unique.email()
    email_set.add(email)

    hashed_password = bcrypt.hashpw(b'Contraseniaa1', bcrypt.gensalt()).decode()
    insert_query += f"('{username}', '{email}', '{hashed_password}'),\n"

# Eliminar la coma final y agregar punto y coma al final
insert_query = insert_query[:-2] + ";"


# Guardar en un archivo
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '..', 'sql', 'users.sql')
print(file_path)
with open(file_path, 'w') as f:
    f.write(insert_query)
    f.close()
