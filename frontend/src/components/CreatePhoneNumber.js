import React, { Fragment } from 'react'
import {
  Select,
  FormControl,
  Button,
  Dialog,
  DialogActions,
  DialogTitle,
  InputLabel,
  MenuItem,
  Box,
  TextField,
  Container,
  CssBaseline
} from '@mui/material'
import AddIcon from '@mui/icons-material/Add';
import api from '../axios'

export default class CreatePhoneNumber extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      contactID: props.contactID,
      open: false,
      phonenumber_type: '',
      phoneNumber: ''
    }
  }

  handleToggle = () => {
    this.setState({
      open: !this.state.open
    })
  }

  handleSubmit = (e) => {
    e.preventDefault()
    api.post('/contacts/phone-number', {
      contact: this.state.contactID,
      phonenumber_type: this.state.phonenumber_type,
      phoneNumber: this.state.phoneNumber
    })
    .then((res) => {
      if (res.status === 201){
        this.props.callbackData(res.data.id)
        this.setState({ open: false, phonenumber_type: '', phoneNumber: '' })
      } else {
        // handle error
        console.log(res)
      }
    })
    .catch((err) => {
      console.log(err)
    })
  }

  render() {

    const { open } = this.state
    return (
      <Fragment>
        <Button onClick={this.handleToggle} color="success" variant="contained">
          Add <AddIcon />
        </Button>

        <Dialog
          open={open}
          keepMounted
          onClose={this.handleToggle}
          aria-describedby="alert-dialog-slide-description"
          sx={{
            minWidth: 25
          }}
        >
          <DialogTitle>{"Create new Phone Number"}</DialogTitle>
            <Container component="main" maxWidth="md">
              <CssBaseline />
              <Box
                sx={{
                  marginTop: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                }}
              >
                <Box component="form" onSubmit={this.handleSubmit} noValidate mx={3} my={3}>
                  <FormControl fullWidth>
                    <InputLabel id="demo-simple-select-label">Phone Number Type</InputLabel>
                    <Select
                      labelId="demo-simple-select-label"
                      id="demo-simple-select"
                      value={this.state.phonenumber_type}
                      label="Phone Number Type"
                      onChange={(e) => this.setState({phonenumber_type: e.target.value})}
                    >
                      <MenuItem value="mob">Mobile</MenuItem>
                      <MenuItem value="home">Home</MenuItem>
                      <MenuItem value="work">Work</MenuItem>
                    </Select>
                  </FormControl>
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="phone-number"
                    label="Phone Number"
                    name="phoneNumber"
                    autoFocus
                    onChange={(e) => this.setState({phoneNumber: e.target.value})}
                  />
                  <DialogActions sx={{ mt: 5 }}>
                    <Button onClick={this.handleToggle} variant="contained" color="error">Cancel</Button>
                    <Button type="submit" variant='contained' color="success">Create</Button>
                  </DialogActions>
                </Box>
              </Box>
            </Container>
        </Dialog>
      </Fragment>
    )
  }
}
