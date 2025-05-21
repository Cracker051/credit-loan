import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

const Header: React.FC = () => {
  const [isUser, setIsUser] = useState<boolean>(false);
  const navigate = useNavigate();

  useEffect(() => {
    const updateUserStatus = () => {
      const token = localStorage.getItem("accessToken");
      setIsUser(!!token);
    };

    updateUserStatus();
    window.addEventListener("storage", updateUserStatus);

    return () => {
      window.removeEventListener("storage", updateUserStatus);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("user");
    setIsUser(false);
    navigate("/login");
  };

  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Banking
        </Typography>
        <Box>
          <Button color="inherit" component={Link} to="/">
            Головна
          </Button>
          <Button color="inherit" component={Link} to="/calculator">
            Калькулятор
          </Button>
          {isUser && (
            <>
              <Button color="inherit" component={Link} to="/requests">
                Запити
              </Button>
              <Button color="inherit" onClick={handleLogout}>
                Вихід
              </Button>
            </>
          )}
          {!isUser && (
            <>
              <Button color="inherit" component={Link} to="/login">
                Логін
              </Button>
              <Button color="inherit" component={Link} to="/register">
                Реєстрація
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;