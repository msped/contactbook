import React, { useState, useEffect } from 'react'
import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import AddIcon from '@mui/icons-material/Add';
import api from '../axios'

import Contact from '../components/Contact'
import { Button } from '@mui/material';

const theme = createTheme();

export default function Contacts() {
    const [ contacts, setContacts ] = useState([])

    useEffect(() => {
        const search = async () => {
            const { data } = await api.get('/contacts')
            setContacts(data)
        }
        search()
    }, [])


    return (
        <ThemeProvider theme={theme}>
            <Grid container spacing={2}>
                <Grid item xs={12} md={8}>
                    <Typography variant="h1">
                        Contacts
                    </Typography>
                </Grid>
                <Grid item xs={12} md={4}>
                    <Button
                        variant="contained"
                        href="/create/contact"
                        sx={{alignItems: 'center'}}
                    >
                        Create <AddIcon fontSize='small'/>
                    </Button>
                </Grid>
                {contacts.map((item) => (
                    <Grid key={item.id} item xs={12}>
                        <Contact contact={item} />
                    </Grid>
                ))}
            </Grid>
        </ThemeProvider>
    )
}
