import axios from "axios"

const API = axios.create({
    baseURL: "placement-portal-application-v2-production.up.railway.app"
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