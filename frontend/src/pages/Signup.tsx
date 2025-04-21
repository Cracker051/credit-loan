import { Box, TextField, Button, Typography } from "@mui/material";

const Signup: React.FC = () => {
    return (
        <Box sx={{ maxWidth: 400, mx: "auto", mt: 5, p: 3, bgcolor: "background.paper", borderRadius: 2 }}>
            <Typography variant="h6">Реєстрація</Typography>
            <TextField fullWidth label="Name" margin="normal" />
            <TextField fullWidth label="Email" margin="normal" />
            <TextField fullWidth label="Password" margin="normal" type="password" />
            <Button fullWidth variant="contained" color="primary" sx={{ mt: 2 }}>Зареєструватись</Button>
        </Box>
    );
};

export default Signup;
