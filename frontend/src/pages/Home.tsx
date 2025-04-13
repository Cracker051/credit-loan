import { Container, Typography } from "@mui/material";
import Calculator from "../components/Calculator";

const Home: React.FC = () => {
    return (
        <Container>
            <Typography variant="h4" sx={{ mt: 4, textAlign: "center" }}>Формування портфеля кредитів</Typography>
            <Calculator />
        </Container>
    );
};

export default Home;
