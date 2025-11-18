## Registration System Testing Guide

The registration system is now fully implemented and ready to test. Here's what has been set up:

### System Components

#### Frontend (Vue.js)
- **RegisterForm.vue** - Complete form with validation
  - User type selection (Locador/Locatário)
  - Personal info: nome, email, username, cpf, tel
  - Address fields: cep, rua, numero, bairro, cidade, estado, complemento, observacao
  - Password validation with requirements display
  
- **RegisterView.vue** - View wrapper

#### Backend (Django)
- **RegisterView (APIView)** - Handles POST requests to `/api/register/`
  - Creates Django User
  - Creates Endereco (Address)
  - Creates Locador or Locatario based on user_type
  - Validates all required fields
  - Automatically logs in user after registration

#### Database Models
- **Locador** - Landlord model
  - endereco (ForeignKey)
  - user, tel, cpf, nome, email, senha
  
- **Locatario** - Tenant model
  - endereco (ForeignKey)
  - user, tel, cpf, nome, email, senha
  
- **Endereco** - Address model
  - cep, rua, numero, bairro, cidade, estado, complemento, observacao

### How to Test Registration

1. **Start the Django server**
   ```
   python manage.py runserver
   ```

2. **Start the Vue.js development server**
   ```
   npm run serve
   ```

3. **Navigate to registration page**
   - Go to `http://localhost:8080/register`

4. **Fill out the form**
   - Select user type (Locador or Locatário)
   - Enter personal information
   - Enter address information
   - Create a password that meets the requirements:
     - At least 8 characters
     - At least one number
     - At least one special character (@$!%*?&)
     - At least one uppercase letter
     - At least one lowercase letter
   - Confirm password

5. **Submit**
   - Click "Cadastrar"
   - Should see success message
   - Should be automatically logged in
   - Should be redirected to home page

### API Endpoint

**POST** `/api/register/`

Request body:
```json
{
  "user_type": "locador",
  "username": "johndoe",
  "email": "john@example.com",
  "password1": "SecurePass123!",
  "password2": "SecurePass123!",
  "nome": "John Doe",
  "cpf": "12345678900",
  "tel": "11999999999",
  "cep": "01310100",
  "rua": "Avenida Paulista",
  "numero": "1578",
  "bairro": "Bela Vista",
  "cidade": "São Paulo",
  "estado": "SP",
  "complemento": "Apt 1234",
  "observacao": "Downtown area"
}
```

Response on success:
```json
{
  "success": true,
  "message": "Usuário registrado com sucesso!",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "user_type": "locador"
}
```

### Data Validation Rules

- **username** - Must be unique, max 20 characters
- **email** - Must be unique, valid email format
- **cpf** - Must be unique, 11 digits
- **tel** - 11 digits
- **nome** - Max 100 characters
- **password1** - Must meet complexity requirements
- **Address fields** - All required except complemento and observacao

### Key Features

✅ User type differentiation (Locador/Locatário)
✅ Address creation with registration
✅ Password strength validation
✅ Duplicate checking (username, email, CPF)
✅ Automatic login after registration
✅ CSRF token protection
✅ Database transaction support (atomic)
✅ Error handling and validation messages
