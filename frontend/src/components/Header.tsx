import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { Link } from "react-router-dom";

const Header: React.FC = () => {
    return (
        <AppBar position="static" color="primary">
            <Toolbar>
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    Banking
                </Typography>
                <Box>
                    <Button color="inherit" component={Link} to="/">Головна</Button>
                    <Button color="inherit" component={Link} to="/calculator">Калькулятор</Button>
                    <Button color="inherit" component={Link} to="/login">Логін</Button>
                    <Button color="inherit" component={Link} to="/register">Реєстрація</Button>
                </Box>
            </Toolbar>
        </AppBar>
    );
};

export default Header;
