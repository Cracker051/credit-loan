import { createTheme } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        primary: { main: "#2E3B55" },
        secondary: { main: "#7D8DAA" },
        background: { default: "#F4F6F8", paper: "#FFFFFF" },
        text: { primary: "#333", secondary: "#555" },
    },
    typography: {
        fontFamily: "Arial, sans-serif",
    },
});

export default theme;
