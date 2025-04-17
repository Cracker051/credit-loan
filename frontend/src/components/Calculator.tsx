import { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  MenuItem,
  IconButton,
  Stack
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import {
  calcLastPayment,
  computeIncome,
  TimePeriodType,
  Rate,
  TimePeriod,
  Payment,
} from "./nonConsumerUtils";

interface PaymentInput {
  amount: string;
  date: string;
}

const Calculator: React.FC = () => {
  const [amount, setAmount] = useState<string>("");
  const [rateValue, setRateValue] = useState<string>("");
  const [rateFrequency, setRateFrequency] = useState<TimePeriodType>(TimePeriodType.MONTH);
  const [duration, setDuration] = useState<string>("");
  const [startDate, setStartDate] = useState<string>("");
  const [payments, setPayments] = useState<PaymentInput[]>([]);

  const [lastPayment, setLastPayment] = useState<Payment | null>(null);
  const [income, setIncome] = useState<number | null>(null);

  const handleAddPayment = () => {
    setPayments([...payments, { amount: "", date: "" }]);
  };

  const handlePaymentChange = (index: number, field: keyof PaymentInput, value: string) => {
    const newPayments = [...payments];
    newPayments[index] = {
      ...newPayments[index],
      [field]: value,
    };
    setPayments(newPayments);
  };

  const handleRemovePayment = (index: number) => {
    setPayments(payments.filter((_, i) => i !== index));
  };

  const handleCalculate = () => {
    const parsedAmount = Number(amount);
    const parsedRate = Number(rateValue);
    const parsedDuration = Number(duration);

    if (isNaN(parsedAmount) || isNaN(parsedRate) || isNaN(parsedDuration) || !startDate) return;

    const rate: Rate = {
      value: parsedRate,
      frequency: rateFrequency,
    };

    const repaymentPeriod: TimePeriod = {
      unit: TimePeriodType.MONTH,
      duration: parsedDuration,
      startDate: new Date(startDate),
    };

    const parsedPayments: Payment[] = payments
      .filter(p => p.amount && p.date)
      .map(p => ({
        amount: Number(p.amount),
        date: new Date(p.date),
      }));

    const last = calcLastPayment(parsedAmount, rate, repaymentPeriod, parsedPayments);
    const inc = computeIncome(parsedAmount, rate, repaymentPeriod, parsedPayments);

    setLastPayment(last);
    setIncome(inc);
  };

  return (
    <Box sx={{ p: 3, bgcolor: "background.paper", borderRadius: 2 }}>
      <Typography variant="h6">Калькулятор неспоживчого кредиту</Typography>
      <TextField fullWidth label="Сума кредиту" margin="normal" type="number" value={amount} onChange={e => setAmount(e.target.value)} />
      <TextField fullWidth label="Ставка (0.01 = 1%)" margin="normal" type="number" value={rateValue} onChange={e => setRateValue(e.target.value)} />
      <TextField
        select
        fullWidth
        label="Тип ставки"
        margin="normal"
        value={rateFrequency}
        onChange={e => setRateFrequency(Number(e.target.value))}
      >
        <MenuItem value={TimePeriodType.DAY}>Щоденна</MenuItem>
        <MenuItem value={TimePeriodType.MONTH}>Щомісячна</MenuItem>
        <MenuItem value={TimePeriodType.QUARTER}>Щоквартальна</MenuItem>
        <MenuItem value={TimePeriodType.YEAR}>Щорічна</MenuItem>
      </TextField>
      <TextField fullWidth label="Тривалість (в місяцях)" margin="normal" type="number" value={duration} onChange={e => setDuration(e.target.value)} />
      <TextField fullWidth label="Дата початку" type="date" InputLabelProps={{ shrink: true }} margin="normal" value={startDate} onChange={e => setStartDate(e.target.value)} />

      <Box sx={{ mt: 2 }}>
        <Typography variant="subtitle1">Графік платежів:</Typography>
        {payments.map((payment, index) => (
          <Stack direction="row" spacing={2} alignItems="center" key={index} sx={{ my: 1 }}>
            <TextField
              fullWidth
              label="Сума"
              type="number"
              value={payment.amount}
              onChange={e => handlePaymentChange(index, "amount", e.target.value)}
            />
            <TextField
              fullWidth
              label="Дата"
              type="date"
              InputLabelProps={{ shrink: true }}
              value={payment.date}
              onChange={e => handlePaymentChange(index, "date", e.target.value)}
            />
            <IconButton onClick={() => handleRemovePayment(index)}>
              <DeleteIcon />
            </IconButton>
          </Stack>
        ))}
        <Button onClick={handleAddPayment}>Додати платіж</Button>
      </Box>

      <Button variant="contained" color="primary" sx={{ mt: 3 }} onClick={handleCalculate}>Розрахувати</Button>

      {lastPayment && (
        <Box sx={{ mt: 3 }}>
          <Typography>Останній платіж: {lastPayment.amount.toFixed(2)} грн, дата: {lastPayment.date.toLocaleDateString()}</Typography>
        </Box>
      )}
      {income !== null && (
        <Box sx={{ mt: 1 }}>
          <Typography>Прибуток: {income.toFixed(2)} грн</Typography>
        </Box>
      )}
    </Box>
  );
};

export default Calculator;
