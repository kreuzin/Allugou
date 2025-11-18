<template>
  <div class="register-container">
    <div class="register-form">
      <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>
      
      <div v-if="success" class="alert alert-success" role="alert">
        {{ success }}
      </div>
      
      <form @submit.prevent="handleSubmit" v-if="!success">
        <div class="card mb-4">
          <div class="card-body">
            
            <!-- Tipo de usuário -->
            <div class="user-type-section text-center mb-4">
              <label class="form-label d-block mb-3">Tipo de usuário</label>
              <div class="btn-group" role="group" aria-label="Tipo de usuário">
                <input type="radio" class="btn-check" name="user_type" id="locador" value="locador"
                  v-model="formData.user_type" required autocomplete="off">
                <label class="btn btn-outline-primary px-4" for="locador">Locador</label>

                <input type="radio" class="btn-check" name="user_type" id="locatario" value="locatario"
                  v-model="formData.user_type" required autocomplete="off">
                <label class="btn btn-outline-primary px-4" for="locatario">Locatário</label>
              </div>
            </div>

            <!-- Informações Pessoais e Endereço -->
            <div class="row g-4">
              <div class="col-md-6">
                <div class="card h-100">
                  <div class="card-body">
                    <h5 class="card-title mb-3">Informações Pessoais</h5>
                    
                    <div class="form-group mb-3">
                      <label for="nome" class="form-label">Nome completo</label>
                      <input type="text" class="form-control" id="nome"
                        v-model="formData.nome" required />
                    </div>

                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label for="cpf" class="form-label">CPF</label>
                        <input type="text" class="form-control" id="cpf"
                          v-model="formData.cpf" maxlength="11" required />
                      </div>
                      <div class="col-md-6 mb-3">
                        <label for="tel" class="form-label">Telefone</label>
                        <input type="tel" class="form-control" id="tel"
                          v-model="formData.tel" maxlength="11" required />
                      </div>
                    </div>

                    <div class="form-group mb-3">
                      <label for="email" class="form-label">E-mail</label>
                      <input type="email" class="form-control" id="email"
                        v-model="formData.email" required />
                    </div>

                    <div class="form-group mb-3">
                      <label for="username" class="form-label">Nome de usuário</label>
                      <input type="text" class="form-control" id="username"
                        v-model="formData.username" required />
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-md-6">
                <div class="card h-100">
                  <div class="card-body">
                    <h5 class="card-title mb-3">Endereço</h5>
                    
                    <div class="row g-3">
                      <div class="col-md-4">
                        <label for="cep" class="form-label">CEP</label>
                        <input type="text" class="form-control" id="cep"
                          v-model="formData.cep" maxlength="8" required />
                      </div>

                      <div class="col-md-8">
                        <label for="rua" class="form-label">Rua</label>
                        <input type="text" class="form-control" id="rua"
                          v-model="formData.rua" required />
                      </div>

                      <div class="col-md-4">
                        <label for="numero" class="form-label">Número</label>
                        <input type="text" class="form-control" id="numero"
                          v-model="formData.numero" required />
                      </div>

                      <div class="col-md-8">
                        <label for="bairro" class="form-label">Bairro</label>
                        <input type="text" class="form-control" id="bairro"
                          v-model="formData.bairro" required />
                      </div>

                      <div class="col-md-8">
                        <label for="cidade" class="form-label">Cidade</label>
                        <input type="text" class="form-control" id="cidade"
                          v-model="formData.cidade" required />
                      </div>

                      <div class="col-md-4">
                        <label for="estado" class="form-label">Estado</label>
                        <input type="text" class="form-control" id="estado"
                          v-model="formData.estado" maxlength="2" required />
                      </div>

                      <div class="col-12">
                        <label for="complemento" class="form-label">Complemento</label>
                        <input type="text" class="form-control" id="complemento"
                          v-model="formData.complemento" />
                      </div>

                      <div class="col-12">
                        <label for="observacao" class="form-label">Observações</label>
                        <textarea class="form-control" id="observacao"
                          v-model="formData.observacao" rows="2"></textarea>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Senha -->
            <div class="card mt-4">
              <div class="card-body">
                <h5 class="card-title mb-3">Senha</h5>
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label for="password1" class="form-label">Senha</label>
                      <input type="password" class="form-control"
                        :class="{ 'is-invalid': !isPasswordValid && formData.password1 }"
                        id="password1" v-model="formData.password1"
                        @input="validatePassword" required />
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="form-group mb-3">
                      <label for="password2" class="form-label">Confirmar senha</label>
                      <input type="password" class="form-control"
                        :class="{ 'is-invalid': !passwordsMatch && formData.password2 }"
                        id="password2" v-model="formData.password2" required />
                      <div class="invalid-feedback" v-if="!passwordsMatch && formData.password2">
                        As senhas não coincidem
                      </div>
                    </div>
                  </div>

                  <div class="col-12">
                    <div class="password-requirements p-3 bg-light rounded">
                      <p class="text-muted mb-2"><small>Sua senha deve conter:</small></p>
                      <div class="row">
                        <div class="col-md-6">
                          <ul class="requirements-list">
                            <li :class="{ 'text-success': hasMinLength }">
                              <i :class="hasMinLength ? 'fas fa-check' : 'fas fa-times'"></i>
                              Mínimo de 8 caracteres
                            </li>
                            <li :class="{ 'text-success': hasNumber }">
                              <i :class="hasNumber ? 'fas fa-check' : 'fas fa-times'"></i>
                              Pelo menos um número
                            </li>
                            <li :class="{ 'text-success': hasSpecialChar }">
                              <i :class="hasSpecialChar ? 'fas fa-check' : 'fas fa-times'"></i>
                              Pelo menos um caractere especial (@$!%*?&)
                            </li>
                          </ul>
                        </div>
                        <div class="col-md-6">
                          <ul class="requirements-list">
                            <li :class="{ 'text-success': hasUpperCase }">
                              <i :class="hasUpperCase ? 'fas fa-check' : 'fas fa-times'"></i>
                              Pelo menos uma letra maiúscula
                            </li>
                            <li :class="{ 'text-success': hasLowerCase }">
                              <i :class="hasLowerCase ? 'fas fa-check' : 'fas fa-times'"></i>
                              Pelo menos uma letra minúscula
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Botão de cadastro -->
            <div class="text-center mt-4">
              <button type="submit" class="btn btn-primary btn-lg px-5" :disabled="!isFormValid">
                Cadastrar
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../utils/api';

