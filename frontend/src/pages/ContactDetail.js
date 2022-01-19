import { Avatar, createTheme, Grid, ThemeProvider, Typography } from '@mui/material'
import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import api from '../axios'

import ContentTable from '../components/Table'
import CreatePhoneNumber from '../components/CreatePhoneNumber'
import CreateEmail from '../components/CreateEmail'

const theme = createTheme();

export default function ContactDetail() {

    const { contact_id } = useParams()
    const [ contact, setContact ] = useState([])
    const [ callBack, setCallBack ] = useState([])

    const phonenumbers = contact.phone_number
    const emails = contact.email

    useEffect(() => {
        const search = async () => {
            const { data } = await api.get('/contacts/' + contact_id)
            setContact(data)
        }
        search()
    }, [contact_id, callBack])

    const handlePhoneNumberCallback = (childData) => {
        setCallBack(childData)
    }

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
                    <CreatePhoneNumber contactID={contact_id} callbackData={handlePhoneNumberCallback} />
                    <Grid container spacing={0} mt={2}>
                    { phonenumbers === undefined || phonenumbers.length === 0 ? (
                        <Grid item xs={12}>
                            <Typography textAlign="center">This contact has no phone number entries.</Typography>
                        </Grid>
                    ) : (
                        
                        <Grid item xs={12}>
                            <ContentTable table="Numbers" items={phonenumbers} />
                        </Grid>
                    )}
                    </Grid>
                </Grid>

                <Grid item xs={12} mt={10}>
                    <CreateEmail contactID={contact_id} callbackData={handlePhoneNumberCallback} />
                    <Grid container spacing={0} mt={2}>
                    { emails === undefined || emails.length === 0 ? (
                        <Grid item xs={12}>
                            <Typography textAlign="center">This contact has no email entries.</Typography>
                        </Grid>
                    ) : (
                        <Grid item xs={12}>
                            <ContentTable table="Emails" items={emails} />
                        </Grid>
                    )}
                    </Grid>
                </Grid>
            </Grid>
        </ThemeProvider>
    )
}
