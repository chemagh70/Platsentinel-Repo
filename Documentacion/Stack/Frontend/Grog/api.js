// codigo_fuente/dashboard/src/utilidades/api.js
import axios from 'axios';

const api = axios.create({
    baseURL: 'https://api.platsentinel.com',
    headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
    }
});

export async function iniciarEscaneo(target) {
    try {
        const response = await api.post('/scans', { target });
        return response.data;
    } catch (error) {
        console.error('Error al iniciar escaneo:', error);
        throw error;
    }
}

export async function obtenerInformes() {
    try {
        const response = await api.get('/reports');
        return response.data;
    } catch (error) {
        console.error('Error al obtener informes:', error);
        throw error;
    }
}

export async function gestionarServicio(id, action) {
    try {
        const response = await api.post(`/services/${id}/${action}`);
        return response.data;
    } catch (error) {
        console.error('Error al gestionar servicio:', error);
        throw error;
    }
}

export async function obtenerTutoriales() {
    try {
        const response = await api.get('/tutorials');
        return response.data;
    } catch (error) {
        console.error('Error al obtener tutoriales:', error);
        throw error;
    }
}