export default {
  name: 'RegisterForm',
  data() {
    return {
      formData: {
        user_type: '',
        username: '',
        email: '',
        password1: '',
        password2: '',
        nome: '',
        cpf: '',
        tel: '',
        // campos de endereço
        cep: '',
        rua: '',
        numero: '',
        bairro: '',
        cidade: '',
        estado: '',
        complemento: '',
        observacao: ''
      },
      error: null,
      success: null,
      hasMinLength: false,
      hasNumber: false,
      hasSpecialChar: false,
      hasUpperCase: false,
      hasLowerCase: false
    }
  },
  computed: {
    isPasswordValid() {
      return this.hasMinLength && this.hasNumber && this.hasSpecialChar && 
             this.hasUpperCase && this.hasLowerCase;
    },
    passwordsMatch() {
      return !this.formData.password2 || this.formData.password1 === this.formData.password2;
    },
    isFormValid() {
      return this.formData.user_type &&
             this.formData.username && 
             this.formData.email &&
             this.formData.nome &&
             this.formData.cpf &&
             this.formData.tel &&
             this.formData.cep &&
             this.formData.rua &&
             this.formData.numero &&
             this.formData.bairro &&
             this.formData.cidade &&
             this.formData.estado &&
             this.isPasswordValid && 
             this.passwordsMatch;
    }
  },
  methods: {
    validatePassword() {
      const password = this.formData.password1;
      this.hasMinLength = password.length >= 8;
      this.hasNumber = /\d/.test(password);
      this.hasSpecialChar = /[@$!%*?&]/.test(password);
      this.hasUpperCase = /[A-Z]/.test(password);
      this.hasLowerCase = /[a-z]/.test(password);
    },
    async handleSubmit() {
      try {
        this.error = null;
        
        if (!this.isPasswordValid) {
          this.error = 'Por favor, atenda a todos os requisitos de senha';
          return;
        }
        
        if (!this.passwordsMatch) {
          this.error = 'As senhas não coincidem';
          return;
        }

        // garantir que o token csrf seja obtido
        await api.get('/api/csrf/');

        console.log('Sending registration data:', this.formData);
        
        const response = await api.post('/api/register/', this.formData);
        
        console.log('Registration response:', response);
        
        if (response.data.success) {
          console.log('User registered successfully!');
          
          // definir usuário na loja imediatamente
          this.$store.commit('auth/setUser', response.data.user);
          this.$store.commit('auth/setAuthenticated', true);
          
          // tentar autenticar com o backend
          await this.$store.dispatch('auth/login', {
            username: this.formData.username,
            password: this.formData.password1
          }).catch(err => {
            console.log('Login error (user already created):', err);
          });
          
          // mostrar mensagem de sucesso
          this.success = 'Cadastro realizado com sucesso! Redirecionando...';
          this.error = null;
          
          // redirecionar após um curto atraso
          setTimeout(() => {
            this.$router.replace('/').catch(err => {
              console.log('Navigation completed');
            });
          }, 1500);
        } else {
          this.error = response.data.message || 'Falha no cadastro'
        }
      } catch (err) {
        console.error('Erro detalhado:', err);
        console.error('Response:', err.response);
        console.error('Request:', err.request);
        this.error = err.response?.data?.message || 'Falha no cadastro. Por favor, tente novamente.'
      }
    }
  }
}
</script>

<style scoped>
.register-form {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 1rem;
}

.card {
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.card-title {
  color: #2c3e50;
  font-weight: 600;
}

.requirements-list {
  list-style: none;
  padding-left: 0;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.requirements-list li {
  margin-bottom: 0.5rem;
  color: #6c757d;
  display: flex;
  align-items: center;
}

.requirements-list li.text-success {
  color: #198754 !important;
}

.requirements-list li i {
  margin-right: 0.5rem;
  width: 16px;
}

.form-label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.5rem;
}

.form-control {
  padding: 0.75rem 1rem;
  border-radius: 6px;
  border: 1px solid #ced4da;
  transition: all 0.2s ease;
}

.form-control:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.15);
}

.btn-group {
  gap: 0.5rem;
}

.btn-check:checked + .btn-outline-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
  color: white;
}

.btn-outline-primary {
  border-width: 2px;
}

.btn-primary {
  padding: 1rem 2.5rem;
  font-weight: 500;
  font-size: 1.1rem;
  transition: all 0.2s ease;
}

.btn-primary:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.invalid-feedback {
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.password-requirements {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
}

.bg-light {
  background-color: #f8f9fa !important;
}

@media (max-width: 768px) {
  .register-form {
    padding: 0.5rem;
  }

  .card {
    margin-bottom: 1rem;
  }

  .btn-primary {
    width: 100%;
    padding: 0.75rem;
  }
}
</style>