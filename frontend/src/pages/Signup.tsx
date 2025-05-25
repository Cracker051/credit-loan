import { useState } from "react";
import { Box, TextField, Button, Typography } from "@mui/material";
import { API_DOMAIN } from "../utils/constants";
import { useNavigate } from "react-router-dom";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Signup: React.FC = () => {
    const navigate = useNavigate();
    const [form, setForm] = useState({
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        role: "user",
    });
    const [loading, setLoading] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setForm(prev => ({ ...prev, [name]: value }));
    };

    const validate = () => {
        const { first_name, last_name, email, password } = form;
        if (!first_name.trim()) {
            toast.error("Будь ласка, введіть ім'я");
            return false;
        }
        if (!last_name.trim()) {
            toast.error('Будь ласка, введіть прізвище');
            return false;
        }
        if (!email) {
            toast.error('Будь ласка, введіть ваш email');
            return false;
        }
        const emailRegex = /\S+@\S+\.\S+/;
        if (!emailRegex.test(email)) {
            toast.error('Неправильний формат email');
            return false;
        }
        if (!password) {
            toast.error('Будь ласка, введіть пароль');
            return false;
        }
        const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()]).{8,}$/;
        if (!passwordRegex.test(password)) {
            toast.error('Пароль має бути не менше 8 символів, містити велику літеру, цифру та спеціальний символ');
            return false;
        }
        return true;
    };

    const handleSubmit = async () => {
        if (!validate()) return;
        setLoading(true);
        try {
            const response = await fetch(`${API_DOMAIN}/auth/register/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(form),
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

            toast.success('Реєстрація пройшла успішно');
            navigate("/");
        } catch (error: any) {
            console.error("Signup failed:", error);
            toast.error(`Помилка реєстрації: ${error.message}`);
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
                    Реєстрація
                </Typography>
                <TextField
                    fullWidth
                    label="Ім'я"
                    name="first_name"
                    value={form.first_name}
                    onChange={handleChange}
                    margin="normal"
                />
                <TextField
                    fullWidth
                    label="Прізвище"
                    name="last_name"
                    value={form.last_name}
                    onChange={handleChange}
                    margin="normal"
                />
                <TextField
                    fullWidth
                    label="Email"
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    margin="normal"
                    type="email"
                />
                <TextField
                    fullWidth
                    label="Пароль"
                    name="password"
                    type="password"
                    value={form.password}
                    onChange={handleChange}
                    margin="normal"
                />
                <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    sx={{ mt: 2 }}
                    onClick={handleSubmit}
                    disabled={loading}
                >
                    {loading ? 'Зачекайте...' : 'Зареєструватись'}
                </Button>
            </Box>
        </>
    );
};

export default Signup;
