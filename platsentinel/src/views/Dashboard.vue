<template>

  <div>
    <h1>PlatSentinel Dashboard</h1>
    <p>Esta es la sección de dashboard con datos y controles.</p>
  </div>

  <br>

  <h3>Indicadores Clave de Riesgo</h3>
  <div id="contenido">
    <table>
      <tr>
        <th>Transacciones</th>
        <th>Alertas</th>
        <th>Importe alto</th>
        <th>% alertas</th>
      </tr>
      <tr>
        <td>11</td>
        <td>1</td>
        <td>1</td>
        <td>9,09%</td>
      </tr>
    </table>
  </div>
  <br>
  <br>
  
  <h3>Análisis Avanzado de Riesgo</h3>
  <div id="contenido">
    <table>
      <tr>
        <th>País Origen</th>
        <th>País Destino</th>
        <th>Cantidad Transacciones</th>
        <th>Suma Importes</th>
        <th>Promedio Importes</th>
        <th>Cantidad Trans. Sospechosas</th>
      </tr>
      <tr>
        <td>España</td>
        <td>México</td>
        <td>11</td>
        <td>20.500</td>
        <td>1.863,63</td>
        <td>1</td>
      </tr>
    </table>
  </div>
  <br>
  <br>

  <h3>Gráficos de Riesgo</h3>
  <div id="contenido">
    <img title="Gráfico de Riesgo" src="/src/views/images/dashboard_grafico_1.png" alt="Gráfico de Riesgo" width=100%>
  </div>
  <br>
  <br>

  <h3>Carga masiva de Transacciones</h3>
  <div id="contenido">
  	<p></p>
  </div>
  <br>
  <br>

  <h3>Transacciones Registradas</h3>
  <div id="contenido">
    <p></p>
  </div>
  <br>
  <br>

  <h3>Transacciones Sospechosas</h3>
  <div id="contenido">
    <table>
      <tr>
        <th>Cuenta Origen</th>
        <th>Cuenta Destino</th>
        <th>importe</th>
        <th>Fecha</th>
        <th>Origen</th>
        <th>Destino</th>
        <th>Canal</th>
        <th>Día Semana</th>
      </tr>
      <tr>
        <td>ORIG999</td>
        <td>DEST999</td>
        <td>15.000,00</td>
        <td>2025-06-29 00:00:00</td>
        <td>España</td>
        <td>México</td>
        <td>Transferencia</td>
        <td>6</td>
      </tr>
    </table>
  </div>
  <br>
  <br>

  <h3>Herramientas</h3>
  <div id="contenido">
    <p></p>
  </div>
  <br>
  <br>

  <h3>Auditoría Forense del Sistema</h3>
  <div id="contenido">
    <p></p>
  </div>
  <br>
  <br>









</template>