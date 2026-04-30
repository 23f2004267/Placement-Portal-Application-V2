import axios from "axios"

const API = axios.create({
    baseURL: "http://127.0.0.1:5000"
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