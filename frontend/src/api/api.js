import axios from "axios"

console.log("API URL =", import.meta.env.VITE_API_URL)

const API = axios.create({
    baseURL: import.meta.env.VITE_API_URL
})

API.interceptors.request.use(
    function(config) {

        const token = localStorage.getItem("token")
        console.log("TOKEN:", token)
        console.log("TOKEN SENT:", token)

        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }

        return config
    },
    function(error) {
        return Promise.reject(error)
    }
)

export default API