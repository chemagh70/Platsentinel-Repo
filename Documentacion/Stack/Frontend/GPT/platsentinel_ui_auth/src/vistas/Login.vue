<template>
  <div class="login">
    <h2>🔐 Iniciar Sesión</h2>
    <form @submit.prevent="login">
      <input v-model="usuario" type="text" placeholder="Usuario" required />
      <input v-model="clave" type="password" placeholder="Contraseña" required />
      <button type="submit">Entrar</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      usuario: "",
      clave: "",
      error: ""
    };
  },
  methods: {
    async login() {
      try {
        const datos = new URLSearchParams();
        datos.append("username", this.usuario);
        datos.append("password", this.clave);

        const res = await fetch("http://localhost:8000/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: datos
        });

        const data = await res.json();

        if (res.ok) {
          localStorage.setItem("token", data.access_token);
          this.$router.push("/");
        } else {
          this.error = data.detail || "Error de autenticación";
        }
      } catch (err) {
        this.error = "Error de red";
      }
    }
  }
};
</script>

<style>
.login {
  max-width: 400px;
  margin: auto;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
}
input {
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.5rem;
}
button {
  padding: 0.5rem 1rem;
}
</style>