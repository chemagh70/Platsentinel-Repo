```vue
<!-- src/vistas/InicioSesion.vue -->
<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold mb-4 text-center">Iniciar Sesión</h2>
      <form @submit.prevent="iniciarSesion" class="space-y-4">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">Usuario</label>
          <input v-model="username" type="text" id="username" class="mt-1 block w-full p-2 border rounded" required>
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <input v-model="password" type="password" id="password" class="mt-1 block w-full p-2 border rounded" required>
        </div>
        <button type="submit" class="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">Iniciar Sesión</button>
      </form>
      <p v-if="error" class="text-red-500 text-center mt-2">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      error: '',
    };
  },
  methods: {
    async iniciarSesion() {
      try {
        const response = await axios.post('http://localhost:8000/auth/login', {
          username: this.username,
          password: this.password,
        });
        this.$router.push('/');
      } catch (err) {
        this.error = 'Credenciales inválidas';
      }
    },
  },
};
</script>
```