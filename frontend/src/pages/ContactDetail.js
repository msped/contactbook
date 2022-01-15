import { Avatar, createTheme, Grid, ThemeProvider, Typography } from '@mui/material'
import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import api from '../axios'



import ContentTable from '../components/Table'

const theme = createTheme();

export default function ContactDetail() {

    const { contact_id } = useParams()
    const [ contact, setContact ] = useState([])

    const phonenumbers = contact.phone_number
    const emails = contact.email

    useEffect(() => {
        const search = async () => {
            const { data } = await api.get('/contacts/' + contact_id)
            setContact(data)
        }
        search()
    }, [contact_id])


    return (
        <ThemeProvider theme={theme}>
            <Grid container spacing={2} mt={8}>
                <Grid 
                    item
                    xs={12} 
                    sm={2}
                    mb={2}
                    container
                    direction="column"
                    justify="center"
                    alignItems="center"
                >
                    <Avatar 
                        alt={contact.name} 
                        src={contact.profile_picture} 
                        sx={{ 
                            width: 100,
                            height: 100,
                        }}
                    />
                </Grid>
                <Grid item xs={12} sm={10}>
                    <Typography 
                        variant='h3' 
                        sx={{
                            textAlign: {
                                xs: 'center',
                                sm: 'left',
                                md: 'left'
                            }
                        }}
                    >
                        {contact.name}
                    </Typography>
                </Grid>
                <Grid item xs={12} mt={5}>
                    { phonenumbers === undefined || phonenumbers.length == 0 ? 
                       <Typography textAlign="center">This contact has no phone number entries.</Typography>
                    : <ContentTable table="Numbers" items={phonenumbers} />}
                </Grid>

                <Grid item xs={12} mt={10}>
                    { emails === undefined || emails.length == 0 ? 
                        <Typography textAlign="center">This contact has no email entries.</Typography>
                    : <ContentTable table="Emails" items={emails} />}
                </Grid>
            </Grid>
        </ThemeProvider>
    )
}
