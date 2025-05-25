import {
    Box,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    useMediaQuery,
    useTheme,
    Checkbox,
    FormControlLabel,
} from "@mui/material";
import { useEffect, useState } from "react";
import { API_DOMAIN } from "../utils/constants";
import { useNavigate } from "react-router-dom";

interface Payment {
    date: string;
    amount: number;
}

interface CreditRequest {
    id: string;
    userName: string;
    creditName: string;
    amount: number;
    schedule: Payment[];
    recommended: boolean;
}

const CreditRequests: React.FC = () => {
    const [requests, setRequests] = useState<CreditRequest[]>([]);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [selectedSchedule, setSelectedSchedule] = useState<Payment[] | null>(null);
    const [isPayAble, setIsPayAble] = useState(false);
    const theme = useTheme();
    const fullScreen = useMediaQuery(theme.breakpoints.down("sm"));
    const navigate = useNavigate();

    const token = localStorage.getItem("accessToken");

    const mapToMockRequest = (creditRequest: any) => ({
        id: creditRequest.plan?.toString() || "0",
        userName: creditRequest.user_email,
        creditName: creditRequest.plan_name,
        amount: creditRequest.amount,
        schedule: (creditRequest.return_schedule || []).map((item: any) => ({
            date: item.date,
            amount: item.amount,
        })),
    });

    const getRequests = async () => {
        try {
            let url = `${API_DOMAIN}/credit/requests/portfolio/`;
            if (isPayAble) url += 'non_deterministic';

            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!response.ok) throw new Error(`Error ${response.status}`);

            const items = await response.json();
            const detailPromises = items.map(async (item: any) => {
                const res = await fetch(
                    `${API_DOMAIN}/credit/requests/${item.credit_request_id}`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                if (!res.ok) throw new Error(`Error fetching ID ${item.credit_request_id}: ${res.status}`);
                const creditRequest = await res.json();
                const data = mapToMockRequest(creditRequest);
                return { ...data, recommended: item.is_selected >= 0.5 };
            });

            const details = await Promise.all(detailPromises);
            setRequests(details);
        } catch (error) {
            console.error("Request failed:", error);
        }
    };

    useEffect(() => {
        getRequests();
    }, [isPayAble]);

    const handleAccept = async () => {
        try {
            const response = await fetch(
                `${API_DOMAIN}/credit/requests/portfolio/accept`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            if (!response.ok) throw new Error(`Error ${response.status}`);
            navigate("/", { replace: true });
        } catch (error) {
            console.error("Accept failed:", error);
        }
    };

    const handleReject = async () => {
        try {
            const response = await fetch(
                `${API_DOMAIN}/credit/requests/portfolio/reject`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            if (!response.ok) throw new Error(`Error ${response.status}`);
            navigate("/", { replace: true });
        } catch (error) {
            console.error("Reject failed:", error);
        }
    };

    const handleOpenSchedule = (schedule: Payment[]) => {
        setSelectedSchedule(schedule);
        setDialogOpen(true);
    };
    const handleCloseSchedule = () => {
        setDialogOpen(false);
        setSelectedSchedule(null);
    };

    return (
        <Box sx={{ p: { xs: 2, md: 4 }, bgcolor: "#f3f6f9", minHeight: "100vh" }}>
            <Typography
                variant="h4"
                sx={{
                    mb: 2,
                    fontWeight: "bold",
                    color: "#1976d2",
                    textAlign: { xs: "center", md: "left" },
                }}
            >
                Кредитні запити
            </Typography>
            <FormControlLabel
                control={
                    <Checkbox
                        checked={isPayAble}
                        onChange={(e) => setIsPayAble(e.target.checked)}
                        sx={{ color: '#1976d2', '&.Mui-checked': { color: '#2e7d32' } }}
                    />
                }
                label="Враховувати ймовірність неплатоспроможності"
                sx={{ mb: 2 }}
            />

            <TableContainer component={Paper} elevation={3}>
                <Table size="small">
                    <TableHead>
                        <TableRow sx={{ bgcolor: "#e3f2fd" }}>
                            <TableCell sx={{ fontWeight: 600 }}>№ Запиту</TableCell>
                            <TableCell sx={{ fontWeight: 600 }}>Ім’я користувача</TableCell>
                            <TableCell sx={{ fontWeight: 600 }}>Назва кредиту</TableCell>
                            <TableCell sx={{ fontWeight: 600 }}>Сума</TableCell>
                            <TableCell sx={{ fontWeight: 600 }}>Графік</TableCell>
                            <TableCell sx={{ fontWeight: 600 }}>Рекомендовано</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {requests.map((req) => (
                            <TableRow
                                key={req.id}
                                sx={{
                                    bgcolor: req.recommended ? "#e8f5e9" : "#ffebee",
                                    '&:hover': { backgroundColor: '#f1f8e9' },
                                }}
                            >
                                <TableCell>{req.id}</TableCell>
                                <TableCell>{req.userName}</TableCell>
                                <TableCell>{req.creditName}</TableCell>
                                <TableCell>{req.amount.toLocaleString()} ₴</TableCell>
                                <TableCell>
                                    <Button
                                        variant="text"
                                        onClick={() => handleOpenSchedule(req.schedule)}
                                        sx={{ color: "#1976d2", fontWeight: 500 }}
                                    >
                                        Переглянути
                                    </Button>
                                </TableCell>
                                <TableCell>
                                    <Typography
                                        sx={{
                                            color: req.recommended ? "#2e7d32" : "#c62828",
                                            fontWeight: "bold",
                                        }}
                                    >
                                        {req.recommended ? "Так" : "Ні"}
                                    </Typography>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <Box sx={{ mt: 2, display: "flex", justifyContent: "flex-end", gap: 2 }}>
                <Button variant="contained" color="success" onClick={handleAccept} sx={{ textTransform: 'none' }}>
                    Прийняти
                </Button>
                <Button variant="contained" color="error" onClick={handleReject} sx={{ textTransform: 'none' }}>
                    Відхилити
                </Button>
            </Box>

            <Dialog open={dialogOpen} onClose={handleCloseSchedule} fullScreen={fullScreen} maxWidth="sm" fullWidth>
                <DialogTitle>Графік платежів</DialogTitle>
                <DialogContent dividers>
                    {selectedSchedule?.map((p, i) => (
                        <Box
                            key={i}
                            sx={{ display: 'flex', justifyContent: 'space-between', p: 1, borderBottom: '1px solid #eee' }}
                        >
                            <Typography>Дата: {p.date}</Typography>
                            <Typography>Сума: {p.amount} ₴</Typography>
                        </Box>
                    ))}
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseSchedule}>Закрити</Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default CreditRequests;
