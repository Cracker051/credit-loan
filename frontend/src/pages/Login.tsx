import { Box, TextField, Button, Typography } from "@mui/material";

const Login: React.FC = () => {
    return (
        <Box sx={{ maxWidth: 400, mx: "auto", mt: 5, p: 3, bgcolor: "background.paper", borderRadius: 2 }}>
            <Typography variant="h6">Логін</Typography>
            <TextField fullWidth label="Email" margin="normal" type="email" />
            <TextField fullWidth label="Password" margin="normal" type="password" />
            <Button fullWidth variant="contained" color="primary" sx={{ mt: 2 }}>Увійти</Button>
        </Box>
    );
};

export default Login;
