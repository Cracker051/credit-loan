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
} from "@mui/material";
import { useEffect, useState } from "react";

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

const mockRequests: CreditRequest[] = [
    {
        id: "1",
        userName: "Марянчук Олександр",
        creditName: "Автокредит",
        amount: 15000,
        schedule: [
            { date: "2025-06-01", amount: 500 },
            { date: "2025-07-01", amount: 500 },
        ],
        recommended: true,
    },
    {
        id: "2",
        userName: "Олена Коваль",
        creditName: "Іпотека",
        amount: 80000,
        schedule: [
            { date: "2025-06-01", amount: 1000 },
            { date: "2025-07-01", amount: 1000 },
        ],
        recommended: false,
    },
];

const CreditRequests: React.FC = () => {
    const [requests, setRequests] = useState<CreditRequest[]>([]);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [selectedSchedule, setSelectedSchedule] = useState<Payment[] | null>(null);
    const theme = useTheme();
    const fullScreen = useMediaQuery(theme.breakpoints.down("sm"));

    useEffect(() => {
        setRequests(mockRequests);
    }, []);

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
                    mb: 4,
                    fontWeight: "bold",
                    color: "#1976d2",
                    textAlign: { xs: "center", md: "left" },
                }}
            >
                Кредитні запити
            </Typography>

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
                            <TableCell align="center" sx={{ fontWeight: 600 }}>Дії</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {requests.map((req) => (
                            <TableRow
                                key={req.id}
                                sx={{
                                    bgcolor: req.recommended ? "#e8f5e9" : "#ffebee",
                                    "&:hover": { backgroundColor: "#f1f8e9" },
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
                                <TableCell align="center">
                                    <Button
                                        variant="outlined"
                                        color="success"
                                        sx={{ mr: 1, textTransform: "none" }}
                                    >
                                        Прийняти
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        color="error"
                                        sx={{ textTransform: "none" }}
                                    >
                                        Відхилити
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <Dialog
                open={dialogOpen}
                onClose={handleCloseSchedule}
                fullScreen={fullScreen}
                maxWidth="sm"
                fullWidth
            >
                <DialogTitle>Графік платежів</DialogTitle>
                <DialogContent dividers>
                    {selectedSchedule?.map((p, i) => (
                        <Box
                            key={i}
                            sx={{
                                display: "flex",
                                justifyContent: "space-between",
                                p: 1,
                                borderBottom: "1px solid #eee",
                            }}
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
