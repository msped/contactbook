import React, { useState } from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import { styled } from '@mui/material/styles';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import api from '../axios';
import { useNavigate } from 'react-router-dom';

const theme = createTheme();

const Input = styled('input')({
    display: 'none',
});

export default function CreateContact() {
    const history = useNavigate()
    const [ profilePicture, setProfilePicture ] = useState()
    const [ name, setName ] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()
        api.post('/contacts/', {
            profile_picture: profilePicture,
            name: name
        })
        .then((res) => {
            if (res.status === 201){
                history("/contacts")
            } else {
                // handle error
                console.log(res)
            }
        })
    }

    return (
        <ThemeProvider theme={theme}>
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
                >
                    <Typography component="h1" variant="h4">
                        Create Contact
                    </Typography>
                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                        <label htmlFor="contained-button-file">
                            <Input accept="image/*" id="contained-button-file" type="file" onChange={(e) => setProfilePicture(e.target.files)}/>
                            <Button variant="contained" component="span">
                                Profile Picture
                            </Button>
                        </label>
                        {profilePicture ? <span style={{margin: '0 20px'}}>{profilePicture[0].name}</span>: ''}
                        
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="name"
                            label="Name"
                            name="name"
                            autoComplete="name"
                            autoFocus
                            onChange={(e) => setName(e.target.value)}
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                        Create
                        </Button>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    )
}
