import { useState } from "react";
import { Box, TextField, Button, Typography } from "@mui/material";

const Calculator: React.FC = () => {
    const [amount, setAmount] = useState<number | "">("");
    const [rate, setRate] = useState<number | "">("");
    const [years, setYears] = useState<number | "">("");
    const [payment, setPayment] = useState<number | null>(null);

    return (
        <Box sx={{ p: 3, bgcolor: "background.paper", borderRadius: 2 }}>
            <Typography variant="h6">Калькулятор</Typography>
            <TextField fullWidth label="Поле 1" margin="normal" type="number" value={amount} onChange={e => setAmount(Number(e.target.value) || "")} />
            <TextField fullWidth label="Поле 2" margin="normal" type="number" value={rate} onChange={e => setRate(Number(e.target.value) || "")} />
            <TextField fullWidth label="Поле 3" margin="normal" type="number" value={years} onChange={e => setYears(Number(e.target.value) || "")} />
            <Button variant="contained" color="primary" sx={{ mt: 2 }}>Розрахувати</Button>
            {payment !== null && <Typography sx={{ mt: 2 }}>Результат: ${payment}</Typography>}
        </Box>
    );
};

export default Calculator;
