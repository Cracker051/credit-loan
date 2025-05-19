import { useState } from "react";
import { Box, TextField, Button, Typography } from "@mui/material";
import { API_DOMAIN } from "../utils/constants";
import {useNavigate} from "react-router-dom";

const Login: React.FC = () => {
    const navigate = useNavigate();
    const [credentials, setCredentials] = useState({
        username: "",
        password: "",
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setCredentials((prev) => ({ ...prev, [name]: value }));
    };

    const handleLogin = async () => {
        try {
            const response = await fetch(`${API_DOMAIN}/auth/login/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(credentials),
            });

            if (!response.ok) throw new Error(`Login error: ${response.status}`);

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

            console.log(decodeRes);

            if (!decodeRes.ok) throw new Error(`Decode error: ${decodeRes.status}`);
            const userData = await decodeRes.json();
            localStorage.setItem("user", JSON.stringify(userData));

            console.log("Login & decode successful:", userData);
            navigate("/");
        } catch (error) {
            console.error("Login failed:", error);
        }
    };

    return (
        <Box sx={{ maxWidth: 400, mx: "auto", mt: 5, p: 3, bgcolor: "background.paper", borderRadius: 2 }}>
            <Typography variant="h6">Логін</Typography>
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
                label="Password"
                name="password"
                value={credentials.password}
                onChange={handleChange}
                margin="normal"
                type="password"
            />
            <Button fullWidth variant="contained" color="primary" sx={{ mt: 2 }} onClick={handleLogin}>
                Увійти
            </Button>
        </Box>
    );
};

export default Login;
