import { Container, Typography } from "@mui/material";
import Calculator from "../components/Calculator";

const CalculatorPage: React.FC = () => {
    return (
        <Container>
            <Typography variant="h4" sx={{ mt: 4, textAlign: "center" }}>
                Калькулятор кредитів
            </Typography>
            <Calculator />
        </Container>
    );
};

export default CalculatorPage;
