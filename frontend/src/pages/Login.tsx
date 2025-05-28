import { useState } from "react";
import { Box, TextField, Button, Typography } from "@mui/material";
import { API_DOMAIN } from "../utils/constants";
import { useNavigate } from "react-router-dom";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Login: React.FC = () => {
    const navigate = useNavigate();
    const [credentials, setCredentials] = useState({
        username: "",
        password: "",
    });
    const [loading, setLoading] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setCredentials(prev => ({ ...prev, [name]: value }));
    };

    const validate = () => {
        const { username, password } = credentials;
        if (!username) {
            toast.error('Будь ласка, введіть ваш email');
            return false;
        }
        const emailRegex = /\S+@\S+\.\S+/;
        if (!emailRegex.test(username)) {
            toast.error('Неправильний формат email');
            return false;
        }
        if (!password) {
            toast.error('Будь ласка, введіть пароль');
            return false;
        }
        return true;
    };

    const handleLogin = async () => {
        if (!validate()) return;
        setLoading(true);
        try {
            const response = await fetch(`${API_DOMAIN}/auth/login/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(credentials),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Статус ${response.status}: ${errorText}`);
            }

            const tokens = await response.json();
            localStorage.setItem("accessToken", tokens.access);
            localStorage.setItem("refreshToken", tokens.refresh);

            const decodeRes = await fetch(`${API_DOMAIN}/auth/decode/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ token: tokens.access }),
            });

            if (!decodeRes.ok) {
                throw new Error(`Помилка декодування: ${decodeRes.status}`);
            }
            const userData = await decodeRes.json();
            localStorage.setItem("user", JSON.stringify(userData));

            toast.success('Вхід успішний');
            navigate("/");
        } catch (error: any) {
            console.error("Login failed:", error);
            toast.error(`Помилка входу: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <ToastContainer
                position="top-center"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
            />
            <Box sx={{ maxWidth: 400, mx: "auto", mt: 5, p: 3, bgcolor: "background.paper", borderRadius: 2 }}>
                <Typography variant="h6" gutterBottom>
                    Логін
                </Typography>
                <TextField
                    fullWidth
                    label="Email"
                    name="username"
                    value={credentials.username}
                    onChange={handleChange}
                    margin="normal"
                    type="email"
                />
                <TextField
                    fullWidth
                    label="Пароль"
                    name="password"
                    value={credentials.password}
                    onChange={handleChange}
                    margin="normal"
                    type="password"
                />
                <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    sx={{ mt: 2 }}
                    onClick={handleLogin}
                    disabled={loading}
                >
                    {loading ? 'Зачекайте...' : 'Увійти'}
                </Button>
            </Box>
        </>
    );
};

export default Login;
