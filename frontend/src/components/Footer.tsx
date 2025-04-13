import { Box, Typography } from "@mui/material";

const Footer: React.FC = () => {
    return (
        <Box sx={{ textAlign: "center", py: 2, bgcolor: "primary.main", color: "white" }}>
            <Typography variant="body2">© 2025 Banking. All rights reserved.</Typography>
        </Box>
    );
};

export default Footer;
