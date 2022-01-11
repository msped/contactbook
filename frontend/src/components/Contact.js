import React from 'react'
import Avatar from '@mui/material/Avatar';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material';

const theme = createTheme()

export default function Contact({contact}) {
    const viewURL = `/contact/${contact.id}`

    return (
        <ThemeProvider theme={theme}>
            <Card sx={{ minWidth: 275 }}>
                <CardContent>
                    <Grid container spacing={3}>
                        <Grid item xs={2}>
                            <Avatar alt={contact.name} src={contact.profile_picture} sx={{width: 75, height: 75}} />
                        </Grid>
                        <Grid item xs={8}>
                            <Typography>
                                {contact.name}
                            </Typography>
                        </Grid>
                        <Grid item xs={2}>
                            <Button size="small" variant='contained' href={viewURL}>View</Button>
                        </Grid>
                    </Grid>
                </CardContent>
            </Card>
        </ThemeProvider>
    )
}
