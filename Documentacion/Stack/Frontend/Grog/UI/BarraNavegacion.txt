```vue
<!-- src/componentes/BarraNavegacion.vue -->
<template>
  <nav class="bg-gray-800 text-white p-4">
    <div class="container mx-auto flex justify-between items-center">
      <div class="text-xl font-bold">PlatSentinel</div>
      <ul class="flex space-x-6">
        <li><router-link to="/" class="hover:text-gray-300">Inicio</router-link></li>
        <li><router-link to="/scans" class="hover:text-gray-300">Escaneos</router-link></li>
        <li><router-link to="/reports" class="hover:text-gray-300">Informes</router-link></li>
        <li><router-link to="/services" class="hover:text-gray-300">Servicios</router-link></li>
        <li><router-link to="/learning" class="hover:text-gray-300">Aprendizaje</router-link></li>
        <li><a href="/login" class="hover:text-gray-300">Salir</a></li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'BarraNavegacion',
};
</script>
```