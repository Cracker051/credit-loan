import { useState } from "react";
import { Box, TextField, Button, Typography } from "@mui/material";
import {API_DOMAIN} from "../utils/constants";
import {useNavigate} from "react-router-dom";

const Signup: React.FC = () => {
    const navigate = useNavigate();
    const [form, setForm] = useState({
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        role: "user",
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setForm((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async () => {
        try {
            const response = await fetch(`${API_DOMAIN}/auth/register/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(form),
            });

            if (!response.ok) throw new Error(`Registration error: ${response.status}`);

            const tokens = await response.json();
            localStorage.setItem("accessToken", tokens.access);
            localStorage.setItem("refreshToken", tokens.refresh);

            const decodeRes = await fetch(`${API_DOMAIN}/auth/decode/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "token": tokens.access
                }),
            });

            if (!decodeRes.ok) throw new Error(`Decode error: ${decodeRes.status}`);
            const userData = await decodeRes.json();
            localStorage.setItem("user", JSON.stringify(userData));

            console.log("Signup & decode successful:", userData);

            navigate("/");
        } catch (error) {
            console.error("Signup failed:", error);
        }
    };

    return (
        <Box sx={{ maxWidth: 400, mx: "auto", mt: 5, p: 3, bgcolor: "background.paper", borderRadius: 2 }}>
            <Typography variant="h6">Реєстрація</Typography>
            <TextField
                fullWidth
                label="First Name"
                name="first_name"
                value={form.first_name}
                onChange={handleChange}
                margin="normal"
            />
            <TextField
                fullWidth
                label="Last Name"
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
            />
            <TextField
                fullWidth
                label="Password"
                name="password"
                type="password"
                value={form.password}
                onChange={handleChange}
                margin="normal"
            />
            <Button fullWidth variant="contained" color="primary" sx={{ mt: 2 }} onClick={handleSubmit}>
                Зареєструватись
            </Button>
        </Box>
    );
};

export default Signup;
