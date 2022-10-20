import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

export function Header() {
    return (
        <Box sx={{mb: 3}}>
            <AppBar position="static">
                <Toolbar>
                    <Typography
                        variant="h6"
                        component="div"              
                    >
                        React Demo App
                    </Typography>
                </Toolbar>
            </AppBar>
        </Box>
    );
}
