import { Box, Container, Typography, Button, Paper } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

const Home: React.FC = () => {
    return (
        <Box sx={{ bgcolor: "#e3f2fd", py: 10 }}>
            <Container maxWidth="md">
                <Paper
                    elevation={8}
                    sx={{
                        p: { xs: 4, sm: 6 },
                        borderRadius: 4,
                        textAlign: "center",
                        bgcolor: "#ffffff",
                        boxShadow: "0 8px 24px rgba(33, 150, 243, 0.2)",
                    }}
                >
                    <Typography
                        variant="h3"
                        gutterBottom
                        sx={{ fontWeight: "bold", color: "#1565c0" }}
                    >
                        Інструмент формування кредитного портфелю
                    </Typography>

                    <Typography variant="h6" sx={{ color: "#424242", mb: 3 }}>
                        Ефективне управління кредитами для фінансових організацій
                    </Typography>

                    <Typography variant="body1" sx={{ fontSize: "1.1rem", mb: 5, color: "#616161" }}>
                        Цей програмний інструмент створений для адміністраторів фінансових установ та кредитних агентств.
                        Використовуйте вбудований калькулятор, щоб формувати портфелі кредитів, оптимізувати графіки погашення
                        та контролювати ризики. Ваша аналітика — наш пріоритет.
                    </Typography>

                    <Box
                        component="img"
                        src="/assets/calculator.jpg"
                        alt="Кредитний калькулятор"
                        sx={{
                            width: "100%",
                            height: "auto",
                            borderRadius: 4,
                            boxShadow: 4,
                            mb: 4,
                        }}
                    />

                    <Button
                        component={RouterLink}
                        to="/calculator"
                        variant="contained"
                        size="large"
                        sx={{
                            px: 6,
                            py: 1.5,
                            fontSize: "1.1rem",
                            fontWeight: "bold",
                            backgroundColor: "#1976d2",
                            '&:hover': {
                                backgroundColor: "#0d47a1",
                            },
                            borderRadius: 3,
                            boxShadow: "0 4px 10px rgba(25, 118, 210, 0.3)",
                            transition: "0.3s ease-in-out"
                        }}
                    >
                        Перейти до калькулятора
                    </Button>
                </Paper>
            </Container>
        </Box>
    );
};

export default Home;
