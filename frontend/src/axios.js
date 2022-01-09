import axios from 'axios'

const apiURL = 'http://127.0.0.1:8000/api/'

const api = axios.create({
    baseURL: apiURL,
    timeout: 5000,
    headers: {
        Authorization : localStorage.getItem('access_token')
            ? 'Bearer ' + localStorage.getItem('access_token')
            : null
    }
})

export default api