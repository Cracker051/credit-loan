import { useState, useEffect } from "react";
import {API_DOMAIN} from "../utils/constants";
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



const Calculator: React.FC = () => {
  const [ratePackages, setRatePackages] = useState<{ name: string; value: number }[]>([]);
  const [calculationReady, setCalculationReady] = useState(false);

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
      setCalculationReady(true);
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
    const userStr = localStorage.getItem("user");
    try {
      const user = userStr ? JSON.parse(userStr) : null;
      const role = user?.role__name;
      setIsAdmin(role === "admin" || role === "operator");
    } catch (e) {
      console.error("Failed to parse user:", e);
      setIsAdmin(false);
    }
  }, []);
  useEffect(() => {
    const type = activeTab === 0 ? "Purpose" : "Consumer";
    fetchRatePackages(type);
    setCalculationReady(false);
  }, [activeTab]);
  const fetchRatePackages = async (targetType: string) => {
    try {
      const res = await fetch(`${API_DOMAIN}/credit/plans/`);
      const data = await res.json();
      const mapped = data
        .filter((item: any) => item.type === targetType)
        .map((item: any) => ({
          id: item.id,
          name: item.name,
          value: parseFloat(item.interest_rate) * 100,
        }));
      setRatePackages(mapped);
    } catch (error) {
      console.error("Failed to fetch credit plans:", error);
    }
  };
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
  const handlePackageChangeConsumer = (pkg: string) => {
    setSelectedPackage(pkg);
    const found = ratePackages.find(p => p.name === pkg);
    if (found) setConsumerRate(found.value.toString());
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
    // setRateValue("44.02");
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
  const timePeriodMap = {
    [TimePeriodType.DAY]: "Day",
    [TimePeriodType.MONTH]: "Month",
    [TimePeriodType.QUARTER]: "Quarter",
    [TimePeriodType.YEAR]: "Year",
  };
  
  const handleSubmitRequest = async () => {
    const token = localStorage.getItem("accessToken");
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    let payload;
    if (activeTab === 0) {
    payload = {
      amount: Number(amount),
      repayment_period_unit: timePeriodMap[rateFrequency],
      repayment_period_duration: Number(duration),
      repayment_period_start_date: startDate,
      status: "Pending",
      return_schedule: [
        ...payments.map(p => ({
          amount: Number(p.amount),
          date: p.date,
        })),
        ...(lastPayment ? [{
          amount: lastPayment.amount,
          date: lastPayment.date.toISOString().substring(0, 10),
        }] : [])
      ],
      user: user?.id,
      // plan: selectedPackage, // make with ID (PK)
      plan: 0,
    };
    } else {
      const months = Number(consumerMonths);
      const amountNum = Number(consumerAmount);
      const monthlyPaymentRounded = Number((monthlyPayment ?? 0).toFixed(2));
      const start = new Date(consumerStartDate);
  
      const consumerSchedule = [];
      for (let i = 1; i <= months; i++) {
        const payDate = new Date(start);
        payDate.setMonth(payDate.getMonth() + i);
        consumerSchedule.push({
          amount: monthlyPaymentRounded,
          date: payDate.toISOString().substring(0, 10),
        });
      }
  
      payload = {
        amount: amountNum,
        repayment_period_unit: "Month",
        repayment_period_duration: months,
        repayment_period_start_date: consumerStartDate,
        status: "Pending",
        return_schedule: consumerSchedule,
        user: user?.id,
        // plan: selectedPackage, // make with ID (PK)
        plan: 0,
      };
    }
  
    try {
      const response = await fetch(`${API_DOMAIN}/credit/requests/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        throw new Error("Failed to submit credit request");
      }
  
      const result = await response.json();
      alert("Заявку подано успішно!");
      console.log(result);
    } catch (err) {
      console.error(err);
      alert("Помилка при відправці заявки");
    }
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
    setCalculationReady(true);
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
                  <MenuItem key={pkg.name} value={pkg.name}>{`Пакет ${pkg.name} (${pkg.value}%) `}</MenuItem>
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
          {calculationReady && (
          <Button variant="contained" color="success" onClick={handleSubmitRequest} sx={{ mt: 2 }}>
            Подати заявку
          </Button>
          )}

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
          <FormControl fullWidth>
              <InputLabel id="package-label">Пакет</InputLabel>
              <Select
                labelId="package-label"
                value={selectedPackage}
                label="Пакет"
                onChange={e => handlePackageChangeConsumer(e.target.value)}
              >
                {ratePackages.map(pkg => (
                  <MenuItem key={pkg.name} value={pkg.name}>{`Пакет ${pkg.name} (${pkg.value}%) `}</MenuItem>
                ))}
              </Select>
            </FormControl>
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
            InputProps={{ readOnly: !isAdmin }}
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
          {calculationReady && (
          <Button variant="contained" color="success" onClick={handleSubmitRequest} sx={{ mt: 2 }}>
            Подати заявку
          </Button>
          )}
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