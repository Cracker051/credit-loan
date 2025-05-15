import { useState, useEffect } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  MenuItem,
  IconButton,
  Stack,
  Tabs,
  Tab,
  Select,
  FormControl,
  InputLabel
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
const ratePackages = [
  { name: "A", value: 10 },
  { name: "B", value: 20 },
  { name: "C", value: 44.02 },
];
const Calculator: React.FC = () => {
  // Споживчий калькулятор
  const [consumerAmount, setConsumerAmount] = useState<string>("");
  const [consumerRate, setConsumerRate] = useState<string>("");
  const [consumerMonths, setConsumerMonths] = useState<string>("");
  const [consumerStartDate, setConsumerStartDate] = useState<string>("");
  const [monthlyPayment, setMonthlyPayment] = useState<number | null>(null);
  const [totalOverpay, setTotalOverpay] = useState<number | null>(null);
  const [totalAmount, setTotalAmount] = useState<number | null>(null);

  const handleConsumerCalculate = () => {
    const P = Number(consumerAmount);
    const r = Number(consumerRate) / 100 / 12;
    const n = Number(consumerMonths);

    if (P > 0 && r > 0 && n > 0) {
      const A = P * (r / (1 - Math.pow(1 + r, -n)));
      const total = A * n;
      const overpay = total - P;

      setMonthlyPayment(A);
      setTotalOverpay(overpay);
      setTotalAmount(total);
    }
  };
 // НЕспоживчий калькулятор
  const [activeTab, setActiveTab] = useState<number>(0);
  const [amount, setAmount] = useState<string>("");
  const [rateValue, setRateValue] = useState<string>("");
  const [rateFrequency, setRateFrequency] = useState<TimePeriodType>(TimePeriodType.MONTH);
  const [selectedPackage, setSelectedPackage] = useState<string>("");
  const [duration, setDuration] = useState<string>("");
  const [startDate, setStartDate] = useState<string>("");
  const [payments, setPayments] = useState<PaymentInput[]>([]);

  const [lastPayment, setLastPayment] = useState<Payment | null>(null);
  const [income, setIncome] = useState<number | null>(null);
  const [isAdmin, setIsAdmin] = useState<boolean>(false);

  useEffect(() => {
    setIsAdmin(localStorage.getItem("role") === "admin");
  }, []);

  useEffect(() => {
    const months = Number(duration);
    if (months > 0) {
      if (months < 3) setRateFrequency(TimePeriodType.DAY);
      else if ([3, 6, 9].includes(months)) setRateFrequency(TimePeriodType.QUARTER);
      else if (months < 12) setRateFrequency(TimePeriodType.MONTH);
      else setRateFrequency(TimePeriodType.YEAR);
    }
  }, [duration]);
  const handlePackageChange = (pkg: string) => {
    setSelectedPackage(pkg);
    const found = ratePackages.find(p => p.name === pkg);
    if (found) setRateValue(found.value.toString());
  };
  const generateAnnuityPayments = () => {
    const principal = Number(amount);
    const months = Number(duration);
    const annualRate = Number(rateValue) / 100;
    const start = new Date(startDate);

    if (!principal || !months || !annualRate || !startDate) return;

    const monthlyRate = Math.pow(1 + annualRate, 1 / 12) - 1;
    const annuity = principal * (monthlyRate / (1 - Math.pow(1 + monthlyRate, -months)));

    const result: PaymentInput[] = [];
    for (let i = 1; i < months; i++) {
      const payDate = new Date(start);
      payDate.setMonth(payDate.getMonth() + i);
      result.push({
        amount: annuity.toFixed(2),
        date: payDate.toISOString().substring(0, 10),
      });
    }
    setPayments(result);
  };

  const handleAutofill = () => {
    const today = new Date();
    setAmount("100000");
    setRateValue("44.02");
    setDuration("5");
    setStartDate(today.toISOString().substring(0, 10));
    // setTimeout(() => generateAnnuityPayments(), 100);
  };

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

  // const handleRemovePayment = (index: number) => {
  //   setPayments(payments.filter((_, i) => i !== index));
  // };
  const handleRemovePayment = (index: number) => {
    const updated = [...payments];
    updated[index] = { ...updated[index], amount: "0" };
    setPayments(updated);
  };
  const convertAnnualTo = (annualRate: number, target: TimePeriodType): number => {
    switch (target) {
      case TimePeriodType.DAY:
        return Math.pow(1 + annualRate, 1 / 365) - 1;
      case TimePeriodType.MONTH:
        return Math.pow(1 + annualRate, 1 / 12) - 1;
      case TimePeriodType.QUARTER:
        return Math.pow(1 + annualRate, 1 / 4) - 1;
      case TimePeriodType.YEAR:
      default:
        return annualRate;
    }
  };

  const handleCalculate = () => {
    const parsedAmount = Number(amount);
    const parsedRatePercent = Number(rateValue);
    const parsedDuration = Number(duration);

    if (
      isNaN(parsedAmount) ||
      isNaN(parsedRatePercent) ||
      isNaN(parsedDuration) ||
      !startDate ||
      parsedRatePercent <= 0 ||
      parsedRatePercent >= 100
    ) return;

    const convertedRate = convertAnnualTo(parsedRatePercent / 100, rateFrequency);

    const rate: Rate = {
      value: convertedRate,
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
      <Tabs value={activeTab} onChange={(_, v) => setActiveTab(v)} sx={{ mb: 3 }}>
        <Tab label="Неспоживчий кредит" />
        <Tab label="Споживчий кредит" />
      </Tabs>

      {activeTab === 0 && (
        <>
          <Typography variant="h6">Калькулятор неспоживчого кредиту</Typography>

          <Stack direction="row" spacing={2} alignItems="center" sx={{ mt: 2, mb: 2 }}>
            <Button variant="outlined" onClick={handleAutofill}>Автозаповнення</Button>

            <FormControl fullWidth>
              <InputLabel id="package-label">Пакет</InputLabel>
              <Select
                labelId="package-label"
                value={selectedPackage}
                label="Пакет"
                onChange={e => handlePackageChange(e.target.value)}
              >
                {ratePackages.map(pkg => (
                  <MenuItem key={pkg.name} value={pkg.name}>{`Пакет ${pkg.name} (${pkg.value}%)`}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Stack>

          <TextField fullWidth label="Сума кредиту" margin="normal" type="number" value={amount} onChange={e => setAmount(e.target.value)} />
          <TextField
            fullWidth
            label="Ставка (% річна)"
            margin="normal"
            type="number"
            value={rateValue}
            onChange={e => setRateValue(e.target.value)}
            InputProps={{ readOnly: !isAdmin }}
          />

          {isAdmin && (
            <TextField
              select
              fullWidth
              label="Тип ставки (визначається автоматично)"
              margin="normal"
              value={rateFrequency}
              onChange={e => setRateFrequency(Number(e.target.value))}
            >
              <MenuItem value={TimePeriodType.DAY}>Щоденна</MenuItem>
              <MenuItem value={TimePeriodType.MONTH}>Щомісячна</MenuItem>
              <MenuItem value={TimePeriodType.QUARTER}>Щоквартальна</MenuItem>
              <MenuItem value={TimePeriodType.YEAR}>Щорічна</MenuItem>
            </TextField>
          )}

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
                  InputProps={{ readOnly: true }}
                />
                <IconButton onClick={() => handleRemovePayment(index)}>
                  <DeleteIcon />
                </IconButton>
              </Stack>
            ))}
            {/* <Button onClick={handleAddPayment}>Додати платіж</Button> */}
            <Button variant="outlined" sx={{ mb: 2 }} onClick={generateAnnuityPayments}>
            Згенерувати графік платежів
            </Button>
            {lastPayment && (
              <Stack direction="row" spacing={2} alignItems="center" sx={{ mt: 2 }}>
                <TextField
                  label="Останній платіж"
                  fullWidth
                  value={lastPayment.amount.toFixed(2)}
                  InputProps={{ readOnly: true }}
                />
                <TextField
                  label="Дата останнього платежу"
                  fullWidth
                  value={lastPayment.date.toLocaleDateString("uk-UA")}
                  InputProps={{ readOnly: true }}
                />
              </Stack>
            )}
          </Box>

          <Button variant="contained" color="primary" sx={{ mt: 3 }} onClick={handleCalculate}>Розрахувати</Button>

          {income !== null && isAdmin && (
            <Box sx={{ mt: 1 }}>
              <Typography>Прибуток: {income.toFixed(2)} грн</Typography>
            </Box>
          )}
        </>
      )}

      {activeTab === 1 && (
        <>
          <Typography variant="h6">Калькулятор споживчого кредиту</Typography>
          <TextField
            fullWidth
            label="Сума кредиту"
            margin="normal"
            value={consumerAmount}
            onChange={e => setConsumerAmount(e.target.value)}
          />
          <TextField
            fullWidth
            label="Ставка (% річна)"
            margin="normal"
            value={consumerRate}
            onChange={e => setConsumerRate(e.target.value)}
          />
          <TextField
            fullWidth
            label="Термін (в місяцях)"
            margin="normal"
            value={consumerMonths}
            onChange={e => setConsumerMonths(e.target.value)}
          />
          <TextField
            fullWidth
            label="Дата видачі"
            type="date"
            InputLabelProps={{ shrink: true }}
            margin="normal"
            value={consumerStartDate}
            onChange={e => setConsumerStartDate(e.target.value)}
          />
          <Button variant="contained" sx={{ mt: 2 }} onClick={handleConsumerCalculate}>
            Розрахувати
          </Button>
          {monthlyPayment !== null && (
            <Box sx={{ mt: 2 }}>
              <Typography>Щомісячний платіж: {monthlyPayment.toFixed(2)} грн</Typography>
              <Typography>Загальна переплата: {totalOverpay?.toFixed(2)} грн</Typography>
              <Typography>Загальна сума: {totalAmount?.toFixed(2)} грн</Typography>
            </Box>
          )}
        </>
      )}
    </Box>
  );
};

export default Calculator;